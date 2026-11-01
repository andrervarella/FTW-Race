// Simulação determinística (sem DOM, sem Phaser). Passo fixo de 1/60 s é responsabilidade do chamador.
import { DEFAULTS, LATERAL_LIMIT, CHECKPOINTS, otherDriver } from './config.js';

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function makeDriver(driver, lateral, charges) {
  return { driver, distance: 0, lateral, speed: 0, steer: 0, laps: 0, nextCheckpoint: 1, charges,
    nitroRemaining: 0, nitroHeld: false, collisionRemaining: 0, lapStart: 0, lapTimes: [], finishTime: null, offRoad: false };
}

export function createRace(track, playerKey, options = {}) {
  const config = { ...DEFAULTS, ...options };
  if (!Number.isInteger(config.laps) || config.laps < 1 || !Number.isInteger(config.nitroCharges) || config.nitroCharges < 0)
    throw new Error('Configuração de corrida inválida');
  return {
    track, config, phase: 'countdown', resumePhase: 'countdown', countdown: config.countdown, elapsed: 0, winner: null,
    player: makeDriver(playerKey, -0.32, config.nitroCharges),
    cpu: makeDriver(otherDriver(playerKey), 0.32, config.nitroCharges),
  };
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
  d.collisionRemaining = Math.max(0, d.collisionRemaining - dt);
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
  d.steer = Number(input.right) - Number(input.left);
  const curv = track.sample(d.distance).curvature;
  d.lateral += d.steer * dt * (0.45 + d.speed * 0.03) - curv * d.speed * d.speed * dt * 0.012;
  if (Math.abs(d.lateral) > LATERAL_LIMIT) { d.lateral = clamp(d.lateral, -LATERAL_LIMIT, LATERAL_LIMIT); d.speed = Math.max(0, d.speed - 35 * dt); }
  const from = d.distance;
  d.distance += d.speed * dt;
  crossCheckpoints(race, d, from, d.distance, race.elapsed, dt);
}

// Piloto CPU. "catchUp" (±) ajusta levemente o ritmo para manter a disputa próxima; não é trapaça de posição.
export function cpuControls(race, d = race.cpu, rival = race.player) {
  const track = race.track, L = track.length;
  const now = track.sample(d.distance).curvature;
  const ahead = Math.abs(track.sample(d.distance + d.speed * 0.55).curvature);
  const target = (0.25 - d.lateral) * 4 + now * d.speed * d.speed * 0.012;
  let gap = d.distance - rival.distance; // >0: CPU na frente
  gap = ((gap + L / 2) % L + L) % L - L / 2;
  const catchUp = clamp(-gap / 400, -0.04, 0.06);
  const base = ahead > 0.013 ? 37 : ahead > 0.006 ? 49 : 61;
  const vTarget = base * (1 + catchUp);
  const pos = track.wrap(d.distance);
  return {
    left: target < -0.12, right: target > 0.12, throttle: d.speed < vTarget, brake: d.speed > vTarget + 5,
    nitro: d.nitroRemaining <= 0 && d.distance > L * 0.12 && (pos < L * 0.3 || (d.charges === 1 && pos > L * 0.7)) && ahead < 0.004,
  };
}

export function stepRace(race, playerInput, dt) {
  if (!Number.isFinite(dt) || dt <= 0 || race.phase === 'paused' || race.phase === 'finished') return;
  dt = Math.min(dt, 0.05);
  if (race.phase === 'countdown') { race.countdown = Math.max(0, race.countdown - dt); if (race.countdown === 0) race.phase = 'racing'; return; }
  race.elapsed += dt;
  const { player, cpu, track, config } = race;
  stepDriver(race, cpu, cpuControls(race), dt);
  stepDriver(race, player, playerInput, dt);
  const L = track.length, diff = Math.abs(player.distance - cpu.distance), dd = Math.min(diff % L, L - (diff % L));
  if (dd < 7 && Math.abs(player.lateral - cpu.lateral) < 0.3 && player.collisionRemaining === 0 && cpu.collisionRemaining === 0) {
    player.speed *= 0.7; cpu.speed *= 0.7; player.collisionRemaining = cpu.collisionRemaining = 0.8;
    const dir = player.lateral <= cpu.lateral ? -1 : 1;
    player.lateral = clamp(player.lateral + dir * 0.12, -LATERAL_LIMIT, LATERAL_LIMIT);
    cpu.lateral = clamp(cpu.lateral - dir * 0.12, -LATERAL_LIMIT, LATERAL_LIMIT);
  }
  if (player.laps >= config.laps || cpu.laps >= config.laps) {
    const pt = player.finishTime ?? Infinity, ct = cpu.finishTime ?? Infinity;
    race.winner = pt <= ct ? player.driver : cpu.driver;
    race.phase = 'finished'; player.nitroRemaining = cpu.nitroRemaining = 0;
  }
}

export const playerPosition = (race) => (race.player.distance >= race.cpu.distance ? 1 : 2);
export const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${(s % 60).toFixed(1).padStart(4, '0')}`;
