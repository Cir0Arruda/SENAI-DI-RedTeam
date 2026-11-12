from pathlib import Path
import numpy as np,struct,json,zipfile
DT=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')])
def read(path):
 p=Path(path);raw=p.read_bytes();n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n;return np.frombuffer(raw,dtype=DT,offset=84)['v'].astype(float).copy()
def volume(v):return np.einsum('ij,ij->i',v[:,0],np.cross(v[:,1],v[:,2])).sum()/6

def clean(v,expected_cm3):
 vol=abs(volume(v));ratio=(expected_cm3*1000/vol)**(1/3);scale=min([.1,1,10,1000],key=lambda x:abs(x-ratio));assert abs(scale/ratio-1)<.01,(ratio,scale);v=v*scale
 _,ids=np.unique(np.round(v.reshape(-1,3),6),axis=0,return_inverse=True);ids=ids.reshape(-1,3);ns=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);area=np.linalg.norm(ns,axis=1);keep=(area>1e-12)&(ids[:,0]!=ids[:,1])&(ids[:,1]!=ids[:,2])&(ids[:,2]!=ids[:,0]);deg=int((~keep).sum());v=v[keep];ids=ids[keep];ns=ns[keep];area=area[keep]
 canon=np.sort(ids,axis=1);_,inv,cnt=np.unique(canon,axis=0,return_inverse=True,return_counts=True);remove=np.zeros(len(v),bool)
 for g in np.flatnonzero(cnt==2):
  ii=np.flatnonzero(inv==g)
  if np.dot(ns[ii[0]],ns[ii[1]])/(area[ii[0]]*area[ii[1]])<-.99999:remove[ii]=True
 v=v[~remove];ids=ids[~remove];edges=np.concatenate([ids[:,[0,1]],ids[:,[1,2]],ids[:,[2,0]]]);_,counts=np.unique(np.sort(edges,axis=1),axis=0,return_counts=True);bad=int((counts!=2).sum());assert bad==0,('nonmanifold_or_boundary_edges',bad)
 oriented=np.where(edges[:,0]<edges[:,1],1,-1);_,inverse=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True);balances=np.bincount(inverse,weights=oriented);assert (balances==0).all(),'winding mismatch'
 signed=volume(v);flipped=bool(signed<0)
 if flipped:v=v[:,[0,2,1],:]
 err=100*abs(abs(signed)-expected_cm3*1000)/(expected_cm3*1000);assert err<1,(err,expected_cm3)
 return v,{'unit':'mm','native_to_mm_scale':scale,'triangles':len(v),'volume_mm3':abs(signed),'CAD_volume_cm3':expected_cm3,'volume_error_percent':err,'bad_edges':bad,'winding_mismatches':0,'degenerate_removed':deg,'opposite_zero_volume_flap_triangles_removed':int(remove.sum()),'global_winding_flipped':flipped}

def write(path,v,label='SAMI R04 | mm | nominal envelope, not FE results'):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);a=np.zeros(len(v),dtype=DT);a['v']=v;normal=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);ln=np.linalg.norm(normal,axis=1);a['n']=normal/ln[:,None];path.write_bytes(label.encode('ascii')[:80].ljust(80,b' ')+struct.pack('<I',len(v))+a.tobytes())

def pads(O):
 rec=json.loads((O/'02_STL_PAD/exportacao_Fusion.json').read_text(encoding='utf-8'));out=[];placed=[]
 for i,r in enumerate(sorted(rec['rows'],key=lambda r:r['name'])):
  v,check=clean(read(r['stl_raw']),r['volume_cm3']);lo=v.min(axis=(0,1));hi=v.max(axis=(0,1));shift=np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]]);v-=shift;name=r['name']+'.stl';write(O/'02_STL_PAD'/name,v);check.update({'file':name,'dimensions_mm':(hi-lo).tolist(),'shift_from_world_mm':shift.tolist()});out.append(check)
  w=v.copy();w[:,:,0]+=42+(i%3)*82;w[:,:,1]+=42+(i//3)*82;placed.append(w)
 write(O/'02_STL_PAD/PADs_8_PARTES_MESA.stl',np.concatenate(placed),'SAMI R04 PADs | mm | 8 separate solids | layout only')
 with zipfile.ZipFile(O/'02_STL_PAD/PADs_STL_INDIVIDUAIS.zip','w',zipfile.ZIP_DEFLATED) as z:
  for x in out:z.write(O/'02_STL_PAD'/x['file'],x['file'])
 (O/'02_STL_PAD/validacao_STL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'PADs_verified':len(out),'max_volume_error_percent':max(x['volume_error_percent'] for x in out)}))

def part(O,key):
 rec=json.loads((O/f'04_Modificadores/{key}_regioes.json').read_text(encoding='utf-8'));base=next(x for x in rec['regions'] if x['label']=='BASE');v,check=clean(read(base['stl_raw']),rec['scope']['source_volume_cm3']);lo=v.min(axis=(0,1));hi=v.max(axis=(0,1));shift=np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]]);v-=shift;dst=O/f'03_STL_Garra/GARRA_{key}_BASE20.stl';write(dst,v);rows=[dict(check,file=str(dst.relative_to(O)),type='whole_part',dimensions_mm=(hi-lo).tolist(),shift_world_mm=shift.tolist())]
 for r in rec['regions']:
  if r['label']=='BASE':continue
  u,c=clean(read(r['stl_raw']),r['modifier_envelope_volume_cm3_not_printed_region_volume']);u-=shift;dst=O/f'04_Modificadores/{key}/MOD_{r["label"]}_{r["percent"]}.stl';write(dst,u);rows.append(dict(c,file=str(dst.relative_to(O)),type='nonprinting_modifier',infill_percent=r['percent']))
 (O/f'04_Modificadores/{key}_validacao_STL.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'part':key,'meshes_verified':len(rows),'actual_dimensions_mm':(hi-lo).tolist(),'max_volume_error_percent':max(x['volume_error_percent'] for x in rows)}))

if __name__=='__main__':
 import sys
 O=Path(__file__).resolve().parents[2]/'desempenho'
 if sys.argv[1]=='PAD':pads(O)
 else:part(O,sys.argv[1])

