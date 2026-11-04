"""Measure live Web Audio output through real touch/UI with strict autoplay.

No production debug hooks. Test-only taps observe the final output graph; controlled
cue calls exercise the same live GameAudio instance after the real race/UI flow.
"""
import argparse
import base64
import functools
import http.server
import json
from pathlib import Path
import threading
import traceback
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from published_runtime import inspect_published_runtime, resolve_runtime_base

PROBE = r'''(() => {
 const Original = window.AudioContext;
 const connect = AudioNode.prototype.connect;
 window.__audioContexts = []; window.__audioOutputs = []; window.__audioResumeCalls = [];
 window.AudioContext = class extends Original {
   constructor(...args) { super(...args); window.__audioContexts.push(this); }
 };
 const resume = Original.prototype.resume;
 Original.prototype.resume = function() {
   __audioResumeCalls.push({active:navigator.userActivation.isActive,state:this.state});
   return resume.call(this);
 };
 AudioNode.prototype.connect = function(destination,...args) {
   const result = connect.call(this,destination,...args);
   if (destination === this.context.destination) {
     const analyser=this.context.createAnalyser(); analyser.fftSize=2048;
     const silence=this.context.createGain(); silence.gain.value=0;
     connect.call(this,analyser); connect.call(analyser,silence); connect.call(silence,this.context.destination);
     const recording=this.context.createMediaStreamDestination(); connect.call(this,recording);
     __audioOutputs.push({context:this.context,analyser,recording});
   }
   return result;
 };
 const sample = async (output,milliseconds=300) => {
   if (!output) return {peak:0,rms:0,frames:0,context:null};
   const start=performance.now(), before=output.context.currentTime;
   let peak=0,sum=0,frames=0,snapshots=0,maxTimerGap=0,lastSnapshot=start;
   do {
     const now=performance.now();maxTimerGap=Math.max(maxTimerGap,now-lastSnapshot);lastSnapshot=now;snapshots++;
     const data=new Float32Array(output.analyser.fftSize); output.analyser.getFloatTimeDomainData(data);
     for(const value of data){ if(!Number.isFinite(value))throw Error('Nonfinite output sample');peak=Math.max(peak,Math.abs(value));sum+=value*value;frames++; }
     await new Promise(resolve=>setTimeout(resolve,10));
   // One delayed 10ms timer previously ended the wall-clock window after a
   // single <47ms analyser block. Observe multiple actual output blocks even
   // when a loaded browser delays timers; never lower the signal threshold.
   } while((performance.now()-start<milliseconds||snapshots<8)&&performance.now()-start<10000);
   const elapsed=output.context.currentTime-before;
   // Suspended analysers retain the last rendered block; it is not live output.
   if(output.context.state!=='running'||elapsed===0)return {peak:null,rms:null,frames:0,context:output.context.state,contextElapsed:elapsed,snapshots,wallElapsed:performance.now()-start,maxTimerGap};
   if(snapshots<8)throw Error('Insufficient live audio observations: '+snapshots+' in '+(performance.now()-start)+'ms');
   return {peak,rms:Math.sqrt(sum/Math.max(frames,1)),frames,context:output.context.state,contextElapsed:elapsed,snapshots,wallElapsed:performance.now()-start,maxTimerGap};
 };
 window.__sampleLiveAudio = milliseconds => sample(__audioOutputs.at(-1),milliseconds);
 window.__sampleAudioBus = async (name,milliseconds=300) => {
   const audio=window.__liveGameAudio;
   const node=name==='engine'?audio.eng.g:name==='music'?audio.musicBus:audio.sfxBus;
   const analyser=audio.ctx.createAnalyser(),silence=audio.ctx.createGain();silence.gain.value=0;
   connect.call(node,analyser);connect.call(analyser,silence);connect.call(silence,audio.ctx.destination);
   try{return await sample({context:audio.ctx,analyser},milliseconds);}
   finally{node.disconnect(analyser);analyser.disconnect();silence.disconnect();}
 };
 window.__recordLiveAudio = milliseconds => new Promise(resolve => {
   const output=__audioOutputs.at(-1),chunks=[];
   const recorder=new MediaRecorder(output.recording.stream);
   recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
   recorder.onstop=async()=>{const blob=new Blob(chunks,{type:recorder.mimeType});const bytes=new Uint8Array(await blob.arrayBuffer());let binary='';for(const b of bytes)binary+=String.fromCharCode(b);resolve({base64:btoa(binary),mime:blob.type,bytes:bytes.length});};
   recorder.start();setTimeout(()=>recorder.stop(),milliseconds);
 });
 window.__measureContinuousCue = async name => {
   const audio=__liveGameAudio,update=audio.update,hadOwn=Object.hasOwn(audio,'update');
   // Controlled subsystem stimuli on the real mixer. Keep the UI frame loop
   // from replacing this temporary sound state; no race state is modified.
   audio.update=()=>{};
   try {
     const player={speed:name==='skid'?40:name==='gravel'?20:60,wheel:name==='skid'?1:0,offRoad:name==='gravel',nitroRemaining:0,laps:0};
     update.call(audio,{phase:'racing',player,config:{laps:1}},{throttle:true});
     for(const gain of [audio.eng.g,...['skid','gravel','wind'].filter(key=>key!==name).map(key=>audio[key].g)]){
       gain.gain.cancelScheduledValues(audio.ctx.currentTime);gain.gain.setValueAtTime(0,audio.ctx.currentTime);
     }
     await new Promise(resolve=>setTimeout(resolve,220));return await __sampleLiveAudio(220);
   } finally { if(hadOwn)audio.update=update;else delete audio.update;update.call(audio,null,{}); }
 };
})();'''

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*_): pass


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url',nargs='?')
    parser.add_argument('--output',default='work/audio-live')
    parser.add_argument('--executable-path')
    args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    server=None
    if args.url:
        url=args.url
    else:
        root=Path(__file__).resolve().parents[2]
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        url=f'http://127.0.0.1:{server.server_port}/game/'
    report={'url':url,'scope':'real Chromium mobile/touch emulation; live output graph, not physical speakers','cues':[],'errors':[],
            'http_errors':[],'failed_requests':[],'console_errors':[],'screenshots':[]}
    try:
        published=inspect_published_runtime(url)
        runtime_url=published['resolved_runtime_url']
        report.update({key:published[key]for key in ['requested_url','resolved_runtime_url','header_diagnostics']})
        with sync_playwright()as p:
            options={'args':['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=document-user-activation-required'],'ignore_default_args':['--mute-audio']}
            if args.executable_path:options['executable_path']=args.executable_path
            browser=p.chromium.launch(**options);report['browser']=browser.version
            # A normal first touch must unlock the music, without first visiting
            # a sound control or injecting an AudioContext resume from automation.
            gesture_context=browser.new_context(viewport={'width':915,'height':412},is_mobile=True,has_touch=True)
            gesture=gesture_context.new_page();gesture.add_init_script(PROBE);gesture.goto(url)
            gesture.wait_for_function('document.body.dataset.ready === "true"')
            assert resolve_runtime_base(gesture.content(),gesture.url,urljoin(url,'./'))==runtime_url
            assert gesture.evaluate('__audioContexts.length')==0
            gesture.locator('#press-start').tap();gesture.wait_for_timeout(450)
            first_gesture=gesture.evaluate('__sampleLiveAudio(250)')
            report['first_press_start_touch']=first_gesture
            assert first_gesture['rms']>0.001 and gesture.evaluate('__audioResumeCalls[0].active'),'The first normal touch must resume Web Audio under trusted activation'
            gesture_context.close()
            report['keyboard']=[]
            for key in ['Space','Enter']:
                keyboard_context=browser.new_context(viewport={'width':915,'height':412})
                keyboard=keyboard_context.new_page();keyboard.add_init_script(PROBE);keyboard.goto(url)
                keyboard.wait_for_function('document.body.dataset.ready === "true"')
                assert resolve_runtime_base(keyboard.content(),keyboard.url,urljoin(url,'./'))==runtime_url
                keyboard.evaluate('''async moduleUrl=>{
                  const {GameAudio}=await import(moduleUrl),unlock=GameAudio.prototype.unlock;
                  GameAudio.prototype.unlock=function(...args){window.__liveGameAudio=this;return unlock.apply(this,args);};
                }''',urljoin(runtime_url,'src/audio.js'))
                keyboard.locator('#screen-sound').focus();keyboard.keyboard.press(key);keyboard.wait_for_timeout(350)
                signal=keyboard.evaluate('__sampleLiveAudio(200)')
                mode=keyboard.evaluate('__liveGameAudio.mode')
                report['keyboard'].append({'key':key,'mode':mode,**signal})
                assert mode=='tudo' and signal['rms']>0.001,(key,mode,signal)
                keyboard_context.close()
            context=browser.new_context(viewport={'width':915,'height':412},is_mobile=True,has_touch=True)
            page=context.new_page();page.add_init_script(PROBE)
            page.on('pageerror',lambda error:report['errors'].append(str(error)))
            page.on('response',lambda response:report['http_errors'].append({'status':response.status,'url':response.url})if response.status>=400 else None)
            page.on('requestfailed',lambda request:report['failed_requests'].append({'url':request.url,'failure':request.failure}))
            page.on('console',lambda message:report['console_errors'].append(message.text)if message.type=='error'else None)
            page.goto(url);page.wait_for_function('document.body.dataset.ready === "true"')
            assert resolve_runtime_base(page.content(),page.url,urljoin(url,'./'))==runtime_url,'Audio probe must import the module selected by the actual page'
            page.evaluate('''async moduleUrl=>{
              const {GameAudio}=await import(moduleUrl),unlock=GameAudio.prototype.unlock;
              GameAudio.prototype.unlock=function(...args){window.__liveGameAudio=this;return unlock.apply(this,args);};
              window.__liveAudioEvents=[];
              for(const method of ['beep','nitro','hit']){
                const original=GameAudio.prototype[method];
                GameAudio.prototype[method]=function(...args){__liveAudioEvents.push({method,args});return original.apply(this,args);};
              }
            }''',urljoin(runtime_url,'src/audio.js'))
            assert page.evaluate('__audioContexts.length')==0,'Before a gesture no context should be created'
            page.locator('#screen-sound').tap();page.wait_for_timeout(450)
            first=page.evaluate('__sampleLiveAudio(350)');report['first_sound_tap']=first
            report['first_sound_mode']=page.evaluate('__liveGameAudio.mode')
            assert report['first_sound_mode']=='tudo' and first['rms']>0.001,'First sound tap must enable menu music, not switch to silent effects-only menu'
            assert page.evaluate('__audioResumeCalls[0].active'),'Initial audio resume must run inside a trusted gesture'
            assert page.locator('#screen-sound').inner_text()!='ATIVAR SOM'
            recording=page.evaluate('__recordLiveAudio(1000)');(out/'menu-live.webm').write_bytes(base64.b64decode(recording.pop('base64')));report['recording']=recording
            page.evaluate("window.dispatchEvent(new Event('blur'))")
            page.wait_for_function('__liveGameAudio.ctx.state === "suspended" && document.querySelector("#screen-sound").textContent === "ATIVAR SOM"')
            page.locator('#screen-sound').tap();page.wait_for_timeout(250)
            control_resume=page.evaluate('__sampleLiveAudio(200)');report['resume_via_sound_control']=control_resume
            assert page.evaluate('__liveGameAudio.mode')=='tudo' and control_resume['rms']>0.001
            page.locator('#screen-sound').tap();page.wait_for_timeout(650)
            effects=page.evaluate('__sampleLiveAudio(180)');report['effects_menu_output']=effects;assert page.evaluate('__liveGameAudio.mode')=='efeitos' and effects['rms']<0.0001
            page.locator('#screen-sound').tap();page.wait_for_timeout(450)
            mute=page.evaluate('__sampleLiveAudio(180)');report['muted_menu_output']=mute;assert page.evaluate('__liveGameAudio.mode')=='mudo' and mute['rms']<0.0001
            page.evaluate("window.dispatchEvent(new Event('blur'))")
            page.wait_for_function('__liveGameAudio.ctx.state === "suspended"')
            location=page.locator('.cover-location').bounding_box()
            page.touchscreen.tap(location['x']+location['width']/2,location['y']+location['height']/2);page.wait_for_timeout(200)
            mute_resume=page.evaluate('__sampleLiveAudio(180)');report['mute_after_background_gesture']=mute_resume
            assert page.evaluate('__liveGameAudio.mode')=='mudo' and mute_resume['rms']<0.0001
            # Other gestures preserve an explicit mute choice.
            page.locator('#press-start').tap();page.wait_for_timeout(180)
            assert page.evaluate('__liveGameAudio.mode')=='mudo'
            assert page.evaluate('__sampleLiveAudio(180)')['rms']<0.0001
            page.locator('#screen-sound').tap();page.wait_for_timeout(350)
            assert page.evaluate('__liveGameAudio.mode')=='tudo'
            assert page.evaluate('__sampleLiveAudio(200)')['rms']>0.001
            assert page.locator('[data-driver]').count()==3
            page.locator('[data-driver="marquinhos"]').tap()
            assert page.locator('[data-driver="marquinhos"]').get_attribute('aria-pressed')=='true'
            report['selected_driver']='marquinhos'
            page.locator('#laps').select_option('1');page.get_by_role('button',name='CONFIRMAR PILOTO',exact=True).tap();page.get_by_role('button',name='LARGAR',exact=True).tap()
            page.wait_for_function('document.querySelector("#ui").dataset.phase === "countdown"')
            countdown=page.evaluate('__sampleLiveAudio(500)');report['countdown']=countdown
            assert countdown['rms']>0.001
            page.wait_for_function('document.querySelector("#ui").dataset.phase === "racing"')
            page.wait_for_timeout(700)
            engine=page.evaluate('__sampleAudioBus("engine",250)');report['engine_bus']=engine;assert engine['rms']>0.001
            music=page.evaluate('__sampleAudioBus("music",250)');report['racing_music_bus']=music;assert music['rms']>0.001
            page.locator('#sound').tap();page.wait_for_timeout(700)
            effects_engine=page.evaluate('__sampleAudioBus("engine",200)')
            effects_music=page.evaluate('__sampleAudioBus("music",200)')
            report['effects_race_buses']={'engine':effects_engine,'music':effects_music}
            assert page.evaluate('__liveGameAudio.mode')=='efeitos' and effects_engine['rms']>0.001 and effects_music['rms']<0.0001
            page.locator('#sound').tap();page.wait_for_timeout(500)
            muted_race=page.evaluate('__sampleLiveAudio(200)');report['muted_race_output']=muted_race
            assert page.evaluate('__liveGameAudio.mode')=='mudo' and muted_race['rms']<0.0001
            page.locator('#sound').tap();page.wait_for_timeout(500)
            assert page.evaluate('__liveGameAudio.mode')=='tudo' and page.evaluate('__sampleLiveAudio(200)')['rms']>0.001
            cdp=context.new_cdp_session(page)
            nitro_box=page.locator('[data-action="nitro"]').bounding_box()
            throttle_box=page.locator('[data-action="throttle"]').bounding_box()
            points=[{'x':box['x']+box['width']/2,'y':box['y']+box['height']/2,'id':index,'radiusX':5,'radiusY':5,'force':1}
                    for index,box in enumerate([nitro_box,throttle_box],1)]
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':points})
            page.wait_for_function('document.querySelector("#charges-left").textContent === "1"')
            nitro=page.evaluate('__sampleLiveAudio(300)');report['real_nitro_control']=nitro;assert nitro['rms']>0.001
            page.screenshot(path=str(out/'marquinhos-live-nitro-audio.png'));report['screenshots'].append('marquinhos-live-nitro-audio.png')
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            report['race_cue_calls']=page.evaluate('__liveAudioEvents')
            assert sum(event['method']=='beep'for event in report['race_cue_calls'])>=3
            assert any(event['method']=='nitro'for event in report['race_cue_calls'])
            # A pause must stop the clock of the actual output context.
            resumes_before_pause=page.evaluate('__audioResumeCalls.length')
            page.locator('#pause').tap();page.wait_for_timeout(180)
            paused=page.evaluate('__sampleLiveAudio(180)');report['pause']=paused
            assert paused['context']=='suspended' and paused['contextElapsed']==0
            assert page.evaluate('__audioResumeCalls.length')==resumes_before_pause,'The pause gesture must not resume the audio itself'
            page.get_by_role('button',name='CONTINUAR',exact=True).tap();page.wait_for_timeout(200)
            resumed=page.evaluate('__sampleLiveAudio(220)');report['resume']=resumed
            assert resumed['context']=='running' and resumed['rms']>0.001
            page.locator('#pause').tap();page.get_by_role('button',name='TROCAR PILOTO',exact=True).tap();page.get_by_role('button',name='VOLTAR',exact=True).tap();page.wait_for_timeout(200)
            assert page.evaluate('__sampleLiveAudio(180)')['rms']>0.001
            # Isolate the actual effect bus: menu has no engine; effects mode has no music.
            page.locator('#screen-sound').tap();page.wait_for_timeout(750)
            assert page.evaluate('__liveGameAudio.mode')=='efeitos'
            assert page.evaluate('__sampleLiveAudio(160)')['rms']<0.0001
            cues=[('selection',[]),('beep',[False]),('beep',[True]),('nitro',[]),('hit',[1]),('lap',[]),('finish',[])]+[('podium',[i])for i in range(6)]
            for method,params in cues:
                page.wait_for_timeout(1200 if method=='podium' else 800)
                page.evaluate('''cue=>__liveGameAudio[cue.method](...cue.params)''',{'method':method,'params':params})
                signal=page.evaluate('__sampleLiveAudio(350)');report['cues'].append({'method':method,'params':params,**signal});assert signal['rms']>0.0001,(method,params,signal)
            report['continuous_cues']=[]
            for name in ['skid','gravel','wind']:
                signal=page.evaluate('name=>__measureContinuousCue(name)',name)
                report['continuous_cues'].append({'name':name,**signal})
                assert signal['rms']>0.0001,(name,signal)
            page.locator('#screen-sound').tap();page.wait_for_timeout(500)
            page.evaluate('__liveGameAudio.hit(1);__liveGameAudio.nitro();__liveGameAudio.podium(5)')
            muted=page.evaluate('__sampleLiveAudio(300)');assert muted['rms']<0.0001
            report['resume_calls']=page.evaluate('__audioResumeCalls')
            assert not report['errors'] and not report['http_errors'] and not report['failed_requests'] and not report['console_errors'],report
            report['status']='passed';browser.close()
    except Exception:
        report['status']='failed';report['exception']=traceback.format_exc()
    finally:
        if server:server.shutdown();server.server_close()
        (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'output':str(out),'first_sound_tap':report.get('first_sound_tap'),'first_sound_mode':report.get('first_sound_mode'),'cues':len(report['cues'])}))
    raise SystemExit(0 if report['status']=='passed' else 1)

if __name__=='__main__':main()
