"""Real DOM UI regression suite. Run against a server rooted at repository root."""
import sys
from playwright.sync_api import sync_playwright
url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/game/tests/ui-flow.html'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
    page = browser.new_page(viewport={'width':960,'height':540}, has_touch=True)
    page.goto(url)
    page.wait_for_function('window.ui !== undefined')
    assert page.evaluate('ui.screen') == 'title', 'first state must be title'
    page.get_by_role('button',name='PRESS START',exact=True).click()
    assert page.evaluate('ui.screen') == 'driverSelect'
    assert page.evaluate('ui.race') is None, 'first start only unlocks audio and opens selection'
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
    for winner in ['daniel','felipe','npc-blue','npc-yellow','npc-purple','npc-silver']:
        page.evaluate("""winner => {
            ui.showGrid(1, 2);
            const r = ui.race;
            r.phase = 'finished'; r.winner = winner; r.elapsed = 40;
            for (const d of r.racers) { d.finishTime = d.driver === winner ? 40 : null; d.laps = d.driver === winner ? 1 : 0; }
            ui.showResults();
        }""", winner)
        assert page.locator('tbody tr').count() == 6
        assert page.locator('tbody tr').first.get_attribute('data-result-driver') == winner
        assert page.locator('td', has_text='Não concluiu').count() == 5
        page.get_by_role('button',name='VER PÓDIO',exact=True).click()
        assert page.locator('.podium-screen').get_attribute('data-winner') == winner
        assert f'{winner}-0.png' in page.locator('.champion-frame').get_attribute('src')
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
    browser.close()
    print('UI V4: title/select/grid/countdown/pause, multi-pointer release, keyboard, reduced motion and six winner results/podium PASS')
