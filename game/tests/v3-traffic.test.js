import test from 'node:test';
import assert from 'node:assert/strict';
import {buildTrack} from '../src/track.js';
import {createRace,stepRace,playerPosition,resolveContact} from '../src/sim.js';
import {NPC_KEYS,DRIVERS,CAR_LENGTH,CAR_WIDTH} from '../src/config.js';
const idle={left:false,right:false,throttle:false,brake:false,nitro:false};
test('seis carros e quatro novos pilotos sem marcas',()=>{const r=createRace(buildTrack(),'felipe');assert.equal(r.racers.length,6);assert.equal(new Set(r.racers.map(x=>x.driver)).size,6);assert.equal(playerPosition(r),5);for(const key of NPC_KEYS)assert.match(DRIVERS[key].car,/provisória/);});
test('simulacao de 20 s finita',()=>{const r=createRace(buildTrack(),'daniel');for(let i=0;i<1200;i++)stepRace(r,{...idle,throttle:true},1/60);for(const d of r.racers)for(const k of ['distance','lateral','speed','wheel'])assert.ok(Number.isFinite(d[k]));assert.ok(playerPosition(r)>=1&&playerPosition(r)<=6);});
test('colisao com rival extra',()=>{const r=createRace(buildTrack(),'daniel');r.phase='racing';r.player.distance=100;r.player.lateral=0;r.player.speed=60;for(const d of r.opponents){d.distance=300;d.lateral=1.2;d.speed=20;}r.extras[0].distance=104;r.extras[0].lateral=0;r.extras[0].speed=20;resolveContact(r);assert.ok(r.hitCount>0);assert.ok(Math.abs(r.extras[0].distance-r.player.distance)>=CAR_LENGTH||Math.abs(r.extras[0].lateral-r.player.lateral)>=CAR_WIDTH);});
