import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import { vehicleAppearance, NPC_FRAME } from '../src/vehicle-visual.js';
import { createRaceScene } from '../src/render.js';
import { createRace, stepRace, pauseRace } from '../src/sim.js';
import { buildTrack } from '../src/track.js';
import { NPC_KEYS } from '../src/config.js';

test('each NPC has rear, two distinct turn views and all three brake views', () => {
  for (const driver of NPC_KEYS) {
    for (const [wheel, braking, frame] of [[0,false,0],[-1,false,1],[1,false,2],[0,true,3],[-1,true,4],[1,true,5]]) {
      const look=vehicleAppearance({driver,wheel,braking,speed:40});
      assert.equal(look.texture,driver); assert.equal(look.frame,frame);
      assert.equal(look.widthScale,NPC_FRAME.width/NPC_FRAME.height);
    }
  }
});
test('view hysteresis uses wheel inertia and prevents threshold flicker', () => {
  const car={driver:'npc-blue',wheel:-.7,speed:40,braking:false};
  let look=vehicleAppearance(car);assert.equal(look.turn,-1);
  for(const wheel of [-.58,-.4,-.3]) {look=vehicleAppearance({...car,wheel},look.turn);assert.equal(look.frame,1);}
  assert.equal(vehicleAppearance({...car,wheel:-.2},look.turn).frame,0);
  assert.equal(vehicleAppearance({...car,speed:0},-1).frame,0);
  assert.equal(vehicleAppearance({...car,speed:0,braking:true},-1).frame,3);
});
test('official cars retain their existing distinct views and square scale', () => {
  assert.deepEqual(vehicleAppearance({driver:'daniel',wheel:-1,speed:40}),{texture:'daniel-left',frame:null,widthScale:1,renderScale:1,turn:-1});
  assert.equal(vehicleAppearance({driver:'felipe',wheel:0,speed:40,braking:true}).texture,'felipe');
});
test('runtime preloads four raster atlases with six real frames, no NPC SVG',async()=>{
  const Scene=createRaceScene({Scene:class{}},{assets:''});const scene=new Scene(),files=[];
  scene.load=Object.fromEntries(['image','svg','spritesheet'].map(method=>[method,(key,url,options)=>files.push({method,key,url,options})]));scene.load.on=()=>{};scene.preload();
  const meta=JSON.parse(await readFile(new URL('../assets/v4/cars/npc-cars.json',import.meta.url),'utf8'));
  assert.equal(meta.frames.length,6);
  for(const key of NPC_KEYS){
    const file=files.find(f=>f.key===key);assert.equal(file.method,'spritesheet');assert.match(file.url,/npc-raster/);await access(new URL(file.url));
    assert.equal(file.options.frameWidth,NPC_FRAME.width);assert.equal(file.options.frameHeight,NPC_FRAME.height);
    const png=await readFile(new URL(file.url));assert.equal(png.readUInt32BE(16),NPC_FRAME.width*3);assert.equal(png.readUInt32BE(20),NPC_FRAME.height*2);
  }
  assert.equal(files.filter(f=>f.method==='svg'&&NPC_KEYS.includes(f.key)).length,0);
});
test('brake lamp state follows the real input for player and AI and freezes on pause',()=>{
  const race=createRace(buildTrack(),'daniel');assert.equal(race.player.braking,false);race.phase='racing';
  const idle={left:false,right:false,throttle:false,brake:false,nitro:false};
  for(const d of race.racers)d.speed=100;
  stepRace(race,{...idle,brake:true},1/60);assert.equal(race.player.braking,true);assert.ok(race.opponents.every(d=>d.braking));
  pauseRace(race);stepRace(race,idle,1/60);assert.equal(race.player.braking,true);
  race.phase='racing';stepRace(race,idle,1/60);assert.equal(race.player.braking,false);
});
