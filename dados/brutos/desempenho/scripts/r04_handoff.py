from pathlib import Path
import json,shutil,csv
R=Path.cwd();O=R.parent/'desempenho';S=O/'00_Continuar/estado.json';q=json.loads(S.read_text(encoding='utf-8'));q.update({'phase':'CAD_STL_verified_slicing_K1Max_real_scale_preparation','printer_decision':'User authorized any larger printer; use original scale and source orientation, no tilted X1 in final mass totals','printer_reference':'Creality K1 Max300x300x300, stock0.4mm profile','native_PAD_document':'SAMI R04 - PADs SEPARADOS - TPU95A40','native_PA_documents':['SAMI R04 - '+x+' - MODIFICADORES TPMSD' for x in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']],'geometry_mode':'3 whole PA parts plus nonprinting modifiers; not separate physical inserts','mesh_checks':'8PAD+3PA+9modifier STLs closed and winding checked; see validation JSONs','actual_simulation_results':False,'video_status':'paused_by_user_until_all_engineering_data','latest_PAD_X1_slice':'completed test,120.63g incl supports,10h29m32s; bed50 warning, superseded in final by K1Max bed35 profile','X1_oriented_tests':'cancelled and obsolete by user request to use larger printer; no scaling ever applied to new STLs','next':'Finish K1Max profile import and flat real-scale slicing, extract actual object/support consumption; keep all mechanical/thermal/wear claims pending constitutive inputs.'});S.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
text='''# Continuidade SAMI - leia primeiro

O usuário pediu pausar o vídeo até existir a base completa de simulação. Não renderizar novo vídeo nem tratar o anterior1D como validação. Esta pasta é a entrega de continuidade para Claude/Claudio ou outro agente.

## Escopo obrigatório R04

Garra PA-CF: cinco perímetros, TPMS-D20% base; amarelo30%, azul50%, rosa70%. Prioridade de sobreposição70>50>30>20. O usuário confirmou que as cores se aplicam à garra, inclusive70% sob os PADs. PADs TPU95A40%, em arquivos separados. Manter escala1:1. Usuário autorizou trocar de impressora para calcular massa/consumo na orientação original. Referência final em preparação: Creality K1 Max300mm,0,4mm, fonte oficial Orca. Não somar testesX1 inclinados40graus aos dados finais.

As imagens fornecidas estão em07_Referencias. As larguras/profundidades das zonas não estão cotadas: máscaras tridimensionais são hipóteses dimensionadas, não reconstrução exata da pintura2D. Leia os arquivos04_Modificadores/*_regioes.json. Rosa: cilindrosR31,5mm,Z264..293mm; amareloR46mm,Z230..310mm; azul corredores18mm superiores/16mm inferiores seguindo caminhos registrados, recortados pelo próprio slicer dentro da peça.

## Arquivos já concretos

- 01_Fusion/PADs_R04_SEPARADOS.f3d e.step: oito partes PAD sem a garra.
- 02_STL_PAD/*.stl: oito STL individuais em mm, centralizadosXY e minZ0; ZIP dos individuais e conjunto com8 partes dispostas na mesa. Validação de fechamento/arestas/orientação/volume emvalidacao_STL.json.
- 03_STL_Garra/GARRA_*_BASE20.stl: três envelopes estruturais sem ferragens. Componentes originais: Corpo Supor e duas ocorrências Suporte_Ventosas_S.
- 04_Modificadores/{SUPERIOR,INFERIOR_ESQ,INFERIOR_DIR}/MOD_*.stl: volumes não imprimíveis para alterar densidade, alinhados ao STL principal. Não imprimir como peças de reforço separadas, pois isso criaria interfaces físicas diferentes do pedido.
- 01_Fusion/GARRA_*_ZONAS_R04.f3d/.step: preparaçãoCAD com envelope e modificadores sobrepostos, não uma partição física pronta para malhar. O nomeZONAS é histórico do arquivo; o modo está explícito nos JSONs.
- 05_Orca/*.3mf: projetos com material e modificadores incorporados. Os primeiros arquivosX1 podem aparecer fora da mesa; osX1 inclinados são referência obsoleta. Os K1MAX_ESCALA_REAL são os casos finais a usar.
- 05_Orca/ORCA_ANTERIOR_MONTAGEM_ESCALADA.3mf preserva o projeto que estava aberto: montagem completa com ferragens, reduzida a44,532%. Não usar para massa/engajamento da garra em escala real.

## Limites e falhas já investigados

A tentativa de recortar oBRep complexo da garra por booleanas falhou ASM_EDGECOIN_PROBLEM na interseção. Não repetir a operação inalterada. Foi adotado o fluxo correto de modificadores doOrca, com geometrias simples fechadas; o slicer os recorta dentro da peça. Não interpretar volume dos envelopes de modificador como volume realmente impresso da região.

O Fusion anterior bloqueou impacto por material inválido, causa interna específica não exposta. Não preencher escoamento, ruptura, damping ou curvas de vida com números inventados. As antigas estáticas maciças resolvidas não validam o novoTPMS-D zonal. Não remover modos rígidos para contornar apoios mal mapeados. Nenhuma nova análise3D de impacto/temperatura/falha/desgaste foi resolvida nesta revisão.

A ficha sólida BambuPA6-CF V3 e PolyFlexTPU95V5.4 é referência, não lei efetiva da impressão20/30/50/70% ou40%. Material/grade instalado ainda não confirmado. Cinco perímetros e porcentagem de núcleo não podem virar porcentagem direta de resistência nem da massa total. Usar massa do fatiador para peças, suportes e consumo separados. Peso da montagem completa inclui ferragens/ventosas: materiais CAD de ferragens eram padrões de importação, não medições.

Os requisitos obrigatórios incluem impacto, temperatura, ruptura, desgaste, amortecimento e durabilidade. Permanecem necessárias leis calibradas, orientação/umidade, cargas/cinemática e condições decontato. Para impacto do robô,24kg de carga útil não são automaticamente a massa efetiva de colisão. Temperatura de bico/mesa é processamento, não temperatura de serviço.

## Ferramentas e execução segura

Um único controlador doFusion/Orca. MCP compacto existente usaPython do projeto FUSION/.venv-fusion-mcp/Scripts/python.exe, servidor FUSION/fusion_mcp_compact/server.py e backendAutodesk localhttp://127.0.0.1:27182/mcp. Não imprimir APIs/malhas inteiras. ScriptsR04 têm guardas de documento/status para evitar duplicação; consultar osJSON antes de executá-los. O scriptbridge.script(code,False) faz mudanças; readOnlyTrue somente para leitura real.

Controle de UIWindows deve usar apenas @oai/sky pelo node_repl; nunca PowerShellUIAutomation,pyautogui ou terminal para cliques. CLI nativa documentada doOrca pode fatiar sem GUI. Nunca enviar à impressora. Fonte CLI/docs em07_Referencias/Orca_fonte e links no relatório. Se aCLI usar --outputdir, --export-3mf recebe somente basename, senão a versão instalada concatena indevidamente caminhoWindows absoluto.

Consultarstatus.json de cada fatiamento antes de reenviar. Código0 e arquivo3MF não bastam: verificar Metadata/plate_*.gcode, slice_info.config e outside=false. Falhas e tentativas estão preservadas. Não confundir fatiamento com FEA. O usuário quer consumo real de geometria em escala nominal e máximo de dados tecnicamente sustentados.
'''
(O/'00_Continuar/CONTINUAR_NO_CLAUDE.md').write_text(text,encoding='utf-8');(O/'CLAUDE.md').write_text('Leia00_Continuar/CONTINUAR_NO_CLAUDE.md e00_Continuar/estado.json antes de agir. Vídeo pausado. Um controladorFusion/Orca; sem agentes paralelos por padrão. Não inventar resultados físicos a partir de fatiamento.\n',encoding='utf-8')
for p in (R/'fusion_mcp_compact').glob('r04_*.py'):shutil.copy2(p,O/'scripts'/p.name)
checks=[['Impacto3D','pendente','massa efetiva, velocidade, contatos/retencao e lei do PAD/estrutura zonal'],['Temperatura3D','pendente','condutividade, calor especifico, CTE/E(T), ambiente e contato'],['Ruptura/delaminacao','pendente','criterios direcionais e curvas de falha da impressao'],['Amortecimento/absorcao real','pendente','curvas de compressao/descarga vs taxa/temperatura'],['Desgaste/durabilidade','pendente','espectro de ciclos, fluencia, fadiga/rasgo e ensaios de desgaste'],['Consumo/peso de polimeros','em fatiamento','somar massa das3PA e8PAD sem suportes; consumo total separado']]
with (O/'06_Engenharia/matriz_ensaios.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['ensaio','estado','dados_necessarios']);w.writerows(checks)
print('handoff_saved')
