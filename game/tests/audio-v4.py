"""Real Web Audio checks: 7 winners × 3 modes, six podium beats and lifecycle silence.
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
          const { podiumMarkup, updatePodium } = await import('/game/src/podium.js');
          const { createRace } = await import('/game/src/sim.js');
          const { buildTrack } = await import('/game/src/track.js');
          const winners = ['daniel', 'felipe', 'marquinhos', 'npc-blue', 'npc-yellow', 'npc-purple', 'npc-silver'];
          const beatTimes = [0.05, 1.25, 2.65, 3.95, 5.35, 7.55];
          const track = buildTrack();
          const rendered = [];
          for (const mode of ['tudo', 'efeitos', 'mudo']) {
            for (const winner of winners) {
              const race = createRace(track, 'marquinhos');
              if (race.racers.length !== 7) throw Error('podium audio requires all seven real participants');
              race.phase = 'finished'; race.winner = winner;
              const champion = race.racers.find(racer => racer.driver === winner);
              champion.finishTime = 80; champion.laps = 3;
              const root = document.createElement('div');
              root.innerHTML = podiumMarkup(race, '/game/assets/legacy/');
              if (root.querySelector('.podium-heading h1').textContent !== (winner === 'marquinhos' ? 'Marquinhos' : root.querySelector('.champion-frame').alt)) throw Error(`wrong podium winner ${winner}`);
              if (root.textContent.includes('#null')) throw Error(`invented podium number ${winner}`);
              const c = new OfflineAudioContext(1, 160000, 16000), a = new GameAudio(c);
              a.build(); a.setMode(mode);
              const stages = [];
              const feedback = { podium(stage) { stages.push(stage); a.podium(stage, beatTimes[stage]); } };
              updatePodium(root, race, 0, feedback);
              for (let i = 0; i < 80; i++) updatePodium(root, race, 0.1, feedback);
              if (stages.join(',') !== '0,1,2,3,4,5') throw Error(`podium sequence ${winner}/${mode}: ${stages}`);
              if (!root.querySelector('.champion-frame').src.endsWith(`/${winner}-5.png`)) throw Error(`wrong final podium frame ${winner}`);
              const buf = await c.startRendering(), samples = buf.getChannelData(0);
              let peak = 0, nonzero = 0;
              for (const v of samples) { if (!Number.isFinite(v)) throw Error('nonfinite podium sample'); peak = Math.max(peak, Math.abs(v)); if (Math.abs(v) > 0.00001) nonzero++; }
              if (mode === 'mudo' ? peak > 0.000001 : nonzero < 100) throw Error(`podium audio ${winner}/${mode}: peak ${peak}, samples ${nonzero}`);
              const beats = beatTimes.map((at, stage) => {
                const start = Math.floor(at * 16000), end = Math.min(samples.length, start + 8000);
                const active = samples.subarray(start, end).some(value => Math.abs(value) > 0.00001);
                if (active !== (mode !== 'mudo')) throw Error(`podium beat ${winner}/${mode}/${stage}: active ${active}`);
                return { stage, active };
              });
              rendered.push({ winner, mode, stages, beats, peak, nonzero });
            }
          }
          if (rendered.length !== 21) throw Error(`expected 21 winner/mode combinations, got ${rendered.length}`);
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
