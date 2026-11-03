import test from 'node:test';
import assert from 'node:assert/strict';
import * as config from '../src/config.js';
import { createRace, cpuControls, resolveContact, stepRace } from '../src/sim.js';

const idle = Object.freeze({ left: false, right: false, throttle: false, brake: false, nitro: false });
const straight = { length: 1000, wrap: d => ((d % 1000) + 1000) % 1000, sample: () => ({ curvature: 0 }) };
const officialKeys = ['daniel', 'felipe', 'marquinhos'];
const npcKeys = ['npc-blue', 'npc-yellow', 'npc-purple', 'npc-silver'];

for (const selected of officialKeys) {
  test(`${selected} races against both other officials and all four original NPCs`, () => {
    const race = createRace(straight, selected);
    assert.deepEqual(race.racers.map(d => d.driver).sort(), [...officialKeys, ...npcKeys].sort());
    assert.equal(race.player.driver, selected);
    assert.equal(race.opponents.length, 6);
    assert.equal(race.cpu.driver, selected === 'daniel' ? 'felipe' : 'daniel');
    assert.deepEqual(race.extras.map(d => d.driver), npcKeys);
    for (const key of officialKeys.filter(key => key !== selected)) {
      const opponent = race.opponents.find(d => d.driver === key);
      assert.equal(opponent.charges, 2);
      assert.ok(opponent.profile > 0);
    }
    const before = JSON.stringify(race.racers);
    resolveContact(race);
    assert.equal(JSON.stringify(race.racers), before, 'grid must begin separated, including the larger truck');
    race.phase = 'racing';
    for (let frame = 0; frame < 60; frame++) stepRace(race, idle, 1 / 60);
    for (const opponent of race.opponents) assert.ok(opponent.distance > 1, `${opponent.driver} must drive under AI`);
  });
}

test('playable identity supplies truck dimensions without inventing a number or surname', () => {
  assert.deepEqual(config.PLAYABLE_KEYS, officialKeys);
  const truck = config.DRIVERS.marquinhos;
  assert.equal(truck.name, 'Marquinhos');
  assert.equal(truck.first, 'Marquinhos');
  assert.equal(truck.last, '');
  assert.equal(truck.number, null);
  assert.equal(truck.vehicleType, 'truck');
  assert.equal(truck.renderScale, 1.7168195718654433);
  assert.equal(truck.collisionWidthFactor, 1.4);
  assert.equal(truck.collisionLengthFactor, 1.4);
  for (const key of ['daniel', 'felipe', ...npcKeys]) {
    assert.equal(config.DRIVERS[key].renderScale, 1);
    assert.equal(config.DRIVERS[key].collisionWidthFactor, 1);
    assert.equal(config.DRIVERS[key].collisionLengthFactor, 1);
  }
});

function isolatePair(selected, other) {
  const race = createRace(straight, selected);
  const opponent = race.opponents.find(d => d.driver === other);
  assert.ok(opponent, `${other} must remain on the grid`);
  race.racers = [race.player, opponent];
  race.player.distance = 100; race.player.lateral = 0; race.player.speed = 60;
  opponent.distance = 110; opponent.lateral = 0; opponent.speed = 20;
  return { race, opponent };
}

for (const [selected, other] of [['marquinhos', 'daniel'], ['daniel', 'marquinhos']]) {
  test(`truck rear contact uses both vehicles' lengths with ${selected} selected`, () => {
    const { race, opponent } = isolatePair(selected, other);
    resolveContact(race);
    assert.ok(race.hitCount > 0);
    assert.ok(Math.abs(opponent.distance - race.player.distance - 10.8) < 1e-8);
    assert.ok(race.player.speed < 20);
  });

  test(`truck side contact uses both vehicles' widths with ${selected} selected`, () => {
    const { race, opponent } = isolatePair(selected, other);
    opponent.distance = 100; opponent.lateral = 0.6;
    resolveContact(race);
    assert.ok(race.hitCount > 0);
    assert.ok(Math.abs(opponent.lateral - race.player.lateral - 0.66) < 1e-8);
    assert.equal(race.player.distance, 100);
    assert.equal(opponent.distance, 100);
  });
}

test('ordinary cars retain their previous collision dimensions', () => {
  const { race, opponent } = isolatePair('daniel', 'felipe');
  resolveContact(race);
  assert.equal(race.hitCount, 0);
  opponent.distance = 100; opponent.lateral = 0.6;
  resolveContact(race);
  assert.equal(race.hitCount, 0);
});

test('larger truck contact across the lap boundary preserves completed progress', () => {
  const { race, opponent } = isolatePair('marquinhos', 'daniel');
  race.player.distance = 2995;
  opponent.distance = 1005;
  resolveContact(race);
  assert.ok(Math.abs(race.player.distance - 2994.2) < 1e-8);
  assert.equal(opponent.distance, 1005);
  assert.equal(race.player.laps, 0);
  assert.equal(opponent.laps, 0);
});

test('AI leaves additional passing space when either vehicle is a truck', () => {
  for (const selected of ['daniel', 'marquinhos']) {
    const race = createRace(straight, selected);
    race.player.distance = 100; race.player.speed = 20; race.player.lateral = -0.85;
    race.cpu.distance = 130; race.cpu.speed = 20; race.cpu.lateral = 0.15;
    const controls = cpuControls(race, race.player, race.cpu);
    assert.equal(controls.left, selected === 'marquinhos');
    assert.equal(controls.right, selected === 'daniel');
  }
});

test('truck acceleration, steering and nitro retain the same arcade response as the cars', () => {
  function drive(selected) {
    const race = createRace(straight, selected, { countdown: 0 });
    race.phase = 'racing';
    race.opponents = []; race.racers = [race.player];
    for (let frame = 0; frame < 120; frame++)
      stepRace(race, { ...idle, throttle: true, right: frame < 10, nitro: frame === 30 }, 1 / 60);
    return ['distance', 'speed', 'lateral', 'wheel', 'charges', 'nitroRemaining'].map(key => race.player[key]);
  }
  assert.deepEqual(drive('marquinhos'), drive('daniel'));
});

test('seven vehicles separate from a pile-up even when the larger truck is against either road limit', () => {
  for (const lateral of [0, -1.65, 1.65]) {
    const race = createRace(straight, 'marquinhos');
    race.racers.forEach(d => { d.distance = 100; d.lateral = lateral; });
    for (let frame = 0; frame < 120; frame++) resolveContact(race);
    for (let i = 0; i < race.racers.length; i++) for (let j = i + 1; j < race.racers.length; j++) {
      const a = race.racers[i], b = race.racers[j];
      const truckPair = a.driver === 'marquinhos' || b.driver === 'marquinhos';
      assert.ok(Math.abs(a.distance - b.distance) >= (truckPair ? 10.8 : 9) - 1e-6 ||
        Math.abs(a.lateral - b.lateral) >= (truckPair ? 0.66 : 0.55) - 1e-6, `${a.driver}/${b.driver} remain overlapped at ${lateral}`);
    }
  }
});
