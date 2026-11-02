"""Reproducible, non-destructive extraction of supplied FTW V4 reference boards.
Needs Pillow; no external service/network. New art remains pending human review.
"""
from pathlib import Path
from PIL import Image
import hashlib, json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'game/assets/v4'
records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(im):
    im=im.convert('RGBA'); im.putalpha(im.getchannel('A').point(lambda a: 0 if a<40 else 255 if a>240 else a)); return im

def record(target,source,rect,pivot=(.5,1),frames=None):
    im=Image.open(target).convert('RGBA'); a=im.getchannel('A'); hist=a.histogram()
    records.append(dict(path=str(target.relative_to(ROOT/'game')),source=str(source.relative_to(ROOT)),sourceSha256=sha(source),sha256=sha(target),crop=rect,size=list(im.size),pivot=pivot,alphaRange=a.getextrema(),transparentPixels=hist[0],opaquePixels=hist[255],frames=frames,status='derived-preview-human-review-pending',license='user-supplied-project-reference'))

def extract(source,name,rect,maxsize):
    src=ROOT/source; im=clean(Image.open(src).crop(rect)); bbox=im.getbbox(); im=im.crop(bbox); im.thumbnail(maxsize,Image.Resampling.LANCZOS); im=clean(im)
    dst=OUT/name; dst.parent.mkdir(parents=True,exist_ok=True); im.save(dst); record(dst,src,rect)

