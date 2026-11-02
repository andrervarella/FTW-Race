import test from 'node:test';
import assert from 'node:assert/strict';
import { podiumStage, podiumMarkup } from '../src/podium.js';
import { createRace } from '../src/sim.js';
import { buildTrack } from '../src/track.js';
import { DRIVERS } from '../src/config.js';

test('seis gestos em sequência com tempo limitado e final estável', () => {
  assert.equal(podiumStage(0), 0);
  assert.equal(podiumStage(1.3), 1);
  assert.equal(podiumStage(2.7), 2);
  assert.equal(podiumStage(4), 3);
  assert.equal(podiumStage(5.5), 4);
  assert.equal(podiumStage(8), 5);
  assert.equal(podiumStage(1000), 5);
});

test('pódio identifica cada vencedor real sem mostrar rosto de outro piloto', () => {
  for (const winner of Object.keys(DRIVERS)) {
    const race = createRace(buildTrack(), 'daniel');
    race.phase = 'finished'; race.winner = winner;
    const car = race.racers.find(d => d.driver === winner);
    car.finishTime = 80; car.laps = 3;
    const markup = podiumMarkup(race, './assets/legacy/');
    assert.match(markup, new RegExp(`data-winner="${winner}"`));
    assert.ok(markup.includes(DRIVERS[winner].name));
    assert.ok(markup.includes('podium-replay') && markup.includes('podium-select') && markup.includes('podium-title'));
    assert.ok(markup.includes(`/${winner}-`));
  }
});
