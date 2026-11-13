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

**[S4] HyperFrames 0.9.41 e FFmpeg.**
- Uso: os 3 vídeos desenhados da apresentação ([V1] e [V2]). O HyperFrames transforma uma página HTML em vídeo, quadro a quadro; o FFmpeg comprime o arquivo final.
- Projeto: <https://github.com/heygen-com/hyperframes> · <https://ffmpeg.org/>

---

## 1A. Arquivos 3D finais da garra SAI

**[A1] Pacote `modelos/SAI_final/`: os arquivos que entraram nos cálculos, prontos para imprimir.**
- 4 projetos do OrcaSlicer com as zonas internas (superior giroide 25% com 4 zonas; inferiores giroide 20% com 3 zonas; 8 PADs em TPU 95A, giroide 40%), os STL das peças e das zonas, o CAD (STEP) da garra montada e dos PADs, e um `LEIA-ME`.
- Conferência por script: material, paredes, preenchimento, cada zona contra o STL de origem, malhas fechadas e a mesma variante do FE ([E1]). Resultado: 0 erros. Script: [`sai_pacote_final.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/sai_pacote_final.py).
- Pasta: [`modelos/SAI_final/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/modelos/SAI_final) · conferência: [`manifesto.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/modelos/SAI_final/manifesto.json).

---

## 2. Simulações no Autodesk Fusion

**[F1] Garra superior maciça em PA6-CF, 24 kg divididos nas 4 interfaces.** Criado em 11/11/2026, 00:28.

| Item | Valor |
|---|---|
| Estudo | tensão estática, linear, isotrópico |
| Peça | só a superior, **maciça (100%)**: sem preenchimento, paredes nem camadas |
| Malha | 3 mm, parabólica, 498.261 nós e 339.001 elementos; sem refinamento adaptativo (0 etapas) e sem estudo de convergência |
| Fixação | furos da flange do robô |
| Carga | 4 × 88,84 N em −Z = 355,36 N, ou seja, 24 kg × (9,81 + 5 m/s²), **dividida igualmente nas 4 interfaces (as duas asas)**. O caso de 24 kg numa asa só está no [E1]. |
| Material | Bambu PA6-CF: E 4.430 MPa, resistência 102 MPa ([M1]) |
| Resultado | von Mises máxima 3,23 MPa · 1ª principal 5,16 MPa · **FS mínimo 19,8** |

- Relatório: [`SAMI_PA6CF_24kg_Relatorio_Fusion.html`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.html) (texto: [`.txt`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.txt)).

**[F2] Mesma garra em Tritan TX1001 (referência da garra atual).** Criado em 11/11/2026, 00:58.
- Mesma malha, fixação e carga do [F1].
- Material: E 1.548 MPa, resistência 58 MPa ([M3]).
- Resultado: von Mises máxima 3,22 MPa · 1ª principal 5,03 MPa · **FS mínimo 11,5**.
- O FS 11,5 corresponde ao critério de ruptura (58 ÷ 5,03), mas o cabeçalho do relatório exportado mostra "resistência a escoamento". Pelo escoamento seria 13,3 (43 ÷ 3,22). Conferir no Fusion.
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
- Por isso o R07 usa o FE próprio ([E1]), com o fator de pico 2,2, calibrado contra o Fusion [F1]: a mesma peça maciça, com a mesma carga, dá von Mises 3,23 MPa no Fusion e 1,46 MPa no FE por voxels (3,23 ÷ 1,46 = 2,2; o deslocamento bate: 0,080 × 0,078 mm).

---

## 3. Fatiamentos (OrcaSlicer)

**[O1] Garra R07 com e sem esqueleto, nas bases 20% e 25%.**
- Resultado (sem esqueleto): 1.432,8 g de peças, 1.744,5 g de filamento e 75,2 h de impressão.
- Tempo por peça na K1 Max: superior 34,2 h, inferior esquerda 20,5 h, inferior direita 20,5 h. Com os 8 PADs ([O3], 11,0 h), o SAI inteiro leva **86,2 h** (cerca de 3,6 dias de impressora).
- O Orca avisa, em todas as peças de PA6-CF, que o bico precisa ser mais duro que o de latão (aviso `1000C002` nos logs). Por isso a troca para o bico de aço endurecido. A ficha do material diz o mesmo ([M1]).
- Peça superior de Tritan para comparação: **35,1 h**. É a garra atual fatiada com favo 3D 30% no mesmo perfil (80,5 h para as 3 peças, [`decisao/DECISAO_ESQUELETO.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/DECISAO_ESQUELETO.json)) × 43,65%, a parte da peça superior na massa ([`decisao/peso_conjunto.csv`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/peso_conjunto.csv)).
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
- Custo real em 2 anos (slides de Custos e Retorno): [`custos/CUSTO_REAL.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md), com as entradas e fontes em [`custos/entradas_custo.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json) e o modelo em [`custo_real.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/custo_real.py).

**[E7] Vídeos e figuras.**
- São renderizados só a partir dos campos já calculados; nenhum vídeo cria resultado novo.
- Scripts: [`r07_videos.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_videos.py) e [`r07_video_sai.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_video_sai.py).
- Números: [`videos/videos_r07.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/videos/videos_r07.json).

