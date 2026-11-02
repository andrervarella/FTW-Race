// Parâmetros provisórios (docs/00 e AGENTS.md): 3 voltas, 2 cargas de nitro, horizontal.
export const DEFAULTS = Object.freeze({
  laps: 3,
  nitroCharges: 2,
  nitroDuration: 2.5, // s
  nitroMultiplier: 1.35,
  maxSpeed: 64, // unidades de pista por segundo (x3.6 = km/h exibido, valor de jogo, não medida real)
  countdown: 3,
});
export const ROAD_WIDTH = 18; // largura em unidades de pista (v0.1.0: 12); lateral = ±1 é a borda do asfalto
export const CAR_LENGTH = 9; // caixa de colisão (unidades de pista)
export const CAR_WIDTH = 0.55; // caixa de colisão (unidades laterais; 1 = meia pista)
export const LATERAL_LIMIT = 1.65; // limite duro (zebra + escape)
export const CHECKPOINTS = 8; // portões igualmente espaçados; o 8 é a linha de chegada

export const NPC_KEYS = Object.freeze(['npc-blue','npc-yellow','npc-purple','npc-silver']);
export const DRIVERS = Object.freeze({
  daniel: { key: 'daniel', name: 'Daniel Mencacci', first: 'Daniel', number: 22, car: 'Mercedes AMG A45 verde', color: '#b0f138' },
  felipe: { key: 'felipe', name: 'Felipe Mencacci', first: 'Felipe', number: 25, car: 'Mercedes AMG A45 vermelha', color: '#ef5349' },
  'npc-blue': { key: 'npc-blue', name: 'Rival Azul', number: 31, color: '#29b6ff', car: 'Hatch de corrida (arte provisória)' },
  'npc-yellow': { key: 'npc-yellow', name: 'Rival Amarelo', number: 34, color: '#ffcf32', car: 'Hatch de corrida (arte provisória)' },
  'npc-purple': { key: 'npc-purple', name: 'Rival Roxo', number: 38, color: '#ad75f8', car: 'Hatch de corrida (arte provisória)' },
  'npc-silver': { key: 'npc-silver', name: 'Rival Prata', number: 41, color: '#d2e0eb', car: 'Hatch de corrida (arte provisória)' },
});
export const otherDriver = (key) => (key === 'daniel' ? 'felipe' : 'daniel');
