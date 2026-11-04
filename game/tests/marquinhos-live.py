"""Measure the served Marquinhos sprites using the actual production Phaser scene.

The separate HTML fixture supplies controlled race states; the playable page has
no production test hooks. v4-live.py covers the natural unmodified seven-car race.
"""
import argparse
import functools
import http.server
import json
from pathlib import Path
import threading
import traceback
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from published_runtime import inspect_published_runtime

SCALE = 1.7168195718654433
VIEWS = [(0, 0, False), (1, -1, False), (2, 1, False),
         (3, 0, True), (4, -1, True), (5, 1, True)]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?')
    parser.add_argument('--output', default='work/marquinhos-live')
    parser.add_argument('--executable-path')
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    server = None
    if args.url:
        url = args.url
    else:
        root = Path(__file__).resolve().parents[2]
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f'http://127.0.0.1:{server.server_port}/game/'
    report = {'url': url, 'scope': 'Real Chromium/Phaser; viewport emulation, no physical Android',
              'errors': [], 'http_errors': [], 'console_errors': [], 'failed_requests': [], 'views': [], 'screenshots': []}
    page = None
    try:
        published = inspect_published_runtime(url)
        runtime_url = published['resolved_runtime_url']
        report.update({key: published[key] for key in ['requested_url', 'resolved_runtime_url', 'header_diagnostics']})
        with sync_playwright() as p:
            options = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
            if args.executable_path:
                options['executable_path'] = args.executable_path
            browser = p.chromium.launch(**options)
            report['browser'] = browser.version
            page = browser.new_page(viewport={'width': 915, 'height': 412}, is_mobile=True, has_touch=True)
            page.on('pageerror', lambda error: report['errors'].append(str(error)))
            page.on('response', lambda response: report['http_errors'].append({'status': response.status, 'url': response.url}) if response.status >= 400 else None)
            page.on('console', lambda message: report['console_errors'].append(message.text) if message.type == 'error' else None)
            page.on('requestfailed', lambda request: report['failed_requests'].append({'url': request.url, 'failure': request.failure}))
            report['fixture_url'] = urljoin(runtime_url, 'tests/marquinhos-render.html')
            response = page.goto(report['fixture_url'])
            assert response and response.status == 200
            page.wait_for_function('window.marquinhosReady === true')
            assert page.evaluate('!!marquinhosGame.renderer'), 'Actual Phaser renderer must run'

            def measure(key, player=False, wheel=0, braking=False):
                page.evaluate('args => renderVehicle(...args)', [key, player, wheel, braking])
                # Two render frames must elapse after the controlled input changes.
                page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
                return page.evaluate('measureRenderedVehicle()')

            def shot(name):
                path = output / f'{name}.png'
                page.screenshot(path=str(path))
                report['screenshots'].append(path.name)

            reference = measure('npc-blue')
            assert reference['visible'] and reference['key'] == 'npc-blue'
            shot('reference-car-same-depth')
            truck = measure('marquinhos')
            assert truck['key'] == 'marquinhos', 'Production renderer must load the truck spritesheet'
            assert truck['visible'] and truck['source'] == {'width': 560, 'height': 512}
            assert truck['position'] == reference['position']
            assert abs(truck['x'] - reference['x']) < 1e-6 and abs(truck['y'] - reference['y']) < 1e-6
            for dimension in ['width', 'height']:
                ratio = truck[dimension] / reference[dimension]
                assert abs(ratio - SCALE) < 1e-6, f'Actual Phaser {dimension} must enlarge uniformly: {ratio}'
            assert abs(truck['width'] / truck['height'] - 560 / 512) < 1e-6
            report['same_depth'] = {'reference': reference, 'truck': truck,
                                    'width_ratio': truck['width'] / reference['width'],
                                    'height_ratio': truck['height'] / reference['height']}
            shot('marquinhos-truck-same-depth')
            for player in [False, True]:
                anchor = None
                dimensions = None
                for frame, wheel, braking in VIEWS:
                    actual = measure('marquinhos', player, wheel, braking)
                    assert actual['key'] == 'marquinhos' and actual['frame'] == frame, actual
                    assert actual['visible'] and not actual['flipX'] and not actual['flipY']
                    assert actual['source'] == {'width': 560, 'height': 512}
                    assert actual['originX'] == .5 and actual['originY'] == 470 / 512
                    # Steering adds intentional camera sway; all views retain size
                    # and rear-axle y, and each brake pair retains the same x.
                    if anchor is None:
                        anchor = actual['y']
                        dimensions = [actual['width'], actual['height']]
                    assert actual['y'] == anchor and [actual['width'], actual['height']] == dimensions
                    report['views'].append({'role': 'player' if player else 'opponent', **actual})
                    shot(f'{"player" if player else "opponent"}-frame-{frame}')
            for role in ['player', 'opponent']:
                rows = [row for row in report['views'] if row['role'] == role]
                assert all(rows[i]['x'] == rows[i + 3]['x'] for i in range(3)), 'Braking cannot move the sprite pivot'
            report['collision'] = {}
            for axis in ['width', 'length']:
                normal = page.evaluate('axis => compareCollision("daniel", axis)', axis)
                enlarged = page.evaluate('axis => compareCollision("marquinhos", axis)', axis)
                assert normal['playerHit'] == 0 and enlarged['playerHit'] > 0, (axis, normal, enlarged)
                report['collision'][axis] = {'car': normal, 'truck': enlarged}
            assert not page.evaluate('marquinhosErrors')
            assert not report['errors'] and not report['http_errors'] and not report['console_errors'] and not report['failed_requests'], report
            report['status'] = 'passed'
            browser.close()
    except Exception:
        report['status'] = 'failed'
        report['exception'] = traceback.format_exc()
        if page and not page.is_closed():
            try:
                page.screenshot(path=str(output / 'failure.png'))
            except Exception:
                pass
    finally:
        if server:
            server.shutdown()
            server.server_close()
        (output / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(output), 'views': len(report['views'])}))
    raise SystemExit(0 if report['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
