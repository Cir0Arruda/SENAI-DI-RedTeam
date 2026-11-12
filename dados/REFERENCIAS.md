# Referências do Projeto SAI

Tudo o que a apresentação mostra sai dos arquivos listados aqui. Cada item diz:
- o que é;
- como foi feito;
- o resultado;
- onde está o arquivo.

Links internos apontam para este repositório: <https://github.com/Cir0Arruda/SENAI-DI-RedTeam>.

**Importante:** nenhum resultado desta lista é ensaio físico. São simulações por computador, fatiamentos e cálculos, com as hipóteses escritas em cada arquivo. Os ensaios de bancada recomendados estão no item [T1].

---

## 1. Software

**[S1] Autodesk Fusion, versão 2706.1.17, Licença Educacional (Autodesk).**
- Uso: modelo 3D da garra e dos PADs (STEP/F3D) e estudos de **tensão estática** (solver na nuvem).
- A versão está registrada no cabeçalho dos próprios relatórios exportados ([F1], [F2], [F3]).
- Produto: <https://www.autodesk.com/products/fusion-360/>
- Licença educacional: <https://www.autodesk.com/education/edu-software/overview>
- Documentação de simulação: <https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM>

**[S2] OrcaSlicer 2.5.0 (linha de comando).**
- Uso: fatiamento real de todas as peças. A partir dele saem massa, filamento, tempo e avisos.
- Configuração: perfil Creality K1 Max, escala 1:1, PA6-CF 1,10 g/cm³, 5 paredes, camada de 0,2 mm.
- **Nada foi enviado à impressora.**
- Projeto: <https://github.com/SoftFever/OrcaSlicer>

**[S3] Python 3.14.7, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2.**
- Uso: FE por voxels, impacto transiente, fadiga, custos, figuras e vídeos.
- Scripts: [`dados/scripts/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/scripts).

---

## 2. Simulações no Autodesk Fusion

**[F1] Garra superior maciça em PA6-CF, 24 kg.** Criado em 11/11/2026, 00:28.

| Item | Valor |
|---|---|
| Estudo | tensão estática, malha adaptativa (10% refinado) |
| Malha | 498.261 nós e 339.001 elementos |
| Fixação | furos da flange do robô |
| Carga | 4 × 88,84 N em −Z = 355,36 N, ou seja, 24 kg × (9,81 + 5 m/s²) |
| Material | Bambu PA6-CF: E 4.430 MPa, resistência 102 MPa ([M1]) |
| Resultado | von Mises máxima 3,23 MPa · 1ª principal 5,16 MPa · **FS mínimo 19,8** |

- Relatório: [`SAMI_PA6CF_24kg_Relatorio_Fusion.html`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.html) (texto: [`.txt`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.txt)).

**[F2] Mesma garra em Tritan TX1001 (referência da garra atual).** Criado em 11/11/2026, 00:58.
- Mesma malha, fixação e carga do [F1].
- Material: E 1.548 MPa, resistência 58 MPa ([M3]).
- Resultado: von Mises máxima 3,22 MPa · **FS mínimo 11,5**.
- O PA6-CF teve cerca de **65% menos deslocamento** que o Tritan.
- Relatório: [`SAMI_TRITAN_24kg_Relatorio_Fusion.html`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_TRITAN_24kg_Relatorio_Fusion.html).
- Evidência (hash SHA-256 do arquivo original): [`_evidence.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_TRITAN_24kg_Relatorio_Fusion_evidence.json).
- Comparação e limites dos dois estudos: [`COMPARACAO_SAMI_2026-11-11.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/COMPARACAO_SAMI_2026-11-11.md).

**[F3] Estudo de conferência do método: esfera de 50 mm, 100 N.**
- Modelo: esfera maciça de 50 mm, calota de baixo fixa e 100 N na calota de cima.
- Material: SUNLU ABS-Like.
- Arquivos: [`Esfera_SUNLU_100N_Relatorio_Fusion.html`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/Esfera_SUNLU_100N_Relatorio_Fusion.html) e [`RESULTADOS_ESFERA_SUNLU.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/RESULTADOS_ESFERA_SUNLU.md).

**[F4] Garra R07 com preenchimento: não resolvido no Fusion.**
- O modelo de 2 corpos (casca e núcleo homogeneizado) foi montado.
- O solve parou num erro de malha na casca.
- Registro: [`RELATORIO_R07.md`, seção 4](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md) e [`fusion_build_2corpos.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/fusion/fusion_build_2corpos.json).
- Por isso o R07 usa o FE próprio ([E1]), com o pico calibrado no Fusion (fator 2,2, medido no R06).

---

## 3. Fatiamentos (OrcaSlicer)

**[O1] Garra R07 com e sem esqueleto, nas bases 20% e 25%.**
- Resultado (sem esqueleto): 1.432,8 g de peças, 1.744,5 g de filamento e 75,2 h de impressão.
- Dados: [`orca/r07_fatiamento_base25.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_fatiamento_base25.json) e [`orca/r07_fatiamento_base20.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_fatiamento_base20.json).
- Logs de cada peça: [`brutos/desempenho/05_Orca/R07/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/05_Orca/R07).

