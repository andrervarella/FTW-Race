"""Regress original Mercedes size and useful sprite clearance from real touch hit areas."""
import argparse
import json
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright
from published_runtime import inspect_published_runtime

SCALE = 1.7168195718654433
VIEWS = [(0, False), (-1.5, False), (1.5, False), (0, True), (-1.5, True), (1.5, True)]


def frames(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')


def intersects(a, b):
    return a['left'] < b['right'] and b['left'] < a['right'] and a['top'] < b['bottom'] and b['top'] < a['bottom']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', help='Source or immutable runtime URL ending in /')
    parser.add_argument('--output', default='work/mobile-race-layout')
    parser.add_argument('--executable-path')
    args = parser.parse_args()
    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    report = {'url': args.url, 'scope': 'Real Chromium/Phaser, emulated mobile; no physical-device claim',
              'measurements': [], 'errors': [], 'http_errors': [], 'failed_requests': [], 'failures': [], 'screenshots': []}
    try:
        published = inspect_published_runtime(args.url)
        runtime_url = published['resolved_runtime_url']
        report.update({key: published[key] for key in ['requested_url', 'resolved_runtime_url', 'header_diagnostics']})
        with sync_playwright() as p:
            options = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
            if args.executable_path:
                options['executable_path'] = args.executable_path
            browser = p.chromium.launch(**options)
            report['browser'] = browser.version
            for width, height in [(915, 412), (740, 360), (568, 320), (1024, 461),
                                  (761, 412), (780, 412), (800, 412), (844, 412)]:
                page = browser.new_page(viewport={'width': width, 'height': height}, is_mobile=True, has_touch=True)
                page.on('pageerror', lambda error: report['errors'].append(str(error)))
                page.on('response', lambda response: report['http_errors'].append({'status': response.status, 'url': response.url}) if response.status >= 400 else None)
                page.on('requestfailed', lambda request: report['failed_requests'].append({'url': request.url, 'failure': request.failure}))
                page.goto(urljoin(runtime_url, 'tests/mobile-race-layout.html'))
                page.wait_for_function('window.layoutReady && layoutGame.scene.getScene("race").player.visible')
                assert page.evaluate('!!layoutGame.renderer'), 'Actual Phaser renderer must run'
                for bottom, left, right in [(0, 0, 0), (32, 24, 24), (32, 44, 0), (32, 0, 44)]:
                    for driver in ['daniel', 'felipe', 'marquinhos']:
                        for wheel, braking in VIEWS:
                            page.evaluate('args => selectLayoutVehicle(...args)', [driver, wheel, braking, bottom, left, right])
                            frames(page)
                            measured = page.evaluate('measureLayout()')
                            measured.update({'viewport': [width, height], 'safeBottom': bottom, 'safeLeft': left, 'safeRight': right})
                            report['measurements'].append(measured)
                            label = f'{width}x{height}/{bottom}/{left}/{right}/{driver}/{wheel}/{braking}'
                            checks = []
                            original = min(width * .22, height * .47)
                            if driver != 'marquinhos':
                                checks.append((abs(measured['canvasHeight'] - original) < 1e-6, 'restore original Mercedes size'))
                            else:
                                checks.append((abs(measured['canvasHeight'] - original * SCALE / 1.2) < 1e-6, 'truck remains visibly larger with a shared scene camera'))
                            checks.append((measured['racerCount'] == 7, 'seven racers'))
                            useful = measured['useful']
                            checks.append((useful['left'] >= left and useful['right'] <= width - right, 'vehicle inside horizontal safe area'))
                            checks.append((useful['top'] >= 0 and useful['bottom'] <= height - bottom - 4, 'vehicle above bottom safe area'))
                            for button in measured['controls']:
                                checks.append((button['width'] >= 44 and button['height'] >= 44, f'{button["action"]} at least 44px'))
                                checks.append((not intersects(useful, button), f'vehicle clear of {button["action"]}'))
                                checks.append((button['left'] >= left - .1 and button['right'] <= width - right + .1, f'{button["action"]} inside horizontal safe area'))
                                checks.append((button['bottom'] <= height - bottom + .1, f'{button["action"]} above bottom safe area'))
                            report['failures'].extend(f'{label}: {message}' for passed, message in checks if not passed)
                            if wheel == 0 and not braking:
                                name = f'{width}x{height}-safe{bottom}-{left}-{right}-{driver}.png'
                                page.screenshot(path=str(output / name)); report['screenshots'].append(name)
                        # All opponents share one world scale, regardless of the selected driver.
                        page.evaluate('placeEqualDepthRivals()'); frames(page)
                        rivals = page.evaluate('measureEqualDepthRivals()')
                        car = next(item for item in rivals if item['driver'].startswith('npc-'))
                        for rival in rivals:
                            ratio = SCALE if rival['driver'] == 'marquinhos' else 1
                            assert abs(rival['height'] / car['height'] - ratio) < 1e-6
                            assert abs(rival['width'] / rival['height'] - rival['sourceWidth'] / rival['sourceHeight']) < 1e-6
                # The real grid renders the same race before its touch controls
                # mount. Their arrival must invalidate cached layout bounds.
                page.evaluate('showLayoutGrid()'); frames(page)
                page.evaluate('startLayoutGrid()'); frames(page)
                started = page.evaluate('measureLayout()')
                assert started['useful']['bottom'] <= height - 32 - 4, 'newly mounted controls must apply the bottom safe area'
                assert not any(intersects(started['useful'], button) for button in started['controls']), 'newly mounted controls must reserve the vehicle corridor'
                # Landscape-primary ↔ landscape-secondary can swap the notch
                # without resizing or replacing the active race/control nodes.
                previous_x = started['x']
                for left, right in [(0, 44), (44, 0)]:
                    page.evaluate('args => setLayoutSafeArea(...args)', [32, left, right]); frames(page)
                    rotated = page.evaluate('measureLayout()')
                    assert abs(rotated['x'] - previous_x) > 1, 'same-size rotation must move the vehicle into the changed safe corridor'
                    assert not any(intersects(rotated['useful'], button) for button in rotated['controls']), 'same-size rotation must update the vehicle corridor'
                    previous_x = rotated['x']
                report['errors'].extend(page.evaluate('layoutErrors'))
                page.close()
            browser.close()
        assert not report['errors'], report['errors']
        assert not report['http_errors'], report['http_errors']
        assert not report['failed_requests'], report['failed_requests']
        assert not report['failures'], '\n'.join(report['failures'][:20])
        report['status'] = 'PASS'
    except Exception as error:
        report['status'] = 'FAIL'; report['exception'] = str(error)
        raise
    finally:
        (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
