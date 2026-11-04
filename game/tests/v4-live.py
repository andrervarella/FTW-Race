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

from playwright.sync_api import sync_playwright
from published_runtime import inspect_published_runtime, resolve_runtime_base


def ready(url, seconds):
    deadline = time.monotonic() + seconds
    while True:
        try:
            published = inspect_published_runtime(url)
            text = published['runtime_html']
            if 'V4' in text and 'src/main.js' in text:
                return published
            problem = 'Missing V4 bootstrap in the resolved runtime HTML'
        except Exception as error:
            problem = str(error)
        if time.monotonic() >= deadline:
            raise AssertionError('Public V4 did not become ready: ' + problem)
        print('Waiting for public V4:', problem, flush=True)
        time.sleep(min(3, max(0, deadline - time.monotonic())))


def loaded_images(page):
    page.wait_for_function('''() => [...document.images].every(img => img.complete && img.naturalWidth > 0)''')


def verify_approved_art(page, runtime_url):
    """Compare actual served art against the checked-out, owner-approved sources."""
    import hashlib
    game = Path(__file__).resolve().parents[1]
    pilots = json.loads((game / 'assets/v4/drivers/approved-pilots.json').read_text())
    encodings = json.loads((game / 'assets/v4/title/web-encodings.json').read_text())
    assert pilots['approval'] == 'approved-by-owner'
    expected = [{'path': row['file'].removeprefix('game/'), 'sha256': row['sha256'], 'size': [256,512]}
                for row in pilots['views']]
    expected += [{'path': row['file'].removeprefix('game/'), 'sha256': row['sha256'], 'size': row['size']}
                 for row in encodings]
    assert len(pilots['views']) == 16 and len(encodings) == 8, 'Original pilot poses and all cover encodings must remain in the served build'
    for manifest in ['cars/marquinhos.json', 'drivers/marquinhos.json']:
        prepared = json.loads((game / 'assets/v4' / manifest).read_text())
        assert prepared['integrationAcceptance']['status'] == 'owner-requested-integration'
        expected += [{'path': row['file'].removeprefix('game/'), 'sha256': row['sha256'], 'size': row['size']}
                     for row in prepared['assets']]
    for name in ['ftw-official.png', 'diabo-verde-official.png']:
        data = (game / 'assets/v4/title' / name).read_bytes()
        expected.append({'path': 'assets/v4/title/' + name, 'sha256': hashlib.sha256(data).hexdigest()})
    expected = list({item['path']: item for item in expected}.values())
    assert len(expected) == 43, 'All 43 accepted art files must be verified'
    for item in expected:
        item['url'] = urljoin(runtime_url, item['path'])
    actual = page.evaluate('''async entries => Promise.all(entries.map(async item => {
      const response = await fetch(item.url);
      if (!response.ok) throw new Error('Approved image HTTP '+response.status+': '+item.path);
      const bytes = await response.arrayBuffer();
      const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
      const bitmap = await createImageBitmap(new Blob([bytes]));
      const result = {path:item.path, sha256:hash, size:[bitmap.width,bitmap.height], bytes:bytes.byteLength};
      bitmap.close(); return result;
    }))''', expected)
    for want, got in zip(expected, actual):
        assert got['sha256'] == want['sha256'], 'Served approved art differs: ' + want['path']
        if 'size' in want:
            assert got['size'] == want['size'], 'Unexpected approved art dimensions: ' + want['path']
    control = page.locator('#press-start').bounding_box()
    assert control['height'] >= 43.9 and control['width'] >= 43.9, 'Physical touch target must remain at least44px'
    assert page.locator('.cover-hero img').count() == 3, 'Cover must include all three playable drivers'
    assert all('portrait.webp' in path for path in page.locator('.cover-hero img').evaluate_all('imgs => imgs.map(i=>i.src)'))
    assert page.locator('.cover-marquinhos img').count() >= 1, 'Marquinhos must be visible on the cover'
    assert '7' in page.locator('.cover-field').inner_text(), 'Cover must announce the seven-vehicle roster'
    image_sources = page.locator('img').evaluate_all('imgs => imgs.map(img => img.src)')
    assert all(src.startswith(runtime_url) for src in image_sources), 'Visible cover artwork must come from the actual runtime release'
    return {'assets': actual, 'touch_target': control, 'image_sources': image_sources}


