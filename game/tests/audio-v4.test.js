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
