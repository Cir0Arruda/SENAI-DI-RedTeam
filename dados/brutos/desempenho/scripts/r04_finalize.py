from pathlib import Path
import json,csv,hashlib,zipfile,shutil
O=Path(__file__).resolve().parents[2]/'desempenho';R=Path(__file__).resolve().parents[1]
checks=[['Impacto3D','bloqueado','Leis efetivas zonais; compressao/descarga PAD40; contatos, retencao e cinemática reais'],['Temperatura3D','bloqueado','k,cp,E(T),CTE, condicoes de contorno e condicionamento'],['Ruptura/delaminacao','bloqueado','Criterios direcionais e dados de falha da impressao'],['Amortecimento/absorcao','bloqueado','Histerese e dependencia de taxa/temperatura PAD40'],['Desgaste/durabilidade','bloqueado','Fluencia/fadiga/rasgo/desgaste e espectro real'],['Consumo/peso de polimeros','fatiamento concluido e verificado','Quatro casos escala1; CSV/JSON de massa; sem ferragens'],['Exterior da garra','inalterado, auditado','Mesma tesselação com translacao; modificadores nao imprimiveis'],['Video','pausado por usuario','Aguardar resultados completos de engenharia']]
with (O/'06_Engenharia/matriz_ensaios.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.writer(f);w.writerow(['ensaio','estado','dados_necessarios_ou_evidencia']);w.writerows(checks)
ledger={'revision':'R04_internal_only','external_changes_prohibited':True,'new_Fusion_solver_jobs':0,'old_static_baselines_repeated':False,'new_study_geometry':'01_Fusion/GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.f3d','geometry_prepared':True,'actual_internal_lattice_or_effective_laws_prepared':False,'mesh_generated':False,'contacts_and_supports_validated':False,'cost_displayed':None,'submission_id':None,'cases':[{'case':name,'status':'blocked','solver_run':False,'results':None} for name in ['PA_TPMSD_ZONAL_SEM_PAD_IMPACTO','PA_TPMSD_ZONAL_COM_PAD40_IMPACTO','TERMICO_TRANSIENTE_SERVICO','DESGASTE_FADIGA_FLUENCIA_24_7']],'reason':'Current CAD retains solid envelopes, not explicit TPMS-D or calibrated regional shell/core. Prior A1 had invalid material and missing contacts; no unchanged re-precheck. Constitutive/contact/load data remain missing. Slicing is not mechanical simulation.'}
(O/'06_Engenharia/REGISTRO_SIMULACOES_R04.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'05_Orca/USO_DOS_PROJETOS.txt').write_text('Abrir *K1MAX_ESCALA_REAL.3mf como PROJETO, nao apenas como geometria. Garra: um normal_part e tres modifier_part internos; base20%,30/50/70%,TPMS-D,5paredes. Mascaras nao sao corpos adicionais. PADs40% em projeto separado. Todos escala1:1, sem alterar exterior.\nResultados_*_K1MAX sao fatiamentos calculados, nao FEA e nao liberacao para imprimir. Avisos de bico/mesa preservados. Nunca enviar estes Gcodes sem revisao do perfil da impressora real.\nArquivos X1 ou MONTAGEM_ESCALADA sao referencias antigas, nao resultados finais.\n',encoding='utf-8')
for p in (R/'fusion_mcp_compact').glob('r04_*.py'):shutil.copy2(p,O/'scripts'/p.name)
files=[]
for p in O.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(O);parts=rel.parts
 if any(x in parts for x in ['QA_PDF','origem','FERRAMENTAS_NAO_SIMULAR']):continue
 if rel.name.endswith('.zip'):continue
 if parts[0]=='05_Orca':
  if len(parts)==2 and not (rel.name.endswith('K1MAX_ESCALA_REAL.3mf') or rel.name in ['configuracao_referencia_K1MAX.json','USO_DOS_PROJETOS.txt','perfil_anterior_resolvido.json']):continue
  if len(parts)>2 and parts[1].startswith('Resultado_'):
   if not parts[1].endswith('_K1MAX') or p.suffix.lower() not in ['.json','.csv','.png','.log']:continue
  elif len(parts)>2:continue
 if parts[0]=='01_Fusion' and len(parts)==2:
  if not (rel.name.startswith('GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO') or rel.name.startswith('PADs_R04_SEPARADOS') or rel.name.endswith('_EXTERIOR_INALTERADO.png')):continue
 files.append(p)
manifest=[]
for p in sorted(files):manifest.append({'file':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()})
mp=O/'MANIFESTO_ENTREGA_R04.json';manifest=[m for m in manifest if m['file']!=mp.name];mp.write_text(json.dumps({'scope':'Light handoff package: STL, prepared 3MF, clean CAD, report, sources and verified numerical outputs. Large sliced3MF/Gcode remain in local05_Orca/Resultado_*_K1MAX and are deliberately excluded. No videos. No solved FEA.','files':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
files=[p for p in files if p!=mp]+[mp];dest=O/'SAMI_R04_INTERNO_STL_3MF_RELATORIO.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,p.relative_to(O).as_posix())
with zipfile.ZipFile(dest) as z:assert z.testzip() is None;count=len(z.namelist())
for f in ['PADs_STL_INDIVIDUAIS.zip']:
 with zipfile.ZipFile(O/'02_STL_PAD'/f) as z:assert z.testzip() is None and len(z.namelist())==8
print(json.dumps({'package':str(dest),'files':count,'bytes':dest.stat().st_size,'zip_crc':'passed','PAD_STL_count':8,'large_gcode_excluded':True,'FEA_solved':False}))
