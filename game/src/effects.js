// Bounded, renderer-independent animation state. The renderer owns/reuses images.
export class SpriteEffects {
  constructor(limit = 48) { this.limit = limit; this.active = []; }
  emit(family, { x, y, vx = 0, vy = 0, duration = 0.5, size = 32 }) {
    if (this.active.length >= this.limit) return null;
    const p = { family, x, y, vx, vy, duration, size, age: 0, frame: 0 };
    this.active.push(p); return p;
  }
  update(dt, paused = false) {
    if (paused || !Number.isFinite(dt) || dt <= 0) return;
    for (const p of this.active) {
      p.age += dt; p.x += p.vx * dt; p.y += p.vy * dt;
      p.frame = Math.min(3, Math.floor(p.age / p.duration * 4));
    }
    this.active = this.active.filter(p => p.age < p.duration);
  }
  clear() { this.active.length = 0; }
}
