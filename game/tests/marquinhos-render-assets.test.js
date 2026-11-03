import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { createRaceScene } from '../src/render.js';
import { vehicleAppearance } from '../src/vehicle-visual.js';
import { createRace } from '../src/sim.js';
import { buildTrack } from '../src/track.js';

const scale = 1.7168195718654433;
const states = [[0, false], [-1, false], [1, false], [0, true], [-1, true], [1, true]];
const hash = data => createHash('sha256').update(data).digest('hex');
const file = path => new URL(path, import.meta.url);

function sceneHarness(race, width = 915, height = 412) {
  const Scene = createRaceScene({ Scene: class {} }, { track: race.track, getRace: () => race, onReady() {} });
  const scene = new Scene();
  function image(x, y, texture, frame = null) {
    const sprite = { x, y, textureKey: texture, frame, texture: { getSourceImage: () => ({ width: 560, height: 512 }) } };
    for (const method of ['setOrigin', 'setDepth', 'setAlpha', 'setAngle']) sprite[method] = (...values) => { sprite[method.slice(3).toLowerCase()] = values; return sprite; };
    sprite.setTexture = value => { sprite.textureKey = value; return sprite; };
    sprite.setFrame = value => { sprite.frame = value; return sprite; };
    sprite.setVisible = value => { sprite.visible = value; return sprite; };
    sprite.setPosition = (x, y) => { sprite.x = x; sprite.y = y; return sprite; };
    sprite.setDisplaySize = (width, height) => { sprite.displayWidth = width; sprite.displayHeight = height; return sprite; };
    return sprite;
  }
  scene.add = { image, graphics: () => Object.fromEntries(['clear', 'fillStyle', 'fillRect', 'fillPoints'].map(key => [key, () => {}])) };
  scene.scale = { width, height };
  scene.create();
  return scene;
}

test('Marquinhos has all six authentic truck states and uniform render scale', () => {
  states.forEach(([wheel, braking], frame) => {
    const look = vehicleAppearance({ driver: 'marquinhos', wheel, braking, speed: 40 });
    assert.equal(look.texture, 'marquinhos');
    assert.equal(look.frame, frame);
    assert.equal(look.widthScale, 560 / 512);
    assert.equal(look.renderScale, scale);
  });
});

test('scene preloads native truck atlas and allocates all six rivals', () => {
  const race = createRace(buildTrack(), 'daniel');
  const scene = sceneHarness(race), files = [];
  scene.load = { image() {}, spritesheet: (key, url, options) => files.push({ key, url, options }), on() {} };
  scene.preload();
  const truck = files.find(item => item.key === 'marquinhos');
  assert.ok(truck, 'preload the third playable vehicle');
  assert.match(truck.url, /cars\/marquinhos\.png$/);
  assert.deepEqual(truck.options, { frameWidth: 560, frameHeight: 512 });
  assert.equal(scene.rivals.length, 6, 'every opponent has a sprite');
});

test('truck player and AI use the same uniform proportions without covering mobile HUD', () => {
  const race = createRace(buildTrack(), 'daniel');
  race.phase = 'racing';
  const scene = sceneHarness(race);
  race.player.wheel = 0; race.player.speed = 40;
  scene.update(0, 16);
  const carHeight = scene.player.displayHeight, carWidth = scene.player.displayWidth;
  race.player.driver = 'marquinhos';
  for (const [wheel, braking] of states) {
    Object.assign(race.player, { wheel, braking });
    scene.update(0, 16);
    assert.ok(Math.abs(scene.player.displayHeight / carHeight - scale) < 1e-10);
    assert.ok(Math.abs(scene.player.displayWidth / carWidth - scale * 560 / 512) < 1e-10);
    assert.equal(scene.player.origin[1], 470 / 512);
    assert.ok(scene.player.displayHeight <= 412 * .47 + 1e-10, 'truck has a viewport height budget');
    assert.ok(scene.player.y - scene.player.displayHeight * 470 / 512 > 412 * .37, 'truck stays below the horizon');
  }
  race.player.driver = 'daniel';
  // Matching projected positions reveal any player-only truck scale path.
  Object.assign(race.opponents[0], { driver: 'marquinhos', distance: 35, lateral: 0, wheel: 0, speed: 40 });
  Object.assign(race.opponents[1], { driver: 'npc-blue', distance: 35, lateral: 0, wheel: 0, speed: 40 });
  for (const [wheel, braking] of states) {
    Object.assign(race.opponents[0], { wheel, braking });
    scene.update(0, 16);
    assert.ok(scene.rivals[0].visible);
    assert.ok(Math.abs(scene.rivals[0].displayHeight / scene.rivals[1].displayHeight - scale) < 1e-10);
    assert.ok(Math.abs(scene.rivals[0].displayWidth / scene.rivals[1].displayWidth - scale) < 1e-10);
  }
});

