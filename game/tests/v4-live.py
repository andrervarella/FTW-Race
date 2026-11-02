"""Exercise a real served V4 with Chromium. No simulator state is injected.

Usage: python game/tests/v4-live.py URL [--executable-path /usr/bin/chromium]
Results describe mobile viewport emulation, never a physical Android device.
"""
import argparse
import json
from pathlib import Path
import time
import traceback
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from playwright.sync_api import sync_playwright


def ready(url, seconds):
    deadline = time.monotonic() + seconds
    while True:
        try:
            with urlopen(url, timeout=15) as response:
                text = response.read().decode('utf-8')
                if response.status == 200 and 'V4' in text and 'src/main.js' in text:
                    return
                problem = f'Unexpected HTTP {response.status} or missing V4 bootstrap'
        except Exception as error:
            problem = str(error)
        if time.monotonic() >= deadline:
            raise AssertionError('Public V4 did not become ready: ' + problem)
        print('Waiting for public V4:', problem, flush=True)
        time.sleep(min(3, max(0, deadline - time.monotonic())))


def loaded_images(page):
    page.wait_for_function('''() => [...document.images].every(img => img.complete && img.naturalWidth > 0)''')


def verify_viewport(browser, url, output, width, height, reduced):
    label = f'{width}x{height}' + ('-reduced' if reduced else '')
    report = {'viewport': label, 'device': 'Chromium mobile emulation; no physical Android',
              'errors': [], 'http_errors': [], 'failed_requests': [],
              'outside_subfolder': [], 'console': [], 'screenshots': [], 'checks': []}
    context = browser.new_context(viewport={'width': width, 'height': height},
                                  device_scale_factor=1, is_mobile=True, has_touch=True,
                                  reduced_motion='reduce' if reduced else 'no-preference')
    page = context.new_page()
    page.set_default_timeout(20000)
    page.on('pageerror', lambda error: report['errors'].append(str(error)))
    page.on('console', lambda msg: report['console'].append({'type': msg.type, 'text': msg.text}))
    page.on('response', lambda response: report['http_errors'].append({'status': response.status, 'url': response.url}) if response.status >= 400 else None)
    page.on('requestfailed', lambda request: report['failed_requests'].append({'url': request.url, 'failure': request.failure}))
    allowed = urljoin(url, './')

    def request_seen(request):
        if urlparse(request.url).scheme in ('http', 'https') and not request.url.startswith(allowed):
            report['outside_subfolder'].append(request.url)

    page.on('request', request_seen)

    def shot(name):
        path = output / f'{label}-{name}.png'
        page.screenshot(path=str(path), full_page=True)
        report['screenshots'].append(path.name)

    def screen(name):
        page.wait_for_function('(name) => document.querySelector("#ui").dataset.screen === name', arg=name)

    try:
        response = page.goto(url, wait_until='networkidle')
        assert response and response.status == 200, 'V4 HTML must return HTTP 200'
        page.wait_for_function('document.body.dataset.ready === "true"')
        assert page.evaluate('!!window.__ftwGame?.renderer'), 'Real Phaser renderer must initialize'
        assert page.locator('#fatal').is_hidden(), 'Fatal initialization panel must remain hidden'
        screen('title')
        loaded_images(page)
        shot('title')
        if reduced:
            assert page.locator('#press-start').evaluate('el => getComputedStyle(el).animationName') == 'none'
            report['checks'].append('reduced-motion title')
        page.get_by_role('button', name='PRESS START', exact=True).tap()
        screen('driverSelect')
        assert page.locator('[data-driver]').count() == 2
        page.locator('[data-driver="felipe"]').tap()
        assert page.locator('[data-driver="felipe"]').get_attribute('aria-pressed') == 'true'
        assert 'felipe-rear.png' in page.locator('[data-driver="felipe"] .menu-car').get_attribute('src')
        page.locator('#laps').select_option('1')
        loaded_images(page)
        shot('felipe-selection')
        page.get_by_role('button', name='CONFIRMAR PILOTO', exact=True).tap()
        screen('grid')
        assert page.locator('.grid-intro h1').inner_text().replace('\n', ' ').strip() == 'FELIPE #25'
        assert page.locator('.grid-names > span').count() == 6
        shot('grid')
        page.get_by_role('button', name='LARGAR', exact=True).tap()
        screen('race')
        page.wait_for_function('document.querySelector("#ui").dataset.phase === "racing"')
        report['checks'].append('title, Felipe #25 selection, six-car grid and natural countdown')
        # CDP touch events use hit testing and actual browser input dispatch.
        cdp = context.new_cdp_session(page)
        throttle = page.locator('[data-action="throttle"]').bounding_box()
        left = page.locator('[data-action="left"]').bounding_box()
        assert throttle and left

        def point(box, identifier):
            return {'x': box['x'] + box['width']/2, 'y': box['y'] + box['height']/2,
                    'id': identifier, 'radiusX': 5, 'radiusY': 5, 'force': 1}

        t, l = point(throttle, 1), point(left, 2)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [t]})
        page.wait_for_function('Number(document.querySelector("#speed").textContent) >= 15')
        assert page.locator('[data-action="throttle"]').evaluate('el => el.classList.contains("held")')
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [t, l]})
        page.wait_for_timeout(250)
        assert page.locator('[data-action="left"]').evaluate('el => el.classList.contains("held")')
        shot('racing-multitouch')
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        assert page.locator('.controls .held').count() == 0
        speed = int(page.locator('#speed').inner_text())
        report['speed_kmh_observed'] = speed
        report['checks'].append('real held acceleration, two touch pointers and release')
        page.locator('#pause').tap()
        page.wait_for_function('document.querySelector("#ui").dataset.phase === "paused"')
        frozen_time = page.locator('#time').inner_text()
        page.wait_for_timeout(350)
        assert page.locator('#time').inner_text() == frozen_time
        shot('paused')
        page.get_by_role('button', name='CONTINUAR', exact=True).tap()
        page.wait_for_function('document.querySelector("#ui").dataset.phase === "racing"')
        # Rotation must pause and clear input; restoration leaves an explicit resume.
        page.set_viewport_size({'width': height, 'height': width})
        page.wait_for_function('document.querySelector("#ui").dataset.phase === "paused"')
        assert page.locator('#rotate').is_visible()
        page.set_viewport_size({'width': width, 'height': height})
        page.wait_for_timeout(200)
        page.get_by_role('button', name='TROCAR PILOTO', exact=True).tap()
        screen('driverSelect')
        page.locator('[data-driver="daniel"]').tap()
        assert page.locator('[data-driver="daniel"]').get_attribute('aria-pressed') == 'true'
        assert 'daniel-rear.png' in page.locator('[data-driver="daniel"] .menu-car').get_attribute('src')
        page.get_by_role('button', name='VOLTAR', exact=True).tap()
        screen('title')
        loaded_images(page)
        report['checks'].append('pause/resume, portrait rotation, Daniel #22 and return to title')
        assert not page.evaluate('window.__ftwErrors?.length'), 'Runtime diagnostics must remain empty'
        assert not report['errors'], report['errors']
        assert not report['http_errors'], report['http_errors']
        assert not report['failed_requests'], report['failed_requests']
        assert not report['outside_subfolder'], report['outside_subfolder']
        console_errors = [item for item in report['console'] if item['type'] == 'error']
        assert not console_errors, console_errors
        report['status'] = 'passed'
    except Exception:
        report['status'] = 'failed'
        report['exception'] = traceback.format_exc()
        try:
            shot('failure')
        except Exception:
            pass
    finally:
        (output / f'{label}-report.json').write_text(json.dumps(report, indent=2) + '\n')
        context.close()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--output', default='work/v4-live')
    parser.add_argument('--wait-ready', type=int, default=0)
    parser.add_argument('--executable-path')
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    summary = {'url': args.url, 'scope': 'Independent browser; mobile emulation, no physical Android', 'reports': []}
    try:
        ready(args.url, args.wait_ready)
        with sync_playwright() as p:
            options = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
            if args.executable_path:
                options['executable_path'] = args.executable_path
            browser = p.chromium.launch(**options)
            summary['browser_version'] = browser.version
            for width, height, reduced in [(915, 412, False), (740, 360, True)]:
                report = verify_viewport(browser, args.url, output, width, height, reduced)
                summary['reports'].append(report)
                print(width, height, report['status'], flush=True)
            browser.close()
        summary['status'] = 'passed' if all(r['status'] == 'passed' for r in summary['reports']) else 'failed'
    except Exception:
        summary['status'] = 'failed'
        summary['exception'] = traceback.format_exc()
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'url': args.url, 'status': summary['status'], 'output': str(output)}, indent=2))
    raise SystemExit(0 if summary['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