**[V1] Vídeo da linha de paletização (slide Processo).**
- Desenho animado no [S4], em tempo acelerado e fora de escala. Ilustração, não é simulação.
- Números: só os dados da equipe (6 caixas por minuto, 2 caixas por ciclo, 40 caixas por palete em 4 camadas de 10, 12 itens e 12 kg por caixa). Com eles, um palete leva 6 min 40 s.
- Projeto: [`hyperframes/linha_palete/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/hyperframes/linha_palete).

**[V2] Vídeos do PAD (slides PAD e Valor de teste).**
- Slide PAD: animação do PAD como escudo, feita no [S4] com as forças do [E3] (451 → 169 N, −63%). A animação não calcula nada. Projeto: [`hyperframes/pad_escudo/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/hyperframes/pad_escudo).
- Slide Valor de teste: recorte sem legenda (mesmos 300 quadros, 10 s) do vídeo do estudo R03 ([E3], [`impacto_pad_r03.mp4`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/assets/video/impacto_pad_r03.mp4)). O gráfico ao lado lê a série de forças do próprio R03.

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
- **[M6] Universal Robots UR30, ficha técnica.** Carga útil de 30 kg; usada para a folga de carga do robô no slide Processo. <https://www.universal-robots.com/products/ur30/> · <https://www.universal-robots.com/media/1829274/ur30_datasheet_web.pdf>
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

## 8. Preços de mercado (slides de Custos e Retorno)

**[P1] Entradas do custo real, pesquisadas em nov/2026.** Cada valor tem a fonte e a data no próprio arquivo: [`custos/entradas_custo.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json). Os principais:

| Valor no slide | Fonte |
|---|---|
| PA6-CF R$ 420/kg | Voolt3D R$ 420 e Creality Hyper PA6-CF R$ 434 |
| TPU R$ 158/kg | equipe; mediana do mercado R$ 159,90 (melhorfilamento.com.br) e Brasfila R$ 158 |
| Tritan R$ 220/kg | 3DX CPE com certificado NSF 51 (loja3dxfilamentos.com.br) |
| Energia R$ 0,70/kWh | CPFL Paulista, tarifa A4 verde 2026 (REH 3.579/2026), com impostos |
| Técnico R$ 30,23/h | R$ 3.500/mês (Novo CAGED, via salario.com.br) × 1,9 de encargos ÷ 220 h |
| Impressora K1 Max R$ 5.500 em 5.000 h | lojas no Brasil (R$ 4.940 a 6.507); vida de referência de snapmaker.com e all3dp.com |
| Bico de aço endurecido | cerca de R$ 60 a cada 300 h com fibra de carbono |
| Refugo de 10% no PA6-CF | Filamentive, citado em PMC9706623 (hipótese) |

Modelo e revisão: [E6] e [`custos/CUSTO_REAL.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md).

