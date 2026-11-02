"""A mobile connection taking >12s must recover without a false fatal error."""
import sys, time
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8765/game/'
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':915,'height':412},is_mobile=True,has_touch=True)
    def slow(route):
        time.sleep(13)
        route.continue_()
    page.route('**/assets/v4/cascavel/pit.png',slow)
    page.goto(url,wait_until='domcontentloaded')
    page.wait_for_function('document.body.dataset.ready === "true"',timeout=30000)
    assert page.locator('#fatal').is_hidden(), 'successful delayed assets cannot leave a fatal error visible'
    page.get_by_role('button',name='PRESS START',exact=True).tap()
    assert page.locator('#ui').get_attribute('data-screen')=='driverSelect'
    failed=browser.new_page(viewport={'width':915,'height':412})
    failed.route('**/assets/v4/cascavel/pit.png',lambda route:route.abort())
    failed.goto(url,wait_until='domcontentloaded')
    failed.locator('#fatal').wait_for(state='visible')
    assert 'Erro' in failed.locator('#fatal').inner_text(), 'a genuinely failed asset must still report its error'
    browser.close()
    print('PASS: delayed asset >12s recovers, mobile selection works, genuine asset failures stay visible')