extract('assets/previews/cascavel/reta-principal.png','cascavel/title-straight.png',(0,0,1672,941),(1280,720))
extract('assets/previews/cascavel/curvas-e-mata.png','cascavel/horizon.png',(0,0,1672,190),(1672,190))
veg='assets/previews/cascavel/vegetacao-e-barreiras.png'; boxes='assets/previews/cascavel/boxes-e-sinalizacao.png'
for n,r,s in [('tree',(0,0,450,420),(320,320)),('bush',(1190,230,1672,420),(380,160)),('forest',(0,420,1100,575),(700,150)),('fence',(480,580,930,760),(360,160)),('tires',(950,620,1280,760),(320,140)),('barrier',(1290,600,1672,760),(320,140))]:extract(veg,'cascavel/'+n+'.png',r,s)
for n,r,s in [('pit',(0,0,1671,393),(1100,300)),('stand',(20,397,630,640),(620,280)),('tent',(650,395,1150,650),(500,240)),('board100',(1130,760,1305,920),(170,170)),('board50',(1335,785,1500,925),(170,170))]:extract(boxes,'cascavel/'+n+'.png',r,s)
# Distinct actual views from the original sheets; no mirrored logos/numbers.
for key in ['daniel','felipe']:
    src=ROOT/f'assets/previews/{key}/carro-traseira.png'; source=Image.open(src)
    for view,rect in [('left',(0,0,790,724)),('rear',(795,0,1378,724)),('right',(1380,0,2172,724))]:
        im=clean(source.crop(rect)); im=im.crop(im.getbbox()); im.thumbnail((470,330),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(512,512)); canvas.alpha_composite(im,((512-im.width)//2,470-im.height)); dst=OUT/f'cars/{key}-{view}.png'; canvas.save(dst); record(dst,src,rect,pivot=(.5,470/512))
src=ROOT/'assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png'; board=Image.open(src)
atlas=Image.new('RGBA',(512,512)); families=['smoke','dust','nitro','spark']; frames=[]
for row,family in enumerate(families):
    for col in range(4):
        rect=(col*384,row*256,(col+1)*384,(row+1)*256); im=clean(board.crop(rect)); im=im.crop(im.getbbox()); im.thumbnail((120,100),Image.Resampling.LANCZOS); im=clean(im)
        atlas.alpha_composite(im,(col*128+(128-im.width)//2,row*128+110-im.height)); frames.append(dict(family=family,frame=col,index=row*4+col,rect=[col*128,row*128,128,128],durationMs=100,pivot=[.5,110/128]))
dst=OUT/'fx/effects.png'; atlas.save(dst); record(dst,src,None,pivot=(.5,110/128),frames=frames)
(OUT/'render-assets.json').write_text(json.dumps(dict(version=4,alphaCleanup='alpha<40 removed; >240 opaque, original references untouched',assets=records),indent=2)+'\n')
print(f'Prepared {len(records)} extracted assets with provenance and SHA256.')
# Original vector redraw matched to the supplied A45 rear silhouette; no brand marks.
# Separate body geometry, lamps, wheels, exhaust and spoiler are shared across NPCs.
colors={'blue':('#39b9ed','#15779b','#a8edff',31),'yellow':('#f8cc29','#a58314','#fff0a8',34),'purple':('#a57bea','#6141a3','#e2c8ff',38),'silver':('#bfcdd4','#697f8b','#f5ffff',41)}
for key,(paint,shade,light,number) in colors.items():
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<title>Rival {key} — same A45 rear chassis, original art pending review</title>
<defs><linearGradient id="paint" x2="0" y2="1"><stop stop-color="{light}"/><stop offset=".3" stop-color="{paint}"/><stop offset=".78" stop-color="{paint}"/><stop offset="1" stop-color="{shade}"/></linearGradient><linearGradient id="glass" x2="0" y2="1"><stop stop-color="#354650"/><stop offset=".7" stop-color="#10212b"/><stop offset="1" stop-color="#263e48"/></linearGradient></defs>
<ellipse cx="256" cy="471" rx="204" ry="14" fill="#05090a" opacity=".45"/>
<path d="M74 343Q50 363 57 445L66 466Q90 478 111 465L119 352ZM438 343Q462 363 455 445L446 466Q422 478 401 465L393 352Z" fill="#080c0d" stroke="#273034" stroke-width="6"/>
<path d="M84 358 78 452M96 360 91 459M428 358 434 452M416 360 421 459" stroke="#353a3c" stroke-width="4"/>
<path d="M91 299 108 238 131 165Q149 139 192 137H320Q363 139 381 165L404 238 421 299Q442 329 447 375L443 432Q435 455 408 459H104Q77 455 69 432L65 375Q70 329 91 299Z" fill="url(#paint)" stroke="#10171a" stroke-width="6"/>
<path d="M145 169Q156 152 190 151H322Q356 152 367 169L381 211H131Z" fill="{shade}" stroke="#102027" stroke-width="4"/>
<text x="256" y="194" text-anchor="middle" font-family="sans-serif" font-size="47" font-weight="900" fill="#fff8cb" stroke="#111a21" stroke-width="3" paint-order="stroke">{number}</text>
<path d="M119 242 133 217H379L393 242 385 304Q379 322 358 323H154Q133 322 127 304Z" fill="url(#glass)" stroke="#0b1419" stroke-width="8"/>
<path d="M145 238 362 304M368 238 157 304" stroke="#67818a" stroke-width="7" opacity=".3"/>
<path d="M173 239V309M339 239V309" stroke="#0a1217" stroke-width="11"/>
<path d="M113 220H399L409 208H103Z" fill="#080d11"/>
<path d="M110 212H402V235H110Z" fill="{paint}" stroke="#152328" stroke-width="5"/>
<path d="M164 237V321M348 237V321" stroke="#080d11" stroke-width="12"/>
<path d="M111 238 83 227 67 231 65 248 96 254ZM401 238 429 227 445 231 447 248 416 254Z" fill="{shade}" stroke="#141f26" stroke-width="5"/>
<path d="M105 326Q125 322 155 335L190 351 178 369Q145 383 117 366L96 347Z M407 326Q387 322 357 335L322 351 334 369Q367 383 395 366L416 347Z" fill="#661a25" stroke="#1c1e23" stroke-width="5"/>
<path d="M106 335 159 346 177 354 121 352Z M406 335 353 346 335 354 391 352Z" fill="#ff564b"/>
<path d="M114 350 148 359 171 357M398 350 364 359 341 357" fill="none" stroke="#f8e1cf" stroke-width="4"/>
<path d="M183 369H329L316 390H196Z" fill="#142027"/>
<rect x="214" y="371" width="84" height="18" rx="3" fill="#09131b"/>
<path d="M94 392 101 437Q110 446 135 445H377Q402 446 411 437L418 392 438 405 434 438Q427 452 408 456H104Q85 452 78 438L74 405Z" fill="{shade}"/>
<path d="M95 400 92 428 108 428 113 399Z M417 400 420 428 404 428 399 399Z" fill="#111b20" stroke="#2c383d" stroke-width="3"/>
<path d="M165 434H347L368 461H144Z" fill="#0d161b" stroke="#26353a" stroke-width="5"/>
<path d="M203 437V461M239 437V465M273 437V465M309 437V461" stroke="#424b50" stroke-width="7"/>
<ellipse cx="127" cy="441" rx="29" ry="15" fill="#b3c5ca" stroke="#152229" stroke-width="5"/><ellipse cx="127" cy="441" rx="22" ry="9" fill="#030608"/>
<ellipse cx="385" cy="441" rx="29" ry="15" fill="#b3c5ca" stroke="#152229" stroke-width="5"/><ellipse cx="385" cy="441" rx="22" ry="9" fill="#030608"/>
<rect x="368" y="399" width="13" height="24" rx="3" fill="#a31825" stroke="#171e24" stroke-width="4"/>
<path d="M200 325H312M111 393H401" stroke="{light}" stroke-width="3" opacity=".6"/>
</svg>'''
    dst=ROOT/f'game/cars/npc-{key}.svg'; dst.write_text(svg+'\n')
print('Prepared four original A45 silhouette redraws, pending human art review.')

(OUT/'cars/npc-cars.json').write_text(json.dumps(dict(status='new-original-vector-art-human-review-pending',source='assets/previews/daniel/carro-traseira.png',sourceSha256=sha(ROOT/'assets/previews/daniel/carro-traseira.png'),files=[dict(path=f'cars/npc-{key}.svg',sha256=sha(ROOT/f'game/cars/npc-{key}.svg'),size=[512,512],pivot=[.5,470/512]) for key in colors]),indent=2)+'\n')
