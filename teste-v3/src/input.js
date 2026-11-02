// Entrada: cada ponteiro (dedo/mouse/tecla) guarda UMA ação; vários podem estar ativos ao mesmo tempo (multitoque).
export class InputState {
  constructor() { this.sources = new Map(); }
  press(id, action) { this.sources.set(id, action); }
  release(id) { this.sources.delete(id); }
  clear() { this.sources.clear(); }
  get count() { return this.sources.size; }
  snapshot() {
    const a = new Set(this.sources.values());
    return { left: a.has('left'), right: a.has('right'), throttle: a.has('throttle'), brake: a.has('brake'), nitro: a.has('nitro') };
  }
}
export const KEYMAP = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'throttle', ArrowDown: 'brake', Space: 'nitro', KeyA: 'left', KeyD: 'right', KeyW: 'throttle', KeyS: 'brake' };
