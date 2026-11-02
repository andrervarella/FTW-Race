// Áudio 100% sintetizado (Web Audio): motor com marchas, derrapagem, cascalho, batida, nitro, contagem e trilha em loop.
// Tudo ORIGINAL (nenhum sample, melodia ou código de Top Gear). Estilo: arcade 16-bit, andamento rápido, baixo pulsante.
// Modos: 'tudo' (música + efeitos), 'efeitos', 'mudo'. Não testado em aparelho (ouvido humano) — só renderização offline.
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);
export const MODES = ['tudo', 'efeitos', 'mudo'];
export const MODE_LABEL = { tudo: 'SOM ON', efeitos: 'SÓ EFEITOS', mudo: 'MUDO' };
const GEARS = [0, 55, 100, 145, 195, 250]; // km/h onde cada marcha começa
const TEMPO = 142, STEP = 60 / TEMPO / 4;
const BASS = [45, 41, 48, 43, 45, 41, 43, 40]; // raízes por compasso (Am F C G Am F G E)
const CHORDS = [[69, 72, 76], [65, 69, 72], [72, 76, 79], [67, 71, 74], [69, 72, 76], [65, 69, 72], [67, 71, 74], [64, 68, 71]];
const LEAD = [0, -1, 1, -1, 2, -1, 1, -1, 0, -1, 1, 2, 3, -1, 2, 1]; // índice no acorde (3 = oitava acima), -1 = pausa
const BASS_PAT = [0, 0, 12, 0, 0, 0, 12, 7];

export class GameAudio {
  constructor(ctx = null) {
    this.ctx = ctx; this.mode = 'tudo'; this.ready = false; this.nextNote = 0; this.step = 0; this.timer = null;
    this.suspended = false; this.unlocking = null; this.lifecycle = 0; this.sources = new Set();
    this.prev = { hit: 0, laps: 0, count: -1, nitro: false, phase: '', gear: 1 };
  }
  async unlock() {
    if (this.unlocking) {
      const generation = this.unlockGeneration, pending = this.unlocking;
      const result = await pending;
      // A new user gesture after a blur must not inherit a cancelled unlock.
      return generation !== this.lifecycle ? this.unlock() : result;
    }
    const generation = this.lifecycle;
    this.unlockGeneration = generation;
    this.unlocking = (async () => {
      try {
        if (!this.ctx) {
          const AC = globalThis.window?.AudioContext || globalThis.window?.webkitAudioContext;
          if (!AC) return false;
          this.ctx = new AC();
        }
        if (this.ctx.state === 'closed') return false;
        if (!this.ready) this.build();
        await this.ctx.resume();
        // A blur may have arrived while the browser was granting audio access.
        if (generation !== this.lifecycle) { await this.ctx.suspend?.(); return false; }
        this.suspended = false;
        this.master.gain.setTargetAtTime(0.9, this.ctx.currentTime, 0.04);
        this.setMode(this.mode); this.startMusic();
        return true;
      } catch { return false; } // Audio is optional, including browser/device failures.
    })();
    try { return await this.unlocking; } finally { this.unlocking = null; }
  }
  async suspend() {
    this.suspended = true; this.lifecycle++; this.stopMusic();
    if (!this.ready || this.ctx.state === 'closed') return;
    const t = this.ctx.currentTime;
    for (const bus of [this.master, this.musicBus, this.sfxBus]) {
      bus.gain.cancelScheduledValues(t); bus.gain.setValueAtTime(0, t);
    }
    // Discard already scheduled one-shots so returning from another app cannot replay them.
    for (const source of this.sources) { try { source.stop(); } catch {} }
    this.sources.clear();
    try { if (this.ctx.state === 'running') await this.ctx.suspend?.(); } catch { /* optional audio */ }
  }
  build() {
    const c = this.ctx;
    this.master = c.createGain(); this.master.gain.value = 0.9;
    const comp = c.createDynamicsCompressor(); this.master.connect(comp); comp.connect(c.destination);
    this.musicBus = c.createGain(); this.sfxBus = c.createGain(); this.musicBus.connect(this.master); this.sfxBus.connect(this.master);
    // ruído branco de 2 s (reaproveitado em derrapagem, cascalho, nitro, percussão)
    const buf = c.createBuffer(1, c.sampleRate * 2, c.sampleRate), ch = buf.getChannelData(0); let seed = 12345;
    for (let i = 0; i < ch.length; i++) { seed = (seed * 1664525 + 1013904223) >>> 0; ch[i] = (seed / 4294967296) * 2 - 1; }
    this.noiseBuf = buf;
    // motor: serra + quadrada (sub) + serra desafinada → passa-baixa
    this.eng = { o1: c.createOscillator(), o2: c.createOscillator(), o3: c.createOscillator(), f: c.createBiquadFilter(), g: c.createGain() };
    this.eng.o1.type = 'sawtooth'; this.eng.o2.type = 'square'; this.eng.o3.type = 'sawtooth';
    this.eng.f.type = 'lowpass'; this.eng.f.Q.value = 3; this.eng.g.gain.value = 0;
    for (const o of [this.eng.o1, this.eng.o2, this.eng.o3]) { o.connect(this.eng.f); o.start(); }
    this.eng.f.connect(this.eng.g); this.eng.g.connect(this.sfxBus);
    // derrapagem (ruído passa-banda) e cascalho (ruído passa-baixa) contínuos, com ganho controlado por quadro
    this.skid = this.loopNoise('bandpass', 1900, 4); this.gravel = this.loopNoise('lowpass', 800, 0.7); this.wind = this.loopNoise('highpass', 2500, 0.5);
    this.ready = true;
    this.setMode(this.mode);
  }
  loopNoise(type, freq, q) {
    const c = this.ctx, s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain();
    s.buffer = this.noiseBuf; s.loop = true; f.type = type; f.frequency.value = freq; f.Q.value = q; g.gain.value = 0; s.connect(f); f.connect(g); g.connect(this.sfxBus); s.start();
    return { g, f };
  }
  setMode(m) {
    this.mode = MODES.includes(m) ? m : 'mudo'; if (!this.ready || this.suspended || this.ctx.state === 'closed') return; const t = this.ctx.currentTime;
    m = this.mode;
    this.sfxBus.gain.setTargetAtTime(m === 'mudo' ? 0 : 1, t, 0.05); this.musicBus.gain.setTargetAtTime(m === 'tudo' ? 0.2 : 0, t, 0.08);
  }
  cycleMode() { this.setMode(MODES[(MODES.indexOf(this.mode) + 1) % MODES.length]); return this.mode; }

