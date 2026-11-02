// Simulação determinística (sem DOM, sem Phaser). Passo fixo de 1/60 s é responsabilidade do chamador.
import { DEFAULTS, LATERAL_LIMIT, CHECKPOINTS, CAR_LENGTH, CAR_WIDTH, otherDriver, NPC_KEYS } from './config.js';

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function makeDriver(driver, lateral, charges) {
  return { driver, distance: 0, lateral, speed: 0, steer: 0, wheel: 0, latVel: 0, hitTimer: 0, laps: 0, nextCheckpoint: 1, charges,
    nitroRemaining: 0, nitroHeld: false, collisionRemaining: 0, lapStart: 0, lapTimes: [], finishTime: null, offRoad: false };
}

export function createRace(track, playerKey, options = {}) {
  const config = { ...DEFAULTS, ...options };
  if (!Number.isInteger(config.laps) || config.laps < 1 || !Number.isInteger(config.nitroCharges) || config.nitroCharges < 0)
    throw new Error('Configuração de corrida inválida');
  const player = makeDriver(playerKey, -0.32, config.nitroCharges);
  const cpu = makeDriver(otherDriver(playerKey), 0.32, config.nitroCharges); cpu.profile = 1;
  const extras = NPC_KEYS.map((key, i) => {
    const d = makeDriver(key, [-0.76, 0.75, -0.14, 0.84][i], 0);
    d.distance = [18, 35, 52, 69][i];
    d.profile = [0.93, 0.99, 1.03, 0.91][i];
    return d;
  });
  const opponents = [cpu, ...extras];
  return { track, config, phase: 'countdown', resumePhase: 'countdown', countdown: config.countdown,
    elapsed: 0, winner: null, hit: null, hitCount: 0, player, cpu, extras, opponents,
    racers: [player, ...opponents] };
}

export function pauseRace(race) {
  if (race.phase === 'racing' || race.phase === 'countdown') { race.resumePhase = race.phase; race.phase = 'paused'; race.player.nitroHeld = false; }
}
export function resumeRace(race) { if (race.phase === 'paused') race.phase = race.resumePhase; }

// Portões: 1..7 intermediários, 8 = linha de chegada. Só conta volta se os portões forem cruzados em ordem.
function crossCheckpoints(race, d, from, to, tNow, dt) {
  if (to <= from) return;
  const L = race.track.length;
  for (let lap = Math.floor(from / L); lap <= Math.floor(to / L); lap++) {
    for (let cp = 1; cp <= CHECKPOINTS; cp++) {
      const at = lap * L + (cp * L) / CHECKPOINTS;
      if (at <= from || at > to) continue;
      if (cp === d.nextCheckpoint) {
        if (cp === CHECKPOINTS) {
          const tCross = tNow - dt + dt * ((at - from) / (to - from));
          d.laps++; d.nextCheckpoint = 1; d.lapTimes.push(tCross - d.lapStart); d.lapStart = tCross;
          if (d.laps >= race.config.laps && d.finishTime === null) d.finishTime = tCross;
        } else d.nextCheckpoint++;
      } else if (cp === CHECKPOINTS) d.nextCheckpoint = 1;
    }
  }
}