def verify_viewport(browser, url, runtime_url, output, width, height, reduced):
    label = f'{width}x{height}' + ('-reduced' if reduced else '')
    report = {'viewport': label, 'device': 'Chromium mobile emulation; no physical Android',
              'requested_url': url, 'resolved_runtime_url': runtime_url,
              'errors': [], 'http_errors': [], 'failed_requests': [],
              'outside_subfolder': [], 'outside_runtime': [], 'console': [], 'screenshots': [], 'checks': [], 'npc_asset_requests': []}
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
        if '/cars/npc-raster/' in request.url:
            report['npc_asset_requests'].append(request.url)
        if urlparse(request.url).scheme in ('http', 'https') and not request.url.startswith(allowed):
            report['outside_subfolder'].append(request.url)
        if (urlparse(request.url).scheme in ('http', 'https')
                and request.resource_type in ('script', 'stylesheet', 'image')
                and not request.url.startswith(runtime_url)):
            report['outside_runtime'].append(request.url)

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
        assert resolve_runtime_base(page.content(), page.url, allowed) == runtime_url, 'Browser HTML must select the inspected immutable runtime'
        page.wait_for_function('document.body.dataset.ready === "true"')
        assert page.evaluate('!!window.__ftwGame?.renderer'), 'Real Phaser renderer must initialize'
        assert page.locator('#fatal').is_hidden(), 'Fatal initialization panel must remain hidden'
        loaded_images(page)
        report['approved_art'] = verify_approved_art(page, runtime_url)
        report['checks'].append(f'{len(report["approved_art"]["assets"])} served accepted art hashes/dimensions, original logos and physical title touch target')
        npc_atlases = page.evaluate('''() => {
          const scene = window.__ftwGame.scene.getScene('race');
          return ['npc-blue','npc-yellow','npc-purple','npc-silver'].map(key => {
            const texture = scene.textures.get(key), image = texture.getSourceImage();
            return { key, src: image.src, size: [image.width,image.height],
              frames: Array.from({length:6},(_,i)=>{const f=texture.get(i);return [f.width,f.height];}) };
          });
        }''')
        assert all(item['size'] == [1680,1024] and item['frames'] == [[560,512]]*6 for item in npc_atlases), 'All four reference car atlases must load six complete views'
        expected_npc_files = {item['key']+'.png' for item in npc_atlases}
        assert {Path(urlparse(src).path).name for src in report['npc_asset_requests']} == expected_npc_files, 'The served game must request all four new PNG atlases'
        report['npc_atlases'] = npc_atlases
        report['checks'].append('four reference NPC raster atlases with six curve and brake views each')
        truck_atlas = page.evaluate('''() => {
          const texture = __ftwGame.scene.getScene('race').textures.get('marquinhos');
          const image = texture.getSourceImage();
          return {key:texture.key,src:image.src,size:[image.width,image.height],
            frames:Array.from({length:6},(_,i)=>{const f=texture.get(i);return [f.width,f.height];})};
        }''')
        assert truck_atlas['key'] == 'marquinhos' and truck_atlas['size'] == [1680,1024]
        assert truck_atlas['frames'] == [[560,512]] * 6, 'All six actual truck views must preload'
        report['truck_atlas'] = truck_atlas
        screen('title')
        loaded_images(page)
        shot('title')
        if reduced:
            assert page.locator('#press-start').evaluate('el => getComputedStyle(el).animationName') == 'none'
            report['checks'].append('reduced-motion title')
        page.get_by_role('button', name='PRESS START', exact=True).tap()
        screen('driverSelect')
        assert page.locator('[data-driver]').count() == 3
        assert set(page.locator('[data-driver]').evaluate_all('nodes => nodes.map(n=>n.dataset.driver)')) == {'daniel','felipe','marquinhos'}
        # Exercise every playable card before choosing the new truck for the race.
        for key, number in [('daniel','22'),('felipe','25'),('marquinhos',None)]:
            card = page.locator(f'[data-driver="{key}"]')
            card.tap()
            assert card.get_attribute('aria-pressed') == 'true'
            assert f'{key}-rear.png' in card.locator('.menu-car').get_attribute('src')
            assert 'null' not in card.inner_text() and 'undefined' not in card.inner_text()
            if number:
                assert number in card.inner_text()
            else:
                assert '#' not in card.inner_text(), 'Do not invent a number for Marquinhos'
        page.locator('#laps').select_option('1')
        loaded_images(page)
        shot('marquinhos-selection')
        cards = page.locator('[data-driver]').evaluate_all('''nodes => nodes.map(el => {
          const b=el.getBoundingClientRect();return {driver:el.dataset.driver,x:b.x,y:b.y,width:b.width,height:b.height};
        })''')
        assert all(card['x'] >= -1 and card['x'] + card['width'] <= width + 1 and card['y'] >= -1 and card['y'] + card['height'] <= height + 1 for card in cards), cards
        report['selection_bounds'] = cards
        page.get_by_role('button', name='CONFIRMAR PILOTO', exact=True).tap()
        screen('grid')
        assert page.locator('.grid-intro h1').inner_text().replace('\n', ' ').strip() == 'MARQUINHOS'
        assert page.locator('.grid-names > span').count() == 7
        assert 'null' not in page.locator('.grid-screen').inner_text() and 'undefined' not in page.locator('.grid-screen').inner_text()
        shot('grid')
        page.get_by_role('button', name='LARGAR', exact=True).tap()
        screen('race')
        page.wait_for_function('document.querySelector("#ui").dataset.phase === "racing"')
        assert '/ 7' in page.locator('#position').inner_text()
        assert page.locator('.minimap circle').count() == 7
        assert page.evaluate('__ftwGame.scene.getScene("race").player.texture.key') == 'marquinhos'
        report['checks'].append('three playable drivers, Marquinhos selected without number, seven-car grid/HUD/minimap and natural countdown')
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
        if not reduced:
            # Let the seven-car simulator finish naturally on the actual served URL.
            page.locator('.results-screen').wait_for(state='visible', timeout=180000)
            assert page.locator('tbody tr').count() == 7
            result_keys = page.locator('tbody tr').evaluate_all('rows => rows.map(row=>row.dataset.resultDriver)')
            assert set(result_keys) == {'daniel','felipe','marquinhos','npc-blue','npc-yellow','npc-purple','npc-silver'}
            assert page.locator('tbody tr.player-row').get_attribute('data-result-driver') == 'marquinhos'
            winner = page.locator('tbody tr').first.get_attribute('data-result-driver')
            assert winner in result_keys
            assert 'null' not in page.locator('.results-screen').inner_text() and 'undefined' not in page.locator('.results-screen').inner_text()
            assert page.locator('td', has_text='Não concluiu').count() >= 1
            shot('natural-finish-results')
            page.get_by_role('button', name='VER PÓDIO', exact=True).tap()
            screen('podium')
            assert page.locator('.podium-screen').get_attribute('data-winner') == winner
            page.wait_for_function('document.querySelector(".podium-screen").dataset.stage === "4"', timeout=30000)
            loaded_images(page)
            assert f'{winner}-4.png' in page.locator('.champion-frame').get_attribute('src')
            assert page.locator('.champagne-fx').is_visible()
            shot('real-winner-champagne')
            page.wait_for_function('document.querySelector(".podium-screen").dataset.stage === "5"', timeout=15000)
            loaded_images(page)
            shot('real-winner-final-podium')
            for index, step in [(0, 'two'), (1, 'three')]:
                caption_box = page.locator(f'.runner-{index} span').bounding_box()
                number = page.locator(f'.step-{step} b').bounding_box()
                overlap = (caption_box['x'] < number['x'] + number['width'] and caption_box['x'] + caption_box['width'] > number['x']
                           and caption_box['y'] < number['y'] + number['height'] and caption_box['y'] + caption_box['height'] > number['y'])
                assert not overlap, 'Podium runner caption cannot cover its place number'
            report['checks'].append('natural complete race with Marquinhos, seven real standings and actual-winner animated champagne podium')
            report['natural_winner'] = winner
            report['natural_result_order'] = result_keys
            page.locator('#podium-replay').tap()
            screen('grid')
            page.get_by_role('button', name='LARGAR', exact=True).tap()
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
        assert not report['outside_runtime'], report['outside_runtime']
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
        published = ready(args.url, args.wait_ready)
        summary.update({key: published[key] for key in ['requested_url', 'resolved_runtime_url', 'header_diagnostics']})
        with sync_playwright() as p:
            options = {'args': ['--no-sandbox', '--disable-dev-shm-usage']}
            if args.executable_path:
                options['executable_path'] = args.executable_path
            browser = p.chromium.launch(**options)
            summary['browser_version'] = browser.version
            for width, height, reduced in [(915, 412, False), (740, 360, True), (1440, 900, True)]:
                report = verify_viewport(browser, args.url, published['resolved_runtime_url'], output, width, height, reduced)
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
