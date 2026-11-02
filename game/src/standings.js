// Classificação pura: tempos só existem para quem efetivamente cruzou a chegada.
// Empates usam a ordem canônica, independente da escolha do jogador ou da ordem de atualização.
import { NPC_KEYS } from './config.js';

const ORDER = ['daniel', 'felipe', ...NPC_KEYS];
const orderOf = key => ORDER.indexOf(key);

export function getResults(race) {
  if (race.results) return race.results.map(row => ({ ...row }));
  return [...race.racers].sort((a, b) => {
    const aDone = a.finishTime !== null, bDone = b.finishTime !== null;
    if (aDone !== bDone) return aDone ? -1 : 1;
    if (aDone && a.finishTime !== b.finishTime) return a.finishTime - b.finishTime;
    if (!aDone && a.distance !== b.distance) return b.distance - a.distance;
    return orderOf(a.driver) - orderOf(b.driver);
  }).map((d, i) => ({
    position: i + 1, driver: d.driver, finishTime: d.finishTime,
    finished: d.finishTime !== null, progress: d.distance, laps: d.laps,
    bestLap: d.lapTimes.length ? Math.min(...d.lapTimes) : null,
    isPlayer: d === race.player,
  }));
}
