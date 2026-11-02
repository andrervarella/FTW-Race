"""Keep podium runner captions separate from the place numbers on mobile."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':915,'height':412},has_touch=True,is_mobile=True)
    page.goto('http://127.0.0.1:8765/game/tests/ui-flow.html')
    page.wait_for_function('window.ui !== undefined')
    page.evaluate("ui.showGrid();ui.race.phase='finished';ui.race.winner='npc-purple';ui.showPodium()")
    for i,step in [(0,'two'),(1,'three')]:
        label=page.locator(f'.runner-{i} span').bounding_box()
        number=page.locator(f'.step-{step} b').bounding_box()
        overlap=(label['x']<number['x']+number['width'] and label['x']+label['width']>number['x'] and label['y']<number['y']+number['height'] and label['y']+label['height']>number['y'])
        assert not overlap, f'runner {i} label must not cover podium number'
    browser.close()
    print('PASS: mobile podium labels do not overlap place numbers')
