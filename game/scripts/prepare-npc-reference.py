"""Prepare NPC racing views from the owner's design, without changing source bytes.

One common scale for all teams/poses. Rear-axle X uses the pair of tail lights,
not the full silhouette center, so a turn view does not shift the car sideways.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/previews/v4/npc-cars-views-generated.png'
TARGET=ROOT/'game/assets/v4/cars/npc-raster'
TARGET.mkdir(parents=True,exist_ok=True)
FRAME=(560,512); GROUND=470; SCALE=330/230
NAMES=['rear','left','right','brake','left-brake','right-brake']
source=Image.open(SOURCE).convert('RGBA')

def clean(image):
    pixels=np.array(image)
    pixels[:,:,3]=np.where(pixels[:,:,3]>=60,255,0)
    labels,count=ndimage.label(pixels[:,:,3]>0)
    if count:
        areas=np.bincount(labels.ravel());areas[0]=0
        # Remove tiny disconnected artifacts while retaining mirrors/wing parts.
        allowed=np.flatnonzero(areas>=max(8,areas.max()*.001))
        pixels[:,:,3]=np.where(np.isin(labels,allowed),pixels[:,:,3],0)
    pixels[pixels[:,:,3]==0,:3]=0
    return Image.fromarray(pixels)

def rear_center(image,bbox):
    pixels=np.array(image).astype(float);r,g,b,a=np.moveaxis(pixels,-1,0)
    yy=np.arange(image.height)[:,None]
    mask=(a>0)&(r>110)&(r>g*1.45)&(r>b*1.25)&(yy>bbox[1]+(bbox[3]-bbox[1])*.34)&(yy<bbox[1]+(bbox[3]-bbox[1])*.65)
    midpoint=(bbox[0]+bbox[2])/2
    centers=[]
    for side in [np.arange(image.width)[None,:]<midpoint,np.arange(image.width)[None,:]>=midpoint]:
        _,xs=np.where(mask&side)
        assert len(xs)>20,'Tail light pair required for a stable rear-axle anchor'
        centers.append((int(xs.min())+int(xs.max()))/2)
    return sum(centers)/2

def brake_variant(image):
    p=np.array(image).astype(float);r,g,b,a=np.moveaxis(p,-1,0)
    yy=np.arange(image.height)[:,None]
    box=image.getbbox();top,bottom=box[1],box[3]
    mask=(a>0)&(r>110)&(r>g*1.45)&(r>b*1.25)&(yy>top+(bottom-top)*.34)&(yy<top+(bottom-top)*.65)
    assert mask.sum()>100,'Visible tail lights required for brake variant'
    p[:,:,0][mask]=255
    p[:,:,1][mask]=np.minimum(220,p[:,:,1][mask]+100)
    p[:,:,2][mask]=np.minimum(200,p[:,:,2][mask]+85)
    return Image.fromarray(p.astype('uint8'))

meta={'version':'npc-reference-1','source':'assets/previews/v4/npc-cars-views-generated.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      'reference':'Owner supplied four-car NPC sheet in conversation; approved visual design, original attachment bytes unavailable to executor',
      'status':'reference-design-requested; derived views inspected, owner review of final artwork pending',
      'frameSize':list(FRAME),'pivot':[.5,GROUND/FRAME[1]],'commonScale':SCALE,'frames':NAMES,'files':[],
      'retired':['cars/npc-blue.svg','cars/npc-yellow.svg','cars/npc-purple.svg','cars/npc-silver.svg']}
for row,key in enumerate(['npc-blue','npc-yellow','npc-silver','npc-purple']):
    prepared=[];records=[]
    for col in range(4):
        rect=[round(col*source.width/4),round(row*source.height/4),round((col+1)*source.width/4),round((row+1)*source.height/4)]
        original=clean(source.crop(rect));bbox=original.getbbox();pivot=rear_center(original,bbox)
        crop=original.crop(bbox);w,h=round(crop.width*SCALE),round(crop.height*SCALE)
        crop=crop.resize((w,h),Image.Resampling.NEAREST)
        x=round(FRAME[0]/2-(pivot-bbox[0])*SCALE);y=GROUND-h
        assert x>=0 and x+w<=FRAME[0] and y>0,'Frame must preserve complete wing/mirrors/wheels'
        canvas=Image.new('RGBA',FRAME);canvas.alpha_composite(crop,(x,y))
        prepared.append(canvas)
        records.append({'name':NAMES[col],'sourceCrop':rect,'sourceUsefulBounds':list(bbox),'sourceRearAxleX':pivot})
    prepared.extend([brake_variant(prepared[1]),brake_variant(prepared[2])])
    records.extend([{'name':NAMES[i],'derivedFrom':NAMES[i-3],'operation':'tail-light brightness only; identical alpha/body geometry'}for i in [4,5]])
    atlas=Image.new('RGBA',(FRAME[0]*3,FRAME[1]*2))
    for i,frame in enumerate(prepared):atlas.alpha_composite(frame,((i%3)*FRAME[0],(i//3)*FRAME[1]))
    # One shared palette per atlas prevents color flicker between view states.
    atlas=atlas.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
    path=TARGET/f'{key}.png';atlas.save(path,optimize=True)
    frame_dir=TARGET/'frames'/key;frame_dir.mkdir(parents=True,exist_ok=True)
    for i,record in enumerate(records):
        frame=atlas.crop(((i%3)*FRAME[0],(i//3)*FRAME[1],(i%3+1)*FRAME[0],(i//3+1)*FRAME[1]))
        frame_path=frame_dir/f'{NAMES[i]}.png';frame.save(frame_path,optimize=True)
        record.update({'index':i,'path':str(frame_path.relative_to(ROOT/'game')),'sha256':hashlib.sha256(frame_path.read_bytes()).hexdigest()})
    meta['files'].append({'key':key,'path':str(path.relative_to(ROOT/'game')),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'atlasSize':list(atlas.size),'frames':records})
(ROOT/'game/assets/v4/cars/npc-cars.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Prepared 4 atlases / 24 complete car frames with a shared scale and rear-axle anchor.')
