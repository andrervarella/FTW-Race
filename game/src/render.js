import { DRIVERS, NPC_KEYS, PLAYABLE_KEYS } from './config.js';
import { SpriteEffects } from './effects.js';
import { vehicleAppearance, NPC_FRAME } from './vehicle-visual.js';
// Renderização Phaser (câmera traseira em pseudo-3D sobre a geometria do circuito).
// Usa apenas chamadas Phaser já exercitadas na v0.1.0 (Graphics.fillPoints/fillRect, add.image, setDisplaySize...).
const LOW = typeof location !== 'undefined' && new URLSearchParams(location.search).get('q') === 'baixa'; // ?q=baixa: menos polígonos por quadro
const REDUCED = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
const V4 = new URL('../assets/v4/', import.meta.url).href;
const FX_ROWS = { smoke: 0, dust: 4, nitro: 8, spark: 12 };
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const wrapAngle = (a) => Math.atan2(Math.sin(a), Math.cos(a));
const COLORS = { grass: 0x405b35, grassA: 0x52a13c, grassB: 0x4b9737, outer: 0x999999, kerbA: 0xf3f3e1, kerbB: 0xb3202a, roadA: 0x41454b, roadB: 0x474c51, dash: 0xd4d4bc, line: 0xe8e8dd, edge: 0xe9e9e0, lane: 0x3a3e44, railA: 0xf2f2ea, railB: 0xc42a32, railTop: 0x20262b, post: 0x2b3238, beam: 0xb0f138 };