**[O2] Comparativo de preenchimentos.**
- Variantes: giroide 30/35/40%, Hexa3D 30% (padrão da garra instalada) e TPMS-D 40%.
- Dados: [`orca/r07_comparativo_fatiamento.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_comparativo_fatiamento.json).

**[O3] 8 PADs em TPU 95A, giroide 40%, 3 paredes.**
- Resultado: 139,0 g e 11,0 h.
- Dados: [`orca/pads_tpu95a_fatiamento.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/pads_tpu95a_fatiamento.json).

**[O4] Camadas reais lidas do G-code** (figuras do slide Giroide).
- Dados: [`orca/camadas_r07.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/camadas_r07.json).
- Script: [`r07_camadas.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_camadas.py).

**[O5] Fatiamentos completos com G-code (R04, R06 e R07).**
- Disponíveis na [Release `dados-2026-11-12`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/releases/tag/dados-2026-11-12).

---

## 4. Simulações próprias (Python)

**[E1] FE estático por voxels da garra montada (superior + inferiores).** Script: [`r07_montagem.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_montagem.py).

Método:
- Elementos: voxels de 3 mm, hexaedros de 8 nós.
- Paredes em PA6-CF transversalmente isotrópico: XY 4.430 MPa, Z 2.170 MPa.
- Giroide homogeneizado por Gibson-Ashby ([L1]).
- Engaste nos 6 furos da flange.
- Carga numa asa = massa × (g + 5 m/s²).
- Critério de falha: tração entre camadas (Z). Pico calibrado no Fusion (× 2,2).

Resultado da garra SAI:
- Rompe com **93,3 kg** numa asa (PA6-CF) ou 35,4 kg (pior colagem, PAHT CF15).
- FS a 24 kg: 3,89.

Dados: [`montagem/montagem_R07_SEM.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/montagem/montagem_R07_SEM.json), [`montagem/montagem_resumo.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/montagem/montagem_resumo.json).

**[E2] Tranco: FE transiente 3D da peça superior.** Script: [`r07_impacto.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_impacto.py).
- Método: 24 kg aplicados numa asa em 10 ms; integração de Newmark; amortecimento de Rayleigh de 3%.
- Resultado: fator dinâmico 1,71; tensão Z de pico 18,1 MPa; FS 2,65 (PA6-CF).
- Dados: [`impacto/impacto_F25_SEM.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/impacto/impacto_F25_SEM.json).

**[E3] Impacto no PAD: modelo reduzido de molas (1D).**
- Caso: esfera de 263 g a 1 m/s.
- Resultado: pico de 450,9 N sem PAD e 168,5 N com PAD, ou seja, **−62,6%** dentro das hipóteses.
- **Não é FE da garra real.**
- Relatório: [`RELATORIO_SAMI_HEXA15.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/impacto_pad_hexa15/01_Relatorio/RELATORIO_SAMI_HEXA15.md).
- Limites do PAD (cerca de 240 N para esmagar e 1.380 N para quebrar a garra): [`impacto/pad_limites.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/impacto/pad_limites.json) e [`pad_limites.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/pad_limites.py).

**[E4] Fadiga, fluência e desgaste.**
- Método:
  - curva S-N normalizada, σ/S = 1 − 0,10·log₁₀N;
  - regra de Miner ([L2]);
  - fluência com módulo de 0,70 E em 1.000 h e 0,55 E em 10.000 h;
  - desgaste dos furos pela lei de Archard ([L3]).
- Dados: [`fadiga/r07_vida.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/fadiga/r07_vida.json).

**[E5] Decisão com × sem esqueleto e peso do conjunto.**
- Dados: [`decisao/DECISAO_ESQUELETO.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/DECISAO_ESQUELETO.json), [`decisao/dados_comparativos.csv`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/dados_comparativos.csv) e [`decisao/peso_conjunto.csv`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/peso_conjunto.csv).

**[E6] Estudo de custos e durabilidade.**
- Conteúdo: vida estimada de 12 a 36 meses, custo de aquisição completo e cenários de 24 e 36 meses.
- Estudo: [`estudo_custos/ESTUDO_CUSTOS_DURABILIDADE.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/estudo_custos/ESTUDO_CUSTOS_DURABILIDADE.md).
- Script: [`estudo_custos.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/estudo_custos.py).

