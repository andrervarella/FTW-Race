import test from 'node:test';
import assert from 'node:assert/strict';
import { podiumStage, podiumMarkup } from '../src/podium.js';
import { createRace } from '../src/sim.js';
import { buildTrack } from '../src/track.js';
import { DRIVERS } from '../src/config.js';
import * as podium from '../src/podium.js';

test('champanhe de Marquinhos parte da boca real da garrafa e segue para cima à direita', () => {
  assert.equal(typeof podium.podiumChampagneSpray, 'function', 'pódio deve disponibilizar o emissor medido no sprite');
  const { origin, direction } = podium.podiumChampagneSpray('marquinhos');
  assert.ok(Math.abs(origin[0] * 256 - 198.24242424242425) < 1e-8);
  assert.ok(Math.abs(origin[1] * 512 - 184.07713498622587) < 1e-8);
  assert.deepEqual(direction, [0.5, -0.8660254037844386]);
});

test('champanhe preserva a posição das garrafas aprovadas de Daniel e Felipe', () => {
  assert.equal(typeof podium.podiumChampagneSpray, 'function');
  assert.deepEqual(podium.podiumChampagneSpray('daniel'), { origin: [185 / 256, 165 / 512], direction: [1, 0] });
  assert.deepEqual(podium.podiumChampagneSpray('felipe'), { origin: [43 / 256, 139 / 512], direction: [-1, 0] });
});

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

test('pódio de Marquinhos não inventa número e apresenta os dois rivais seguintes na classificação', () => {
  const race = createRace(buildTrack(), 'daniel');
  race.phase = 'finished'; race.winner = 'marquinhos';
  race.results = ['marquinhos', 'npc-purple', 'felipe', 'daniel', 'npc-blue', 'npc-yellow', 'npc-silver']
    .map((driver, i) => ({ driver, position: i + 1 }));
  const markup = podiumMarkup(race, './assets/legacy/');
  const heading = markup.match(/<header class="podium-heading">(.*?)<\/header>/s)[1];
  assert.match(heading, /<h1>Marquinhos<\/h1>/);
  assert.doesNotMatch(heading, /#/);
  const runners = [...markup.matchAll(/class="runner-frame" src="[^"]*\/([^/]+)-1\.png"/g)].map(match => match[1]);
  assert.deepEqual(runners, ['npc-purple', 'felipe']);
  const emitter = markup.match(/<div class="champagne-fx"([^>]*)>/)[1];
  const left = Number(emitter.match(/left:([\d.]+)%/)?.[1]);
  const top = Number(emitter.match(/top:([\d.]+)%/)?.[1]);
  assert.ok(Math.abs(left - 77.43844696969697) < 1e-8, 'efeito acompanha a garrafa do novo sprite');
  assert.ok(Math.abs(top - 35.95256542699724) < 1e-8, 'efeito acompanha a altura da boca');
  const drops = [...markup.matchAll(/style="--i:\d+;--x:([-\d.]+)px;--y:([-\d.]+)px"/g)];
  assert.equal(drops.length, 24);
  for (const [, x, y] of drops) assert.ok(Number(x) > 0 && Number(y) < 0, 'todas as gotas partem para cima à direita');
});
