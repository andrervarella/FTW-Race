// Interface DOM: navegação visual separada das fases do simulador.
import { DRIVERS } from './config.js';
import { InputState, KEYMAP } from './input.js';
import { GameAudio, MODE_LABEL } from './audio.js';
import { createRace, pauseRace, resumeRace, playerPosition, formatTime } from './sim.js';
import { getResults } from './standings.js';
import { podiumMarkup, updatePodium } from './podium.js';
import { titleMarkup, mountTitle } from './title.js';

export class Ui {
  constructor(root, { track, assets, onRace, debug }) {
    Object.assign(this, { root, track, assets, onRace, debug, race: null, input: new InputState(), audio: new GameAudio(), selected: 'daniel', screen: '', renderedPhase: '', lastHud: 0, fps: 0, fpsAcc: 0, laps: 3, charges: 2 });
    this.listeners = new AbortController();
    const opts = { signal: this.listeners.signal };
    document.addEventListener('pointerdown', () => this.audio.unlock().catch(() => {}), opts);
    window.addEventListener('blur', () => { this.interrupt(); this.audio.suspend?.(); }, opts);
    document.addEventListener('visibilitychange', () => { if (document.hidden) { this.interrupt(); this.audio.suspend?.(); } }, opts);
    document.addEventListener('contextmenu', (e) => e.preventDefault(), opts);
    window.addEventListener('keydown', (e) => {
      if (['Enter', 'Space'].includes(e.code)) this.audio.unlock().catch(() => {});
      if (e.repeat && ['Enter', 'Escape', 'Space'].includes(e.code)) return;
      if (e.code === 'Escape') { e.preventDefault(); this.back(); return; }
      if (e.code === 'Enter' || (e.code === 'Space' && this.screen === 'title')) {
        if (e.target?.matches?.('select, button, input')) return;
        e.preventDefault(); this.audio.unlock().catch(() => {});
        this.root.querySelector('[data-confirm]')?.click(); return;
      }
      const a = KEYMAP[e.code]; if (a && this.screen === 'race' && this.race?.phase === 'racing') { e.preventDefault(); this.input.press(e.code, a); }
    }, opts);
    window.addEventListener('keyup', (e) => this.input.release(e.code), opts);
    this.showTitle();
  }
  get portrait() { return innerHeight > innerWidth; }
  img(name, alt, cls = '') { return `<img class="${cls}" src="${this.assets}${name}" alt="${alt}" draggable="false">`; }
  driverArt(key, cls) { return `<img class="${cls}" src="${new URL(`../assets/v4/drivers/${key}-portrait.webp`, import.meta.url).href}" alt="Ilustração de ${DRIVERS[key].name} — retrato aprovado" draggable="false">`; }
  transition(screen) {
    const titleCleanup = this.titleCleanup; this.titleCleanup = null; titleCleanup?.();
    this.clearInputs(); this.screen = screen; this.root.dataset.screen = screen;
    this.podiumPaused = false;
    this.root.dataset.phase = this.race?.phase || ''; this.renderedPhase = '';
    this.lastUpdate = performance.now(); this.bannerUntil = 0;
  }
  dropRace() { this.race = null; this.onRace(null); }
  brand(copy = 'CASCAVEL') { return `<header class="brand">${this.img('ftw.png', 'FTW', 'ftw-logo')}<span class="brand-title">RACE <em>${copy}</em></span><span class="tag">PRÉVIA V4 · DANIEL E FELIPE APROVADOS</span></header>`; }
  soundButton() { return `<button type="button" class="icon-button" id="screen-sound" aria-label="Alternar som">${MODE_LABEL[this.audio.mode]}</button>`; }
  bindSound() { const b = this.root.querySelector('#screen-sound'); if (b) b.onclick = () => { this.audio.unlock().catch(() => {}); this.audio.cycleMode(); b.textContent = MODE_LABEL[this.audio.mode]; }; }
  feedback() { this.audio.unlock().then(ready => { if (ready) this.audio.selection?.(); }).catch(() => {}); }
  showTitle() {
    this.dropRace(); this.transition('title');
    this.root.innerHTML = titleMarkup(this.soundButton());
    this.titleCleanup = mountTitle(this.root);
    const start = this.root.querySelector('#press-start');
    start.onclick = () => { if (this.screen !== 'title' || !start.isConnected || this.portrait) return; this.audio.unlock().catch(() => {}); this.feedback(); this.showDriverSelect(); };
    this.root.querySelector('#fs').onclick = () => this.fullscreen(); this.bindSound();
  }
  menu() { this.showDriverSelect(); }
  showDriverSelect() {
    this.dropRace(); this.transition('driverSelect');
    const card = (k) => { const d = DRIVERS[k], sel = k === this.selected;
      return `<button type="button" class="driver ${sel ? 'selected' : ''}" data-driver="${k}" aria-pressed="${sel}" style="--driver-color:${d.color}">
        ${this.driverArt(k, 'driver-photo')}
        <span class="driver-copy"><small>PILOTO #${d.number}</small><strong>${d.first}<span>Mencacci</span></strong><span class="driver-line">${d.car.toUpperCase()}</span></span>
        ${this.img(`${k}-rear.png`, d.car, 'menu-car')}<span class="choice">${sel ? 'SELECIONADO' : 'ESCOLHER PILOTO'}</span></button>`; };
    this.root.innerHTML = `<section class="menu">${this.brand()}<div class="select-heading"><h1>SELECT YOUR DRIVER</h1>${this.soundButton()}</div>
      <div class="drivers">${card('daniel')}${card('felipe')}</div>
      <footer class="menu-footer"><div class="race-options"><button type="button" class="text-button" id="back">VOLTAR</button>
        <label>Voltas <select id="laps">${[1,3,5].map(n => `<option ${n === this.laps ? 'selected' : ''}>${n}</option>`).join('')}</select></label>
        <label>Nitros <select id="charges">${[0,1,2].map(n => `<option ${n === this.charges ? 'selected' : ''}>${n}</option>`).join('')}</select></label></div>
        <button class="primary" id="confirm-driver" data-confirm>CONFIRMAR PILOTO</button></footer>
      <p class="build-note">Retratos aprovados · demais artes em revisão · voltas e nitro provisórios · celular na horizontal</p></section>`;
    for (const b of this.root.querySelectorAll('[data-driver]')) b.onclick = () => {
      this.laps = Number(this.root.querySelector('#laps').value); this.charges = Number(this.root.querySelector('#charges').value);
      this.selected = b.dataset.driver; this.feedback(); this.showDriverSelect();
    };
    this.root.querySelector('#back').onclick = () => this.showTitle();
    this.root.querySelector('#confirm-driver').onclick = () => { if (this.screen !== 'driverSelect') return; this.feedback(); this.showGrid(Number(this.root.querySelector('#laps').value), Number(this.root.querySelector('#charges').value)); };
    this.bindSound();
  }
  showGrid(laps = this.laps, charges = this.charges) {
    this.laps = laps; this.charges = charges;
    this.race = createRace(this.track, this.selected, { laps, nitroCharges: charges });
    pauseRace(this.race); this.onRace(this.race); this.transition('grid');
    const d = DRIVERS[this.selected];
    this.root.innerHTML = `<section class="grid-screen">${this.brand()}<div class="grid-intro"><p class="eyebrow">GRID DE LARGADA</p><h1>${d.first.toUpperCase()} <span style="color:${d.color}">#${d.number}</span></h1><p>${laps} VOLTA${laps > 1 ? 'S' : ''} · ${charges} NITROS · CASCAVEL</p><div class="grid-names">${this.race.racers.map((r, i) => `<span style="--driver-color:${DRIVERS[r.driver].color}"><b>${i + 1}</b> ${DRIVERS[r.driver].name}</span>`).join('')}</div><p class="grid-tip">Segure ACELERAR e use as setas. Nitro: duas ações simultâneas ou mais.</p></div><footer class="menu-footer"><button type="button" class="secondary" id="grid-back">TROCAR PILOTO</button><button type="button" class="primary" id="start" data-confirm>LARGAR</button></footer></section>`;
    this.root.querySelector('#grid-back').onclick = () => this.showDriverSelect();
    this.root.querySelector('#start').onclick = () => { this.fullscreen(); this.start(); };
  }
  async fullscreen() {
    try { if (!document.fullscreenElement) await document.documentElement.requestFullscreen({ navigationUI: 'hide' }); await screen.orientation?.lock?.('landscape'); } catch { /* fallback sem trava de orientação */ }
  }
  start(laps = this.laps, charges = this.charges) {
    if (this.screen === 'race') return;
    if (this.screen !== 'grid' || !this.race) this.showGrid(laps, charges);
    resumeRace(this.race); this.transition('race'); this.raceUi(); this.audio.unlock().catch(() => {});
    if (this.portrait) pauseRace(this.race);
  }
  back() {
    if (this.screen === 'race') this.togglePause();
    else if (this.screen === 'driverSelect') this.showTitle();
    else if (this.screen === 'grid' || this.screen === 'results' || this.screen === 'podium') this.showDriverSelect();
  }
  minimap() {
    const p = this.track.points, b = this.track.bounds, pad = 60;
    const vb = `${b.minX - pad} ${b.minY - pad} ${b.maxX - b.minX + 2 * pad} ${b.maxY - b.minY + 2 * pad}`;
    const me = DRIVERS[this.selected].color;
    const rivals = this.race.opponents.map((d,i) => `<circle id="map-rival-${i}" r="30" fill="${DRIVERS[d.driver].color}" stroke="#102019" stroke-width="10"/>`).join('');
    return `<svg viewBox="${vb}" role="img" aria-label="Minimapa de Cascavel"><polyline points="${p.map(q => `${q.x.toFixed(0)},${q.y.toFixed(0)}`).join(' ')}" fill="none" stroke="#ffffff66" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>${rivals}<circle id="map-player" r="42" fill="${me}" stroke="#fff" stroke-width="14"/></svg>`;

  }
  raceUi() {
    const r = this.race;
    this.root.innerHTML = `<section class="race-ui">
      <header class="hud"><div class="cell"><small>POSIÇÃO</small><strong id="position">5<span>/ 6</span></strong></div>
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
  interrupt() {
    this.clearInputs();
    if (this.screen === 'podium') {
      this.podiumPaused = true;
      const scene = this.root.querySelector('.podium-screen');
      if (scene) scene.dataset.paused = 'true';
      const button = this.root.querySelector('#podium-continue');
      if (button) button.hidden = false;
    }
    if (this.race && this.screen === 'race') { pauseRace(this.race); this.update(performance.now()); }
  }
  togglePause() {
    if (!this.race || this.screen !== 'race' || this.race.phase === 'finished') return; this.clearInputs();
    if (this.race.phase === 'paused') { if (this.portrait) return; this.audio.unlock().catch(() => {}); resumeRace(this.race); } else pauseRace(this.race);
    this.renderedPhase = ''; this.update(performance.now());
  }
  modal(phase) {
    const m = this.root.querySelector('#modal'), r = this.race; this.root.querySelector('.controls').classList.toggle('inactive', phase !== 'racing');
    if (phase === 'paused') {
      this.clearInputs(); m.innerHTML = `<div class="backdrop"><section class="dialog"><p class="eyebrow">CORRIDA PAUSADA</p><h2>${this.portrait ? 'Gire o celular' : 'Pausa'}</h2><button class="primary" id="resume" data-confirm>CONTINUAR</button><button class="secondary" id="restart">RECOMEÇAR</button><button class="text-button" id="menu">TROCAR PILOTO</button></section></div>`;
      m.querySelector('#resume').onclick = () => this.togglePause();
      m.querySelector('#restart').onclick = () => this.showGrid(r.config.laps, r.config.nitroCharges);
      m.querySelector('#menu').onclick = () => this.showDriverSelect();
    } else if (phase === 'finished') {
      this.clearInputs(); this.bannerUntil = performance.now() + 1300;
      m.innerHTML = `<div class="backdrop finish-banner"><section class="dialog"><div class="checkered-flag" aria-hidden="true"></div><p class="eyebrow">BANDEIRADA</p><h2>${DRIVERS[r.winner].name}</h2><p>VENCEU EM CASCAVEL</p><button class="primary" id="results" data-confirm>VER CLASSIFICAÇÃO</button></section></div>`;
      m.querySelector('#results').onclick = () => this.showResults();
    } else m.innerHTML = '';
  }
  showResults() {
    if (!this.race || this.race.phase !== 'finished') return;
    this.transition('results'); const rows = getResults(this.race), winner = DRIVERS[this.race.winner], playerResult = rows.find(r => r.isPlayer);
    this.root.innerHTML = `<section class="results-screen">${this.brand('BANDEIRADA')}<div class="results-content"><header><p class="eyebrow">CAMPEÃO DE CASCAVEL</p><h1 style="color:${winner.color}">${winner.name}</h1><p>Sua posição: <b>${playerResult?.position || this.race.resultPosition}º de 6</b></p>${Number.isFinite(playerResult?.bestLap) ? `<p>Melhor volta: <b>${formatTime(playerResult.bestLap)}</b></p>` : ''}<p class="small">Classificação no instante da bandeirada. Tempos apenas de quem concluiu.</p></header><table class="standings"><thead><tr><th scope="col">POS</th><th scope="col">PILOTO / CARRO</th><th scope="col">VOLTA</th><th scope="col">CHEGADA</th></tr></thead><tbody>${rows.map(r => `<tr class="${r.isPlayer ? 'player-row' : ''}" data-result-driver="${r.driver}"><td>${r.position}º</td><th scope="row"><i style="background:${DRIVERS[r.driver].color}"></i>${DRIVERS[r.driver].name}${r.isPlayer ? ' · VOCÊ' : ''}<small>#${DRIVERS[r.driver].number}</small></th><td>${r.laps}/${this.race.config.laps}</td><td>${r.finished ? formatTime(r.finishTime) : 'Não concluiu'}</td></tr>`).join('')}</tbody></table></div><footer class="results-actions"><button class="secondary" id="restart">RECOMEÇAR</button><button class="text-button" id="change-driver">TROCAR PILOTO</button><button class="primary" id="podium" data-confirm>VER PÓDIO</button></footer></section>`;
    this.root.querySelector('#restart').onclick = () => this.showGrid(); this.root.querySelector('#change-driver').onclick = () => this.showDriverSelect(); this.root.querySelector('#podium').onclick = () => this.showPodium();
  }
  showPodium() {
    if (!this.race || this.race.phase !== 'finished') return;
    this.transition('podium'); this.root.innerHTML = podiumMarkup(this.race, this.assets);
    this.root.querySelector('#podium-continue').onclick = () => {
      this.podiumPaused = false; this.lastUpdate = performance.now();
      delete this.root.querySelector('.podium-screen').dataset.paused;
      this.root.querySelector('#podium-continue').hidden = true;
      this.audio.unlock().catch(() => {});
    };
    const bind = (ids, fn) => { for (const id of ids) { const el = this.root.querySelector(id); if (el) el.onclick = fn; } };
    bind(['#podium-replay', '[data-podium="replay"]', '#replay'], () => this.showGrid());
    bind(['#podium-select', '[data-podium="select"]', '#change-driver'], () => this.showDriverSelect());
    bind(['#podium-title', '[data-podium="title"]', '#title'], () => this.showTitle());
    updatePodium(this.root, this.race, 0, this.audio);
  }
  update(now) {
    const dt = Math.min(Math.max((now - (this.lastUpdate ?? now)) / 1000, 0), .1); this.lastUpdate = now;
    const r = this.race; this.fpsAcc += 1; if (now - (this.fpsT || now) >= 1000) { this.fps = this.fpsAcc; this.fpsAcc = 0; this.fpsT = now; } this.fpsT ||= now;
    this.audio.update(this.screen === 'race' ? r : null, this.input.snapshot());
    if (this.screen === 'podium' && !this.podiumPaused && !document.hidden && document.hasFocus()) updatePodium(this.root, r, dt, this.audio);
    if (this.debug) this.debugPanel(now);
    if (!r || this.screen !== 'race') return;
    this.root.dataset.phase = r.phase;
    if (this.renderedPhase !== r.phase) { this.renderedPhase = r.phase; this.modal(r.phase); }
    if (r.phase === 'finished' && this.bannerUntil && now >= this.bannerUntil) { this.showResults(); return; }
    if (now - this.lastHud < 65) return; this.lastHud = now;
    const q = (s) => this.root.querySelector(s);
    q('#position').innerHTML = `${playerPosition(r)}<span>/ ${r.racers.length}</span>`;
    q('#lap').textContent = `${Math.min(r.player.laps + 1, r.config.laps)} / ${r.config.laps}`;
    q('#time').textContent = formatTime(r.elapsed); q('#speed').textContent = String(Math.round(r.player.speed * 3.6));
    q('#charges-left').textContent = String(r.player.charges); q('#surface').textContent = r.player.offRoad ? 'FORA DA PISTA' : '';
    q('#msg').textContent = r.phase === 'countdown' ? String(Math.ceil(r.countdown)) : r.phase === 'racing' && r.elapsed < 1 ? 'VAI!' : '';
    q('#nitro-toast').hidden = r.player.nitroRemaining <= 0 || r.phase !== 'racing';
    for (const [id, d] of [['player', r.player], ...r.opponents.map((d,i) => [`rival-${i}`, d])]) { const p = this.track.at(d.distance), c = q(`#map-${id}`); if (c) { c.setAttribute('cx', p.x); c.setAttribute('cy', p.y); } }
  }
  destroy() { const titleCleanup = this.titleCleanup; this.titleCleanup = null; titleCleanup?.(); this.listeners.abort(); this.clearInputs(); this.audio.suspend?.(); this.dropRace(); this.root.innerHTML = ''; }
  debugPanel(now) {
    let el = document.getElementById('debug'); if (!el) { el = document.createElement('pre'); el.id = 'debug'; document.body.appendChild(el); }
    if (now - (this.dbgT || 0) < 250) return; this.dbgT = now;
    const r = this.race, c = window.__ftwGame?.renderer;
    el.textContent = [`fps ${this.fps}`, `tela ${innerWidth}x${innerHeight} dpr ${devicePixelRatio} ${this.portrait ? 'VERTICAL' : 'horizontal'}`, `render ${c ? (c.type === 2 ? 'WEBGL' : 'CANVAS') : '?'}`,
      `toques ${this.input.count} ${JSON.stringify(this.input.snapshot())}`, r ? `fase ${r.phase} v ${r.player.speed.toFixed(1)} lat ${r.player.lateral.toFixed(2)} volta ${r.player.laps}` : 'menu', `erros ${(window.__ftwErrors || []).length}`].join('\n');
  }
}
