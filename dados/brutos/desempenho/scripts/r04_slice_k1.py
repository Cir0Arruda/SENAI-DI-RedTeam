import subprocess,json,datetime
from pathlib import Path
O=Path.cwd().parent/'desempenho'
for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR','PAD']:
 folder=O/f'05_Orca/Resultado_{key}_K1MAX';folder.mkdir(exist_ok=True);status=folder/'status.json';inp=O/'05_Orca'/('PADs_TPU95A40_K1MAX_ESCALA_REAL.3mf' if key=='PAD' else f'GARRA_{key}_TPMSD_K1MAX_ESCALA_REAL.3mf');out=folder/f'{key}_K1MAX_FATIADO_REFERENCIA.3mf';assert not status.exists() or json.loads(status.read_text())['status']=='failed','Existing active/completed run; do not duplicate'
 if status.exists():
  status.rename(folder/'status_tentativa1_compatibilidade.json');(folder/'Orca_fatiamento.log').rename(folder/'Orca_tentativa1_compatibilidade.log')
 state={'case':key,'status':'running','start_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':str(inp),'output':str(out),'printer_reference':'Creality K1 Max300mm,0.4mm','orientation':'original source Z-up','scale':1,'slicing_not_FEA':True,'sent_to_printer':False};status.write_text(json.dumps(state,indent=2),encoding='utf-8')
 args=['C:/Program Files/OrcaSlicer/orca-slicer.exe',str(inp),'--arrange','1','--slice','0','--mstpp','900','--outputdir',str(folder),'--export-3mf',out.name,'--export-settings','perfil_efetivo.json']
 with (folder/'Orca_fatiamento.log').open('wb') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200,cwd=folder)
 state.update({'status':'output_pending_verification' if r.returncode==0 and out.exists() else 'failed','returncode':r.returncode,'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});status.write_text(json.dumps(state,indent=2),encoding='utf-8');print(json.dumps(state,ensure_ascii=True),flush=True)
 if r.returncode:break
