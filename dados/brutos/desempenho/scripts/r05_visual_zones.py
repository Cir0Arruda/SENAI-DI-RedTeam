"""Actual native Orca paths, coloured by spatial infill modifier membership."""
from pathlib import Path
import json,numpy as np,matplotlib,sys,zipfile,xml.etree.ElementTree as ET
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from r04_mesh_package import read
O=Path(__file__).resolve().parents[2]/'desempenho';D=O/'06_Engenharia/R05_CONFERENCIA_ORCA';D.mkdir(exist_ok=True)
key=sys.argv[1];folder=O/f'05_Orca/Resultado_{key}_K1MAX';p=folder/'plate_1.gcode';zs=[]
with p.open(encoding='utf-8') as f:
 for line in f:
  if line.startswith(';Z:'):zs.append(float(line[3:]))
request=[12,25,45] if key=='SUPERIOR' else ([10,45,69] if key!='PAD' else [5,12,20])
targets=sorted(set(min(zs,key=lambda z:abs(z-t)) for t in request));segs={z:{'wall':[],'infill':[],'skin':[]} for z in targets};cur=None;role='Custom';x=y=None
with p.open(encoding='utf-8') as f:
 for line in f:
  if line.startswith(';Z:'):
   zz=float(line[3:]);cur=zz if zz in segs else None;x=y=None;continue
  if cur is None:continue
  if line.startswith((';TYPE:','; FEATURE:')):role=line.split(':',1)[1].strip();continue
  if not line.startswith(('G0 ','G1 ')):continue
  vals={t[0]:float(t[1:]) for t in line.split(';',1)[0].split()[1:] if t[0] in 'XYE'};xx=vals.get('X',x);yy=vals.get('Y',y)
  if vals.get('E',0)>0 and x is not None and y is not None and xx is not None and yy is not None and ('X' in vals or 'Y' in vals):
   rr=role.lower()
   if 'support' not in rr and rr not in ['brim','skirt','custom']:
    cat='wall' if 'wall' in rr else ('infill' if 'sparse' in rr else 'skin');segs[cur][cat].append([(x,y),(xx,yy)])
  x,y=xx,yy
def plane_segments(v,z):
 # A tiny plane perturbation avoids vertices exactly on the plane.
 z+=1e-7;pieces=[]
 for i,j in [(0,1),(1,2),(2,0)]:
  a=v[:,i];b=v[:,j];mask=(a[:,2]>z)!=(b[:,2]>z);aa=a[mask];bb=b[mask]
  points=aa[:,:2]+(bb[:,:2]-aa[:,:2])*((z-aa[:,2])/(bb[:,2]-aa[:,2]))[:,None]
  ids=np.flatnonzero(mask);pieces.extend(zip(ids,points))
 by={}
 for ident,pt in pieces:by.setdefault(int(ident),[]).append(pt)
 return np.array([points for points in by.values() if len(points)==2],float)
def inside(points,edges):
 result=np.zeros(len(points),bool)
 if not len(edges):return result
 a=edges[:,0];b=edges[:,1];dy=b[:,1]-a[:,1];good=np.abs(dy)>1e-12;a=a[good];b=b[good];dy=dy[good]
 for off in range(0,len(points),2048):
  pp=points[off:off+2048];xx=pp[:,0,None];yy=pp[:,1,None]
  cross=((a[None,:,1]>yy)!=(b[None,:,1]>yy))&(xx<(a[None,:,0]+(yy-a[None,:,1])*(b-a)[None,:,0]/dy[None,:]))
  result[off:off+len(pp)]=(cross.sum(axis=1)%2)==1
 return result
mods={}
if key!='PAD':
 for colour,pct in [('AMARELO',30),('AZUL',50),('ROSA',70)]:mods[pct]=read(O/f'04_Modificadores/{key}/MOD_{colour}_{pct}.stl')+np.array([150.,150.,0.])
colours={20:'#8a949f',30:'#b49700',50:'#0076c7',70:'#d51fb2',40:'#e47922'};records=[]
fig,axes=plt.subplots(1,len(targets),figsize=(16,6))
fig.subplots_adjust(left=.045,right=.99,bottom=.17,top=.83,wspace=.17)
for ax,z in zip(axes,targets):
 cats=segs[z]
 for cat,col,lw in [('skin','#d7dde2',.3),('wall','#16293c',.6)]:
  if cats[cat]:ax.add_collection(LineCollection(cats[cat],colors=col,linewidths=lw))
 arr=np.asarray(cats['infill']);counts={}
 if len(arr):
  mid=arr.mean(axis=1);density=np.full(len(mid),40 if key=='PAD' else 20)
  for pct,v in mods.items():density[inside(mid,plane_segments(v,z))]=pct
  for pct in sorted(set(density)):
   chosen=arr[density==pct];ax.add_collection(LineCollection(chosen,colors=colours[int(pct)],linewidths=.65));counts[int(pct)]=len(chosen)
 ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Z = {z:.2f} mm',fontsize=12);ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.grid(alpha=.12)
 records.append({'layer_Z_mm':z,'sparse_extrusion_segments_by_mask_percent':counts,'walls':len(cats['wall']),'solid_skin_segments':len(cats['skin'])})
legend=[Line2D([0],[0],color=colours[pct],lw=3,label=('PAD gyroid 40%' if pct==40 else f'TPMS-D {pct}%')) for pct in ([40] if key=='PAD' else [20,30,50,70])];legend += [Line2D([0],[0],color='#16293c',lw=2,label='Paredes'),Line2D([0],[0],color='#d7dde2',lw=2,label='Pele/miolo sólido')]
fig.legend(handles=legend,loc='lower center',ncol=len(legend),fontsize=10,bbox_to_anchor=(.5,.03));fig.suptitle(f'{key} | preenchimentos internos no fatiamento real do Orca\nCor indica região de configuração; não é mapa de tensão ou deformação.',fontsize=14)
out=D/f'{key}_PREENCHIMENTOS_INTERNOS.png';fig.savefig(out,dpi=180,bbox_inches='tight',pad_inches=.2);plt.close(fig)
(D/f'{key}_PREENCHIMENTOS_INTERNOS.json').write_text(json.dumps({'source_gcode':str(p),'method':'Native Gcode sparse-infill segments coloured by midpoint containment in exact STL modifier plane sections; walls and solid infill separately displayed. Density values are settings, not measured porosity. Supports omitted.','actual_native_toolpaths':True,'records':records,'not_FEA':True},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'case':key,'image':str(out),'layers':records},ensure_ascii=True),flush=True)