test('runtime Marquinhos art is byte-identical to prepared sources', async () => {
  const copies = [
    ['drivers/marquinhos-neutral.png', 'truck-driver/neutral.png'],
    ['drivers/marquinhos-portrait.png', 'truck-driver/portrait.png'],
    ['drivers/marquinhos-portrait.webp', 'truck-driver/portrait.webp'],
    ['title/marquinhos-front-portrait.png', 'truck-driver/portrait.png'],
    ['title/marquinhos-front-portrait.webp', 'truck-driver/portrait.webp'],
    ['cars/marquinhos.png', 'truck-vehicle/truck-atlas.png'],
    ['cars/marquinhos-front.png', 'truck-vehicle/front-menu.png'],
    ...['rear', 'left', 'right', 'brake', 'left-brake', 'right-brake'].map(state => [`cars/marquinhos-${state}.png`, `truck-vehicle/${state}.png`]),
    ...Array.from({ length: 6 }, (_, i) => [`podium/marquinhos-${i}.png`, `truck-driver/podium-${i}.png`]),
  ];
  for (const [runtime, source] of copies) {
    assert.equal(hash(await readFile(file(`../assets/v4/${runtime}`))), hash(await readFile(file(`../../assets/sprites/v4/${source}`))), runtime);
  }
  const provenance = JSON.parse(await readFile(file('../assets/v4/drivers/marquinhos.json'), 'utf8'));
  assert.equal(provenance.masterApproval.quote, 'Ótimo. Essa última ficou perfeita. Ela é a referência.');
  assert.equal(provenance.integrationAcceptance.date, '2026-11-03');
});

test('Felipe less-chin retouch applies only to the opening portrait', async () => {
  const portrait = await readFile(file('../assets/v4/title/felipe-front-portrait.png'));
  assert.equal(hash(portrait), '98832d1d00feb8f628d76172ad2ace8dcacf75a4a6ea2e7c8af88faf4f7a236b');
  const manifest = JSON.parse(await readFile(file('../../assets/sprites/V4_MANIFEST.json'), 'utf8'));
  const approved = JSON.parse(await readFile(file('../assets/v4/drivers/approved-pilots.json'), 'utf8'));
  const before = [...manifest.assets.filter(row => row.path.includes('/felipe-') && !row.path.includes('/title/')),
    ...approved.views.filter(row => row.file.includes('/felipe-'))].map(row => ({ ...row, path: row.path ?? row.file }));
  for (const row of before) assert.equal(hash(await readFile(file(`../../${row.path}`))), row.sha256, row.path);
});

test('asset inventory records accepted integration separately from earlier pilot approvals', async () => {
  const manifest = JSON.parse(await readFile(file('../../assets/sprites/V4_MANIFEST.json'), 'utf8'));
  for (const path of ['game/assets/v4/cars/marquinhos.png', 'game/assets/v4/drivers/marquinhos-neutral.png', 'game/assets/v4/podium/marquinhos-5.png', 'game/assets/v4/title/marquinhos-front-portrait.png']) {
    const row = manifest.assets.find(item => item.path === path);
    assert.ok(row, `inventory covers ${path}`);
    assert.equal(row.status, 'owner-requested-integration');
    assert.equal(hash(await readFile(file(`../../${path}`))), row.sha256);
  }
  assert.ok(manifest.details.includes('game/assets/v4/cars/marquinhos.json'));
  assert.ok(manifest.details.includes('game/assets/v4/drivers/marquinhos.json'));
});
