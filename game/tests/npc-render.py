"""Real Phaser regression: all four NPC textures, six view states and anchors."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('/workspace/work/qa-npc-reference');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=b.new_page(viewport={'width':915,'height':412},has_touch=True,is_mobile=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:errors.append(f'HTTP{r.status}:{r.url}')if r.status>=400 else None)
    page.goto('http://127.0.0.1:8765/game/tests/npc-render.html')
    page.wait_for_function('window.npcReady && npcGame.scene.getScene("race").rivals.filter(s=>s.texture.key.startsWith("npc-")).length===4')
    states=[];anchors=None
    for frame,wheel,braking in [(0,0,False),(1,-1,False),(2,1,False),(3,0,True),(4,-1,True),(5,1,True)]:
        page.evaluate('''args=>{for(const d of npcRace.extras){d.wheel=args.wheel;d.braking=args.braking;}document.querySelector('#label').textContent='NPC view '+args.frame;}''',{'wheel':wheel,'braking':braking,'frame':frame})
        page.wait_for_function('f=>npcGame.scene.getScene("race").rivals.filter(s=>s.texture.key.startsWith("npc-")).every(s=>Number(s.frame.name)===f)',arg=frame)
        actual=page.evaluate('''()=>npcGame.scene.getScene('race').rivals.filter(s=>s.texture.key.startsWith('npc-')).map(s=>({key:s.texture.key,frame:Number(s.frame.name),x:s.x,y:s.y,ratio:s.displayWidth/s.displayHeight,origin:s.originY,visible:s.visible}))''')
        assert len(actual)==4 and all(s['visible']for s in actual)
        assert all(abs(s['ratio']-560/512)<1e-6 and s['origin']==470/512 for s in actual)
        positions=[(s['x'],s['y'])for s in actual]
        if anchors is None:anchors=positions
        assert positions==anchors,'Changing view must not move the projected rear axle'
        page.screenshot(path=str(out/f'frame-{frame}.png'));states.append(actual)
    assert not page.evaluate('npcErrors') and not errors
    (out/'frames.json').write_text(json.dumps({'states':states,'errors':errors},indent=2))
    b.close();print('PASS: real Phaser, 4 NPCs x6 states, correct aspect/pivot, no frame-induced position jumps or HTTP errors.')
