"""Actual G-code layer plots, not deformation/FEA images."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import json
O=Path(__file__).resolve().parents[2]/'desempenho';folder=O/'05_Orca/Resultado_SUPERIOR_K1MAX';p=folder/'plate_1.gcode'
zs=[]
with p.open(encoding='utf-8') as f:
 for line in f:
  if line.startswith(';Z:'):zs.append(float(line[3:]))
targets=sorted(set(min(zs,key=lambda z:abs(z-t)) for t in [12,25,45]))
segments={z:{'wall':[],'infill':[],'skin':[]} for z in targets};cur=None;role='Custom';x=y=None
with p.open(encoding='utf-8') as f:
 for line in f:
  if line.startswith(';Z:'):
   z=float(line[3:]);cur=z if z in segments else None;x=y=None;continue
  if cur is None:continue
  if line.startswith((';TYPE:','; FEATURE:')):role=line.split(':',1)[1].strip();continue
  if not line.startswith(('G0 ','G1 ')):continue
  vals={t[0]:float(t[1:]) for t in line.split(';',1)[0].split()[1:] if t[0] in 'XYE'}
  xx=vals.get('X',x);yy=vals.get('Y',y)
  if vals.get('E',0)>0 and x is not None and y is not None and xx is not None and yy is not None and ('X' in vals or 'Y' in vals):
   rr=role.lower()
   if 'support' not in rr and rr not in ['brim','skirt','custom']:
    cat='wall' if 'wall' in rr else ('infill' if 'sparse' in rr else 'skin')
    segments[cur][cat].append([(x,y),(xx,yy)])
  x,y=xx,yy
fig,axes=plt.subplots(1,len(targets),figsize=(14,5),layout='constrained')
for ax,z in zip(axes,targets):
 for cat,col,lw in [('skin','#b9c4cc',.35),('infill','#009b9b',.4),('wall','#1a2736',.6)]:
  if segments[z][cat]:ax.add_collection(LineCollection(segments[z][cat],colors=col,linewidths=lw))
 ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Camada Z = {z:.2f} mm');ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.grid(alpha=.15)
fig.suptitle('Trajetórias reais do Orca - reforços internos, exterior original\nSuportes omitidos nesta vista. Não é resultado de deformação.',fontsize=13)
dest=O/'06_Engenharia/CAMADAS_REAIS_INTERNO.png';fig.savefig(dest,dpi=160,bbox_inches='tight',pad_inches=.2);plt.close(fig)
(O/'06_Engenharia/CAMADAS_REAIS_INTERNO.json').write_text(json.dumps({'source':str(p),'layers_mm':targets,'counts':{str(z):{k:len(v) for k,v in cats.items()} for z,cats in segments.items()},'actual_slicer_toolpaths':True,'deformation_or_impact_simulation':False},indent=2),encoding='utf-8')
print(json.dumps({'figure':str(dest),'layers':targets,'actual_toolpaths':True}))
