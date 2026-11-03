import test from 'node:test';
import assert from 'node:assert/strict';
import { buildTrack, WAYPOINTS } from '../src/track.js';
import { createRace, stepRace, cpuControls, pauseRace, resumeRace } from '../src/sim.js';
import { InputState } from '../src/input.js';

const IDLE = { left: false, right: false, throttle: false, brake: false, nitro: false };
const track = buildTrack();
function runBot(opts = {}, maxSeconds = 600) {
  const race = createRace(track, 'daniel', opts);
  const stats = { maxAbsLateral: 0, offRoadFrames: 0, frames: 0, nitroSeen: 0 };
  for (let i = 0; i < maxSeconds * 60 && race.phase !== 'finished'; i++) {
    stepRace(race, cpuControls(race, race.player, race.cpu), 1 / 60);
    if (race.phase === 'racing') { stats.frames++; stats.maxAbsLateral = Math.max(stats.maxAbsLateral, Math.abs(race.player.lateral)); if (race.player.offRoad) stats.offRoadFrames++; if (race.player.nitroRemaining > 0) stats.nitroSeen++; }
  }
  return { race, stats };
}

test('traçado: 36 pontos de controle, circuito fechado, comprimento plausível', () => {
  assert.equal(WAYPOINTS.length, 36);
  const p = track.points; assert.deepEqual(p[0], p[p.length - 1]);
  assert.ok(track.length > 3000 && track.length < 6000, `length=${track.length}`);
  for (let d = 0; d < track.length; d += 25) { const s = track.sample(d); assert.ok(Number.isFinite(s.x + s.y + s.heading + s.curvature)); assert.ok(Math.abs(s.curvature) < 0.05); }
});
test('sentido inverso mantém a mesma largada e o mesmo comprimento aproximado', () => {
  const r = buildTrack({ reverse: true });
  assert.deepEqual(r.points[0], track.points[0]);
  assert.ok(Math.abs(r.length - track.length) / track.length < 0.02);
});
test('multitoque: esquerda + acelerador + nitro simultâneos', () => {
  const i = new InputState(); i.press(1, 'left'); i.press(2, 'throttle'); i.press(3, 'nitro');
  assert.deepEqual(i.snapshot(), { left: true, right: false, throttle: true, brake: false, nitro: true });
  i.release(2); assert.equal(i.snapshot().throttle, false); i.clear(); assert.equal(i.count, 0);
});
test('contagem regressiva e largada', () => {
  const race = createRace(track, 'felipe'); assert.equal(race.cpu.driver, 'daniel');
  for (let i = 0; i < 60 * 3.1; i++) stepRace(race, IDLE, 1 / 60);
  assert.equal(race.phase, 'racing');
});
test('piloto parado nao completa volta; um dos seis rivais termina tres voltas', () => {
  const race = createRace(track, 'daniel');
  for (let i = 0; i < 60 * 400 && race.phase !== 'finished'; i++) stepRace(race, IDLE, 1 / 60);
  const winner = race.racers.find(d => d.driver === race.winner);
  assert.equal(race.phase, 'finished'); assert.equal(race.player.laps, 0);
  assert.ok(winner && winner !== race.player);
  assert.equal(winner.laps, 3); assert.equal(winner.lapTimes.length, 3);
  console.log('  Campeao CPU:', winner.driver, winner.finishTime.toFixed(1), 's');
});
test('bot completa a corrida, usa no máximo 2 nitros e passa pouco tempo fora do asfalto', () => {
  const { race, stats } = runBot();
  assert.equal(race.phase, 'finished'); assert.ok(race.racers.some(d => d.laps >= 3));
  assert.ok(race.player.charges >= 0 && race.cpu.charges >= 0);
  assert.ok(stats.maxAbsLateral <= 1.65 + 1e-9);
  console.log('  bot: tempo', race.elapsed.toFixed(1), 's, fora da pista', (100 * stats.offRoadFrames / stats.frames).toFixed(1), '%, max|lat|', stats.maxAbsLateral.toFixed(2), ', voltas', race.player.lapTimes.map((t) => t.toFixed(1)).join('/'));
  assert.ok(stats.offRoadFrames / stats.frames < 0.1);
});
test('nitro: duas cargas, aceleração acima da velocidade máxima normal, sem terceira ativação', () => {
  const race = createRace(track, 'daniel'); for (let i = 0; i < 200; i++) stepRace(race, IDLE, 1 / 60);
  let peak = 0, activations = 0;
  for (let i = 0; i < 60 * 40; i++) {
    const pulse = i % 240 === 0 || i % 240 === 1;
    const inp = { ...cpuControls(race, race.player, race.cpu), nitro: pulse, throttle: true, brake: false };
    const before = race.player.charges; stepRace(race, inp, 1 / 60); if (race.player.charges < before) activations++;
    peak = Math.max(peak, race.player.speed);
  }
  assert.equal(activations, 2); assert.equal(race.player.charges, 0); assert.ok(peak > race.config.maxSpeed, `peak=${peak}`);
});
test('pausa não avança a simulação', () => {
  const race = createRace(track, 'daniel'); for (let i = 0; i < 200; i++) stepRace(race, IDLE, 1 / 60);
  pauseRace(race); const snap = JSON.stringify([race.elapsed, race.cpu.distance]);
  for (let i = 0; i < 120; i++) stepRace(race, { ...IDLE, throttle: true }, 1 / 60);
  assert.equal(JSON.stringify([race.elapsed, race.cpu.distance]), snap); resumeRace(race); assert.equal(race.phase, 'racing');
});
test('fora do asfalto ainda é possível acelerar e voltar (sem travar em 0 km/h)', () => {
  const race = createRace(track, 'daniel'); for (let i = 0; i < 200; i++) stepRace(race, IDLE, 1 / 60);
  race.player.lateral = -1.4; race.player.speed = 0;
  for (let i = 0; i < 60 * 3; i++) stepRace(race, { ...IDLE, throttle: true, right: i > 30 }, 1 / 60);
  assert.ok(race.player.speed > 5, `speed=${race.player.speed}`); assert.ok(race.player.lateral > -1.4);
});
test('determinismo', () => { const a = runBot(), b = runBot(); assert.equal(a.race.elapsed, b.race.elapsed); });
