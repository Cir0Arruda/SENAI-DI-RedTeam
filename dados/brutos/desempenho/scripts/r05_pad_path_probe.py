from pathlib import Path
from collections import deque
p=Path(__file__).resolve().parents[2]/'desempenho/05_Orca/Resultado_PAD_K1MAX/plate_1.gcode';z=None;role='';x=y=None;n=0;ctx=deque(maxlen=5)
for i,line in enumerate(p.open(encoding='utf-8'),1):
 ctx.append(line.strip())
 if line.startswith(';Z:'):z=float(line[3:]);x=y=None
 if z!=12:continue
 if line.startswith(';TYPE:'):role=line[6:].strip()
 if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
 vals={t[0]:float(t[1:]) for t in line.split(';',1)[0].split()[1:] if t[0] in 'XYE'};xx=vals.get('X',x);yy=vals.get('Y',y)
 if vals.get('E',0)>0 and 'sparse' in role.lower() and None not in [x,y,xx,yy] and ((xx-x)**2+(yy-y)**2)**.5>8:
  print({'line':i,'from':[x,y],'to':[xx,yy],'role':role,'context':list(ctx)});n+=1
  if n==4:break
 x,y=xx,yy
