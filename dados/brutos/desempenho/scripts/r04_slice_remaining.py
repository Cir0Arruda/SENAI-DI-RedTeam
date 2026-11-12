"""Native headless Orca calculation only; no printer transmission or Fusion UI."""
from pathlib import Path
import subprocess,json,datetime,concurrent.futures
O=Path(__file__).resolve().parents[2]/'desempenho'
def run(key):
 folder=O/f'05_Orca/Resultado_{key}_K1MAX';folder.mkdir(exist_ok=True)
 status=folder/'status.json';out=folder/f'{key}_K1MAX_FATIADO_REFERENCIA.3mf'
 assert not status.exists() and not out.exists(),f'{key}: existing run must be inspected, not duplicated'
 inp=O/'05_Orca'/('PADs_TPU95A40_K1MAX_ESCALA_REAL.3mf' if key=='PAD' else f'GARRA_{key}_TPMSD_K1MAX_ESCALA_REAL.3mf')
 q={'case':key,'status':'running','start_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':str(inp),'output':str(out),'scale':1,'orientation':'original source Z up','printer_reference':'Creality K1 Max300mm,0.4mm','slicing_not_FEA':True,'sent_to_printer':False,'external_modification_prohibited':True}
 status.write_text(json.dumps(q,indent=2),encoding='utf-8')
 args=['C:/Program Files/OrcaSlicer/orca-slicer.exe',str(inp),'--arrange','1','--slice','0','--mstpp','0','--outputdir',str(folder),'--export-3mf',out.name,'--export-settings','perfil_efetivo.json']
 try:
  with (folder/'Orca_fatiamento.log').open('wb') as f:
   p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,cwd=folder)
   q['native_pid']=p.pid;status.write_text(json.dumps(q,indent=2),encoding='utf-8')
   try:code=p.wait(timeout=7200)
   except subprocess.TimeoutExpired:
    p.terminate();p.wait(timeout=30);raise
  q.update(status='output_pending_verification' if code==0 and out.exists() else 'failed',returncode=code)
 except Exception as e:q.update(status='failed',error=str(e))
 q['end_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();status.write_text(json.dumps(q,indent=2),encoding='utf-8')
 print(json.dumps({'case':key,'status':q['status'],'returncode':q.get('returncode')}),flush=True)
 return q
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for result in pool.map(run,['PAD','INFERIOR_ESQ','INFERIOR_DIR']):pass
