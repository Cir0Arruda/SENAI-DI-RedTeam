import subprocess,json
from pathlib import Path
O=Path.cwd().parent/'desempenho';r=subprocess.run(['C:/Program Files/OrcaSlicer/orca-slicer.exe','--info',str(O/'05_Orca/ORCA_ANTERIOR_MONTAGEM_ESCALADA.3mf')],capture_output=True,timeout=60);(O/'05_Orca/CLI_info_teste.log').write_bytes(r.stdout+r.stderr);print(json.dumps({'code':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'tail':(r.stdout+r.stderr).decode('utf-8',errors='replace')[-1000:]},ensure_ascii=True))
