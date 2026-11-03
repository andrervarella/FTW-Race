"""Keep podium runner captions separate from the place numbers for all seven winners."""
import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':915,'height':412},has_touch=True,is_mobile=True)
    page.goto(sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/game/tests/ui-flow.html')
    page.wait_for_function('window.ui !== undefined')
    for width,height in [(1600,900),(915,412),(740,360)]:
        page.set_viewport_size({'width':width,'height':height})
        for winner in ['daniel','felipe','marquinhos','npc-blue','npc-yellow','npc-purple','npc-silver']:
            page.evaluate("winner=>{ui.showGrid();ui.race.phase='finished';ui.race.winner=winner;ui.showPodium()}",winner)
            assert '#null' not in page.locator('.podium-screen').inner_text()
            for i,step in [(0,'two'),(1,'three')]:
                label=page.locator(f'.runner-{i} span').bounding_box()
                number=page.locator(f'.step-{step} b').bounding_box()
                overlap=(label['x']<number['x']+number['width'] and label['x']+label['width']>number['x'] and label['y']<number['y']+number['height'] and label['y']+label['height']>number['y'])
                assert not overlap, f'{width}×{height}, {winner}: runner {i} label must not cover podium number'
            for button in page.locator('.podium-actions button').all():
                box=button.bounding_box()
                assert box['height']>=44 and box['width']>=44, f'{width}×{height}, {winner}, {button.inner_text()}: touch target {box}'
                assert box['x']>=0 and box['y']+box['height']<=height+1
    browser.close()
    print('PASS: all seven podium winners at1600×900,915×412,740×360; labels avoid place numbers and touch controls retain44px')
