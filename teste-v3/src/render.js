import { NPC_KEYS } from './config.js';
// Renderização Phaser (câmera traseira em pseudo-3D sobre a geometria do circuito).
// Usa apenas chamadas Phaser já exercitadas na v0.1.0 (Graphics.fillPoints/fillRect, add.image, setDisplaySize...).
const LOW = typeof location !== 'undefined' && new URLSearchParams(location.search).get('q') === 'baixa'; // ?q=baixa: menos polígonos por quadro
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const wrapAngle = (a) => Math.atan2(Math.sin(a), Math.cos(a));
const COLORS = { grass: 0x405b35, grassA: 0x52a13c, grassB: 0x4b9737, outer: 0x999999, kerbA: 0xf3f3e1, kerbB: 0xb3202a, roadA: 0x41454b, roadB: 0x474c51, dash: 0xd4d4bc, line: 0xe8e8dd, edge: 0xe9e9e0, lane: 0x3a3e44, railA: 0xf2f2ea, railB: 0xc42a32, railTop: 0x20262b, post: 0x2b3238, beam: 0xb0f138 };

export function createRaceScene(Phaser, { assets, track, getRace, onReady, onError }) {
  return class RaceScene extends Phaser.Scene {
    constructor() { super('race'); this.scenery = []; this.lastDriver = ''; this.bg = 0; this.prevHeading = null; this.lastHitId = 0; this.fx = []; this.lastFxHit = 0; }
    preload() {
      this.load.image('horizon', `${assets}horizon.png`);
      for (const k of ['tree', 'bush', 'pit', 'stand']) this.load.image(k, `${assets}${k}.png`);
      for (const d of ['daniel', 'felipe']) this.load.image(d, `${assets}${d}-rear.png`);
      for (const key of NPC_KEYS) this.load.svg(key, new URL(`../cars/${key}.svg`, import.meta.url).href, { width: 256, height: 256 });
      this.load.on('loaderror', (f) => onError(new Error(`Imagem não carregou: ${(f && (f.src || f.key)) || '?'}`)));
    }
    create() {
      this.horizon = this.add.image(0, 0, 'horizon').setOrigin(0, 0);
      this.road = this.add.graphics();
      this.scenery = Array.from({ length: 24 }, () => this.add.image(0, 0, 'tree').setOrigin(0.5, 1).setVisible(false));
      this.rivals = Array.from({ length: 5 }, () => this.add.image(0, 0, 'felipe').setOrigin(0.5, 0.95).setDepth(1500));
      this.player = this.add.image(0, 0, 'daniel').setOrigin(0.5, 0.95).setDepth(2000);
      onReady();
    }
    update(time, delta) {
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
      const half = track.width / 2, poly = (color, pts) => { g.fillStyle(color); g.fillPoints(pts, true); };
      // mureta vertical (guard-rail) entre as distâncias de dois pontos projetados; "side" = -1 esquerda, 1 direita
      const rail = (color, a, b, side, off, h) => poly(color, [{ x: a.x + side * off * a.scale, y: a.y }, { x: a.x + side * off * a.scale, y: a.y - h * a.scale },
        { x: b.x + side * off * b.scale, y: b.y - h * b.scale }, { x: b.x + side * off * b.scale, y: b.y }]);
      for (let i = segs.length - 1; i >= 0; i--) {
        const { a, b, d } = segs[i], alt = Math.floor(d / 8) % 2 === 0, block = Math.floor(track.wrap(d) / 16), near = !LOW && d - dist < 110;
        quad(alt ? COLORS.grassA : COLORS.grassB, W / 2, a.y, W, W / 2, b.y, W);
        quad(COLORS.outer, a.x, a.y, half * 1.37 * a.scale, b.x, b.y, half * 1.37 * b.scale);
        quad(alt ? COLORS.kerbA : COLORS.kerbB, a.x, a.y, half * 1.12 * a.scale, b.x, b.y, half * 1.12 * b.scale);
        quad(alt ? COLORS.roadA : COLORS.roadB, a.x, a.y, half * a.scale, b.x, b.y, half * b.scale);
        if (near) quad(COLORS.lane, a.x, a.y, half * 0.34 * a.scale, b.x, b.y, half * 0.34 * b.scale); // faixa de rodagem mais escura (traçado)
        if (near) quad(COLORS.edge, a.x - half * 0.93 * a.scale, a.y, 0.012 * half * a.scale, b.x - half * 0.93 * b.scale, b.y, 0.012 * half * b.scale); // linhas de borda
        if (near) quad(COLORS.edge, a.x + half * 0.93 * a.scale, a.y, 0.012 * half * a.scale, b.x + half * 0.93 * b.scale, b.y, 0.012 * half * b.scale);
        if (alt && near) { quad(COLORS.dash, a.x, a.y, 0.02 * half * a.scale, b.x, b.y, 0.02 * half * b.scale); }
        if (!LOW && block % 4 !== 3) for (const side of [-1, 1]) { // muretas com vãos; listras vermelho/branco
          rail(block % 2 ? COLORS.railA : COLORS.railB, a, b, side, half * 1.75, 1.7);
          if (near) rail(COLORS.railTop, a, b, side, half * 1.75, 0.35);
        }
        if (track.wrap(d) < 4) { // linha de largada + pórtico
          quad(COLORS.line, a.x, a.y, half * a.scale, b.x, b.y, half * b.scale);
          for (const side of [-1, 1]) rail(COLORS.post, a, b, side, half * 1.3, 9);
          poly(COLORS.beam, [{ x: a.x - half * 1.32 * a.scale, y: a.y - 9 * a.scale }, { x: a.x + half * 1.32 * a.scale, y: a.y - 9 * a.scale }, { x: b.x + half * 1.32 * b.scale, y: b.y - 7.2 * b.scale }, { x: b.x - half * 1.32 * b.scale, y: b.y - 7.2 * b.scale }]);
        }
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

      if (!race) { this.player.setVisible(false); for (const s of this.rivals) s.setVisible(false); return; }
      if (this.lastDriver !== race.player.driver) { this.player.setTexture(race.player.driver); this.lastDriver = race.player.driver; }
      const size = Math.min(W * 0.22, H * 0.47);
      const bump = race.player.offRoad && race.phase === 'racing' ? Math.sin(time / 28) * 2.5 : 0;
      const sway = race.player.wheel * W * 0.018;
      const lean = clamp(race.player.wheel * Math.min(6, race.player.speed / 9), -6, 6);
      this.player.setVisible(true).setPosition(W * 0.5 + sway, H * 0.91 + bump).setDisplaySize(size, size)
        .setAlpha(1).setAngle(lean).setDepth(2000);
      for (let i = 0; i < this.rivals.length; i++) {
        const car = race.opponents[i], sprite = this.rivals[i];
        if (!car) { sprite.setVisible(false); continue; }
        const ahead = ((car.distance - race.player.distance + track.length / 2) % track.length + track.length) % track.length - track.length / 2;
        if (ahead > -8 && ahead < 220) {
          const p = project(dist + 8 + ahead, car.lateral * half);
          const sz = Math.min(size * 18 / Math.max(1,p.z), size * 1.6);
          sprite.setTexture(car.driver).setVisible(p.z > 4 && p.y > horizonY)
            .setPosition(p.x,p.y).setDisplaySize(sz,sz)
            .setDepth(ahead < 0 ? 2500 - ahead : 1500 - ahead).setAngle(clamp(car.wheel * 4,-5,5));
        } else sprite.setVisible(false);
      }
      if (race.hit && race.hit.id !== this.lastHitId) { // tremor de câmera na batida
        this.lastHitId = race.hit.id;
        try { this.cameras.main.shake(180, 0.004 + 0.008 * race.hit.strength); } catch (e) { /* câmera indisponível */ }
      }

      // FX PROVISÓRIOS (círculos, sem arte): poeira fora da pista, faíscas na batida, chama do nitro.
      // Substituir por sprites de assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png quando recortados com alpha.
      const dtf = Math.min((delta || 16) / 1000, 0.05), emit = (x, y, vx, vy, life, rad, color) => { if (this.fx.length < 90) this.fx.push({ x, y, vx, vy, life, max: life, rad, color }); };
      if (race.phase === 'racing') {
        if (race.player.offRoad && race.player.speed > 8) for (const s of [-1, 1]) emit(W * 0.5 + s * size * 0.32, H * 0.9, s * (20 + Math.random() * 30), -30 - Math.random() * 40, 0.5, 6 + Math.random() * 6, 0xb69a6a);
        if (race.player.nitroRemaining > 0) for (const s of [-1, 1]) { emit(W * 0.5 + s * size * 0.17, H * 0.9, s * 8, 70, 0.22, 8, 0xffa030); emit(W * 0.5 + s * size * 0.17, H * 0.9, 0, 60, 0.16, 4.5, 0x6fc3ff); }
      }
      if (race.hit && race.hit.id !== this.lastFxHit) { this.lastFxHit = race.hit.id; for (let i = 0; i < 14; i++) { const a = Math.random() * Math.PI * 2, v = 60 + Math.random() * 140; emit(W * 0.5 + Math.cos(a) * size * 0.3, H * 0.8, Math.cos(a) * v, Math.sin(a) * v - 40, 0.35, 3, 0xffe070); } }
      this.fx = this.fx.filter((p) => (p.life -= dtf) > 0);
      for (const p of this.fx) { p.x += p.vx * dtf; p.y += p.vy * dtf; g.fillStyle(p.color, clamp(p.life / p.max, 0, 1) * 0.8); g.fillCircle(p.x, p.y, p.rad * (0.5 + 0.5 * (p.life / p.max))); }

      if (race.player.nitroRemaining > 0) { // linhas de velocidade durante o nitro
        g.lineStyle(2, 0xa8f138, 0.55);
        for (let i = 0; i < 6; i++) { const x = ((i + 1) * W) / 7; g.lineBetween(x, H * 0.6, x + (x - W * 0.5) * 0.15, H * 0.8); }
      }
    }
  };
}
