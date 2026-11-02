import test from 'node:test';
import assert from 'node:assert/strict';
import * as sim from '../src/sim.js';
import { buildTrack } from '../src/track.js';
import { NPC_KEYS, CAR_LENGTH, CAR_WIDTH } from '../src/config.js';

const idle = Object.freeze({ left: false, right: false, throttle: false, brake: false, nitro: false });
const straight = { length: 1000, wrap: d => ((d % 1000) + 1000) % 1000, sample: () => ({ curvature: 0 }) };

function nearFinish(key = 'daniel') {
  const race = sim.createRace(straight, 'daniel', { laps: 1, countdown: 0 });
  race.phase = 'racing'; race.elapsed = 12;
  race.racers.forEach((d, i) => { d.distance = 100 + i * 30; d.speed = 0; d.lateral = 0; });
  const winner = race.racers.find(d => d.driver === key);
  winner.distance = 999.5; winner.speed = 60; winner.nextCheckpoint = 8;
  return race;
}

test('results API exposes pure, detached classification without invented times', () => {
  assert.equal(typeof sim.getResults, 'function');
  const race = nearFinish();
  const rows = sim.getResults(race);
  assert.equal(rows.length, 6);
  assert.deepEqual(rows.map(r => r.position), [1, 2, 3, 4, 5, 6]);
  assert.equal(rows.filter(r => r.isPlayer).length, 1);
  assert.ok(rows.every(r => r.finishTime === null && !r.finished && r.bestLap === null));
  const snapshot = JSON.stringify(rows);
  rows[0].laps = 999;
  assert.notEqual(JSON.stringify(sim.getResults(race)), JSON.stringify(rows));
  assert.equal(JSON.stringify(sim.getResults(race)), snapshot);
});

for (const key of ['daniel', 'felipe', ...NPC_KEYS]) {
  test(`real finish and frozen result for ${key}`, () => {
    const race = nearFinish(key);
    sim.stepRace(race, idle, 1 / 60);
    assert.equal(race.phase, 'finished');
    assert.equal(race.winner, key);
    assert.ok(race.finishedAt > 12 && race.finishedAt < 12 + 1 / 60);
    assert.equal(race.elapsed, race.finishedAt);
    const rows = sim.getResults(race);
    assert.equal(rows[0].driver, key);
    assert.equal(rows[0].finishTime, race.finishedAt);
    assert.equal(rows[0].laps, 1);
    assert.ok(Math.abs(rows[0].progress - 1000) < 1e-8);
    assert.ok(rows.slice(1).every(r => r.finishTime === null && !r.finished));
    const snapshot = JSON.stringify([race.elapsed, rows, race.racers]);
    sim.stepRace(race, { ...idle, throttle: true, nitro: true }, 1 / 60);
    assert.equal(JSON.stringify([race.elapsed, sim.getResults(race), race.racers]), snapshot);
  });
}

test('later crossings in same tick are discarded, including their lap times', () => {
  const race = nearFinish('daniel');
  race.player.distance = 999.95; race.player.lateral = -0.7;
  race.cpu.distance = 999.7; race.cpu.speed = 60; race.cpu.lateral = 0.7; race.cpu.nextCheckpoint = 8;
  sim.stepRace(race, idle, 1 / 60);
  assert.equal(race.winner, 'daniel');
  assert.equal(race.cpu.finishTime, null);
  assert.equal(race.cpu.laps, 0);
  assert.deepEqual(race.cpu.lapTimes, []);
  assert.ok(race.cpu.distance < 1000);
});

test('remaining classification uses progress at flag, before a later in-frame overtake', () => {
  const race = nearFinish(); race.player.distance = 999.95;
  race.cpu.distance = 500.4; race.cpu.speed = 0; race.cpu.lateral = -0.7;
  race.extras[0].distance = 500; race.extras[0].speed = 60; race.extras[0].lateral = 0.7;
  sim.stepRace(race, idle, 1 / 60);
  const rows = sim.getResults(race);
  assert.equal(rows[1].driver, race.cpu.driver);
  assert.equal(rows[2].driver, race.extras[0].driver);
  assert.equal(race.resultPosition, 1);
});

test('ties use canonical driver order, independent of player selection and array order', () => {
  assert.equal(typeof sim.getResults, 'function');
  const race = sim.createRace(straight, 'felipe');
  for (const d of race.racers) { d.distance = 100; d.finishTime = 10; }
  const a = sim.getResults(race).map(r => r.driver);
  race.racers.reverse();
  assert.deepEqual(sim.getResults(race).map(r => r.driver), a);
  assert.deepEqual(a, ['daniel', 'felipe', ...NPC_KEYS]);
});

test('controlled full race is deterministic with exact laps and unfinished racers un-timed', () => {
  function run() {
    const race = sim.createRace(buildTrack(), 'felipe', { laps: 1 });
    for (let frame = 0; frame < 60 * 180 && race.phase !== 'finished'; frame++)
      sim.stepRace(race, sim.cpuControls(race, race.player, race.cpu), 1 / 60);
    assert.equal(race.phase, 'finished');
    assert.equal(sim.getResults(race)[0].laps, 1);
    assert.ok(sim.getResults(race).filter(r => !r.finished).every(r => r.finishTime === null));
    return JSON.stringify([race.finishedAt, sim.getResults(race)]);
  }
  assert.equal(run(), run());
});

test('contact with lapped traffic preserves each racer lap progress', () => {
  const race = sim.createRace(straight, 'daniel');
  race.player.distance = 2100; race.player.lateral = 0; race.player.speed = 60;
  race.cpu.distance = 1101; race.cpu.lateral = 0; race.cpu.speed = 20;
  race.extras.forEach((d, i) => { d.distance = 1300 + i * 40; });
  sim.resolveContact(race);
  assert.equal(race.player.distance, 2092);
  assert.equal(race.cpu.distance, 1101);
});

test('six-car pile-up does not remain overlapped after repeated contact resolution', () => {
  for (const lateral of [0, -1.65, 1.65]) {
    const race = sim.createRace(straight, 'daniel');
    race.racers.forEach(d => { d.distance = 100; d.lateral = lateral; });
    for (let i = 0; i < 120; i++) sim.resolveContact(race);
    for (let i = 0; i < race.racers.length; i++) for (let j = i + 1; j < race.racers.length; j++) {
      const a = race.racers[i], b = race.racers[j];
      assert.ok(Math.abs(a.distance - b.distance) >= CAR_LENGTH - 1e-6 || Math.abs(a.lateral - b.lateral) >= CAR_WIDTH - 1e-6);
    }
  }
});

test('missing ordered checkpoints prevents a false final lap and winner', () => {
  const race = nearFinish(); race.player.nextCheckpoint = 4;
  sim.stepRace(race, idle, 1 / 60);
  assert.equal(race.player.laps, 0);
  assert.equal(race.player.finishTime, null);
  assert.equal(race.finishedAt, null);
  assert.equal(race.winner, null);
  assert.equal(race.phase, 'racing');
});
