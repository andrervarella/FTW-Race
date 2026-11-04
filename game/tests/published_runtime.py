"""Resolve the immutable runtime used by a published V4 HTML document.

Run this module directly for its URL-resolution checks; no browser is required.
"""
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, build_opener


class _RuntimeMetadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values = []

    def handle_starttag(self, tag, attributes):
        if tag.lower() == 'meta':
            attributes = dict(attributes)
            if (attributes.get('name') or '').lower() == 'ftw-runtime-base':
                self.values.append(attributes.get('content'))


def _safe_url(url):
    if '\\' in url or any(ord(char) < 32 for char in url):
        raise ValueError('Runtime URLs cannot contain backslashes or control characters')
    parts = urlsplit(url)
    if '%' in parts.path or '..' in parts.path.split('/'):
        raise ValueError('Runtime URLs cannot contain encoded paths or traversal')
    if parts.username or parts.password:
        raise ValueError('Runtime URLs cannot contain credentials')
    return parts


def _within_scope(url, scope):
    parts, base = _safe_url(url), _safe_url(scope)
    if parts.scheme not in ('http', 'https') or (parts.scheme, parts.netloc.lower()) != (base.scheme, base.netloc.lower()):
        raise ValueError('Runtime URL must keep the requested HTTP origin')
    if not parts.path.startswith(base.path):
        raise ValueError('Runtime URL must stay below the requested game directory')
    return url


def resolve_runtime_base(html, document_url, allowed_base_url=None):
    """Read one runtime meta tag while keeping every probe inside the game URL."""
    _safe_url(document_url)
    scope = allowed_base_url or urljoin(document_url, './')
    _within_scope(document_url, scope)
    parser = _RuntimeMetadata()
    parser.feed(html)
    if len(parser.values) > 1:
        raise ValueError('HTML declares multiple runtime bases')
    value = parser.values[0] if parser.values else './'
    if not value or not value.endswith('/') or '?' in value or '#' in value:
        raise ValueError('Runtime metadata must name a directory without query or fragment')
    _safe_url(value)
    runtime_url = _within_scope(urljoin(document_url, value), scope)
    return runtime_url


class _ScopedRedirect(HTTPRedirectHandler):
    def __init__(self, scope):
        self.scope = scope

    def redirect_request(self, request, response, code, message, headers, newurl):
        _within_scope(newurl, self.scope)
        return super().redirect_request(request, response, code, message, headers, newurl)


def inspect_published_runtime(requested_url, timeout=15):
    """Fetch successful HTML and cache headers for the requested and actual build.

    The standard urllib proxy/TLS behavior is preserved. No cache clearing,
    authentication, or request cache overrides are needed to identify the build.
    """
    scope = urljoin(requested_url, './')
    _within_scope(requested_url, scope)
    opener = build_opener(_ScopedRedirect(scope))
    header_names = ['Cache-Control', 'ETag', 'Last-Modified', 'Expires', 'Date', 'Age',
                    'Vary', 'Content-Type', 'Content-Length', 'Server', 'X-Cache',
                    'X-Cache-Hits', 'X-Served-By', 'Via']

    def fetch_html(url):
        with opener.open(url, timeout=timeout) as response:
            _within_scope(response.url, scope)
            if response.status != 200:
                raise ValueError(f'Published HTML must return HTTP 200: {response.status}')
            diagnostic = {'requested_url': url, 'response_url': response.url,
                          'status': response.status,
                          'headers': {name: response.headers[name] for name in header_names if name in response.headers}}
            return response.read().decode('utf-8'), diagnostic

    html, requested = fetch_html(requested_url)
    runtime_url = resolve_runtime_base(html, requested['response_url'], scope)
    if runtime_url == requested['response_url']:
        runtime_html, runtime = html, requested
    else:
        runtime_html, runtime = fetch_html(runtime_url)
        if resolve_runtime_base(runtime_html, runtime['response_url'], scope) != runtime_url:
            raise ValueError('Immutable runtime HTML must resolve to its own directory')
    return {'requested_url': requested_url, 'resolved_runtime_url': runtime_url,
            'html': html, 'runtime_html': runtime_html,
            'header_diagnostics': {'requested_document': requested, 'runtime_document': runtime}}


