// Interface em DOM por cima do canvas: menu, HUD, controles de toque, pausa, resultado, aviso de orientação, depuração.
import { DRIVERS } from './config.js';
import { InputState, KEYMAP } from './input.js';
import { GameAudio, MODE_LABEL } from './audio.js';
import { createRace, pauseRace, resumeRace, playerPosition, formatTime } from './sim.js';

export class Ui {
  constructor(root, { track, assets, onRace, debug }) {
    Object.assign(this, { root, track, assets, onRace, debug, race: null, input: new InputState(), audio: new GameAudio(), selected: 'daniel', screen: 'menu', renderedPhase: '', lastHud: 0, fps: 0, fpsAcc: 0, fpsN: 0 });
    this.menu();
    document.addEventListener('pointerdown', () => this.audio.unlock().catch(() => {}), { once: true }); // navegadores exigem um toque para liberar o áudio
    const stop = () => this.interrupt();
    window.addEventListener('blur', stop);
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    document.addEventListener('contextmenu', (e) => e.preventDefault());
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Escape') return this.togglePause();
      const a = KEYMAP[e.code]; if (a && this.race?.phase === 'racing') { e.preventDefault(); this.input.press(e.code, a); }
    });
    window.addEventListener('keyup', (e) => this.input.release(e.code));
  }
  get portrait() { return innerHeight > innerWidth; }
  img(name, alt, cls = '') { return `<img class="${cls}" src="${this.assets}${name}" alt="${alt}" draggable="false">`; }

  menu() {
    this.race = null; this.onRace(null); this.input.clear(); this.screen = 'menu'; this.renderedPhase = '';
    const card = (k) => { const d = DRIVERS[k], sel = k === this.selected;
      return `<button type="button" class="driver ${sel ? 'selected' : ''}" data-driver="${k}" aria-pressed="${sel}">
        ${this.img(`${k}-photo.png`, `Foto de ${d.name}`, 'driver-photo')}
        <span class="driver-copy"><small>PILOTO ${d.number}</small><strong>${d.first}<span>Mencacci</span></strong><span class="driver-line">${d.car.toUpperCase()}</span></span>
        ${this.img(`${k}-rear.png`, d.car, 'menu-car')}<span class="choice">${sel ? 'SELECIONADO' : 'ESCOLHER PILOTO'}</span></button>`; };
    this.root.innerHTML = `<section class="menu">
      <header class="brand">${this.img('ftw.png', 'FTW', 'ftw-logo')}<span class="brand-title">RACE <em>CASCAVEL</em></span><span class="tag">VERSÃO DE TESTE · CLAUDE</span></header>
      <div class="drivers">${card('daniel')}${card('felipe')}</div>
      <footer class="menu-footer"><div class="race-options">
        <label>Voltas <select id="laps"><option>1</option><option selected>3</option><option>5</option></select></label>
        <label>Nitros <select id="charges"><option>0</option><option>1</option><option selected>2</option></select></label>
        <button type="button" class="text-button" id="fs">TELA CHEIA</button></div>
        <button class="primary" id="start">LARGAR EM CASCAVEL ›</button></footer>
      <p class="build-note">Arte dos carros em revisão · rival CPU · use o celular na horizontal</p></section>`;
    for (const b of this.root.querySelectorAll('[data-driver]')) b.onclick = () => { this.selected = b.dataset.driver; this.menu(); };
    this.root.querySelector('#fs').onclick = () => this.fullscreen();
    this.root.querySelector('#start').onclick = () => { this.fullscreen(); this.start(Number(this.root.querySelector('#laps').value), Number(this.root.querySelector('#charges').value)); };
  }
  async fullscreen() {
    try { if (!document.fullscreenElement) await document.documentElement.requestFullscreen({ navigationUI: 'hide' }); await screen.orientation?.lock?.('landscape'); } catch { /* nem todo navegador permite */ }
  }
  start(laps, charges) {
    this.race = createRace(this.track, this.selected, { laps, nitroCharges: charges }); this.onRace(this.race);
    this.input.clear(); this.screen = 'race'; this.renderedPhase = ''; this.raceUi();
    this.audio.unlock().catch(() => {});
    if (this.portrait) pauseRace(this.race);
  }
  minimap() {
    const p = this.track.points, b = this.track.bounds, pad = 60;
    const vb = `${b.minX - pad} ${b.minY - pad} ${b.maxX - b.minX + 2 * pad} ${b.maxY - b.minY + 2 * pad}`;
    const me = DRIVERS[this.selected].color, other = DRIVERS[this.selected === 'daniel' ? 'felipe' : 'daniel'].color;
    return `<svg viewBox="${vb}" role="img" aria-label="Minimapa de Cascavel"><polyline points="${p.map((q) => `${q.x.toFixed(0)},${q.y.toFixed(0)}`).join(' ')}" fill="none" stroke="#ffffff66" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/><circle id="map-cpu" r="38" fill="${other}" stroke="#102019" stroke-width="12"/><circle id="map-player" r="42" fill="${me}" stroke="#fff" stroke-width="14"/></svg>`;
  }
  raceUi() {
    const r = this.race;
    this.root.innerHTML = `<section class="race-ui">
      <header class="hud"><div class="cell"><small>POSIÇÃO</small><strong id="position">1<span>/ 2</span></strong></div>
        <div class="cell"><small>VOLTA</small><strong id="lap">1 / ${r.config.laps}</strong></div>
        <div class="cell"><small>TEMPO</small><strong id="time">00:00.0</strong></div>
        <div class="grow"></div><button id="sound" class="icon-button">${MODE_LABEL[this.audio.mode]}</button><button id="pause" class="icon-button" aria-label="Pausar">II</button></header>
      <div class="minimap">${this.minimap()}</div><div class="race-message" id="msg" aria-live="polite"></div>
      <div class="speed"><strong id="speed">0</strong><span>km/h</span><small id="surface"></small></div>
      <div class="nitro-toast" id="nitro-toast" hidden>${this.img('can.png', 'Lata Diabo Verde')}<span>DIABO VERDE<small>NITRO ATIVO</small></span></div>
      <div class="controls"><div class="steering"><button data-action="left" aria-label="Esquerda"><i class="arrow left"></i></button><button data-action="right" aria-label="Direita"><i class="arrow right"></i></button></div>
        <div class="pedals"><button class="nitro-button" data-action="nitro" aria-label="Nitro">${this.img('diabo-verde.png', 'Diabo Verde')}<span>NITRO <b id="charges-left">${r.config.nitroCharges}</b></span></button>
        <button class="brake" data-action="brake">FREIO</button><button class="throttle" data-action="throttle">ACELERAR</button></div></div>
      <div id="modal"></div></section>`;
    this.root.querySelector('#pause').onclick = () => this.togglePause();
    this.root.querySelector('#sound').onclick = (e) => { this.audio.unlock().catch(() => {}); this.audio.cycleMode(); e.currentTarget.textContent = MODE_LABEL[this.audio.mode]; };
    for (const b of this.root.querySelectorAll('[data-action]')) {
      b.addEventListener('pointerdown', (e) => { e.preventDefault(); if (this.race?.phase !== 'racing') return; try { b.setPointerCapture(e.pointerId); } catch {} this.input.press(e.pointerId, b.dataset.action); b.classList.add('held'); });
      const up = (e) => { this.input.release(e.pointerId); b.classList.toggle('held', this.input.snapshot()[b.dataset.action]); };
      for (const ev of ['pointerup', 'pointercancel', 'lostpointercapture']) b.addEventListener(ev, up);
    }
  }
  clearInputs() { this.input.clear(); for (const e of this.root.querySelectorAll('.held')) e.classList.remove('held'); }
  interrupt() { this.clearInputs(); if (this.race) { pauseRace(this.race); this.update(performance.now()); } }
  togglePause() {
    if (!this.race || this.race.phase === 'finished') return; this.clearInputs();
    if (this.race.phase === 'paused') { if (this.portrait) return; resumeRace(this.race); } else pauseRace(this.race);
    this.renderedPhase = ''; this.update(performance.now());
  }
  modal(phase) {
    const m = this.root.querySelector('#modal'), r = this.race; this.root.querySelector('.controls').classList.toggle('inactive', phase !== 'racing');
    if (phase === 'paused') { this.clearInputs(); m.innerHTML = `<div class="backdrop"><section class="dialog"><p class="eyebrow">CORRIDA PAUSADA</p><h2>${this.portrait ? 'Gire o celular' : 'Pausa'}</h2><button class="primary" id="resume">CONTINUAR</button><button class="secondary" id="restart">RECOMEÇAR</button><button class="text-button" id="menu">VOLTAR À SELEÇÃO</button></section></div>`; m.querySelector('#resume').onclick = () => this.togglePause(); }
    else if (phase === 'finished') { this.clearInputs(); const best = Math.min(...r.player.lapTimes, Infinity);
      m.innerHTML = `<div class="backdrop"><section class="dialog result"><p class="eyebrow">BANDEIRADA</p><h2>${r.winner === r.player.driver ? 'Vitória!' : 'O rival levou essa.'}</h2><p>${DRIVERS[r.winner].name} venceu em Cascavel.</p><div class="result-time">${formatTime(r.elapsed)}</div>${Number.isFinite(best) ? `<p class="small">Sua melhor volta: ${formatTime(best)}</p>` : ''}<button class="primary" id="restart">DISPUTAR NOVAMENTE</button><button class="text-button" id="menu">TROCAR PILOTO</button></section></div>`; }
    else m.innerHTML = '';
    const rs = m.querySelector('#restart'); if (rs) rs.onclick = () => this.start(r.config.laps, r.config.nitroCharges);
    const mn = m.querySelector('#menu'); if (mn) mn.onclick = () => this.menu();
  }
  update(now) {
    const r = this.race; this.fpsAcc += 1; if (now - (this.fpsT || now) >= 1000) { this.fps = this.fpsAcc; this.fpsAcc = 0; this.fpsT = now; } this.fpsT ||= now;
    this.audio.update(this.screen === 'race' ? r : null, this.input.snapshot());
    if (this.debug) this.debugPanel(now);
    if (!r || this.screen !== 'race') return;
    this.root.dataset.phase = r.phase;
    if (this.renderedPhase !== r.phase) { this.renderedPhase = r.phase; this.modal(r.phase); }
    if (now - this.lastHud < 65) return; this.lastHud = now;
    const q = (s) => this.root.querySelector(s);
    q('#position').innerHTML = `${playerPosition(r)}<span>/ 2</span>`;
    q('#lap').textContent = `${Math.min(r.player.laps + 1, r.config.laps)} / ${r.config.laps}`;
    q('#time').textContent = formatTime(r.elapsed); q('#speed').textContent = String(Math.round(r.player.speed * 3.6));
    q('#charges-left').textContent = String(r.player.charges); q('#surface').textContent = r.player.offRoad ? 'FORA DA PISTA' : '';
    q('#msg').textContent = r.phase === 'countdown' ? String(Math.ceil(r.countdown)) : r.phase === 'racing' && r.elapsed < 1 ? 'VAI!' : '';
    q('#nitro-toast').hidden = r.player.nitroRemaining <= 0 || r.phase !== 'racing';
    for (const [id, d] of [['player', r.player], ['cpu', r.cpu]]) { const p = this.track.at(d.distance), c = q(`#map-${id}`); c.setAttribute('cx', p.x); c.setAttribute('cy', p.y); }
  }
  debugPanel(now) {
    let el = document.getElementById('debug'); if (!el) { el = document.createElement('pre'); el.id = 'debug'; document.body.appendChild(el); }
    if (now - (this.dbgT || 0) < 250) return; this.dbgT = now;
    const r = this.race, c = window.__ftwGame?.renderer;
    el.textContent = [`fps ${this.fps}`, `tela ${innerWidth}x${innerHeight} dpr ${devicePixelRatio} ${this.portrait ? 'VERTICAL' : 'horizontal'}`, `render ${c ? (c.type === 2 ? 'WEBGL' : 'CANVAS') : '?'}`,
      `toques ${this.input.count} ${JSON.stringify(this.input.snapshot())}`, r ? `fase ${r.phase} v ${r.player.speed.toFixed(1)} lat ${r.player.lateral.toFixed(2)} volta ${r.player.laps}` : 'menu', `erros ${(window.__ftwErrors || []).length}`].join('\n');
  }
}
