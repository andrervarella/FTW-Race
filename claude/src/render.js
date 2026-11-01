// Renderização Phaser (câmera traseira em pseudo-3D sobre a geometria do circuito).
// Usa apenas chamadas Phaser já exercitadas na v0.1.0 (Graphics.fillPoints/fillRect, add.image, setDisplaySize...).
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const wrapAngle = (a) => Math.atan2(Math.sin(a), Math.cos(a));
const COLORS = { grass: 0x405b35, grassA: 0x52a13c, grassB: 0x4b9737, outer: 0x999999, kerbA: 0xf3f3e1, kerbB: 0xb3202a, roadA: 0x41454b, roadB: 0x454a4e, dash: 0xd4d4bc, line: 0xe8e8dd };

export function createRaceScene(Phaser, { assets, track, getRace, onReady, onError }) {
  return class RaceScene extends Phaser.Scene {
    constructor() { super('race'); this.scenery = []; this.lastDriver = ''; this.bg = 0; this.prevHeading = null; }
    preload() {
      this.load.image('horizon', `${assets}horizon.png`);
      for (const k of ['tree', 'bush', 'pit', 'stand']) this.load.image(k, `${assets}${k}.png`);
      for (const d of ['daniel', 'felipe']) this.load.image(d, `${assets}${d}-rear.png`);
      this.load.on('loaderror', (f) => onError(new Error(`Imagem não carregou: ${(f && (f.src || f.key)) || '?'}`)));
    }
    create() {
      this.horizon = this.add.image(0, 0, 'horizon').setOrigin(0, 0);
      this.road = this.add.graphics();
      this.scenery = Array.from({ length: 24 }, () => this.add.image(0, 0, 'tree').setOrigin(0.5, 1).setVisible(false));
      this.rival = this.add.image(0, 0, 'felipe').setOrigin(0.5, 0.95).setDepth(1500);
      this.player = this.add.image(0, 0, 'daniel').setOrigin(0.5, 0.95).setDepth(2000);
      onReady();
    }
    update(time) {
      if (!this.road) return;
      const W = this.scale.width, H = this.scale.height, horizonY = H * 0.37;
      const race = getRace(), g = this.road;
      const dist = race ? race.player.distance : 0, lat = race ? race.player.lateral : 0;
      const cam = track.sample(dist), look = track.sample(dist + 8).heading;
      const f = { x: Math.cos(look), y: Math.sin(look) }, S = { x: -f.y, y: f.x };
      const focal = W * 0.82, camH = 5.2;

      // fundo: desliza ao curvar (sensação de giro), nunca sai da imagem
      if (this.prevHeading !== null) this.bg = clamp(this.bg - wrapAngle(look - this.prevHeading) * W * 1.6, -W * 0.35, W * 0.35);
      this.bg *= 0.985; this.prevHeading = look;
      this.horizon.setDisplaySize(W * 1.7, H * 0.39).setPosition(-W * 0.35 + this.bg, 0);

      g.clear(); g.fillStyle(COLORS.grass); g.fillRect(0, horizonY, W, H - horizonY);

      // projeção: ponto da pista a "l" unidades, deslocado "off" unidades para o lado
      const project = (l, off = 0) => {
        const c = track.sample(l), nx = -Math.sin(c.heading), ny = Math.cos(c.heading);
        const gx = c.x + nx * off - cam.x - S.x * lat * track.width / 2, gy = c.y + ny * off - cam.y - S.y * lat * track.width / 2;
        const z = gx * f.x + gy * f.y + 10, side = gx * S.x + gy * S.y;
        return { x: W * 0.5 + (side * focal) / z, y: horizonY + (camH * focal) / z, scale: focal / z, z };
      };
      const segs = []; let minY = Infinity;
      for (let l = 0; l < 240; l += 4) {
        const a = project(dist + l), b = project(dist + l + 4);
        if (a.z < 4 || b.z < 4 || b.y >= a.y || b.y > minY) break;
        segs.push({ a, b, d: dist + l }); minY = b.y;
      }
      const quad = (color, x1, y1, w1, x2, y2, w2) => { g.fillStyle(color); g.fillPoints([{ x: x1 - w1, y: y1 }, { x: x1 + w1, y: y1 }, { x: x2 + w2, y: y2 }, { x: x2 - w2, y: y2 }], true); };
      for (let i = segs.length - 1; i >= 0; i--) {
        const { a, b, d } = segs[i], alt = Math.floor(d / 8) % 2 === 0;
        quad(alt ? COLORS.grassA : COLORS.grassB, W / 2, a.y, W, W / 2, b.y, W);
        quad(COLORS.outer, a.x, a.y, 8.2 * a.scale, b.x, b.y, 8.2 * b.scale);
        quad(alt ? COLORS.kerbA : COLORS.kerbB, a.x, a.y, 6.7 * a.scale, b.x, b.y, 6.7 * b.scale);
        quad(alt ? COLORS.roadA : COLORS.roadB, a.x, a.y, 6 * a.scale, b.x, b.y, 6 * b.scale);
        if (alt) quad(COLORS.dash, a.x, a.y, 0.035 * a.scale, b.x, b.y, 0.035 * b.scale);
        if (track.wrap(d) < 4) quad(COLORS.line, a.x, a.y, 6 * a.scale, b.x, b.y, 6 * b.scale);
      }

      // cenário determinístico (sem Math.random), fora do asfalto
      for (const s of this.scenery) s.setVisible(false);
      let used = 0;
      const place = (key, at, off, size) => {
        if (used >= this.scenery.length) return;
        const rel = track.wrap(at - dist); if (rel < 3 || rel > 220) return;
        const p = project(dist + rel, off); if (p.z < 12 || p.y < horizonY) return;
        const spr = this.scenery[used++].setTexture(key).setVisible(true).setPosition(p.x, p.y).setDepth(1000 - p.z);
        const img = spr.texture.getSourceImage(), w = size * p.scale;
        spr.setDisplaySize(w, (w * img.height) / img.width);
      };
      for (let l = Math.floor(dist / 48) * 48; l < dist + 220; l += 48) {
        const k = Math.floor(track.wrap(l) / 48);
        if (k % 3 !== 1) place(k % 2 ? 'bush' : 'tree', l, -14 - ((k * 7) % 13), k % 2 ? 5.5 : 5);
        if (track.wrap(l) > 240 && k % 3 === 0) place('tree', l, 17 + ((k * 11) % 9), 4.5);
      }
      place('pit', 60, 20, 28); place('stand', 75, -20, 16);

      if (!race) { this.player.setVisible(false); this.rival.setVisible(false); return; }
      if (this.lastDriver !== race.player.driver) { this.player.setTexture(race.player.driver); this.rival.setTexture(race.cpu.driver); this.lastDriver = race.player.driver; }
      const size = Math.min(W * 0.22, H * 0.47), bump = race.player.offRoad && race.phase === 'racing' ? Math.sin(time / 28) * 2.5 : 0;
      this.player.setVisible(true).setPosition(W * 0.5, H * 0.91 + bump).setDisplaySize(size, size)
        .setAlpha(race.player.collisionRemaining > 0 ? 0.7 : 1).setAngle(race.player.steer * Math.min(3, race.player.speed / 20));
      const ahead = track.wrap(race.cpu.distance - race.player.distance);
      if (ahead < 220 && ahead > 1) {
        const p = project(dist + ahead, race.cpu.lateral * track.width / 2), sz = Math.min(size * 1.1, p.scale * 3.4);
        this.rival.setVisible(p.z > 5 && p.y > horizonY).setPosition(p.x, p.y).setDisplaySize(sz, sz);
      } else this.rival.setVisible(false);

      if (race.player.nitroRemaining > 0) { // linhas de velocidade durante o nitro
        g.lineStyle(2, 0xa8f138, 0.55);
        for (let i = 0; i < 6; i++) { const x = ((i + 1) * W) / 7; g.lineBetween(x, H * 0.6, x + (x - W * 0.5) * 0.15, H * 0.8); }
      }
    }
  };
}
