"""Encode approved art for mobile delivery; preserve every original PNG."""
from pathlib import Path
from PIL import Image
import hashlib,json
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'game/assets/v4'
rows=[]
for folder,name,maximum in [('drivers','daniel-portrait',900),('drivers','felipe-portrait',900),('title','daniel-front-sheet',1600),('title','felipe-front-sheet',1600),('title','background',1600)]:
    source=ASSETS/folder/(name+'.png');target=source.with_suffix('.webp')
    original=Image.open(source).convert('RGB' if name=='background' else 'RGBA')
    image=original.copy();image.thumbnail((maximum,1000 if name=='background' else maximum),Image.Resampling.LANCZOS)
    if name=='background':image.save(target,format='WEBP',quality=92,method=6)
    else:
        image.save(target,format='WEBP',lossless=True,exact=True,method=6)
        assert np.array_equal(np.array(image),np.array(Image.open(target).convert('RGBA')))
    rows.append({'file':str(target.relative_to(ROOT)),'source':str(source.relative_to(ROOT)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'originalSize':list(original.size),'size':list(image.size),'method':'WebP92 scenery; original PNG preserved' if name=='background' else 'aspect-preserving downsample and lossless WebP; encoded pixels verified exactly','bytes':target.stat().st_size,'approval':'owner-approved-design; technical delivery encoding'})
(ASSETS/'title/web-encodings.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Encoded5approved title layers:',sum(row['bytes']for row in rows),'bytes; logos remain original PNGs.')
