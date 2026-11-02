import { buildTrack } from './track.js';
import { stepRace } from './sim.js';
import { createRaceScene } from './render.js';
import { Ui } from './ui.js';

const boot = window.__boot || { step() {}, show() {} };
boot.step('módulos carregados');
const params = new URLSearchParams(location.search);
const ASSETS = params.get('assets') || new URL('../../assets/', import.meta.url).href; // gh-pages/claude/src -> gh-pages/assets/
const debug = params.has('debug');
window.__ftwErrors = [];

function showError(msg) {
  window.__ftwErrors.push(String(msg));
  boot.show(`Erro: ${msg}`);
}

const loadScript = (src) => new Promise((ok, no) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = () => no(new Error(`falha ao carregar ${src}`)); document.head.appendChild(s); });
async function loadPhaser() {
  boot.step('carregando Phaser local');
  try { const m = await import(new URL('phaser-Czz4FBZH.js', ASSETS).href); const P = m.g(m.r()); if (P?.Game) return P; boot.step('Phaser local sem Game'); } catch (e) { boot.step(`Phaser local falhou: ${e?.message || e}`); console.warn('Phaser local falhou', e); }
  boot.step('carregando Phaser da CDN');
  await loadScript('https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js'); return window.Phaser; // plano B
}

const track = buildTrack({ reverse: params.get('sentido') === 'inverso' });
let current = null;
const ui = new Ui(document.getElementById('ui'), { track, assets: ASSETS, debug, onRace: (r) => { current = r; } });
boot.step('interface criada');
const Phaser = await loadPhaser();
boot.step('Phaser carregado; criando jogo');
const Scene = createRaceScene(Phaser, { assets: ASSETS, track, getRace: () => current, onError: showError,
  onReady: () => { document.getElementById('loading')?.remove(); document.body.dataset.ready = 'true'; boot.last = 'pronto'; } });
window.__ftwGame = new Phaser.Game({ type: Phaser.AUTO, parent: 'world', backgroundColor: '#405b35', antialias: true, disableContextMenu: true,
  scale: { mode: Phaser.Scale.RESIZE, width: innerWidth, height: innerHeight }, audio: { noAudio: true }, scene: [Scene],
  render: { roundPixels: false, powerPreference: 'high-performance' }, fps: { target: 60, forceSetTimeOut: false } });
boot.step('jogo criado; carregando imagens');

let last = performance.now(), acc = 0;
function frame(now) {
  const dt = Math.min((now - last) / 1000, 0.1); last = now;
  if (ui.portrait && ui.race && ui.race.phase !== 'paused' && ui.race.phase !== 'finished') ui.interrupt();
  acc += dt;
  while (acc >= 1 / 60) { if (ui.race) stepRace(ui.race, ui.input.snapshot(), 1 / 60); acc -= 1 / 60; }
  ui.update(now); requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
