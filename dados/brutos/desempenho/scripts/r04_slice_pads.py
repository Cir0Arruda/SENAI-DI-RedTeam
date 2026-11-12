import subprocess,json,datetime
from pathlib import Path
O=Path.cwd().parent/'desempenho';folder=O/'05_Orca/Resultado_PAD';folder.mkdir(exist_ok=True);status=folder/'status.json';inp=O/'05_Orca/PADs_TPU95A40_PREPARADO.3mf';out=folder/'PADs_TPU95A40_FATIADO_TESTE.3mf';args=['C:/Program Files/OrcaSlicer/orca-slicer.exe',str(inp),'--arrange','1','--slice','0','--mstpp','900','--outputdir',str(folder),'--export-3mf',out.name,'--export-settings','perfil_efetivo.json']
assert not status.exists() or json.loads(status.read_text())['status']=='failed','Existing active/successful run; do not duplicate'
if status.exists():
 status.rename(folder/'status_tentativa1_caminho.json');(folder/'Orca_fatiamento.log').rename(folder/'Orca_tentativa1_caminho.log')
state={'status':'running','start_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':str(inp),'output':str(out),'slicing_only_not_FEA':True,'sent_to_printer':False};status.write_text(json.dumps(state,indent=2),encoding='utf-8')
with (folder/'Orca_fatiamento.log').open('wb') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200,cwd=folder)
state.update({'status':'sliced' if r.returncode==0 and out.exists() else 'failed','returncode':r.returncode,'output_exists':out.exists(),'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});status.write_text(json.dumps(state,indent=2),encoding='utf-8');print(json.dumps(state))
