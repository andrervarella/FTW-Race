import { NPC_KEYS } from './config.js';

export const NPC_FRAME = Object.freeze({ width: 560, height: 512, ground: 470 });

// Separate enter/exit thresholds retain a coherent view while the wheel settles.
// This is view state only: it never changes steering, grip or race progress.
export function vehicleAppearance(car, previousTurn = 0) {
  const wheel = Number.isFinite(car.wheel) ? car.wheel : 0;
  let turn = 0;
  if (car.speed > 10) {
    if (previousTurn === -1 && wheel < -.25) turn = -1;
    else if (previousTurn === 1 && wheel > .25) turn = 1;
    else if (wheel < -.6) turn = -1;
    else if (wheel > .6) turn = 1;
  }
  if (NPC_KEYS.includes(car.driver)) {
    const view = turn < 0 ? 1 : turn > 0 ? 2 : 0;
    return { texture: car.driver, frame: view + (car.braking ? 3 : 0), widthScale: NPC_FRAME.width / NPC_FRAME.height, turn };
  }
  return { texture: car.driver + (turn < 0 ? '-left' : turn > 0 ? '-right' : ''), frame: null, widthScale: 1, turn };
}
