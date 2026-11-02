import base64,hashlib,json,os,urllib.request
from pathlib import Path
REPOSITORY='andrervarella/FTW-Race'
ROOT=Path(__file__).resolve().parent
EXPECTED={'3c1ec92c1856ace5f897be912b56caa917d6e22b': {'path': 'assets/previews/v4/approved-pilots/daniel-face-v2.png', 'size': 1892158, 'dimensions': [1312, 1199]}, '60f56bdfe439e3073435802afd3de7b6c3eaf11c': {'path': 'assets/previews/v4/approved-pilots/daniel-full-sprites-corrected.png', 'size': 1781173, 'dimensions': [1254, 1254]}, '839a979a2bf687b9481a2a4a69ded737d32d30a0': {'path': 'assets/previews/v4/approved-pilots/felipe-face-cap.png', 'size': 1870192, 'dimensions': [1182, 1331]}, 'b152bb9540e37b7bcea8a618ebc5f1b523373f6a': {'path': 'assets/previews/v4/approved-pilots/felipe-face-v2.png', 'size': 2026378, 'dimensions': [1182, 1331]}, '0591fc8b0a5253bb8ab5be3a7a078f4f7668886e': {'path': 'assets/previews/v4/approved-pilots/felipe-full-sprites-corrected.png', 'size': 2081536, 'dimensions': [1254, 1254]}, '8c1192d9818dc8f6f7ff7f70ec4cc654921ed677': {'path': 'game/assets/v4/drivers/daniel-portrait.webp', 'size': 585996, 'dimensions': [900, 822]}, '8d117a536396297952871b4d33900bbce6029c6b': {'path': 'game/assets/v4/drivers/felipe-portrait.webp', 'size': 620716, 'dimensions': [799, 900]}, 'e72f8b43fc54e3bdc9fd4b22e5aa547cdfe020c6': {'path': 'game/assets/v4/title/background.png', 'size': 2821411, 'dimensions': [1672, 941]}, '44ecaba6364d676b31a18a310745fce3c98a7ea5': {'path': 'game/assets/v4/title/background.webp', 'size': 492732, 'dimensions': [1600, 900]}, 'e2a513659cbb92831f967d72a27180fd41b1ca0c': {'path': 'game/assets/v4/title/daniel-front-sheet.webp', 'size': 802736, 'dimensions': [1600, 533]}, 'a5efb5a29ae1e15e50de38a59c3dc41dec584adc': {'path': 'game/assets/v4/title/felipe-front-sheet.webp', 'size': 752916, 'dimensions': [1600, 533]}}

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
