"""Generate/verify the complete V4 SHA256 inventory without modifying any artwork."""
from pathlib import Path
import hashlib, json, sys
from PIL import Image

root=Path(__file__).resolve().parents[2]
manifest=root/'assets/sprites/V4_MANIFEST.json'
def record(path, status):
    data={'path':str(path.relative_to(root)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes':path.stat().st_size, 'status':status}
    if path.suffix.lower() in ['.png','.jpg','.jpeg','.webp']:
        with Image.open(path) as im:
            data['size']=list(im.size)
            if im.mode=='RGBA': data['alphaExtrema']=list(im.getchannel('A').getextrema())
    return data

if '--write' in sys.argv:
    rows=[]
    for folder in ['referencias','assets/previews']:
        for p in sorted((root/folder).rglob('*')):
            if p.suffix.lower() not in ['.png','.jpg','.jpeg','.webp']:continue
            status='rejected-not-distributed' if '/arquivo/' in str(p) else 'official-user-reference' if folder=='referencias' else 'preliminary-human-review-pending'
            if '/approved-pilots/' in str(p): status='owner-approved-source'
            rows.append(record(p,status))
    for folder in ['assets/sprites/v4/truck-driver', 'assets/sprites/v4/truck-vehicle']:
        for p in sorted((root/folder).rglob('*')):
            if p.is_file():
                status = 'owner-approved-master' if p.name == 'approved-master.png' else 'prepared-source-owner-requested-integration'
                rows.append(record(p, status))
    for folder in ['game/assets','game/cars']:
        for p in sorted((root/folder).rglob('*')):
            if p.is_file():
                accepted = p.name.startswith('marquinhos') or p.name.startswith('felipe-front-portrait.')
                approved = '/drivers/' in str(p) or '/title/' in str(p) or ('/podium/' in str(p) and p.name.startswith(('daniel-','felipe-')))
                status = ('owner-requested-integration' if accepted else 'owner-approved-derived' if approved else
                          'original-logo-or-legacy-engine' if '/legacy/' in str(p) else 'derived-or-new-art-human-review-pending')
                rows.append(record(p,status))
    manifest.write_text(json.dumps({'version':'4-preview','approval':'Daniel/Felipe original art and cover previously approved; prepared Marquinhos and Felipe title retouch accepted by latest owner integration request; other-new-art-review-pending','details':['game/assets/v4/render-assets.json','game/assets/v4/cars/npc-cars.json','game/assets/v4/cars/marquinhos.json','game/assets/v4/podium/frames.json','game/assets/v4/drivers/approved-pilots.json','game/assets/v4/drivers/marquinhos.json','game/assets/v4/title/approval.json'],'assets':rows},indent=2)+'\n')
else:
    data=json.loads(manifest.read_text())
    for row in data['assets']:
        p=root/row['path'];assert p.is_file(),row['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
    for key in ['daniel','felipe','marquinhos','npc-blue','npc-yellow','npc-purple','npc-silver']:
        hashes=[]
        for i in range(6):
            p=root/f'game/assets/v4/podium/{key}-{i}.png'
            im=Image.open(p);assert im.size==((320,512) if key.startswith('npc-') else (256,512))
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
            hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
        assert len(set(hashes))==6,key
    # Source copies and row-major atlas mapping are independent of file names and
    # image encoders. Compare actual RGBA pixels; no flipped/mirrored substitute.
    for category in ['drivers', 'cars']:
        meta=json.loads((root/f'game/assets/v4/{category}/marquinhos.json').read_text())
        source=root/meta['sourceMetadata']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['sourceMetadataSha256'],str(source)
        assert meta['integrationAcceptance']['status']=='owner-requested-integration'
        for row in meta['assets']:
            original,target=root/row['source'],root/row['file']
            digest=hashlib.sha256(original.read_bytes()).hexdigest()
            assert digest==row['sourceSha256']==row['sha256']==hashlib.sha256(target.read_bytes()).hexdigest(),row['file']
    vehicle=json.loads((root/'game/assets/v4/cars/marquinhos.json').read_text())
    assert vehicle['sheetGrid']==[3,2] and vehicle['frameSize']==[560,512]
    atlas=Image.open(root/'game/assets/v4/cars/marquinhos.png').convert('RGBA')
    assert atlas.size==(1680,1024)
    for i,state in enumerate(vehicle['frameOrder']):
        frame=Image.open(root/f'game/assets/v4/cars/marquinhos-{state}.png').convert('RGBA')
        assert frame.size==(560,512) and frame.getchannel('A').getextrema()==(0,255)
        x,y=(i%3)*560,(i//3)*512
        assert atlas.crop((x,y,x+560,y+512)).tobytes()==frame.tobytes(),state
    # Native rear useful widths327/401, both divided by a512px frame height:
    # the uniform display multiplier produces1.40x useful Mercedes width.
    assert abs((327/401)*vehicle['renderScale']-1.4)<1e-12
    assert hashlib.sha256((root/'game/assets/v4/title/felipe-front-portrait.png').read_bytes()).hexdigest()=='98832d1d00feb8f628d76172ad2ace8dcacf75a4a6ea2e7c8af88faf4f7a236b'
    print(f"PASS: {len(data['assets'])} assets SHA256; 42 distinct full-body frames with real alpha; 19 byte-identical Marquinhos runtime images; six row-major truck atlas frames; 1.40x useful width and uniform scale; Felipe title retouch.")
