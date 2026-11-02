import test from 'node:test';
import assert from 'node:assert/strict';
import { access, readFile, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';
import { buildTrack } from '../src/track.js';
import { createRace, resolveContact, stepRace } from '../src/sim.js';
import { ROAD_WIDTH, CAR_LENGTH, CAR_WIDTH } from '../src/config.js';

const gameDir = fileURLToPath(new URL('../', import.meta.url));
const idle = Object.freeze({ left: false, right: false, throttle: false, brake: false, nitro: false });

test('fonte distribuida inclui UI, CSS e dependencias esperadas', async () => {
  for (const name of ['index.html', 'styles.css', 'src/ui.js', 'src/main.js', 'src/audio.js', 'src/render.js', 'src/sim.js']) {
    await access(resolve(gameDir, name));
  }
  const html = await readFile(resolve(gameDir, 'index.html'), 'utf8');
  assert.match(html, /href="styles\.css"/);
  assert.match(html, /src="src\/main\.js"/);
});

test('todas as importacoes relativas de src resolvem arquivos locais', async () => {
  const srcDir = resolve(gameDir, 'src');
  for (const filename of (await readdir(srcDir)).filter(n => n.endsWith('.js'))) {
    const body = await readFile(resolve(srcDir, filename), 'utf8');
    for (const [, relative] of body.matchAll(/(?:^|\n)\s*(?:import|export)\s+[^\n]*?\s+from\s+['"](\.[^'"]+)['"]/g)) {
      await access(resolve(dirname(resolve(srcDir, filename)), relative));
    }
  }
});

test('interface e audio podem ser importados no Node sem DOM', async () => {
  const [{ Ui }, { GameAudio, MODE_LABEL }] = await Promise.all([
    import('../src/ui.js'),
    import('../src/audio.js')
  ]);
  assert.equal(typeof Ui, 'function');
  assert.equal(typeof GameAudio, 'function');
  assert.equal(typeof MODE_LABEL.tudo, 'string');
});

test('largura de pista ampliada e contato longitudinal evitam atravessar carros', () => {
  assert.equal(ROAD_WIDTH, 18);
  const race = createRace(buildTrack(), 'daniel');
  race.phase = 'racing';
  race.player.distance = 100;
  race.cpu.distance = 101;
  race.player.lateral = race.cpu.lateral = 0;
  race.player.speed = 50; race.cpu.speed = 20;
  resolveContact(race);
  const longitudinal = Math.abs(race.cpu.distance - race.player.distance);
  const lateral = Math.abs(race.cpu.lateral - race.player.lateral);
  assert.ok(longitudinal >= CAR_LENGTH || lateral >= CAR_WIDTH);
  assert.equal(race.hitCount, 1);
});

test('direcao ganha inercia sem salto instantaneo', () => {
  const race = createRace(buildTrack(), 'daniel', { countdown: 0 });
  race.phase = 'racing';
  stepRace(race, { ...idle, right: true, throttle: true }, 1 / 60);
  assert.ok(race.player.wheel > 0 && race.player.wheel < 1);
  assert.ok(Number.isFinite(race.player.lateral));
});
