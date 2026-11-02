"""Normalize explicitly requested sprite crops; references and generated source stay untouched."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json

repo=Path(__file__).resolve().parents[2]
if (repo/'game/assets/v4/drivers/approved-pilots.json').exists():
    raise SystemExit('Historical podium generator disabled: use prepare-approved-pilots.py to preserve owner-approved art.')
source=repo/'assets/previews/v4/podium-generated-source.png'
target=repo/'game/assets/v4/podium'
target.mkdir(parents=True,exist_ok=True)
im=Image.open(source).convert('RGBA')
# Tool returns RGB glow even in alpha=0 pixels; discard low-alpha halos.
alpha=im.getchannel('A').point(lambda a: 0 if a<40 else 255 if a>225 else a)
im.putalpha(alpha)
boxes=[(15,48,263,520),(272,48,493,520),(493,0,727,520),(731,48,984,520),(1000,55,1279,520),(1280,10,1536,520)]
records=[]
for row,key in enumerate(['daniel','felipe']):
    for frame,(x0,y0,x1,y1) in enumerate(boxes):
        if row: y0=520 if frame==2 else y0+515; y1=1024
        crop=im.crop((x0,y0,x1,y1))
        bbox=crop.getbbox()
        if bbox: crop=crop.crop(bbox)
        crop=crop.resize((round(crop.width*.9),round(crop.height*.9)),Image.Resampling.NEAREST)
        canvas=Image.new('RGBA',(256,512))
        canvas.alpha_composite(crop,((256-crop.width)//2,500-crop.height))
        path=target/f'{key}-{frame}.png';canvas.save(path,optimize=True)
        records.append({'file':str(path.relative_to(repo)),'source':str(source.relative_to(repo)),'sourceCrop':[x0,y0,x1,y1],'frame':frame,'pivot':[.5,500/512],'size':[256,512],'approval':'pending-human-review','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

colors={'npc-blue':(41,182,255),'npc-yellow':(255,207,50),'npc-purple':(173,117,248),'npc-silver':(210,224,235)}
npc_source=repo/'assets/previews/v4/npc-podium-generated-source.png'
npc=Image.open(npc_source).convert('RGBA')
npc.putalpha(npc.getchannel('A').point(lambda a: 0 if a<40 else 255 if a>225 else a))
# Six genuine complete-body poses; no human face; common scale/ground for all teams.
npc_boxes=[(0,145,332,706),(340,145,652,706),(670,0,977,706),(1018,145,1320,706),(1380,145,1747,706),(1775,0,2172,706)]
for key,color in colors.items():
    for frame,box in enumerate(npc_boxes):
        crop=npc.crop(box);bbox=crop.getbbox()
        if bbox:crop=crop.crop(bbox)
        pixels=[]
        for r,g,b,a in crop.get_flattened_data():
            # Recolor neutral suit/helmet only: gold trophy, green bottle, visor and boots stay intact.
            value=(r+g+b)/3
            if key!='npc-silver' and a and max(r,g,b)-min(r,g,b)<42 and 45<value<232:
                r,g,b=[round(min(255,c*value/180)) for c in color]
            pixels.append((r,g,b,a))
        crop.putdata(pixels)
        crop=crop.resize((round(crop.width*.70),round(crop.height*.70)),Image.Resampling.NEAREST)
        canvas=Image.new('RGBA',(320,512));canvas.alpha_composite(crop,((320-crop.width)//2,500-crop.height))
        path=target/f'{key}-{frame}.png';canvas.save(path,optimize=True)
        records.append({'file':str(path.relative_to(repo)),'source':str(npc_source.relative_to(repo)),'sourceCrop':list(box),'transformation':'neutral suit recolor, no face, common scale .70','frame':frame,'pivot':[.5,500/512],'size':[320,512],'approval':'fictional-new-art-review-pending','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(target/'frames.json').write_text(json.dumps({'frameDurationsMs':[1200,1400,1300,1400,2200,None],'stages':['entry','receive','raise','open','spray','final'],'assets':records},indent=2))
(target/'drop.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="12" height="18" viewBox="0 0 12 18"><path fill="#fbf5d5" d="M6 0 11 10 11 15 8 18 3 17 0 13 2 8Z"/><path fill="#fff" d="M5 6 7 9 7 13 4 12Z"/></svg>')
print('Prepared',len(records),'full-body frames; human likeness approval pending')
