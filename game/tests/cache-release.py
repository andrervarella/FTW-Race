"""Reproduce a stale in-app-browser cache, then open the immutable share URL.

Old HTML, ESM dependencies, CSS and images receive a one-year cache lifetime.
This is a Chromium cache regression, not a claim of testing the WhatsApp app.
"""
import argparse
import functools
import http.server
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import threading
import traceback
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OLD = 'f9102a0a47b92398ced97e052abf15adbe222b14'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='work/cache-release')
    parser.add_argument('--executable-path')
    parser.add_argument('--old-game', type=Path, help='Checked-out old runtime; CI uses the published two-driver commit')
    args = parser.parse_args()
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ftw-cache-') as temp:
        temp = Path(temp)
        if args.old_game:
            old = args.old_game.resolve()
            if not (old / 'index.html').is_file():
                raise ValueError('Old runtime checkout is missing')
        else:
            archive = subprocess.check_output(['git', 'archive', OLD, 'game'], cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
                bundle.extractall(temp / 'old', filter='data')
            old = temp / 'old/game'
        # The pre-fix update has fresh HTML but repeats every dependency URL.
        unversioned = temp / 'unversioned'
        shutil.copytree(ROOT / 'game', unversioned, ignore=shutil.ignore_patterns('__pycache__'))
        packaged = temp / 'packaged'
        spec = importlib.util.spec_from_file_location('release_packager', ROOT / 'game/scripts/package-v4-release.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        manifest = module.package(packaged)
        requests = []

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **kw):
                super().__init__(*a, directory=str(server.directory), **kw)
            def log_message(self, *_):
                pass
            def do_GET(self):
                requests.append({'phase': server.phase, 'path': self.path})
                super().do_GET()
            def end_headers(self):
                self.send_header('Cache-Control', 'public, max-age=31536000')
                super().end_headers()

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        server.directory, server.phase = old, 'old'
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f'http://127.0.0.1:{server.server_port}/'
        report = {'scope': 'real Chromium with old one-year HTTP cache; no WhatsApp device access', 'errors': []}
        try:
            with sync_playwright() as p:
                options = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
                if args.executable_path:
                    options['executable_path'] = args.executable_path
                browser = p.chromium.launch(**options)
                context = browser.new_context(viewport={'width':915, 'height':412}, is_mobile=True, has_touch=True)
                page = context.new_page()
                page.on('pageerror', lambda e: report['errors'].append(str(e)))

                def select(address):
                    page.goto(address)
                    page.wait_for_function('document.body.dataset.ready === "true"', timeout=60000)
                    page.get_by_role('button', name='PRESS START', exact=True).tap()
                    return page.locator('[data-driver]').count()

                assert select(url) == 2
                report['old_roster'] = 2
                page.goto('about:blank')
                server.directory, server.phase = unversioned, 'query-only'
                assert select(url + '?new-html=1') == 2, 'Querying only HTML must reproduce the cached dependency bug'
                assert not any(r['phase'] == 'query-only' and r['path'].split('?')[0] == '/src/config.js' for r in requests)
                report['query_only_roster'] = 2
                page.goto('about:blank')
                server.directory, server.phase = packaged, 'immutable'
                address = url + 'releases/' + manifest['release'] + '/'
                assert select(address) == 3
                assert page.locator('[data-driver="marquinhos"]').count() == 1
                page.locator('[data-driver="marquinhos"]').tap()
                page.get_by_role('button', name='CONFIRMAR PILOTO', exact=True).tap()
                assert page.locator('.grid-names span').count() == 7
                report.update({'new_roster':3, 'grid':7, 'release':manifest['release'], 'loaded_url':page.url, 'browser':browser.version})
                page.screenshot(path=str(out / 'warm-cache-marquinhos-grid.png'))
                assert all('/releases/' + manifest['release'] + '/' in r['path'] for r in requests if r['phase'] == 'immutable')
                assert not report['errors'], report['errors']
                # Fresh canonical HTML points to the same immutable graph.
                page.goto('about:blank')
                assert select(url + '?share=' + manifest['release']) == 3
                report['fresh_canonical_roster'] = 3
                assert not report['errors'], report['errors']
                report['status'] = 'passed'
                browser.close()
        except Exception:
            report['status'] = 'failed'
            report['exception'] = traceback.format_exc()
            raise
        finally:
            server.shutdown(); server.server_close()
            report['requests'] = requests
            (out / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({k:v for k,v in report.items() if k != 'requests'}))


if __name__ == '__main__':
    main()
