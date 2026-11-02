import test from 'node:test';
import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { createRaceScene } from '../src/render.js';

test('sprite effects have a hard mobile budget and recycle expired slots', async () => {
  const { SpriteEffects } = await import('../src/effects.js');
  const pool = new SpriteEffects(3);
  for (let i = 0; i < 4; i++) pool.emit('dust', { x: i, y: 0, duration: 1, size: 20 });
  assert.equal(pool.active.length, 3);
  pool.update(1.01);
  assert.equal(pool.active.length, 0);
  assert.ok(pool.emit('spark', { x: 2, y: 3, duration: 0.4, size: 12 }));
  assert.equal(pool.active.length, 1);
});

test('paused effects freeze motion and frame timing; reset clears a previous race', async () => {
  const { SpriteEffects } = await import('../src/effects.js');
  const pool = new SpriteEffects(4);
  pool.emit('smoke', { x: 10, y: 20, vx: 40, vy: -20, duration: 1, size: 30 });
  pool.update(0.26);
  assert.equal(pool.active[0].frame, 1);
  assert.equal(pool.active[0].x, 20.4);
  const before = structuredClone(pool.active);
  pool.update(0.4, true);
  assert.deepEqual(pool.active, before);
  pool.clear();
  assert.equal(pool.active.length, 0);
});

test('V4 preload uses extracted individual scenery, car views and an animated FX atlas', async () => {
  const Scene = createRaceScene({ Scene: class {} }, { assets: new URL('../assets/legacy/', import.meta.url).href });
  const scene = new Scene(), files = [];
  scene.load = Object.fromEntries(['image', 'svg', 'spritesheet'].map(method => [method, (key, url) => files.push({key,url})]));
  scene.load.on = () => {};
  scene.preload();
  for (const key of ['fx', 'pit', 'tree', 'stand', 'fence', 'daniel-left', 'daniel-right', 'felipe-left', 'felipe-right']) {
    const item = files.find(f => f.key === key);
    assert.ok(item, `missing V4 sprite ${key}`);
    assert.match(item.url, /\/v4\//);
    await access(new URL(item.url));
  }
  for (const key of ['blue', 'yellow', 'purple', 'silver']) {
    const svg = await readFile(new URL(`../cars/npc-${key}.svg`, import.meta.url),'utf8');
    assert.match(svg, /same A45 rear chassis/);
    assert.doesNotMatch(svg, /FTW|DIABO/i);
  }
});
