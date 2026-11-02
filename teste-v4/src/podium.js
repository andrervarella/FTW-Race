import { DRIVERS } from './config.js';
import { getResults } from './standings.js';

const states = new WeakMap();
const starts = [0, 1.2, 2.6, 3.9, 5.3, 7.5];
const labels = ['SUBINDO AO PÓDIO', 'A TAÇA É SUA', 'CAMPEÃO DE CASCAVEL', 'HORA DE COMEMORAR', 'FESTA NO PÓDIO', 'ATÉ A PRÓXIMA CORRIDA'];
export const podiumStage = seconds => starts.reduce((stage, at, i) => seconds >= at ? i : stage, 0);
const art = (driver, frame) => new URL(`../assets/v4/podium/${driver}-${frame}.png`, import.meta.url).href;
const sprite = (driver, frame, cls) => `<img class="${cls}" src="${art(driver, frame)}" alt="${DRIVERS[driver].name}" draggable="false">`;

export function podiumMarkup(race, assets) {
  const results = getResults(race), winner = race.winner, d = DRIVERS[winner];
  const runners = results.filter(row => row.driver !== winner).slice(0, 2);
  return `<section class="podium-screen" data-winner="${winner}" aria-label="Pódio de Cascavel">
    <header class="podium-heading"><img src="${assets}ftw.png" alt="FTW"><div><small>BANDEIRADA · CASCAVEL</small><h1>${d.name}</h1><p>CAMPEÃO · #${d.number}</p></div></header>
    <div class="podium-scene" aria-label="Comemoração em seis poses de corpo inteiro">
      <button class="primary podium-continue" id="podium-continue" hidden>CONTINUAR COMEMORAÇÃO</button>
      <div class="podium-lights" aria-hidden="true"></div>
      <div class="podium-person champion" style="--team:${d.color}">${sprite(winner, 0, 'champion-frame')}<div class="champagne-fx" aria-hidden="true">${Array.from({length:24}, (_, i) => `<img src="${new URL('../assets/v4/podium/drop.svg', import.meta.url).href}" style="--i:${i}" alt="">`).join('')}</div></div>
      ${runners.map((row, i) => `<div class="podium-person runner runner-${i}">${sprite(row.driver, 1, 'runner-frame')}<span>${DRIVERS[row.driver].name}</span></div>`).join('')}
      <div class="podium-step step-two"><b>2</b></div><div class="podium-step step-one"><b>1</b></div><div class="podium-step step-three"><b>3</b></div>
      <div class="podium-stage-label" aria-live="polite">${labels[0]}</div>
    </div>
    <footer class="podium-actions"><button class="primary" id="podium-replay">CORRER NOVAMENTE</button><button class="secondary" id="podium-select">TROCAR PILOTO</button><button class="text-button" id="podium-title">VOLTAR À CAPA</button><button class="text-button" id="podium-sound">SOM</button></footer>
    <small class="podium-review">V4 · Daniel e Felipe aprovados · arte dos rivais em revisão</small>
  </section>`;
}

export function updatePodium(root, race, dt, audio) {
  const scene = root.querySelector('.podium-screen');
  if (!scene || !race?.winner) return;
  let state = states.get(scene);
  if (!state) { state = { elapsed: 0, stage: -1 }; states.set(scene, state); }
  if (typeof document !== 'undefined' && document.hidden) return;
  state.elapsed += Math.max(0, Math.min(Number.isFinite(dt) ? dt : 0, 0.1));
  const stage = podiumStage(state.elapsed);
  if (stage !== state.stage) {
    state.stage = stage; scene.dataset.stage = String(stage);
    scene.querySelector('.champion-frame').src = art(race.winner, stage);
    scene.querySelector('.podium-stage-label').textContent = labels[stage];
    audio?.podium?.(stage);
  }
  const sound = scene.querySelector('#podium-sound');
  if (sound && !sound.onclick) sound.onclick = () => { audio?.unlock?.(); audio?.cycleMode?.(); sound.textContent = audio?.mode === 'mudo' ? 'MUDO' : 'SOM'; };
}
