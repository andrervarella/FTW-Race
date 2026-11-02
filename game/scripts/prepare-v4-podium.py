"""Normalize explicitly requested sprite crops; references and generated source stay untouched."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json

repo=Path(__file__).resolve().parents[2]
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

colors={'npc-blue':'#29b6ff','npc-yellow':'#ffcf32','npc-purple':'#ad75f8','npc-silver':'#d2e0eb'}
# Fictional helmeted competitors: each frame is a complete drawing, with separate pose geometry.
# Low-resolution pixel artwork is authored here, not cut/rotated from a real person.
for key,color in colors.items():
    for frame in range(6):
        px=Image.new('RGBA',(128,256)); d=ImageDraw.Draw(px)
        dark='#101b2b';light='#dae8ef';ink='#080f19';gold='#f6ca49'
        def poly(points,fill,outline=ink):d.polygon(points,fill=fill,outline=outline,width=2)
        # Legs and shoes with entrance-step variant.
        poly([(48,159),(64,164),(61,230),(44,230)],color)
        poly([(64,164),(80,159),(87,230 if frame else 220),(69,230 if frame else 220)],color)
        d.rectangle((40,229,61,240),fill=ink);d.rectangle((68,229 if frame else 219,94,240 if frame else 230),fill=ink)
        poly([(42,91),(84,91),(90,145),(80,172),(48,172),(39,145)],color)
        d.rectangle((48,99,80,110),fill=light);d.rectangle((48,115,80,141),fill=dark)
        d.line((46,155,81,155),fill=light,width=5)
        # Full arm contours are independently drawn for each storyboard pose.
        arms=[([(43,94),(32,116),(25,100),(19,105),(28,132),(43,121)],[(84,94),(96,126),(89,150),(81,143),(85,123)]),
              ([(43,94),(28,121),(51,141),(58,132),(42,119),(49,104)],[(84,94),(100,121),(77,141),(69,132),(86,119),(78,103)]),
              ([(43,97),(27,73),(38,36),(47,40),(42,71),(55,91)],[(83,97),(102,73),(90,36),(81,40),(86,71),(72,91)]),
              ([(43,94),(28,119),(61,133),(65,122),(43,111),(51,102)],[(84,94),(103,111),(86,130),(78,121),(88,108)]),
              ([(43,95),(26,111),(41,134),(49,127),(39,113),(52,103)],[(84,95),(103,122),(68,143),(63,132),(87,118),(77,104)]),
              ([(43,97),(27,74),(33,46),(43,48),(40,74),(55,91)],[(83,97),(102,75),(96,48),(86,50),(89,75),(73,91)])]
        for arm in arms[frame]:poly(arm,color)
        # Closed fictional helmet: no invented human face.
        d.rounded_rectangle((44,49,84,93),radius=13,fill=color,outline=ink,width=3)
        poly([(45,63),(83,63),(80,78),(48,78)],dark)
        d.line((51,66,76,66),fill='#87c7d7',width=3)
        d.rectangle((51,83,77,89),fill=light)
        # Trophy and bottle are integral hand-held pose art; independent spray is layered by DOM.
        if frame in [1,2,5]:
            tx,ty= (53,112) if frame==1 else (51,13) if frame==2 else (20,23)
            poly([(tx,ty),(tx+25,ty),(tx+21,ty+21),(tx+14,ty+25),(tx+5,ty+21)],gold)
            d.rectangle((tx+10,ty+23,tx+15,ty+32),fill=gold);d.rectangle((tx+4,ty+32,tx+22,ty+36),fill='#967334')
            d.arc((tx-6,ty+2,tx+8,ty+20),70,270,fill=gold,width=3);d.arc((tx+18,ty+2,tx+33,ty+20),270,90,fill=gold,width=3)
        if frame in [3,4,5]:
            bx,by=(72,111) if frame==3 else (47,125) if frame==4 else (87,28)
            d.rectangle((bx,by,bx+10,by+27),fill='#184b38',outline=ink,width=2)
            d.rectangle((bx+3,by-10,bx+7,by),fill='#2d7b44');d.rectangle((bx+2,by+8,bx+8,by+17),fill='#e2cc7c')
        out=px.resize((256,512),Image.Resampling.NEAREST);path=target/f'{key}-{frame}.png';out.save(path,optimize=True)
        records.append({'file':str(path.relative_to(repo)),'source':'game/scripts/prepare-v4-podium.py (original authored pixel drawing)','frame':frame,'pivot':[.5,240/256],'size':[256,512],'approval':'fictional-new-art-review-pending','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(target/'frames.json').write_text(json.dumps({'frameDurationsMs':[1200,1400,1300,1400,2200,None],'stages':['entry','receive','raise','open','spray','final'],'assets':records},indent=2))
(target/'drop.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="12" height="18" viewBox="0 0 12 18"><path fill="#fbf5d5" d="M6 0 11 10 11 15 8 18 3 17 0 13 2 8Z"/><path fill="#fff" d="M5 6 7 9 7 13 4 12Z"/></svg>')
print('Prepared',len(records),'full-body frames; human likeness approval pending')
