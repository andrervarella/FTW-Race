"""Real Web Audio checks, including rendered podium FX and lifecycle silence.
Run from repo root: python3 game/tests/audio-v4.py (Chromium needs browser permissions).
"""
import functools
import http.server
import json
import pathlib
import threading
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[2]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        page.goto(f'http://127.0.0.1:{server.server_port}/')
        result = page.evaluate('''async () => {
          const { GameAudio } = await import('/game/src/audio.js');
          const rendered = [];
          for (const mode of ['tudo', 'efeitos', 'mudo']) {
            for (let stage = 0; stage < 6; stage++) {
              const c = new OfflineAudioContext(1, 32000, 16000), a = new GameAudio(c);
              a.build(); a.setMode(mode); a.podium(stage, 0.05);
              const buf = await c.startRendering(), samples = buf.getChannelData(0);
              let peak = 0, nonzero = 0;
              for (const v of samples) { if (!Number.isFinite(v)) throw Error('nonfinite podium sample'); peak = Math.max(peak, Math.abs(v)); if (Math.abs(v) > 0.00001) nonzero++; }
              if (mode === 'mudo' ? peak > 0.000001 : nonzero < 100) throw Error(`podium audio ${mode}/${stage}: peak ${peak}, samples ${nonzero}`);
              rendered.push({ mode, stage, peak, nonzero });
            }
          }
          const c = new OfflineAudioContext(1, 8000, 16000), a = new GameAudio(c);
          a.build(); a.selection(0.02);
          const buf = await c.startRendering();
          if (!buf.getChannelData(0).some(v => Math.abs(v) > 0.00001)) throw Error('selection silent');
          window.audioV4 = new GameAudio();
          const button = document.createElement('button'); button.id = 'audio-v4-unlock'; button.textContent = 'Audio';
          button.onclick = () => { window.unlocked = Promise.all([audioV4.unlock(), audioV4.unlock(), audioV4.unlock()]); };
          document.body.append(button);
          return { rendered, selection: 'PASS' };
        }''')
        page.locator('#audio-v4-unlock').click()
        lifecycle = page.evaluate('''async () => {
          const states = await window.unlocked, a = window.audioV4;
          if (!states.every(Boolean) || a.ctx.state !== 'running') throw Error('unlock failed');
          const timer = a.timer;
          await a.unlock();
          if (a.timer !== timer) throw Error('duplicate music timer');
          a.podium(4);
          await a.suspend();
          if (a.timer !== null || a.ctx.state !== 'suspended' || a.sources.size) throw Error('suspend left work active');
          const step = a.step;
          await new Promise(r => setTimeout(r, 220));
          if (a.step !== step) throw Error('music advanced while suspended');
          await a.unlock();
          if (a.ctx.state !== 'running' || a.timer === null) throw Error('resume failed');
          a.setMode('mudo'); a.selection(); a.podium(3);
          if (a.sources.size) throw Error('mute schedules new feedback');
          await a.suspend();
          const interrupted = a.unlock();
          const paused = a.suspend();
          const resumed = a.unlock();
          await Promise.all([interrupted, paused]);
          if (!(await resumed) || a.ctx.state !== 'running') throw Error('unlock after interrupted gesture failed');
          await a.suspend(); await a.ctx.close();
          if (await a.unlock()) throw Error('closed audio context should remain silent');
          return { repeatedUnlock: 'PASS', suspend: 'PASS', resume: 'PASS', mute: 'PASS' };
        }''')
        print(json.dumps({'browser': browser.version, **result, 'lifecycle': lifecycle}, ensure_ascii=False))
        browser.close()
finally:
    server.shutdown(); server.server_close()