function stepDriver(race, d, input, dt) {
  const cfg = race.config, track = race.track;
  d.collisionRemaining = Math.max(0, d.collisionRemaining - dt); d.hitTimer = Math.max(0, d.hitTimer - dt);
  if (input.nitro && !d.nitroHeld && d.charges > 0 && d.nitroRemaining <= 0) { d.charges--; d.nitroRemaining = cfg.nitroDuration; }
  d.nitroHeld = input.nitro;
  d.nitroRemaining = Math.max(0, d.nitroRemaining - dt);
  const nitro = d.nitroRemaining > 0;
  d.offRoad = Math.abs(d.lateral) > 1;
  // fora do asfalto: velocidade máxima menor, mas ainda dá para acelerar e voltar (v0.1.0 travava em 0 km/h na grama)
  const vmax = cfg.maxSpeed * (nitro ? cfg.nitroMultiplier : 1) * (d.offRoad ? 0.55 : 1);
  const accel = input.brake ? -55 : input.throttle ? (nitro ? 32 : 20) : -12;
  if (d.speed > vmax) d.speed = Math.max(vmax, d.speed - ((input.brake ? 55 : 18) + (d.offRoad ? 30 : 0)) * dt);
  else d.speed = clamp(d.speed + (accel - (d.offRoad ? 12 : 0)) * dt, 0, vmax);
  // Direção com inércia (v0.2): o volante "anda" até o alvo e o carro desliza lateralmente com massa.
  d.steer = Number(input.right) - Number(input.left);
  const rate = d.steer === 0 ? 9 : 6;
  d.wheel += clamp(d.steer - d.wheel, -rate * dt, rate * dt);
  const curv = track.sample(d.distance).curvature;
  const targetVel = d.wheel * (0.6 + d.speed * 0.028) - curv * d.speed * d.speed * 0.008;
  d.latVel += (targetVel - d.latVel) * Math.min(1, 7 * dt);
  d.lateral += d.latVel * dt;
  d.speed = Math.max(0, d.speed - Math.abs(d.wheel) * d.speed * 0.05 * dt); // perde um pouco ao esterçar forte
  if (Math.abs(d.lateral) > LATERAL_LIMIT) { d.lateral = clamp(d.lateral, -LATERAL_LIMIT, LATERAL_LIMIT); d.latVel = 0; d.speed = Math.max(0, d.speed - 35 * dt); }
  const from = d.distance;
  d.distance += d.speed * dt;
  crossCheckpoints(race, d, from, d.distance, race.elapsed, dt);
}

// Piloto CPU. "catchUp" (±) ajusta levemente o ritmo para manter a disputa próxima; não é trapaça de posição.
export function cpuControls(race, d = race.cpu, rival = race.player) {
  const track = race.track, L = track.length;
  const now = track.sample(d.distance).curvature;
  const ahead = Math.abs(track.sample(d.distance + d.speed * 0.55).curvature);
  // linha: perto da direita; se o rival está logo à frente e na mesma faixa, procura espaço para ultrapassar
  let line = 0.25;
  const gapAhead = ((rival.distance - d.distance) % L + L) % L;
  if (gapAhead < 60 && Math.abs(rival.lateral - d.lateral) < 0.9 && d.speed > rival.speed * 0.85) line = rival.lateral > 0 ? rival.lateral - 0.95 : rival.lateral + 0.95;
  line = clamp(line, -1.2, 1.2);
  const target = (line - d.lateral) * 4 + now * d.speed * d.speed * 0.008 * 1.5;
  let gap = d.distance - rival.distance; // >0: CPU na frente
  gap = ((gap + L / 2) % L + L) % L - L / 2;
  const catchUp = clamp(-gap / 400, -0.04, 0.06);
  const base = ahead > 0.013 ? 37 : ahead > 0.006 ? 49 : 61;
  const vTarget = base * (1 + catchUp) * (d.profile ?? 1);
  const pos = track.wrap(d.distance);
  return {
    left: target < -0.12, right: target > 0.12, throttle: d.speed < vTarget, brake: d.speed > vTarget + 5,
    nitro: d.nitroRemaining <= 0 && d.distance > L * 0.12 && (pos < L * 0.3 || (d.charges === 1 && pos > L * 0.7)) && ahead < 0.004,
  };
}


