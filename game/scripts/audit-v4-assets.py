"""Generate/verify the complete V4 SHA256 inventory without modifying any artwork."""
from pathlib import Path
import hashlib, json, sys
from PIL import Image

root=Path(__file__).resolve().parents[2]
manifest=root/'assets/sprites/V4_MANIFEST.json'
def record(path, status):
    data={'path':str(path.relative_to(root)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes':path.stat().st_size, 'status':status}
    if path.suffix.lower() in ['.png','.jpg','.jpeg']:
        with Image.open(path) as im:
            data['size']=list(im.size)
            if im.mode=='RGBA': data['alphaExtrema']=list(im.getchannel('A').getextrema())
    return data

if '--write' in sys.argv:
    rows=[]
    for folder in ['referencias','assets/previews']:
        for p in sorted((root/folder).rglob('*')):
            if p.suffix.lower() not in ['.png','.jpg','.jpeg']:continue
            status='rejected-not-distributed' if '/arquivo/' in str(p) else 'official-user-reference' if folder=='referencias' else 'preliminary-human-review-pending'
            rows.append(record(p,status))
    for folder in ['game/assets','game/cars']:
        for p in sorted((root/folder).rglob('*')):
            if p.is_file():rows.append(record(p,'original-logo-or-legacy-engine' if '/legacy/' in str(p) else 'derived-or-new-art-human-review-pending'))
    manifest.write_text(json.dumps({'version':'4-preview','approval':'not-final-human-art-review-required','details':['game/assets/v4/render-assets.json','game/assets/v4/cars/npc-cars.json','game/assets/v4/podium/frames.json'],'assets':rows},indent=2)+'\n')
else:
    data=json.loads(manifest.read_text())
    for row in data['assets']:
        p=root/row['path'];assert p.is_file(),row['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
    for key in ['daniel','felipe','npc-blue','npc-yellow','npc-purple','npc-silver']:
        hashes=[]
        for i in range(6):
            p=root/f'game/assets/v4/podium/{key}-{i}.png'
            im=Image.open(p);assert im.size==((320,512) if key.startswith('npc-') else (256,512))
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
            hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
        assert len(set(hashes))==6,key
    print(f"PASS: {len(data['assets'])} assets SHA256; 36 distinct full-body frames, dimensions and real alpha.")
