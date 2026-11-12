import subprocess,json,datetime
from pathlib import Path
O=Path.cwd().parent/'desempenho'
for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
 folder=O/f'05_Orca/Resultado_{key}_X1_REF';folder.mkdir(exist_ok=True);status=folder/'status.json';inp=O/f'05_Orca/GARRA_{key}_TPMSD_REF_X1_ORIENTADA.3mf';out=folder/f'GARRA_{key}_TPMSD_X1_REF_FATIADA.3mf';assert not status.exists(),'Existing run; inspect before repeat'
 state={'case':key,'status':'running','start_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input':str(inp),'output':str(out),'printer':'X1 reference, production printer unconfirmed','scale':1,'slicing_not_FEA':True,'sent_to_printer':False};status.write_text(json.dumps(state,indent=2),encoding='utf-8')
 args=['C:/Program Files/OrcaSlicer/orca-slicer.exe',str(inp),'--arrange','1','--slice','0','--mstpp','900','--outputdir',str(folder),'--export-3mf',out.name,'--export-settings','perfil_efetivo.json']
 with (folder/'Orca_fatiamento.log').open('wb') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200,cwd=folder)
 state.update({'status':'output_pending_verification' if r.returncode==0 and out.exists() else 'failed','returncode':r.returncode,'end_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()});status.write_text(json.dumps(state,indent=2),encoding='utf-8');print(json.dumps(state,ensure_ascii=True),flush=True)
 if r.returncode:break