def _self_tests():
    import http.server
    import threading
    import unittest

    class RuntimeResolutionTests(unittest.TestCase):
        def test_canonical_document_uses_declared_release(self):
            html = "<META content='releases/abc123def456/' NAME='ftw-runtime-base'>"
            self.assertEqual(resolve_runtime_base(html, 'https://example.test/FTW-Race/teste-v4/?v=abc123def456'),
                             'https://example.test/FTW-Race/teste-v4/releases/abc123def456/')

        def test_immutable_document_uses_its_own_directory(self):
            self.assertEqual(resolve_runtime_base('<meta name="ftw-runtime-base" content="./">',
                                                 'https://example.test/FTW-Race/teste-v4/releases/abc123def456/index.html'),
                             'https://example.test/FTW-Race/teste-v4/releases/abc123def456/')

        def test_local_source_without_metadata_keeps_game_directory(self):
            self.assertEqual(resolve_runtime_base('<title>FTW Race V4</title>', 'http://127.0.0.1:8000/game/'),
                             'http://127.0.0.1:8000/game/')

        def test_unsafe_metadata_cannot_change_the_runtime_scope(self):
            for value in ['https://other.test/FTW-Race/teste-v4/', '//other.test/release/',
                          '/FTW-Race/teste-v3/', '../teste-v4/releases/one/',
                          'releases/%2e%2e/one/', 'releases/%252e%252e/one/',
                          'releases\\one/', 'releases/one/?v=2', 'releases/one/#part',
                          '', 'releases/one']:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    resolve_runtime_base(f'<meta name="ftw-runtime-base" content="{value}">',
                                         'https://example.test/FTW-Race/teste-v4/')

        def test_duplicate_runtime_metadata_is_rejected(self):
            with self.assertRaises(ValueError):
                resolve_runtime_base('<meta name="ftw-runtime-base" content="./">' * 2,
                                     'https://example.test/FTW-Race/teste-v4/')

        def test_http_inspection_reports_the_requested_and_runtime_cache_headers(self):
            class PublishedFixture(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    path = urlsplit(self.path).path
                    if path == '/teste-v4/redirect/':
                        self.send_response(302)
                        self.send_header('Location', '/outside/')
                        self.end_headers()
                        return
                    if path == '/teste-v4/':
                        html = '<meta name="ftw-runtime-base" content="releases/abc123def456/">'
                        etag = '"canonical-fixture"'
                    elif path == '/teste-v4/releases/abc123def456/':
                        html = '<meta name="ftw-runtime-base" content="./">'
                        etag = '"runtime-fixture"'
                    else:
                        self.send_error(404)
                        return
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('ETag', etag)
                    self.send_header('Cache-Control', 'max-age=600')
                    self.end_headers()
                    self.wfile.write(html.encode())

                def log_message(self, *_):
                    pass

            server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), PublishedFixture)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                origin = f'http://127.0.0.1:{server.server_port}'
                result = inspect_published_runtime(origin + '/teste-v4/?v=abc123def456')
                self.assertEqual(result['requested_url'], origin + '/teste-v4/?v=abc123def456')
                self.assertEqual(result['resolved_runtime_url'], origin + '/teste-v4/releases/abc123def456/')
                self.assertEqual(result['header_diagnostics']['requested_document']['headers']['ETag'], '"canonical-fixture"')
                self.assertEqual(result['header_diagnostics']['runtime_document']['headers']['ETag'], '"runtime-fixture"')
                self.assertEqual(result['header_diagnostics']['runtime_document']['headers']['Cache-Control'], 'max-age=600')
                with self.assertRaises(ValueError):
                    inspect_published_runtime(origin + '/teste-v4/redirect/')
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeResolutionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    _self_tests()
