"""Validate distributed sprite bytes, dimensions, alpha and separate animation frames."""
from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'assets/v4/render-assets.json').read_text())
for item in manifest['assets']:
 p=root/item['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
 im=Image.open(p).convert('RGBA'); assert list(im.size)==item['size'],p
 hist=im.getchannel('A').histogram()
 if p.name not in ['horizon.png','title-straight.png']:
  assert hist[0]>0 and hist[255]>0, f'No useful alpha {p}'
  assert hist[0]==item['transparentPixels'],p
 if p.name=='effects.png':
  assert len(item['frames'])==16
  for f in item['frames']:
   x,y,w,h=f['rect']; assert im.crop((x,y,x+w,y+h)).getbbox(),f
print(f"PASS: {len(manifest['assets'])} sprite files; SHA256, size, real alpha and 16 FX frames.")