**[E7] Vídeos e figuras.**
- São renderizados só a partir dos campos já calculados; nenhum vídeo cria resultado novo.
- Scripts: [`r07_videos.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_videos.py) e [`r07_video_sai.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_video_sai.py).
- Números: [`videos/videos_r07.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/videos/videos_r07.json).

**Relatório técnico completo do R07:** [`dados/RELATORIO_R07.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md).

**Logs, JSON e CSV de todas as rodadas (R04 a R07):** [`dados/brutos/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos).

**Campos de FE, modelos 3D, vídeos e fatiamentos completos:** [Release `dados-2026-11-12`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/releases/tag/dados-2026-11-12).

---

## 5. Testes

**[T1] Ensaios de bancada recomendados (ainda não realizados).** Fonte: [`RELATORIO_R07.md`, item 3.7](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md).
1. Carga de prova: 24 kg numa asa por 1 min, critério do tipo EN 13155 ([N1]).
2. Ruptura numa asa.
3. Fadiga: 10⁵ ciclos de 0 a 24 kg.
4. Tranco com parada de emergência (acelerômetro).
5. Fluência: 168 h com 24 kg.

**[T2] Testes do processo de simulação.**
- Verificação de malhas STL fechadas: [`02_STL_PAD/validacao_STL.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/02_STL_PAD).
- Conferência dos fatiamentos: [`06_Engenharia/R05_CONFERENCIA_ORCA/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/06_Engenharia/R05_CONFERENCIA_ORCA).
- Estudo de conferência da esfera: [F3].

---

## 6. Materiais (fichas técnicas dos fabricantes)

- **[M1] Bambu Lab PA6-CF, ficha V3.0.** E XY 4.430 MPa; tração XY/Z 102/48 MPa; HDT 164 °C. <https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf>
- **[M2] Forward AM Ultrafuse PAHT CF15, ficha v3.5.** Tração XY/ZX 103,2/18,2 MPa; usado como pior caso de colagem. <https://forward-am.com/wp-content/uploads/2024/10/Ultrafuse_PAHT_CF15_TDS_EN_v3.5-1.pdf>
- **[M3] Eastman Tritan TX1001.** E 1.548 MPa; ruptura 58 MPa; material da garra atual (resina moldada). <https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312>
- **[M4] Bambu Lab TPU 95A HF, ficha V3.0** (PADs). <https://store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/Bambu_TPU_95A_HF_Technical_Data_Sheet.pdf>
- **[M5] Lubrizol ESTANE X-595A-11**, TPU 97A de referência para os PADs. <https://www.lubrizol.com/-/media/Lubrizol/Engineered-Polymers/Documents/Engineered-Polymer-TDS/ESTANE-X595-A11.pdf>
- Cartões de material usados no FE: [`materiais/materiais_R07.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/materiais/materiais_R07.json).

---

## 7. Literatura e normas

- **[L1]** GIBSON, L. J.; ASHBY, M. F. *Cellular Solids: Structure and Properties*. 2. ed. Cambridge University Press, 1997. DOI 10.1017/CBO9781139878326. Fundamenta a lei do giroide homogeneizado.
- **[L2]** MINER, M. A. Cumulative damage in fatigue. *Journal of Applied Mechanics*, v. 12, p. A159–A164, 1945. DOI 10.1115/1.4009458. Fundamenta a soma de dano da fadiga.
- **[L3]** ARCHARD, J. F. Contact and rubbing of flat surfaces. *Journal of Applied Physics*, v. 24, p. 981–988, 1953. DOI 10.1063/1.1721448. Fundamenta o desgaste dos furos.
- **[L4]** NIST. *Weld formation during material extrusion additive manufacturing* (colagem entre camadas). <https://www.nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing>
- **[L5]** NIST IR 8059. *Materials testing standards for additive manufacturing of polymer materials*. <https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8059.pdf>
- **[L6]** Estudo de orientação de impressão em polímeros com fibra (PMC11669830). <https://pmc.ncbi.nlm.nih.gov/articles/PMC11669830/>
- **[L7]** Fluência em peças impressas (arXiv 2302.11240). <https://arxiv.org/abs/2302.11240>
- **[N1]** EN 13155. *Cranes: Safety. Non-fixed load lifting attachments* (dispositivos de içamento, incluindo a vácuo). Usada como referência de critério para o ensaio de carga de prova.

---

## 8. Dados informados pela equipe

Origem: equipe do projeto, com base na linha da Ajinomoto. Ficam registrados em [`dados/README.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/README.md).
- Preços: PA6-CF R$ 258/kg, TPU R$ 158/kg, garra de Tritan R$ 250, bico endurecido R$ 23,50.
- Quebras: a garra de Tritan quebra a cada 3 meses.
- Parada: 45 min, 280 caixas, 12 itens e 12 kg por caixa, 40 caixas por palete.
- Massa da garra instalada: 2,834 kg.
- Prazos: Tritan 15–20 dias; PA6-CF 5–8 dias úteis.
