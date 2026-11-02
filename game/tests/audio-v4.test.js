import test from 'node:test';
import assert from 'node:assert/strict';
import { GameAudio } from '../src/audio.js';

test('audio unavailable keeps the entire public feedback API silent and nonfatal', async () => {
  const audio = new GameAudio();
  assert.equal(await audio.unlock(), false);
  assert.equal(audio.ready, false);
  assert.equal(audio.timer, null);
  for (const action of [() => audio.selection(), ...[0, 1, 2, 3, 4, 5].map(stage => () => audio.podium(stage)),
    () => audio.hit(1), () => audio.nitro(), () => audio.beep(true), () => audio.lap(), () => audio.finish(),
    () => audio.update(null, {}), () => audio.cycleMode()]) assert.doesNotThrow(action);
  await assert.doesNotReject(() => audio.suspend());
});

test('before the first gesture feedback never creates an AudioContext', () => {
  let created = 0;
  const previous = globalThis.window;
  globalThis.window = { AudioContext: class { constructor() { created++; } } };
  try {
    const audio = new GameAudio();
    audio.selection();
    audio.podium(3);
    assert.equal(created, 0);
    assert.equal(audio.ready, false);
  } finally {
    if (previous === undefined) delete globalThis.window; else globalThis.window = previous;
  }
});

test('browser AudioContext creation failure remains a silent optional feature', async () => {
  const previous = globalThis.window;
  globalThis.window = { AudioContext: class { constructor() { throw new Error('device unavailable'); } } };
  try {
    const audio = new GameAudio();
    assert.equal(await audio.unlock(), false);
    audio.selection(); audio.podium(5);
    assert.equal(audio.ready, false);
    assert.equal(audio.timer, null);
  } finally {
    if (previous === undefined) delete globalThis.window; else globalThis.window = previous;
  }
});

test('a later activation retries resume even while the first attempt is pending', async () => {
  let allowed = false, calls = 0;
  const pending = [];
  const ctx = { state: 'suspended', currentTime: 0, resume() {
    calls++;
    if (allowed) { this.state = 'running'; for (const resolve of pending.splice(0)) resolve(); return Promise.resolve(); }
    return new Promise(resolve => pending.push(resolve));
  } };
  const audio = new GameAudio(ctx);
  audio.build = () => { audio.ready = true; audio.master = { gain: { setTargetAtTime() {} } }; };
  audio.setMode = () => {}; audio.startMusic = () => {};
  const first = audio.unlock();
  allowed = true;
  const activated = audio.unlock();
  const result = await Promise.race([activated, new Promise(resolve => setTimeout(() => resolve('blocked'), 30))]);
  try { assert.equal(result, true, 'new activation must invoke resume rather than await a still-blocked call'); assert.ok(calls >= 2); }
  finally { await ctx.resume(); await Promise.all([first, activated]); }
});

test('sound control resumes an interrupted mode without cycling it and preserves intentional mute', async () => {
  const audio = new GameAudio({ state: 'suspended' });
  audio.ready = true; audio.activated = true; audio.suspended = true;
  audio.setMode = function(mode) { this.mode = mode; };
  audio.unlock = async function() { this.suspended = false; this.ctx.state = 'running'; return true; };
  assert.equal(audio.label, 'ATIVAR SOM');
  await audio.control();
  assert.equal(audio.mode, 'tudo', 'resuming music must not switch to effects-only');
  audio.setMode('efeitos'); audio.suspended = true; audio.ctx.state = 'suspended';
  await audio.control(); assert.equal(audio.mode, 'efeitos');
  audio.setMode('mudo'); audio.suspended = true; audio.ctx.state = 'suspended';
  await audio.unlock(); assert.equal(audio.mode, 'mudo', 'generic gestures preserve a deliberate mute');
  audio.suspended = true; audio.ctx.state = 'suspended';
  await audio.control(); assert.equal(audio.mode, 'tudo', 'a deliberate mute-control click can unmute');
});
