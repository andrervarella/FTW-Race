import base64,hashlib,json,os,urllib.request
from pathlib import Path
REPOSITORY='andrervarella/FTW-Race'
ROOT=Path(__file__).resolve().parent
EXPECTED={'2c7fdc70729253275b3d3694e545bb222a51ee48': {'path': 'game/assets/v4/title/felipe-front-portrait.png', 'size': 2007308, 'dimensions': [1182, 1331]}, '59260035ff5137c52a52b415de9c813632d4e758': {'path': 'game/assets/v4/title/felipe-front-portrait.webp', 'size': 672048, 'dimensions': [799, 900]}}

def assemble(entry):
    check=EXPECTED[entry['sha']]
    assert entry['path']==check['path'] and entry['size']==check['size'] and entry['dimensions']==check['dimensions']
    pieces=[]
    for index,part in enumerate(entry['parts']):
        path=(ROOT/part['path']).resolve();assert path.is_relative_to(ROOT)
        data=json.loads(path.read_text());assert data['sourceGitBlob']==entry['sha'] and data['part']==index and data['dimensions']==check['dimensions'] and data['totalParts']==len(entry['parts'])
        pieces.append(data['base64'])
    encoded=''.join(pieces);raw=base64.b64decode(encoded,validate=True)
    assert len(raw)==entry['size'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['sha']
    return encoded

def main():
    assert os.environ['GITHUB_REPOSITORY']==REPOSITORY
    manifest=json.loads((ROOT/'manifest.json').read_text());assert manifest['repository']==REPOSITORY
    entries=manifest['blobs'];assert set(e['sha']for e in entries)==set(EXPECTED) and len(entries)==len(EXPECTED)
    ready=[(e,assemble(e))for e in entries]
    token=os.environ['GITHUB_TOKEN'];report={'repository':REPOSITORY,'run_id':os.environ['GITHUB_RUN_ID'],'blobs':[]}
    for entry,encoded in ready:
        request=urllib.request.Request('https://api.github.com/repos/'+REPOSITORY+'/git/blobs',data=json.dumps({'content':encoded,'encoding':'base64'}).encode(),headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},method='POST')
        with urllib.request.urlopen(request,timeout=90)as response:actual=json.load(response)['sha']
        assert actual==entry['sha'];report['blobs'].append({'path':entry['path'],'expected':entry['sha'],'actual':actual});print('Verified approved image blob '+actual)
        (ROOT/'result.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
