"""Real DOM UI regression suite. Run against a server rooted at repository root."""
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/game/tests/ui-flow.html'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
    page = browser.new_page(viewport={'width':960,'height':540}, has_touch=True)
    page.goto(url)
    page.wait_for_function('window.ui !== undefined')
    assert page.evaluate('ui.screen') == 'title', 'first state must be title'
    assert page.locator('.cover-hero img').count() == 3, 'cover must include all three prepared pilot portraits'
    assert page.locator('.cover-car img').count() == 3, 'cover must include the IVECO and both Mercedes'
    assert page.locator('.cover-field').inner_text() == '7 VEÍCULOS · 1 CAMPEÃO'
    page.get_by_role('button',name='PRESS START',exact=True).click()
    assert page.evaluate('ui.screen') == 'driverSelect'
    assert page.evaluate('ui.race') is None, 'first start only unlocks audio and opens selection'
    assert page.locator('[data-driver]').count() == 3
    marquinhos = page.locator('[data-driver="marquinhos"]')
    assert 'Marquinhos' in marquinhos.inner_text()
    assert 'Mencacci' not in marquinhos.inner_text() and '#null' not in marquinhos.inner_text()
    assert '/assets/v4/cars/marquinhos-rear.png' in marquinhos.locator('.menu-car').get_attribute('src')
    marquinhos.click()
    page.get_by_role('button',name='CONFIRMAR PILOTO',exact=True).click()
    assert page.evaluate('ui.race.player.driver') == 'marquinhos'
    assert page.locator('.grid-names span').count() == 7
    assert '#null' not in page.locator('.grid-intro').inner_text()
    page.get_by_role('button',name='TROCAR PILOTO',exact=True).click()
    page.locator('[data-driver="felipe"]').click()
    assert page.evaluate('ui.selected') == 'felipe'
    page.evaluate("window.oldConfirm = document.querySelector('#confirm-driver')")
    page.get_by_role('button',name='CONFIRMAR PILOTO',exact=True).click()
    page.evaluate("window.gridRace = ui.race; oldConfirm.click()")
    assert page.evaluate('ui.race === gridRace'), 'stale double-confirm cannot recreate the race'
    assert page.evaluate('ui.screen') == 'grid'
    assert page.evaluate('ui.race.player.driver') == 'felipe'
    assert page.evaluate('ui.race.phase') == 'paused', 'grid cannot advance the simulation'
    page.get_by_role('button',name='LARGAR',exact=True).click()
    assert page.evaluate('ui.race.phase') == 'countdown'
    assert '/ 7' in page.locator('#position').inner_text()
    page.evaluate("ui.race.phase='racing'; ui.update(performance.now())")
    for selector, pointer_id in [('[data-action="left"]', 21), ('[data-action="throttle"]', 22), ('[data-action="nitro"]', 23)]:
        page.locator(selector).dispatch_event('pointerdown', {'pointerId': pointer_id, 'pointerType':'touch', 'bubbles':True})
    assert page.evaluate('ui.input.count') == 3
    assert page.evaluate('ui.input.snapshot().left && ui.input.snapshot().throttle && ui.input.snapshot().nitro')
    page.locator('[data-action="nitro"]').dispatch_event('pointercancel', {'pointerId':23,'bubbles':True})
    assert page.evaluate('ui.input.count') == 2
    page.locator('[data-action="left"]').dispatch_event('lostpointercapture', {'pointerId':21,'bubbles':True})
    assert not page.evaluate('ui.input.snapshot().left')
    page.keyboard.down('ArrowRight')
    assert page.evaluate('ui.input.snapshot().right')
    page.keyboard.press('Escape')
    assert page.evaluate('ui.race.phase') == 'paused'
    assert page.evaluate('ui.input.count') == 0
    page.get_by_role('button',name='TROCAR PILOTO',exact=True).click()
    assert page.evaluate('ui.screen') == 'driverSelect'
    assert page.evaluate('ui.race') is None
    page.locator('[data-driver="daniel"]').click()
    page.wait_for_timeout(150)
    assert page.evaluate('ui.audio.ctx.state') == 'running', 'selection must resume audio after leaving pause'
    page.get_by_role('button',name='VOLTAR',exact=True).click()
    assert page.evaluate('ui.screen') == 'title'
    page.keyboard.press('Enter')
    assert page.evaluate('ui.screen') == 'driverSelect'
    page.emulate_media(reduced_motion='reduce')
    page.get_by_role('button', name='VOLTAR',exact=True).click()
    assert page.locator('.press-start').evaluate("e => getComputedStyle(e).animationName") == 'none'
    for winner in ['daniel','felipe','marquinhos','npc-blue','npc-yellow','npc-purple','npc-silver']:
        page.evaluate("""winner => {
            ui.showGrid(1, 2);
            const r = ui.race;
            r.phase = 'finished'; r.winner = winner; r.elapsed = 40;
            for (const d of r.racers) { d.finishTime = d.driver === winner ? 40 : null; d.laps = d.driver === winner ? 1 : 0; }
            ui.showResults();
        }""", winner)
        assert page.locator('tbody tr').count() == 7
        assert 'de 7' in page.locator('.results-content').inner_text()
        assert '#null' not in page.locator('.results-content').inner_text()
        assert page.locator('tbody tr').first.get_attribute('data-result-driver') == winner
        assert page.locator('td', has_text='Não concluiu').count() == 6
        page.get_by_role('button',name='VER PÓDIO',exact=True).click()
        assert page.locator('.podium-screen').get_attribute('data-winner') == winner
        assert f'{winner}-0.png' in page.locator('.champion-frame').get_attribute('src')
        if winner in ['daniel', 'felipe', 'marquinhos']:
            page.evaluate('for(let i=0;i<56;i++) ui.update(ui.lastUpdate + 100)')
            assert page.locator('.podium-screen').get_attribute('data-stage') == '4'
            page.wait_for_function('document.querySelector(".champion-frame").complete')
            image_box = page.locator('.champion-frame').bounding_box()
            spray_box = page.locator('.champagne-fx').bounding_box()
            mouth = {'daniel':(185,165), 'felipe':(43,139), 'marquinhos':(198.24242424242425,184.07713498622587)}[winner]
            expected_x = image_box['x'] + image_box['width'] * mouth[0] / 256
            expected_y = image_box['y'] + image_box['height'] * mouth[1] / 512
            assert abs(spray_box['x'] - expected_x) < 1.5, f'{winner}: spray must start at the drawn open bottle mouth'
            assert abs(spray_box['y'] - expected_y) < 1.5, f'{winner}: spray height must match the drawn open bottle mouth'
            direction = page.locator('.champagne-fx img').first.evaluate("""el => {
                el.style.animation='none';el.style.transform='translate(var(--x),var(--y))';
                const x=new DOMMatrixReadOnly(getComputedStyle(el).transform).m41;
                el.style.removeProperty('animation');el.style.removeProperty('transform');return x;
            }""")
            assert direction < 0 if winner == 'felipe' else direction > 0
        page.evaluate('for(let i=0;i<90;i++) ui.update(ui.lastUpdate + 100)')
        assert page.locator('.podium-screen').get_attribute('data-stage') == '5'
        page.get_by_role('button',name='VOLTAR À CAPA',exact=True).click()
        assert page.evaluate('ui.screen') == 'title'
    page.evaluate("""() => {
      ui.showGrid(); ui.race.phase='finished'; ui.race.winner='felipe';
      ui.showPodium();
      for (let i=0;i<60;i++) ui.update(performance.now()+100+i*100);
    }""")
    page.evaluate("window.dispatchEvent(new Event('blur'))")
    assert page.locator('#podium-continue').is_visible(), 'podium must explicitly pause after blur'
    assert page.locator('.champagne-fx img').first.evaluate("el=>getComputedStyle(el).animationPlayState") == 'paused'
    stage = page.locator('.podium-screen').get_attribute('data-stage')
    page.evaluate('ui.update(performance.now()+100000)')
    assert page.locator('.podium-screen').get_attribute('data-stage') == stage
    page.locator('#podium-continue').click()
    assert page.locator('#podium-continue').is_hidden()
    assert page.locator('.champagne-fx img').first.evaluate("el=>getComputedStyle(el).animationPlayState") == 'running'
    evidence = Path('/workspace/work/marquinhos-ui')
    evidence.mkdir(parents=True, exist_ok=True)
    layouts = []
    for width, height in [(1600,900), (915,412), (740,360)]:
        page.set_viewport_size({'width':width, 'height':height})
        page.evaluate('ui.showTitle()')
        page.wait_for_function('Array.from(document.querySelectorAll(".cover-artboard img")).every(i=>i.complete && i.naturalWidth>0)')
        cover = page.evaluate("""() => {
          const box = e => {const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height}};
          return {frame:box(document.querySelector('.cover-frame')), start:box(document.querySelector('#press-start')),
            art:[...document.querySelectorAll('.cover-hero, .cover-car')].map(box),
            buttons:[...document.querySelectorAll('.cover-screen button')].map(box)};
        }""")
        frame = cover['frame']
        for box in cover['art']:
            assert box['x'] >= frame['x'] - 1 and box['y'] >= frame['y'] - 1
            assert box['x'] + box['width'] <= frame['x'] + frame['width'] + 1
            assert box['y'] + box['height'] <= frame['y'] + frame['height'] + 1
        assert all(box['width'] >= 44 and box['height'] >= 44 for box in cover['buttons']), 'cover controls retain physical touch size'
        assert page.locator('.cover-car.cover-marquinhos').bounding_box()['width'] > page.locator('.cover-car.cover-daniel').bounding_box()['width']
        page.screenshot(path=str(evidence / f'title-{width}x{height}.png'))
        page.get_by_role('button',name='PRESS START',exact=True).click()
        page.wait_for_function('Array.from(document.querySelectorAll(".driver img")).every(i=>i.complete && i.naturalWidth>0)')
        selection = page.evaluate("""() => {
          const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}};
          return {cards:[...document.querySelectorAll('[data-driver]')].map(box),
            controls:[...document.querySelectorAll('.menu button,.menu select')].map(box),
            clipped:[...document.querySelectorAll('.driver-copy')].some(e=>e.scrollWidth>e.clientWidth+1)};
        }""")
        assert len(selection['cards']) == 3 and not selection['clipped']
        for box in selection['controls']:
            assert box['height'] >= 44 and box['width'] >= 44
            assert box['x'] >= 0 and box['y'] >= 0
            assert box['x'] + box['width'] <= width + 1 and box['y'] + box['height'] <= height + 1
        page.screenshot(path=str(evidence / f'selection-{width}x{height}.png'))
        layouts.append({'viewport':[width,height], 'start':cover['start'], 'cards':selection['cards']})
    page.set_viewport_size({'width':412,'height':915})
    page.evaluate('ui.showTitle()')
    assert page.locator('#rotate').is_visible()
    assert page.locator('#press-start').is_disabled()
    page.locator('#press-start').evaluate('button=>button.click()')
    assert page.evaluate('ui.screen') == 'title', 'portrait cannot start behind rotate prompt'
    (evidence / 'layout.json').write_text(json.dumps(layouts, indent=2))
    browser.close()
    print('UI V4: three pilots, seven results/podium winners, countdown/pause, multi-pointer release, keyboard and reduced motion PASS')