export function createRaceScene(Phaser, { assets, track, getRace, onReady, onError }) {
  return class RaceScene extends Phaser.Scene {
    constructor() { super('race'); this.scenery = []; this.lastDriver = ''; this.bg = 0; this.prevHeading = null; this.lastHitId = 0; this.fxState = new SpriteEffects(LOW || REDUCED ? 18 : 48); this.lastFxHit = 0; this.emitClock = 0; this.lastRace = null; }
    preload() {
      this.load.image('horizon', `${V4}cascavel/horizon.png`);
      for (const k of ['tree', 'bush', 'pit', 'stand', 'fence', 'tires', 'barrier', 'forest', 'board50', 'board100']) this.load.image(k, `${V4}cascavel/${k}.png`);
      for (const d of PLAYABLE_KEYS) {
        if (DRIVERS[d].vehicleType === 'truck') {
          // Native atlas is three columns by two rows, read row-major without mirroring.
          this.load.spritesheet(d, `${V4}cars/${d}.png`, { frameWidth: NPC_FRAME.width, frameHeight: NPC_FRAME.height });
          continue;
        }
        this.load.image(d, `${V4}cars/${d}-rear.png`);
        for (const view of ['left', 'right']) this.load.image(`${d}-${view}`, `${V4}cars/${d}-${view}.png`);
      }
      this.load.spritesheet('fx', `${V4}fx/effects.png`, { frameWidth: 128, frameHeight: 128 });
      for (const key of NPC_KEYS) this.load.spritesheet(key, `${V4}cars/npc-raster/${key}.png`, { frameWidth: NPC_FRAME.width, frameHeight: NPC_FRAME.height });
      this.load.on('loaderror', (f) => onError(new Error(`Imagem não carregou: ${(f && (f.src || f.key)) || '?'}`)));
    }
    create() {
      this.horizon = this.add.image(0, 0, 'horizon').setOrigin(0, 0);
      this.road = this.add.graphics();
      this.scenery = Array.from({ length: 24 }, () => this.add.image(0, 0, 'tree').setOrigin(0.5, 1).setVisible(false));
      this.fxImages = Array.from({ length: this.fxState.limit }, () => this.add.image(0, 0, 'fx', 0).setOrigin(0.5, 110 / 128).setDepth(3000).setVisible(false));
      this.rivals = Array.from({ length: PLAYABLE_KEYS.length + NPC_KEYS.length - 1 }, () => this.add.image(0, 0, 'felipe').setOrigin(0.5, NPC_FRAME.ground / NPC_FRAME.height).setDepth(1500));
      this.player = this.add.image(0, 0, 'daniel').setOrigin(0.5, 470 / 512).setDepth(2000);
      this.carTurns = new Map();
      onReady();
    }
    update(time, delta) {
      if (!this.road) return;
      const W = this.scale.width, H = this.scale.height, horizonY = H * 0.37;
      const race = getRace(), g = this.road;
      if (race !== this.lastRace) { this.fxState.clear(); this.carTurns.clear(); this.lastFxHit = 0; this.lastHitId = 0; this.lastRace = race; this.emitClock = 0; }
      const dist = race ? race.player.distance : 0, lat = race ? race.player.lateral : 0;
      const cam = track.sample(dist), look = track.sample(dist + 8).heading;
      const f = { x: Math.cos(look), y: Math.sin(look) }, S = { x: -f.y, y: f.x };
      const focal = W * 0.82, camH = 5.2;

      // fundo: desliza ao curvar (sensação de giro), nunca sai da imagem
      if (!REDUCED && this.prevHeading !== null) this.bg = clamp(this.bg - wrapAngle(look - this.prevHeading) * W * 1.6, -W * 0.35, W * 0.35);
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
        const rel = track.wrap(at - dist);
        const visibleDistance = segs.length ? segs[segs.length - 1].d - dist + 4 : 0;
        if (rel < 3 || rel > visibleDistance) return;
        const p = project(dist + rel, off); if (p.z < 12 || p.y < horizonY) return;
        const spr = this.scenery[used++].setTexture(key).setVisible(true).setPosition(p.x, p.y).setDepth(1500 - p.z);
        const img = spr.texture.getSourceImage(), w = size * p.scale;
        spr.setDisplaySize(w, (w * img.height) / img.width);
      };
      for (let l = Math.floor(dist / 48) * 48; l < dist + 220; l += 48) {
        const k = Math.floor(track.wrap(l) / 48);
        if (k % 3 !== 1) place(k % 2 ? 'bush' : 'tree', l, -14 - ((k * 7) % 13), k % 2 ? 5.5 : 5);
        if (track.wrap(l) > 240 && k % 3 === 0) place('tree', l, 17 + ((k * 11) % 9), 4.5);
      }
      place('pit', 60, 28, 28); place('stand', 75, -23, 16);
      place('board100', track.length * 0.25 - 100, -13, 2.5); place('board50', track.length * 0.25 - 50, -13, 2.5);
      for (let l = Math.floor(dist / 64) * 64; l < dist + 220; l += 64) {
        if (track.wrap(l) < 230) place('fence', l, 17, 11);
        else if (track.wrap(l) > track.length * 0.35 && track.wrap(l) < track.length * 0.65) place('tires', l, -14, 7);
      }

      if (!race) { this.player.setVisible(false); for (const s of [...this.rivals, ...this.fxImages]) s.setVisible(false); return; }
      // Actual separate views, never mirror a numbered/marked car.
      const applyCarView = (sprite, car) => {
        const look = vehicleAppearance(car, this.carTurns.get(car.driver) || 0);
        this.carTurns.set(car.driver, look.turn);
        sprite.setTexture(look.texture);
        if (look.frame !== null) sprite.setFrame(look.frame);
        return look;
      };
      const playerLook = applyCarView(this.player, race.player);
      // Restore the original Mercedes camera. Only selecting the taller truck
      // pulls the camera back a little; every racer shares that camera, so the
      // truck retains its authentic uniform proportions at equal world depth.
      const cameraScale = DRIVERS[race.player.driver].vehicleType === 'truck' ? 1.2 : 1;
      const size = Math.min(W * 0.22, H * 0.47) / cameraScale;
      // A live computed-style object detects safe-area changes during a 180°
      // rotation even when race, DOM and viewport dimensions stay the same.
      // Geometry is read only when that layout signature changes.
      const controls = this.controlsElement?.isConnected ? this.controlsElement
        : typeof document === 'undefined' ? null : document.querySelector('.controls');
      if (this.controlsElement !== controls) this.controlsStyle = controls ? getComputedStyle(controls) : null;
      const insets = this.controlsStyle
        ? `${this.controlsStyle.paddingLeft}/${this.controlsStyle.paddingRight}/${this.controlsStyle.paddingBottom}` : '';
      if (this.controlsElement !== controls || this.layoutInsets !== insets || this.layoutRace !== race || this.layoutWidth !== W || this.layoutHeight !== H) {
        this.safeBottom = this.controlsStyle ? Math.max(0, parseFloat(this.controlsStyle.paddingBottom) - 12) : 0;
        const steering = controls?.querySelector('.steering')?.getBoundingClientRect();
        const pedals = controls?.querySelector('.pedals')?.getBoundingClientRect();
        this.vehicleLane = steering && pedals ? { left: steering.right, right: pedals.left } : { left: 0, right: W };
        this.controlsElement = controls;
        this.layoutInsets = insets;
        this.layoutRace = race; this.layoutWidth = W; this.layoutHeight = H;
      }
      const playerHeight = size * playerLook.renderScale, playerWidth = playerHeight * playerLook.widthScale;
      const bump = !REDUCED && race.player.offRoad && race.phase === 'racing' ? Math.sin(time / 28) * 2.5 : 0;
      const sway = race.player.wheel * W * 0.018;
      const lean = REDUCED ? 0 : clamp(race.player.wheel, -1.5, 1.5);
      // The approved useful alpha of all views fits within .53 × sprite height
      // on either side, including the visual lean. Reserve that body envelope
      // between the buttons, even beside an asymmetric landscape notch.
      const bodyHalfWidth = playerHeight * .53 + 6, lane = this.vehicleLane;
      const laneCenter = (lane.left + lane.right) / 2;
      const playerX = lane.right - lane.left > bodyHalfWidth * 2
        ? clamp(laneCenter + sway, lane.left + bodyHalfWidth, lane.right - bodyHalfWidth) : laneCenter;
      const playerY = Math.min(H * 0.91, H - this.safeBottom - 12) + bump;
      this.player.setVisible(true).setPosition(playerX, playerY).setDisplaySize(playerWidth, playerHeight)
        .setAlpha(1).setAngle(lean).setDepth(2000);
      for (let i = 0; i < this.rivals.length; i++) {
        const car = race.opponents[i], sprite = this.rivals[i];
        if (!car) { sprite.setVisible(false); continue; }
        const ahead = ((car.distance - race.player.distance + track.length / 2) % track.length + track.length) % track.length - track.length / 2;
        if (ahead > -8 && ahead < 220) {
          const p = project(dist + 8 + ahead, car.lateral * half);
          const sz = Math.min(size * 18 / Math.max(1,p.z), size * 1.6);
          const visibleDistance = segs.length ? segs[segs.length - 1].d - dist + 4 : 0;
          const look = applyCarView(sprite, car), height = sz * look.renderScale;
          sprite.setVisible(p.z > 4 && p.y > horizonY && ahead < visibleDistance)
            .setPosition(p.x,p.y).setDisplaySize(height * look.widthScale,height)
            .setDepth(ahead < 0 ? 2500 - ahead : 1500 - p.z).setAngle(REDUCED ? 0 : clamp(car.wheel, -1.5, 1.5));
        } else sprite.setVisible(false);
      }
      if (race.hit && race.hit.id !== this.lastHitId) { // tremor de câmera na batida
        this.lastHitId = race.hit.id;
        try { if (!REDUCED) this.cameras.main.shake(180, 0.004 + 0.008 * race.hit.strength); } catch (e) { /* câmera indisponível */ }
      }

      // True alpha sprites, extracted from the supplied four-family FX board.
      // A fixed pool bounds draw calls on mobile; pausing freezes their age/position.
      const dtf = Math.min((delta || 16) / 1000, 0.05), live = race.phase === 'racing';
      const emit = (family, x, y, vx, vy, duration, size) => this.fxState.emit(family, { x, y, vx, vy, duration, size });
      if (live) {
        this.emitClock += dtf;
        if (this.emitClock > (REDUCED ? 0.2 : LOW ? 0.09 : 0.045)) {
          this.emitClock = 0;
          if (!REDUCED && race.player.offRoad && race.player.speed > 8) for (const side of [-1, 1]) emit('dust', playerX + side * playerWidth * 0.28, playerY, side * 34, -35, 0.55, playerHeight * 0.37);
          else if (!REDUCED && Math.abs(race.player.wheel) > 0.7 && race.player.speed > 35) for (const side of [-1, 1]) emit('smoke', playerX + side * playerWidth * 0.28, playerY - playerHeight * 0.04, side * 20, -20, 0.45, playerHeight * 0.28);
          if (race.player.nitroRemaining > 0) for (const side of [-1, 1]) emit('nitro', playerX + side * playerWidth * 0.22, playerY + playerHeight * 0.02, side * 6, 55, 0.28, playerHeight * 0.38);
        }
      }
      if (race.hit && race.hit.id !== this.lastFxHit) {
        this.lastFxHit = race.hit.id;
        if (live) for (let i = 0; i < (REDUCED ? 2 : 8); i++) {
          const a = i * Math.PI / 4;
          emit('spark', playerX + Math.cos(a) * playerWidth * 0.25, playerY - playerHeight * 0.23, Math.cos(a) * 100, Math.sin(a) * 65 - 25, 0.4, playerHeight * 0.3);
        }
      }
      if (race.phase === 'finished') this.fxState.clear();
      this.fxState.update(dtf, !live);
      for (let i = 0; i < this.fxImages.length; i++) {
        const p = this.fxState.active[i], image = this.fxImages[i];
        if (!p) { image.setVisible(false); continue; }
        image.setVisible(true).setFrame(FX_ROWS[p.family] + p.frame).setPosition(p.x, p.y)
          .setDisplaySize(p.size, p.size).setAlpha(Math.min(1, (1 - p.age / p.duration) * 1.8))
          .setAngle(p.family === 'nitro' ? -90 : 0);
      }

    }
  };
}