  // ---- efeitos pontuais (todos aceitam "at" para renderização offline) ----
  canPlay() { return this.ready && !this.suspended && this.mode !== 'mudo' && this.ctx.state !== 'closed'; }
  own(source, nodes) {
    this.sources.add(source);
    source.onended = () => { this.sources.delete(source); for (const n of [source, ...nodes]) n.disconnect(); };
  }
  tone(type, f0, f1, dur, vol, at, bus = this.sfxBus) {
    if (!this.canPlay()) return;
    const c = this.ctx, o = c.createOscillator(), g = c.createGain(); o.type = type; o.frequency.setValueAtTime(f0, at); o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), at + dur);
    g.gain.setValueAtTime(vol, at); g.gain.exponentialRampToValueAtTime(0.0001, at + dur); o.connect(g); g.connect(bus); this.own(o, [g]); o.start(at); o.stop(at + dur + 0.02);
  }
  burst(type, freq, q, dur, vol, at, bus = this.sfxBus, sweepTo = null) {
    if (!this.canPlay()) return;
    const c = this.ctx, s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain(); s.buffer = this.noiseBuf; f.type = type; f.frequency.setValueAtTime(freq, at); f.Q.value = q;
    if (sweepTo) f.frequency.exponentialRampToValueAtTime(sweepTo, at + dur);
    g.gain.setValueAtTime(vol, at); g.gain.exponentialRampToValueAtTime(0.0001, at + dur); s.connect(f); f.connect(g); g.connect(bus); this.own(s, [f, g]); s.start(at, Math.random() * 1.5); s.stop(at + dur + 0.02);
  }
  hit(strength, at = this.ctx?.currentTime ?? 0) { this.tone('sine', 150, 38, 0.28, 0.45 * (0.5 + strength), at); this.burst('bandpass', 900, 1.2, 0.14, 0.5 * (0.5 + strength), at); this.burst('highpass', 3000, 1, 0.08, 0.25, at); }
  nitro(at = this.ctx?.currentTime ?? 0) { this.burst('bandpass', 400, 2, 0.7, 0.45, at, this.sfxBus, 3200); this.tone('sawtooth', 180, 900, 0.5, 0.12, at); }
  beep(high, at = this.ctx?.currentTime ?? 0) { this.tone('square', high ? 1046 : 523, high ? 1046 : 523, high ? 0.4 : 0.14, 0.18, at); }
  lap(at = this.ctx?.currentTime ?? 0) { this.tone('square', 880, 880, 0.12, 0.14, at); this.tone('square', 1318, 1318, 0.22, 0.14, at + 0.12); }
  finish(at = this.ctx?.currentTime ?? 0) { [523, 659, 784, 1046].forEach((f, i) => this.tone('square', f, f, 0.18, 0.16, at + i * 0.13)); }

  selection(at = this.ctx?.currentTime ?? 0) {
    this.tone('square', 740, 990, 0.075, 0.1, at);
    this.tone('triangle', 990, 990, 0.12, 0.12, at + 0.06);
  }
  // Six story beats: steps, trophy, lift, cork, spray, applause. No samples or third-party tune.
  podium(stage, at = this.ctx?.currentTime ?? 0) {
    if (!this.canPlay() || !Number.isInteger(stage) || stage < 0 || stage > 5) return;
    if (stage === 0) {
      for (const offset of [0, 0.22, 0.46]) this.burst('lowpass', 380, 0.7, 0.075, 0.23, at + offset);
    } else if (stage === 1) {
      this.tone('sine', 1480, 1450, 0.34, 0.17, at);
      this.tone('triangle', 2220, 2180, 0.18, 0.07, at);
    } else if (stage === 2) {
      [660, 990, 1320].forEach((f, i) => this.tone('triangle', f, f, 0.26, 0.19, at + i * 0.13));
    } else if (stage === 3) {
      this.tone('sine', 640, 85, 0.13, 0.4, at);
      this.burst('bandpass', 1500, 0.6, 0.09, 0.35, at);
    } else if (stage === 4) {
      this.burst('highpass', 3400, 0.8, 0.85, 0.24, at, this.sfxBus, 1500);
      this.burst('bandpass', 780, 0.5, 0.65, 0.08, at + 0.1);
    } else {
      // Staggered filtered noise gives a small crowd without a large mobile voice count.
      for (let i = 0; i < 12; i++) this.burst('bandpass', 900 + (i % 4) * 330, 0.6, 0.11, 0.13, at + i * 0.073);
      [784, 1175, 1568].forEach((f, i) => this.tone('triangle', f, f, 0.32, 0.11, at + i * 0.15));
    }
  }

  // ---- música ----
  startMusic() { if (this.timer !== null || !this.ready || this.suspended || this.ctx.state !== 'running') return; this.nextNote = this.ctx.currentTime + 0.1; this.timer = setInterval(() => this.scheduleMusicUntil(this.ctx.currentTime + 0.15), 25); }
  stopMusic() { clearInterval(this.timer); this.timer = null; }
  scheduleMusicUntil(t) { while (this.nextNote < t) { this.playStep(this.step, this.nextNote); this.nextNote += STEP; this.step = (this.step + 1) % (16 * 8); } }
  playStep(n, at) {
    if (this.mode !== 'tudo' || !this.canPlay()) return;
    const bar = Math.floor(n / 16), s = n % 16, bus = this.musicBus;
    if (s % 2 === 0) this.tone('square', mtof(BASS[bar] + BASS_PAT[s / 2]), mtof(BASS[bar] + BASS_PAT[s / 2]), STEP * 1.7, 0.5, at, bus);
    const li = LEAD[s]; if (li >= 0) { const ch = CHORDS[bar], m = li === 3 ? ch[0] + 12 : ch[li]; this.tone('square', mtof(m), mtof(m), STEP * 1.4, 0.22, at, bus); this.tone('triangle', mtof(m - 12), mtof(m - 12), STEP * 1.4, 0.2, at, bus); }
    if (s % 4 === 0) this.tone('sine', 160, 42, 0.18, 0.9, at, bus);
    if (s === 4 || s === 12) { this.burst('bandpass', 1900, 0.9, 0.14, 0.55, at, bus); this.tone('triangle', 220, 120, 0.1, 0.3, at, bus); }
    if (s % 2 === 0) this.burst('highpass', 7000, 0.8, 0.04, s % 4 === 0 ? 0.2 : 0.12, at, bus);
  }

  // ---- por quadro: motor, pneus e gatilhos de eventos ----
  update(race, input) {
    if (race?.phase === 'paused') { if (!this.suspended) void this.suspend(); return; }
    if (!this.ready || this.suspended || this.ctx.state !== 'running') return;
    const t = this.ctx.currentTime, e = this.eng, p = this.prev;
    if (!race) { e.g.gain.setTargetAtTime(0, t, 0.1); for (const n of [this.skid, this.gravel, this.wind]) n.g.gain.setTargetAtTime(0, t, 0.1); this.musicBus.gain.setTargetAtTime(this.mode === 'tudo' ? 0.2 : 0, t, 0.15); p.phase = ''; return; }
    if (race.phase === 'countdown' && p.phase !== 'countdown') { p.count = -1; p.hit = 0; p.laps = 0; p.nitro = false; }
    const d = race.player, live = race.phase === 'racing' || race.phase === 'countdown';
    const kmh = d.speed * 3.6; let gear = 0; while (gear < GEARS.length - 1 && kmh >= GEARS[gear + 1]) gear++;
    const lo = GEARS[gear], hi = GEARS[gear + 1] ?? lo + 80, rpm = clamp((kmh - lo) / (hi - lo), 0, 1);
    const thr = input && input.throttle ? 1 : 0, nitro = d.nitroRemaining > 0;
    let base = 52 + gear * 6 + rpm * (60 + gear * 4) + (race.phase === 'countdown' ? thr * 40 : 0); if (nitro) base *= 1.1;
    if (gear !== p.gear && live) { base *= 0.82; e.f.frequency.setTargetAtTime(300, t, 0.02); } // queda de giro na troca
    p.gear = gear;
    for (const [o, k] of [[e.o1, 1], [e.o2, 0.5], [e.o3, 2.01]]) o.frequency.setTargetAtTime(base * k, t, 0.04);
    e.f.frequency.setTargetAtTime(380 + rpm * 1100 + thr * 700 + (nitro ? 500 : 0), t, 0.06);
    e.g.gain.setTargetAtTime(live ? 0.07 + thr * 0.07 + rpm * 0.04 + (nitro ? 0.04 : 0) : 0, t, 0.08);
    const grip = Math.abs(d.wheel) * d.speed / 60, onRoad = !d.offRoad && race.phase === 'racing';
    this.skid.g.gain.setTargetAtTime(onRoad ? clamp((grip - 0.5) * 0.22, 0, 0.14) : 0, t, 0.05);
    this.gravel.g.gain.setTargetAtTime(d.offRoad && race.phase === 'racing' ? clamp(d.speed / 60, 0, 1) * 0.16 : 0, t, 0.05);
    this.wind.g.gain.setTargetAtTime(race.phase === 'racing' ? clamp((kmh - 80) / 250, 0, 1) * (nitro ? 0.12 : 0.05) : 0, t, 0.1);
    const music = this.mode === 'tudo' ? (race.phase === 'paused' ? 0.07 : race.phase === 'finished' ? 0.12 : 0.2) : 0;
    this.musicBus.gain.setTargetAtTime(music, t, 0.15);
    if (race.hit && race.hit.id !== p.hit) { p.hit = race.hit.id; this.hit(race.hit.strength); }
    if (nitro && !p.nitro) this.nitro(); p.nitro = nitro;
    if (d.laps > p.laps) { if (d.laps < race.config.laps) this.lap(); p.laps = d.laps; } if (race.phase === 'countdown') { p.laps = 0; p.hit = 0; }
    if (race.phase === 'countdown') { const c = Math.ceil(race.countdown); if (c !== p.count && c > 0) { p.count = c; this.beep(false); } }
    if (race.phase === 'racing' && p.phase === 'countdown') this.beep(true);
    if (race.phase === 'finished' && p.phase !== 'finished') this.finish();
    p.phase = race.phase;
  }
}
