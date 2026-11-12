from pathlib import Path
import numpy as np,json,math
from r04_mesh_package import read,write
from r04_orca_project import build,O
summary=[]
for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
 v=read(O/f'03_STL_Garra/GARRA_{key}_BASE20.stl');points=np.unique(v.reshape(-1,3),axis=0)
 i=np.arange(128);zz=1-2*(i+.5)/128;aa=i*math.pi*(3-math.sqrt(5));dirs=np.column_stack([np.sqrt(1-zz*zz)*np.cos(aa),np.sqrt(1-zz*zz)*np.sin(aa),zz]);idx=[]
 for start in range(0,len(dirs),16):idx.extend(np.argmax(points@dirs[start:start+16].T,axis=0))
 hull=points[np.unique(idx)];candidates=[]
 for tilt in np.arange(0,80.1,2.5):
  if candidates and tilt>min(x[0] for x in candidates)+5:break
  tt=np.deg2rad(tilt)
  for az in np.arange(0,360,15):
   a=np.array([np.cos(np.deg2rad(az)),np.sin(np.deg2rad(az)),0.]);K=np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]]);R0=np.eye(3)+np.sin(tt)*K+(1-np.cos(tt))*(K@K)
   for spin in np.arange(0,180,5):
    z=np.deg2rad(spin);Rz=np.array([[np.cos(z),-np.sin(z),0],[np.sin(z),np.cos(z),0],[0,0,1]]);R=Rz@R0;dims=np.ptp(hull@R.T,axis=0)
    if np.all(dims<=[244,244,244]):candidates.append((float(tilt),float(dims[2]),float(az),float(spin),R))
 chosen=None
 for tilt,_,az,spin,R in sorted(candidates,key=lambda x:(x[0],x[1],x[2],x[3])):
  rot=points@R.T;lo=rot.min(axis=0);hi=rot.max(axis=0);dims=hi-lo
  if np.all(dims<=[244,244,244]):chosen=(tilt,az,spin,R,lo,hi,dims);break
 assert chosen is not None,('No X1 fit without scale',key)
 tilt,az,spin,R,lo,hi,dims=chosen;shift=np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]]);assert abs(np.linalg.det(R)-1)<1e-12
 dst=O/f'03_STL_Garra/REFERENCIA_X1/GARRA_{key}_ORIENTADA_SEM_ESCALA.stl';write(dst,v@R.T-shift,'SAMI R04 | rigid rotation for X1 REFERENCE ONLY | mm');parts=[{'name':f'GARRA_{key}_BASE20_X1_REF','file':dst}]
 for col,pct in [('AMARELO',30),('AZUL',50),('ROSA',70)]:
  src=O/f'04_Modificadores/{key}/MOD_{col}_{pct}.stl';dst=O/f'04_Modificadores/REFERENCIA_X1/{key}/MOD_{col}_{pct}.stl';write(dst,read(src)@R.T-shift);parts.append({'file':dst,'name':f'MOD_{col}_{pct}_NAO_IMPRIMIVEL','modifier':True,'percent':pct})
 project=O/f'05_Orca/GARRA_{key}_TPMSD_REF_X1_ORIENTADA.3mf';build(project,[{'name':f'GARRA_{key}_REF_X1_ESCALA1','parts':parts}],False)
 rec={'part':key,'printer_reference':'Bambu X1, not confirmed user production printer','tilt_deg':tilt,'tilt_axis_azimuth_deg':az,'Z_spin_deg':spin,'rotation_matrix':R.tolist(),'translation_after_rotation_mm':(-shift).tolist(),'actual_dimensions_after_rotation_mm':dims.tolist(),'scale':1.,'full_vertex_fit_verified':True,'limit_mm':[244,244,244],'not_print_or_mechanical_validation':True,'layer_direction_changed_relative_to_source':True,'project':str(project)};summary.append(rec)
 print(json.dumps({k:rec[k] for k in ['part','tilt_deg','actual_dimensions_after_rotation_mm','scale']},ensure_ascii=True),flush=True)
(O/'05_Orca/orientacoes_X1_REFERENCIA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
