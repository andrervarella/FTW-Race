import base64,hashlib,json,os,urllib.request
from pathlib import Path
REPOSITORY='andrervarella/FTW-Race'
EXPECTED='2ec845c8f02415c8a9616f92be1f14012504bf57'
ROOT=Path(__file__).resolve().parent

def assemble(entry):
    assert entry['sha']==EXPECTED and entry['path']=='assets/previews/v4/npc-cars-views-generated.png'
    pieces=[]
    for index,part in enumerate(entry['parts']):
        path=(ROOT/part['path']).resolve();assert path.is_relative_to(ROOT)
        data=json.loads(path.read_text());assert data['sourceGitBlob']==EXPECTED and data['part']==index and data['dimensions']==[1254,1254]
        pieces.append(data['base64'])
    encoded=''.join(pieces);raw=base64.b64decode(encoded,validate=True)
    assert len(raw)==entry['size'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==EXPECTED
    return encoded

def main():
    assert os.environ['GITHUB_REPOSITORY']==REPOSITORY
    manifest=json.loads((ROOT/'manifest.json').read_text());assert manifest['repository']==REPOSITORY
    entries=manifest['blobs'];assert len(entries)==1
    encoded=assemble(entries[0]);token=os.environ['GITHUB_TOKEN']
    request=urllib.request.Request('https://api.github.com/repos/'+REPOSITORY+'/git/blobs',data=json.dumps({'content':encoded,'encoding':'base64'}).encode(),headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},method='POST')
    with urllib.request.urlopen(request,timeout=90)as response:actual=json.load(response)['sha']
    report={'repository':REPOSITORY,'run_id':os.environ['GITHUB_RUN_ID'],'expected':EXPECTED,'actual':actual,'dimensions':[1254,1254]}
    (ROOT/'result.json').write_text(json.dumps(report,indent=2)+'\n');assert actual==EXPECTED
    print('Verified authorized NPC sprite PNG: '+actual)
if __name__=='__main__':main()