// Colisão (v0.2): caixas de CAR_LENGTH x CAR_WIDTH. Nunca deixa um carro atravessar o outro.
// Encostada lateral: separa os carros e tira um pouco de velocidade dos dois. Traseira: o de trás não passa e perde ritmo.
const wrapSigned = (v, L) => ((v + L / 2) % L + L) % L - L / 2;
function resolvePair(race, player, cpu) {
  const { track } = race, L = track.length;
  let gap = wrapSigned(cpu.distance - player.distance, L); // >0: CPU à frente
  let dl = cpu.lateral - player.lateral;
  if (Math.abs(gap) >= CAR_LENGTH || Math.abs(dl) >= CAR_WIDTH) return;
  const front = gap >= 0 ? cpu : player, back = gap >= 0 ? player : cpu;
  const penLong = (CAR_LENGTH - Math.abs(gap)) / CAR_LENGTH, penLat = (CAR_WIDTH - Math.abs(dl)) / CAR_WIDTH;
  const closing = Math.max(0, back.speed - front.speed);
  let strength = 0;
  if (penLat < penLong) { // lado a lado: empurra para os lados
    const dir = dl === 0 ? (cpu.lateral > 0 ? 1 : -1) : Math.sign(dl), need = CAR_WIDTH - Math.abs(dl);
    cpu.lateral = clamp(cpu.lateral + (dir * need) / 2, -LATERAL_LIMIT, LATERAL_LIMIT);
    player.lateral = clamp(player.lateral - (dir * need) / 2, -LATERAL_LIMIT, LATERAL_LIMIT);
    dl = cpu.lateral - player.lateral;
    if (Math.abs(dl) < CAR_WIDTH - 1e-6) { // sem espaço (parede): trata como traseira
      back.distance = front.distance - CAR_LENGTH;
    }
    if (back.hitTimer === 0 && front.hitTimer === 0) { player.speed *= 0.94; cpu.speed *= 0.94; strength = 0.4; }
    player.latVel = -dir * 1.2; cpu.latVel = dir * 1.2;
  } else { // traseira: não atravessa
    back.distance = front.distance - CAR_LENGTH;
    if (back.hitTimer === 0) { strength = clamp(0.3 + closing / 30, 0.3, 1); back.speed = Math.max(0, Math.min(back.speed, front.speed) * 0.92 - 3); front.speed += Math.min(4, closing * 0.25); }
    else back.speed = Math.min(back.speed, front.speed);
    const side = back.lateral <= front.lateral ? -1 : 1;
    back.latVel += side * 0.8; front.latVel -= side * 0.4;
  }
  if (strength > 0) {
    player.hitTimer = cpu.hitTimer = 0.35;
    player.collisionRemaining = cpu.collisionRemaining = 0.8;
    if (player === race.player || cpu === race.player)
      race.hit = { at: race.elapsed, strength, id: ++race.hitCount };
  }
}
export function resolveContact(race) {
  const cars = race.racers ?? [race.player, race.cpu];
  for (let i = 0; i < cars.length; i++)
    for (let j = i + 1; j < cars.length; j++) resolvePair(race, cars[i], cars[j]);
}

export function stepRace(race, playerInput, dt) {
  if (!Number.isFinite(dt) || dt <= 0 || race.phase === 'paused' || race.phase === 'finished') return;
  dt = Math.min(dt, 0.05);
  if (race.phase === 'countdown') { race.countdown = Math.max(0, race.countdown - dt); if (race.countdown === 0) race.phase = 'racing'; return; }
  race.elapsed += dt;
  for (const d of race.opponents) {
    let closest = race.player, bestGap = Infinity;
    for (const rival of race.racers) {
      if (rival === d) continue;
      const gap = race.track.wrap(rival.distance - d.distance);
      if (gap > 0.01 && gap < bestGap) { bestGap = gap; closest = rival; }
    }
    stepDriver(race, d, cpuControls(race, d, closest), dt);
  }
  stepDriver(race, race.player, playerInput, dt);
  resolveContact(race);
  const finishers = race.racers.filter(d => d.finishTime !== null).sort((a,b) => a.finishTime - b.finishTime);
  if (finishers.length) {
    race.winner = finishers[0].driver;
    race.phase = 'finished';
    race.resultPosition = playerPosition(race);
    for (const d of race.racers) d.nitroRemaining = 0;
  }
}
export const playerPosition = race => 1 + (race.opponents ?? [race.cpu]).filter(d => d.distance > race.player.distance).length;
export const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${(s % 60).toFixed(1).padStart(4, '0')}`;
