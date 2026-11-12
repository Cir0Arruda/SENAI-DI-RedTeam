from pathlib import Path
import json,shutil
O=Path.cwd().parent/'desempenho'
for d in ['00_Continuar','01_Fusion','02_STL_PAD','03_STL_Garra','04_Modificadores','05_Orca','06_Engenharia','07_Referencias','scripts']:(O/d).mkdir(parents=True,exist_ok=True)
for label,name in [('PAD_referencia','563ae02c-ed55-4d6c-9136-859ae825ef21'),('requisitos_analise','8abdbb73-992c-4891-aecd-82d6552e41e1'),('zonas_coloridas','f9d41643-52a7-4b7c-bf2d-ed73763d6233')]:
 src=Path('~/AppData/Local/Temp')/('codex-clipboard-'+name+'.png');shutil.copy2(src,O/'07_Referencias'/f'{label}.png')
scope={'revision':'R04_ZONAL_TPMSD','video_status':'paused_by_user_until_all_simulation_data','gripper':{'material':'PA-CF, grade reference Bambu PA6-CF unless changed','wall_loops':5,'base_infill_percent':20,'pattern_requested':'TPM-SD; mapped to Orca TPMS-D pending installed-version check','yellow_percent':30,'pink_percent':70,'blue_percent':50,'overlap_priority_proposed':[70,50,30,20],'zones_source':'user annotated image; spatial widths/depths require approximate CAD masks and review; not exact dimensions from image'},'pad':{'material':'PU/TPU95A','infill_percent':40,'separate_STL':True},'user_confirmed':'All colored zones apply to PA-CF gripper, including pink70 under PAD; PAD40 separate','required_engineering':['impact','temperature','rupture','wear','damping','long-term durability'],'actual_FE_results':False,'slicer_outputs_are_not_mechanical_simulation':True}
(O/'00_Continuar/estado.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2),encoding='utf-8');print('desempenho_created')
