from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageOps

root=Path(__file__).resolve().parents[2]
meta=json.loads((root/'game/assets/v4/cars/npc-cars.json').read_text())
assert hashlib.sha256((root/meta['source']).read_bytes()).hexdigest()==meta['sourceSha256']
assert meta['frameSize']==[560,512] and meta['pivot']==[.5,470/512]
assert len(meta['files'])==4 and len(meta['frames'])==6
for row in meta['files']:
    path=root/'game'/row['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
    atlas=Image.open(path).convert('RGBA');assert atlas.size==(1680,1024)
    frames=[]
    for i,record in enumerate(row['frames']):
        file=root/'game'/record['path'];assert hashlib.sha256(file.read_bytes()).hexdigest()==record['sha256']
        im=Image.open(file).convert('RGBA');assert im.size==(560,512) and im.getchannel('A').getextrema()==(0,255)
        bbox=im.getbbox();assert bbox[0]>0 and bbox[1]>0 and bbox[2]<560 and bbox[3]==470
        frames.append(np.array(im))
        x=(i%3)*560;y=(i//3)*512
        assert np.array_equal(frames[-1],np.array(atlas.crop((x,y,x+560,y+512))))
    assert len({record['sha256']for record in row['frames']})==6
    for normal,brake in [(1,4),(2,5)]:
        assert np.array_equal(frames[normal][:,:,3],frames[brake][:,:,3])
        assert np.count_nonzero(frames[normal][:,:,:3]!=frames[brake][:,:,:3])>100
    assert not np.array_equal(frames[1],np.array(ImageOps.mirror(Image.fromarray(frames[2]))))
print('PASS: 4 raster atlases, 24 distinct views, real alpha, complete bounds, stable ground and no mirrored turn sprites.')