---

## 9. Reciclagem (slide Sustentabilidade)

- **[R1]** Política Nacional de Resíduos Sólidos, Lei 12.305/2010 (separação e destinação dos resíduos). <https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12305.htm>
- **[R2]** BASF, programa CirculAí: recolhe sobras de poliamida PA 6 e PA 66, com ou sem carga, no Brasil. A página não cita fibra de carbono: **confirmar com a BASF** se aceita PA6-CF. <https://download.basf.com/p1/8a80821284d444010184e5e90a2e57d4/pt/CIRCULA%C3%8D_Brochure_South_America_portugu%C3%AAs.pdf?view>
- **[R3]** Reaproveitamento de refugo de poliuretano em solados de calçado (Ecycle). O texto fala de PU, a família do TPU, e não de TPU impresso: **confirmar com um reciclador** do polo calçadista. <https://www.ecycle.com.br/component/content/article/35-atitude/884-poliuretanoo-desconhecido-muito-presente-no-cotidiano.html>

Os destinos do slide (recicladores do polo calçadista para o TPU e de polímeros de engenharia para o PA6-CF) são **proposta da equipe**. As fontes acima mostram que a reciclagem é possível, mas nenhum comprador foi contatado.

---

## 10. Dados informados pela equipe

Origem: equipe do projeto, com base na linha da Ajinomoto. Ficam registrados em [`dados/README.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/README.md) e em [`custos/entradas_custo.json`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json).
- **Linha:** cerca de 6 caixas por minuto; 2 caixas por ciclo do robô (uma em cada asa); 40 caixas por palete, em 4 camadas de 10; 12 itens e 12 kg por caixa.
- **Garra instalada:** Tritan, 2,834 kg; quebra a cada 3 meses (4 vezes por ano), rompendo na raiz.
- **Paradas:** a troca da garra para a linha 45 min (280 caixas); a troca só dos PADs leva cerca de 20 min (120 caixas, estimativa da equipe). Parada para manuseio a cada 45 min de operação.
- **Manutenção proposta:** garra SAI nova a cada 24 meses e PADs a cada trimestre, com data marcada.
- **Impressão:** a mesma impressora que imprime o Tritan imprime o PA6-CF, trocando o bico ([O1]).
- **Prazos:** Tritan importado 15 a 20 dias; PA6-CF nacional 5 a 8 dias úteis.
- **Matriz de prioridade** (slide Ideias anteriores): notas de valor e complexidade de 0 a 10 dadas pela equipe.
- **Valores da equipe que o modelo de custo trocou ou deixou de usar:** PA6-CF R$ 258/kg (o modelo usa R$ 420, preço de mercado), R$ 250 por quebra do Tritan, bico de R$ 23,50 de uma vez e R$ 84.000 por parada. O porquê está em [`custos/CUSTO_REAL.md`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md).

---

## 11. Uso de inteligência artificial

**[C1] Claude Code (Anthropic): apoio nos testes e na organização dos dados.**
- O projeto teve ajuda do Claude Code, assistente de programação com IA da Anthropic, na parte de testes, como a aplicação em Python ([S3], scripts em [`dados/scripts/`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/scripts)).
- **Regra de uso:** o Claude Code foi proibido de buscar informações novas e de mudar o modelo sem permissão da equipe.
- **Para que foi usado:**
  - organização dos dados;
  - validação dos resultados;
  - automação dos testes no Autodesk Fusion ([S1]);
  - identificação de falhas e eventos nos dados.
- Exemplo: a conferência byte a byte das imagens do Fusion ([`evidencias_fusion.py`](https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/evidencias_fusion.py)) achou uma figura corrompida na cópia publicada do relatório [F1], que foi restaurada a partir do arquivo original.
- Produto: <https://claude.com/claude-code>
