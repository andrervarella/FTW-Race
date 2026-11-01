// Motor sintético simples (osciladores Web Audio) — som original, sem samples de terceiros. Mudo por padrão.
export class EngineAudio {
  constructor() { this.ctx = null; this.osc = null; this.gain = null; this.muted = true; }
  async unlock() {
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) throw new Error('sem WebAudio');
      this.ctx = new AC(); this.osc = this.ctx.createOscillator(); this.gain = this.ctx.createGain();
      this.osc.type = 'sawtooth'; this.gain.gain.value = 0; this.osc.connect(this.gain); this.gain.connect(this.ctx.destination); this.osc.start();
    }
    await this.ctx.resume();
  }
  toggle() { this.muted = !this.muted; return this.muted; }
  update(speed, racing, nitro) {
    if (!this.ctx) return; const t = this.ctx.currentTime;
    this.osc.frequency.setTargetAtTime(35 + speed * 2 + (nitro ? 20 : 0), t, 0.12);
    this.gain.gain.setTargetAtTime(!this.muted && racing ? 0.025 : 0, t, 0.05);
  }
}
