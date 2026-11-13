// Gerado por dados/scripts/referencias_site.py a partir de dados/REFERENCIAS.md. Não editar à mão.
window.REFS = {
"fonte": "dados/REFERENCIAS.md",
"intro": "<p>Tudo o que a apresentação mostra sai dos arquivos listados aqui. Cada item diz:</p><ul><li>o que é;</li><li>como foi feito;</li><li>o resultado;</li><li>onde está o arquivo.</li></ul><p>Links internos apontam para este repositório: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam\" target=\"_blank\" rel=\"noopener\">github.com/Cir0Arruda/SENAI-DI-RedTeam</a>.</p><p><b>Importante:</b> nenhum resultado desta lista é ensaio físico. São simulações por computador, fatiamentos e cálculos, com as hipóteses escritas em cada arquivo. Os ensaios de bancada recomendados estão no item <a class=\"rv-x\" href=\"#ref-T1\" data-ref=\"T1\">[T1]</a>.</p><p>---</p>",
"secoes": [
{
"titulo": "Software",
"intro": "",
"itens": [
{
"cod": "S1",
"titulo": "Autodesk Fusion, versão 2706.1.17, Licença Educacional (Autodesk)",
"html": "<ul><li>Uso: modelo 3D da garra e dos PADs (STEP/F3D) e estudos de <b>tensão estática</b> (solver na nuvem).</li><li>A versão está registrada no cabeçalho dos próprios relatórios exportados (<a class=\"rv-x\" href=\"#ref-F1\" data-ref=\"F1\">[F1]</a>, <a class=\"rv-x\" href=\"#ref-F2\" data-ref=\"F2\">[F2]</a>, <a class=\"rv-x\" href=\"#ref-F3\" data-ref=\"F3\">[F3]</a>).</li><li>Produto: <a href=\"https://www.autodesk.com/products/fusion-360/\" target=\"_blank\" rel=\"noopener\">autodesk.com/products/fusion-360</a></li><li>Licença educacional: <a href=\"https://www.autodesk.com/education/edu-software/overview\" target=\"_blank\" rel=\"noopener\">autodesk.com/education/edu-software/overview</a></li><li>Documentação de simulação: <a href=\"https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM\" target=\"_blank\" rel=\"noopener\">help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM</a></li></ul>",
"busca": "s1 autodesk fusion, versao 2706.1.17, licenca educacional (autodesk) uso: modelo 3d da garra e dos pads (step/f3d) e estudos de tensao estatica (solver na nuvem). a versao esta registrada no cabecalho dos proprios relatorios exportados ( [f1] , [f2] , [f3] ). produto: autodesk.com/products/fusion-360 licenca educacional: autodesk.com/education/edu-software/overview documentacao de simulacao: help.autodesk.com/view/fusion360/enu/?contextid=pre-event-sim software"
},
{
"cod": "S2",
"titulo": "OrcaSlicer 2.5.0 (linha de comando)",
"html": "<ul><li>Uso: fatiamento real de todas as peças. A partir dele saem massa, filamento, tempo e avisos.</li><li>Configuração: perfil Creality K1 Max, escala 1:1, PA6-CF 1,10 g/cm³, 5 paredes, camada de 0,2 mm.</li><li><b>Nada foi enviado à impressora.</b></li><li>Projeto: <a href=\"https://github.com/SoftFever/OrcaSlicer\" target=\"_blank\" rel=\"noopener\">github.com/SoftFever/OrcaSlicer</a></li></ul>",
"busca": "s2 orcaslicer 2.5.0 (linha de comando) uso: fatiamento real de todas as pecas. a partir dele saem massa, filamento, tempo e avisos. configuracao: perfil creality k1 max, escala 1:1, pa6-cf 1,10 g/cm3, 5 paredes, camada de 0,2 mm. nada foi enviado a impressora. projeto: github.com/softfever/orcaslicer software"
},
{
"cod": "S3",
"titulo": "Python 3.14.7, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2",
"html": "<ul><li>Uso: FE por voxels, impacto transiente, fadiga, custos, figuras e vídeos.</li><li>Scripts: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/scripts\" target=\"_blank\" rel=\"noopener\"><code>dados/scripts/</code></a>.</li></ul>",
"busca": "s3 python 3.14.7, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2 uso: fe por voxels, impacto transiente, fadiga, custos, figuras e videos. scripts: dados/scripts/ . software"
},
{
"cod": "S4",
"titulo": "HyperFrames 0.9.41 e FFmpeg",
"html": "<ul><li>Uso: os 3 vídeos desenhados da apresentação (<a class=\"rv-x\" href=\"#ref-V1\" data-ref=\"V1\">[V1]</a> e <a class=\"rv-x\" href=\"#ref-V2\" data-ref=\"V2\">[V2]</a>). O HyperFrames transforma uma página HTML em vídeo, quadro a quadro; o FFmpeg comprime o arquivo final.</li><li>Projeto: <a href=\"https://github.com/heygen-com/hyperframes\" target=\"_blank\" rel=\"noopener\">github.com/heygen-com/hyperframes</a> · <a href=\"https://ffmpeg.org/\" target=\"_blank\" rel=\"noopener\">ffmpeg.org</a></li></ul>",
"busca": "s4 hyperframes 0.9.41 e ffmpeg uso: os 3 videos desenhados da apresentacao ( [v1] e [v2] ). o hyperframes transforma uma pagina html em video, quadro a quadro; o ffmpeg comprime o arquivo final. projeto: github.com/heygen-com/hyperframes ffmpeg.org software"
}
]
},
{
"titulo": "Arquivos 3D finais da garra SAI",
"intro": "",
"itens": [
{
"cod": "A1",
"titulo": "Pacote <code>modelos/SAI_final/</code>: os arquivos que entraram nos cálculos, prontos para imprimir",
"html": "<ul><li>4 projetos do OrcaSlicer com as zonas internas (superior giroide 25% com 4 zonas; inferiores giroide 20% com 3 zonas; 8 PADs em TPU 95A, giroide 40%), os STL das peças e das zonas, o CAD (STEP) da garra montada e dos PADs, e um <code>LEIA-ME</code>.</li><li>Conferência por script: material, paredes, preenchimento, cada zona contra o STL de origem, malhas fechadas e a mesma variante do FE (<a class=\"rv-x\" href=\"#ref-E1\" data-ref=\"E1\">[E1]</a>). Resultado: 0 erros. Script: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/sai_pacote_final.py\" target=\"_blank\" rel=\"noopener\"><code>sai_pacote_final.py</code></a>.</li><li>Pasta: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/modelos/SAI_final\" target=\"_blank\" rel=\"noopener\"><code>modelos/SAI_final/</code></a> · conferência: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/modelos/SAI_final/manifesto.json\" target=\"_blank\" rel=\"noopener\"><code>manifesto.json</code></a>.</li></ul>",
"busca": "a1 pacote modelos/sai_final/ : os arquivos que entraram nos calculos, prontos para imprimir 4 projetos do orcaslicer com as zonas internas (superior giroide 25% com 4 zonas; inferiores giroide 20% com 3 zonas; 8 pads em tpu 95a, giroide 40%), os stl das pecas e das zonas, o cad (step) da garra montada e dos pads, e um leia-me . conferencia por script: material, paredes, preenchimento, cada zona contra o stl de origem, malhas fechadas e a mesma variante do fe ( [e1] ). resultado: 0 erros. script: sai_pacote_final.py . pasta: modelos/sai_final/ conferencia: manifesto.json . arquivos 3d finais da garra sai"
}
]
},
{
"titulo": "Simulações no Autodesk Fusion",
"intro": "",
"itens": [
{
"cod": "F1",
"titulo": "Garra superior maciça em PA6-CF, 24 kg divididos nas 4 interfaces",
"html": "<p>Criado em 11/11/2026, 00:28.</p><div class=\"rv-tab\"><table><thead><tr><th>Item</th><th>Valor</th></tr></thead><tbody><tr><td>Estudo</td><td>tensão estática, linear, isotrópico</td></tr><tr><td>Peça</td><td>só a superior, <b>maciça (100%)</b>: sem preenchimento, paredes nem camadas</td></tr><tr><td>Malha</td><td>3 mm, parabólica, 498.261 nós e 339.001 elementos; sem refinamento adaptativo (0 etapas) e sem estudo de convergência</td></tr><tr><td>Fixação</td><td>furos da flange do robô</td></tr><tr><td>Carga</td><td>4 × 88,84 N em −Z = 355,36 N, ou seja, 24 kg × (9,81 + 5 m/s²), <b>dividida igualmente nas 4 interfaces (as duas asas)</b>. O caso de 24 kg numa asa só está no <a class=\"rv-x\" href=\"#ref-E1\" data-ref=\"E1\">[E1]</a>.</td></tr><tr><td>Material</td><td>Bambu PA6-CF: E 4.430 MPa, resistência 102 MPa (<a class=\"rv-x\" href=\"#ref-M1\" data-ref=\"M1\">[M1]</a>)</td></tr><tr><td>Resultado</td><td>von Mises máxima 3,23 MPa · 1ª principal 5,16 MPa · <b>FS mínimo 19,8</b></td></tr></tbody></table></div><ul><li>Relatório: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.html\" target=\"_blank\" rel=\"noopener\"><code>SAMI_PA6CF_24kg_Relatorio_Fusion.html</code></a> (texto: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.txt\" target=\"_blank\" rel=\"noopener\"><code>.txt</code></a>).</li></ul>",
"busca": "f1 garra superior macica em pa6-cf, 24 kg divididos nas 4 interfaces criado em 11/11/2026, 00:28. item valor estudo tensao estatica, linear, isotropico peca so a superior, macica (100%) : sem preenchimento, paredes nem camadas malha 3 mm, parabolica, 498.261 nos e 339.001 elementos; sem refinamento adaptativo (0 etapas) e sem estudo de convergencia fixacao furos da flange do robo carga 4 88,84 n em z = 355,36 n, ou seja, 24 kg (9,81 + 5 m/s2), dividida igualmente nas 4 interfaces (as duas asas) . o caso de 24 kg numa asa so esta no [e1] . material bambu pa6-cf: e 4.430 mpa, resistencia 102 mpa ( [m1] ) resultado von mises maxima 3,23 mpa 1a principal 5,16 mpa fs minimo 19,8 relatorio: sami_pa6cf_24kg_relatorio_fusion.html (texto: .txt ). simulacoes no autodesk fusion"
},
{
"cod": "F2",
"titulo": "Mesma garra em Tritan TX1001 (referência da garra atual)",
"html": "<p>Criado em 11/11/2026, 00:58.</p><ul><li>Mesma malha, fixação e carga do <a class=\"rv-x\" href=\"#ref-F1\" data-ref=\"F1\">[F1]</a>.</li><li>Material: E 1.548 MPa, resistência 58 MPa (<a class=\"rv-x\" href=\"#ref-M3\" data-ref=\"M3\">[M3]</a>).</li><li>Resultado: von Mises máxima 3,22 MPa · 1ª principal 5,03 MPa · <b>FS mínimo 11,5</b>.</li><li>O FS 11,5 corresponde ao critério de ruptura (58 ÷ 5,03), mas o cabeçalho do relatório exportado mostra \"resistência a escoamento\". Pelo escoamento seria 13,3 (43 ÷ 3,22). Conferir no Fusion.</li><li>O PA6-CF teve cerca de <b>65% menos deslocamento</b> que o Tritan.</li><li>Relatório: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_TRITAN_24kg_Relatorio_Fusion.html\" target=\"_blank\" rel=\"noopener\"><code>SAMI_TRITAN_24kg_Relatorio_Fusion.html</code></a>.</li><li>Evidência (hash SHA-256 do arquivo original): <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/SAMI_TRITAN_24kg_Relatorio_Fusion_evidence.json\" target=\"_blank\" rel=\"noopener\"><code>_evidence.json</code></a>.</li><li>Comparação e limites dos dois estudos: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/preparacao_garra/COMPARACAO_SAMI_2026-11-11.md\" target=\"_blank\" rel=\"noopener\"><code>COMPARACAO_SAMI_2026-11-11.md</code></a>.</li></ul>",
"busca": "f2 mesma garra em tritan tx1001 (referencia da garra atual) criado em 11/11/2026, 00:58. mesma malha, fixacao e carga do [f1] . material: e 1.548 mpa, resistencia 58 mpa ( [m3] ). resultado: von mises maxima 3,22 mpa 1a principal 5,03 mpa fs minimo 11,5 . o fs 11,5 corresponde ao criterio de ruptura (58 5,03), mas o cabecalho do relatorio exportado mostra \"resistencia a escoamento\". pelo escoamento seria 13,3 (43 3,22). conferir no fusion. o pa6-cf teve cerca de 65% menos deslocamento que o tritan. relatorio: sami_tritan_24kg_relatorio_fusion.html . evidencia (hash sha-256 do arquivo original): _evidence.json . comparacao e limites dos dois estudos: comparacao_sami_2026-11-11.md . simulacoes no autodesk fusion"
},
{
"cod": "F3",
"titulo": "Estudo de conferência do método: esfera de 50 mm, 100 N",
"html": "<ul><li>Modelo: esfera maciça de 50 mm, calota de baixo fixa e 100 N na calota de cima.</li><li>Material: SUNLU ABS-Like.</li><li>Arquivos: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/Esfera_SUNLU_100N_Relatorio_Fusion.html\" target=\"_blank\" rel=\"noopener\"><code>Esfera_SUNLU_100N_Relatorio_Fusion.html</code></a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/fusion/RESULTADOS_ESFERA_SUNLU.md\" target=\"_blank\" rel=\"noopener\"><code>RESULTADOS_ESFERA_SUNLU.md</code></a>.</li></ul>",
"busca": "f3 estudo de conferencia do metodo: esfera de 50 mm, 100 n modelo: esfera macica de 50 mm, calota de baixo fixa e 100 n na calota de cima. material: sunlu abs-like. arquivos: esfera_sunlu_100n_relatorio_fusion.html e resultados_esfera_sunlu.md . simulacoes no autodesk fusion"
},
{
"cod": "F4",
"titulo": "Garra R07 com preenchimento: não resolvido no Fusion",
"html": "<ul><li>O modelo de 2 corpos (casca e núcleo homogeneizado) foi montado.</li><li>O solve parou num erro de malha na casca.</li><li>Registro: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md\" target=\"_blank\" rel=\"noopener\"><code>RELATORIO_R07.md</code>, seção 4</a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/fusion/fusion_build_2corpos.json\" target=\"_blank\" rel=\"noopener\"><code>fusion_build_2corpos.json</code></a>.</li><li>Por isso o R07 usa o FE próprio (<a class=\"rv-x\" href=\"#ref-E1\" data-ref=\"E1\">[E1]</a>), com o fator de pico 2,2, calibrado contra o Fusion <a class=\"rv-x\" href=\"#ref-F1\" data-ref=\"F1\">[F1]</a>: a mesma peça maciça, com a mesma carga, dá von Mises 3,23 MPa no Fusion e 1,46 MPa no FE por voxels (3,23 ÷ 1,46 = 2,2; o deslocamento bate: 0,080 × 0,078 mm).</li></ul>",
"busca": "f4 garra r07 com preenchimento: nao resolvido no fusion o modelo de 2 corpos (casca e nucleo homogeneizado) foi montado. o solve parou num erro de malha na casca. registro: relatorio_r07.md , secao 4 e fusion_build_2corpos.json . por isso o r07 usa o fe proprio ( [e1] ), com o fator de pico 2,2, calibrado contra o fusion [f1] : a mesma peca macica, com a mesma carga, da von mises 3,23 mpa no fusion e 1,46 mpa no fe por voxels (3,23 1,46 = 2,2; o deslocamento bate: 0,080 0,078 mm). simulacoes no autodesk fusion"
}
]
},
{
"titulo": "Fatiamentos (OrcaSlicer)",
"intro": "",
"itens": [
{
"cod": "O1",
"titulo": "Garra R07 com e sem esqueleto, nas bases 20% e 25%",
"html": "<ul><li>Resultado (sem esqueleto): 1.432,8 g de peças, 1.744,5 g de filamento e 75,2 h de impressão.</li><li>Tempo por peça na K1 Max: superior 34,2 h, inferior esquerda 20,5 h, inferior direita 20,5 h. Com os 8 PADs (<a class=\"rv-x\" href=\"#ref-O3\" data-ref=\"O3\">[O3]</a>, 11,0 h), o SAI inteiro leva <b>86,2 h</b> (cerca de 3,6 dias de impressora).</li><li>O Orca avisa, em todas as peças de PA6-CF, que o bico precisa ser mais duro que o de latão (aviso <code>1000C002</code> nos logs). Por isso a troca para o bico de aço endurecido. A ficha do material diz o mesmo (<a class=\"rv-x\" href=\"#ref-M1\" data-ref=\"M1\">[M1]</a>).</li><li>Peça superior de Tritan para comparação: <b>35,1 h</b>. É a garra atual fatiada com favo 3D 30% no mesmo perfil (80,5 h para as 3 peças, <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/DECISAO_ESQUELETO.json\" target=\"_blank\" rel=\"noopener\"><code>decisao/DECISAO_ESQUELETO.json</code></a>) × 43,65%, a parte da peça superior na massa (<a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/peso_conjunto.csv\" target=\"_blank\" rel=\"noopener\"><code>decisao/peso_conjunto.csv</code></a>).</li><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_fatiamento_base25.json\" target=\"_blank\" rel=\"noopener\"><code>orca/r07_fatiamento_base25.json</code></a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_fatiamento_base20.json\" target=\"_blank\" rel=\"noopener\"><code>orca/r07_fatiamento_base20.json</code></a>.</li><li>Logs de cada peça: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/05_Orca/R07\" target=\"_blank\" rel=\"noopener\"><code>brutos/desempenho/05_Orca/R07/</code></a>.</li></ul>",
"busca": "o1 garra r07 com e sem esqueleto, nas bases 20% e 25% resultado (sem esqueleto): 1.432,8 g de pecas, 1.744,5 g de filamento e 75,2 h de impressao. tempo por peca na k1 max: superior 34,2 h, inferior esquerda 20,5 h, inferior direita 20,5 h. com os 8 pads ( [o3] , 11,0 h), o sai inteiro leva 86,2 h (cerca de 3,6 dias de impressora). o orca avisa, em todas as pecas de pa6-cf, que o bico precisa ser mais duro que o de latao (aviso 1000c002 nos logs). por isso a troca para o bico de aco endurecido. a ficha do material diz o mesmo ( [m1] ). peca superior de tritan para comparacao: 35,1 h . e a garra atual fatiada com favo 3d 30% no mesmo perfil (80,5 h para as 3 pecas, decisao/decisao_esqueleto.json ) 43,65%, a parte da peca superior na massa ( decisao/peso_conjunto.csv ). dados: orca/r07_fatiamento_base25.json e orca/r07_fatiamento_base20.json . logs de cada peca: brutos/desempenho/05_orca/r07/ . fatiamentos (orcaslicer)"
},
{
"cod": "O2",
"titulo": "Comparativo de preenchimentos",
"html": "<ul><li>Variantes: giroide 30/35/40%, Hexa3D 30% (padrão da garra instalada) e TPMS-D 40%.</li><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/r07_comparativo_fatiamento.json\" target=\"_blank\" rel=\"noopener\"><code>orca/r07_comparativo_fatiamento.json</code></a>.</li></ul>",
"busca": "o2 comparativo de preenchimentos variantes: giroide 30/35/40%, hexa3d 30% (padrao da garra instalada) e tpms-d 40%. dados: orca/r07_comparativo_fatiamento.json . fatiamentos (orcaslicer)"
},
{
"cod": "O3",
"titulo": "8 PADs em TPU 95A, giroide 40%, 3 paredes",
"html": "<ul><li>Resultado: 139,0 g e 11,0 h.</li><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/pads_tpu95a_fatiamento.json\" target=\"_blank\" rel=\"noopener\"><code>orca/pads_tpu95a_fatiamento.json</code></a>.</li></ul>",
"busca": "o3 8 pads em tpu 95a, giroide 40%, 3 paredes resultado: 139,0 g e 11,0 h. dados: orca/pads_tpu95a_fatiamento.json . fatiamentos (orcaslicer)"
},
{
"cod": "O4",
"titulo": "Camadas reais lidas do G-code",
"html": "<p>(figuras do slide Giroide).</p><ul><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/orca/camadas_r07.json\" target=\"_blank\" rel=\"noopener\"><code>orca/camadas_r07.json</code></a>.</li><li>Script: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_camadas.py\" target=\"_blank\" rel=\"noopener\"><code>r07_camadas.py</code></a>.</li></ul>",
"busca": "o4 camadas reais lidas do g-code (figuras do slide giroide). dados: orca/camadas_r07.json . script: r07_camadas.py . fatiamentos (orcaslicer)"
},
{
"cod": "O5",
"titulo": "Fatiamentos completos com G-code (R04, R06 e R07)",
"html": "<ul><li>Disponíveis na <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/releases/tag/dados-2026-11-12\" target=\"_blank\" rel=\"noopener\">Release <code>dados-2026-11-12</code></a>.</li></ul>",
"busca": "o5 fatiamentos completos com g-code (r04, r06 e r07) disponiveis na release dados-2026-11-12 . fatiamentos (orcaslicer)"
}
]
},
{
"titulo": "Simulações próprias (Python)",
"intro": "",
"itens": [
{
"cod": "E1",
"titulo": "FE estático por voxels da garra montada (superior + inferiores)",
"html": "<p>Script: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_montagem.py\" target=\"_blank\" rel=\"noopener\"><code>r07_montagem.py</code></a>.</p><p>Método:</p><ul><li>Elementos: voxels de 3 mm, hexaedros de 8 nós.</li><li>Paredes em PA6-CF transversalmente isotrópico: XY 4.430 MPa, Z 2.170 MPa.</li><li>Giroide homogeneizado por Gibson-Ashby (<a class=\"rv-x\" href=\"#ref-L1\" data-ref=\"L1\">[L1]</a>).</li><li>Engaste nos 6 furos da flange.</li><li>Carga numa asa = massa × (g + 5 m/s²).</li><li>Critério de falha: tração entre camadas (Z). Pico calibrado no Fusion (× 2,2).</li></ul><p>Resultado da garra SAI:</p><ul><li>Rompe com <b>93,3 kg</b> numa asa (PA6-CF) ou 35,4 kg (pior colagem, PAHT CF15).</li><li>FS a 24 kg: 3,89.</li></ul><p>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/montagem/montagem_R07_SEM.json\" target=\"_blank\" rel=\"noopener\"><code>montagem/montagem_R07_SEM.json</code></a>, <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/montagem/montagem_resumo.json\" target=\"_blank\" rel=\"noopener\"><code>montagem/montagem_resumo.json</code></a>.</p>",
"busca": "e1 fe estatico por voxels da garra montada (superior + inferiores) script: r07_montagem.py . metodo: elementos: voxels de 3 mm, hexaedros de 8 nos. paredes em pa6-cf transversalmente isotropico: xy 4.430 mpa, z 2.170 mpa. giroide homogeneizado por gibson-ashby ( [l1] ). engaste nos 6 furos da flange. carga numa asa = massa (g + 5 m/s2). criterio de falha: tracao entre camadas (z). pico calibrado no fusion ( 2,2). resultado da garra sai: rompe com 93,3 kg numa asa (pa6-cf) ou 35,4 kg (pior colagem, paht cf15). fs a 24 kg: 3,89. dados: montagem/montagem_r07_sem.json , montagem/montagem_resumo.json . simulacoes proprias (python)"
},
{
"cod": "E2",
"titulo": "Tranco: FE transiente 3D da peça superior",
"html": "<p>Script: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_impacto.py\" target=\"_blank\" rel=\"noopener\"><code>r07_impacto.py</code></a>.</p><ul><li>Método: 24 kg aplicados numa asa em 10 ms; integração de Newmark; amortecimento de Rayleigh de 3%.</li><li>Resultado: fator dinâmico 1,71; tensão Z de pico 18,1 MPa; FS 2,65 (PA6-CF).</li><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/impacto/impacto_F25_SEM.json\" target=\"_blank\" rel=\"noopener\"><code>impacto/impacto_F25_SEM.json</code></a>.</li></ul>",
"busca": "e2 tranco: fe transiente 3d da peca superior script: r07_impacto.py . metodo: 24 kg aplicados numa asa em 10 ms; integracao de newmark; amortecimento de rayleigh de 3%. resultado: fator dinamico 1,71; tensao z de pico 18,1 mpa; fs 2,65 (pa6-cf). dados: impacto/impacto_f25_sem.json . simulacoes proprias (python)"
},
{
"cod": "E3",
"titulo": "Impacto no PAD: modelo reduzido de molas (1D)",
"html": "<ul><li>Caso: esfera de 263 g a 1 m/s.</li><li>Resultado: pico de 450,9 N sem PAD e 168,5 N com PAD, ou seja, <b>−62,6%</b> dentro das hipóteses.</li><li><b>Não é FE da garra real.</b></li><li>Relatório: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/brutos/impacto_pad_hexa15/01_Relatorio/RELATORIO_SAMI_HEXA15.md\" target=\"_blank\" rel=\"noopener\"><code>RELATORIO_SAMI_HEXA15.md</code></a>.</li><li>Limites do PAD (cerca de 240 N para esmagar e 1.380 N para quebrar a garra): <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/impacto/pad_limites.json\" target=\"_blank\" rel=\"noopener\"><code>impacto/pad_limites.json</code></a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/pad_limites.py\" target=\"_blank\" rel=\"noopener\"><code>pad_limites.py</code></a>.</li></ul>",
"busca": "e3 impacto no pad: modelo reduzido de molas (1d) caso: esfera de 263 g a 1 m/s. resultado: pico de 450,9 n sem pad e 168,5 n com pad, ou seja, 62,6% dentro das hipoteses. nao e fe da garra real. relatorio: relatorio_sami_hexa15.md . limites do pad (cerca de 240 n para esmagar e 1.380 n para quebrar a garra): impacto/pad_limites.json e pad_limites.py . simulacoes proprias (python)"
},
{
"cod": "E4",
"titulo": "Fadiga, fluência e desgaste",
"html": "<ul><li>Método:<ul><li>curva S-N normalizada, σ/S = 1 − 0,10·log₁₀N;</li><li>regra de Miner (<a class=\"rv-x\" href=\"#ref-L2\" data-ref=\"L2\">[L2]</a>);</li><li>fluência com módulo de 0,70 E em 1.000 h e 0,55 E em 10.000 h;</li><li>desgaste dos furos pela lei de Archard (<a class=\"rv-x\" href=\"#ref-L3\" data-ref=\"L3\">[L3]</a>).</li></ul></li><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/fadiga/r07_vida.json\" target=\"_blank\" rel=\"noopener\"><code>fadiga/r07_vida.json</code></a>.</li></ul>",
"busca": "e4 fadiga, fluencia e desgaste metodo: curva s-n normalizada, /s = 1 0,10log10n; regra de miner ( [l2] ); fluencia com modulo de 0,70 e em 1.000 h e 0,55 e em 10.000 h; desgaste dos furos pela lei de archard ( [l3] ). dados: fadiga/r07_vida.json . simulacoes proprias (python)"
},
{
"cod": "E5",
"titulo": "Decisão com × sem esqueleto e peso do conjunto",
"html": "<ul><li>Dados: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/DECISAO_ESQUELETO.json\" target=\"_blank\" rel=\"noopener\"><code>decisao/DECISAO_ESQUELETO.json</code></a>, <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/dados_comparativos.csv\" target=\"_blank\" rel=\"noopener\"><code>decisao/dados_comparativos.csv</code></a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/decisao/peso_conjunto.csv\" target=\"_blank\" rel=\"noopener\"><code>decisao/peso_conjunto.csv</code></a>.</li></ul>",
"busca": "e5 decisao com sem esqueleto e peso do conjunto dados: decisao/decisao_esqueleto.json , decisao/dados_comparativos.csv e decisao/peso_conjunto.csv . simulacoes proprias (python)"
},
{
"cod": "E6",
"titulo": "Estudo de custos e durabilidade",
"html": "<ul><li>Conteúdo: vida estimada de 12 a 36 meses, custo de aquisição completo e cenários de 24 e 36 meses.</li><li>Estudo: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/estudo_custos/ESTUDO_CUSTOS_DURABILIDADE.md\" target=\"_blank\" rel=\"noopener\"><code>estudo_custos/ESTUDO_CUSTOS_DURABILIDADE.md</code></a>.</li><li>Script: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/estudo_custos.py\" target=\"_blank\" rel=\"noopener\"><code>estudo_custos.py</code></a>.</li><li>Custo real em 2 anos (slides de Custos e Retorno): <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md\" target=\"_blank\" rel=\"noopener\"><code>custos/CUSTO_REAL.md</code></a>, com as entradas e fontes em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json\" target=\"_blank\" rel=\"noopener\"><code>custos/entradas_custo.json</code></a> e o modelo em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/custo_real.py\" target=\"_blank\" rel=\"noopener\"><code>custo_real.py</code></a>.</li></ul>",
"busca": "e6 estudo de custos e durabilidade conteudo: vida estimada de 12 a 36 meses, custo de aquisicao completo e cenarios de 24 e 36 meses. estudo: estudo_custos/estudo_custos_durabilidade.md . script: estudo_custos.py . custo real em 2 anos (slides de custos e retorno): custos/custo_real.md , com as entradas e fontes em custos/entradas_custo.json e o modelo em custo_real.py . simulacoes proprias (python)"
},
{
"cod": "E7",
"titulo": "Vídeos e figuras",
"html": "<ul><li>São renderizados só a partir dos campos já calculados; nenhum vídeo cria resultado novo.</li><li>Scripts: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_videos.py\" target=\"_blank\" rel=\"noopener\"><code>r07_videos.py</code></a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/r07_video_sai.py\" target=\"_blank\" rel=\"noopener\"><code>r07_video_sai.py</code></a>.</li><li>Números: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/videos/videos_r07.json\" target=\"_blank\" rel=\"noopener\"><code>videos/videos_r07.json</code></a>.</li></ul>",
"busca": "e7 videos e figuras sao renderizados so a partir dos campos ja calculados; nenhum video cria resultado novo. scripts: r07_videos.py e r07_video_sai.py . numeros: videos/videos_r07.json . simulacoes proprias (python)"
},
{
"cod": "V1",
"titulo": "Vídeo da linha de paletização (slide Processo)",
"html": "<ul><li>Desenho animado no <a class=\"rv-x\" href=\"#ref-S4\" data-ref=\"S4\">[S4]</a>, em tempo acelerado e fora de escala. Ilustração, não é simulação.</li><li>Números: só os dados da equipe (6 caixas por minuto, 2 caixas por ciclo, 40 caixas por palete em 4 camadas de 10, 12 itens e 12 kg por caixa). Com eles, um palete leva 6 min 40 s.</li><li>Projeto: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/hyperframes/linha_palete\" target=\"_blank\" rel=\"noopener\"><code>hyperframes/linha_palete/</code></a>.</li></ul>",
"busca": "v1 video da linha de paletizacao (slide processo) desenho animado no [s4] , em tempo acelerado e fora de escala. ilustracao, nao e simulacao. numeros: so os dados da equipe (6 caixas por minuto, 2 caixas por ciclo, 40 caixas por palete em 4 camadas de 10, 12 itens e 12 kg por caixa). com eles, um palete leva 6 min 40 s. projeto: hyperframes/linha_palete/ . simulacoes proprias (python)"
},
{
"cod": "V2",
"titulo": "Vídeos do PAD (slides PAD e Valor de teste)",
"html": "<ul><li>Slide PAD: animação do PAD como escudo, feita no <a class=\"rv-x\" href=\"#ref-S4\" data-ref=\"S4\">[S4]</a> com as forças do <a class=\"rv-x\" href=\"#ref-E3\" data-ref=\"E3\">[E3]</a> (451 → 169 N, −63%). A animação não calcula nada. Projeto: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/hyperframes/pad_escudo\" target=\"_blank\" rel=\"noopener\"><code>hyperframes/pad_escudo/</code></a>.</li><li>Slide Valor de teste: recorte sem legenda (mesmos 300 quadros, 10 s) do vídeo do estudo R03 (<a class=\"rv-x\" href=\"#ref-E3\" data-ref=\"E3\">[E3]</a>, <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/assets/video/impacto_pad_r03.mp4\" target=\"_blank\" rel=\"noopener\"><code>impacto_pad_r03.mp4</code></a>). O gráfico ao lado lê a série de forças do próprio R03.</li></ul>",
"busca": "v2 videos do pad (slides pad e valor de teste) slide pad: animacao do pad como escudo, feita no [s4] com as forcas do [e3] (451 169 n, 63%). a animacao nao calcula nada. projeto: hyperframes/pad_escudo/ . slide valor de teste: recorte sem legenda (mesmos 300 quadros, 10 s) do video do estudo r03 ( [e3] , impacto_pad_r03.mp4 ). o grafico ao lado le a serie de forcas do proprio r03. simulacoes proprias (python)"
},
{
"cod": "",
"titulo": "",
"html": "<p><b>Relatório técnico completo do R07:</b> <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md\" target=\"_blank\" rel=\"noopener\"><code>dados/RELATORIO_R07.md</code></a>.</p><p><b>Logs, JSON e CSV de todas as rodadas (R04 a R07):</b> <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos\" target=\"_blank\" rel=\"noopener\"><code>dados/brutos/</code></a>.</p><p><b>Campos de FE, modelos 3D, vídeos e fatiamentos completos:</b> <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/releases/tag/dados-2026-11-12\" target=\"_blank\" rel=\"noopener\">Release <code>dados-2026-11-12</code></a>.</p>",
"busca": "relatorio tecnico completo do r07: dados/relatorio_r07.md . logs, json e csv de todas as rodadas (r04 a r07): dados/brutos/ . campos de fe, modelos 3d, videos e fatiamentos completos: release dados-2026-11-12 . simulacoes proprias (python)"
}
]
},
{
"titulo": "Testes",
"intro": "",
"itens": [
{
"cod": "T1",
"titulo": "Ensaios de bancada recomendados (ainda não realizados)",
"html": "<p>Fonte: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/RELATORIO_R07.md\" target=\"_blank\" rel=\"noopener\"><code>RELATORIO_R07.md</code>, item 3.7</a>.</p><ol><li>Carga de prova: 24 kg numa asa por 1 min, critério do tipo EN 13155 (<a class=\"rv-x\" href=\"#ref-N1\" data-ref=\"N1\">[N1]</a>).</li><li>Ruptura numa asa.</li><li>Fadiga: 10⁵ ciclos de 0 a 24 kg.</li><li>Tranco com parada de emergência (acelerômetro).</li><li>Fluência: 168 h com 24 kg.</li></ol>",
"busca": "t1 ensaios de bancada recomendados (ainda nao realizados) fonte: relatorio_r07.md , item 3.7 . carga de prova: 24 kg numa asa por 1 min, criterio do tipo en 13155 ( [n1] ). ruptura numa asa. fadiga: 105 ciclos de 0 a 24 kg. tranco com parada de emergencia (acelerometro). fluencia: 168 h com 24 kg. testes"
},
{
"cod": "T2",
"titulo": "Testes do processo de simulação",
"html": "<ul><li>Verificação de malhas STL fechadas: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/02_STL_PAD\" target=\"_blank\" rel=\"noopener\"><code>02_STL_PAD/validacao_STL.json</code></a>.</li><li>Conferência dos fatiamentos: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/brutos/desempenho/06_Engenharia/R05_CONFERENCIA_ORCA\" target=\"_blank\" rel=\"noopener\"><code>06_Engenharia/R05_CONFERENCIA_ORCA/</code></a>.</li><li>Estudo de conferência da esfera: <a class=\"rv-x\" href=\"#ref-F3\" data-ref=\"F3\">[F3]</a>.</li></ul>",
"busca": "t2 testes do processo de simulacao verificacao de malhas stl fechadas: 02_stl_pad/validacao_stl.json . conferencia dos fatiamentos: 06_engenharia/r05_conferencia_orca/ . estudo de conferencia da esfera: [f3] . testes"
}
]
},
{
"titulo": "Materiais (fichas técnicas dos fabricantes)",
"intro": "",
"itens": [
{
"cod": "M1",
"titulo": "Bambu Lab PA6-CF, ficha V3.0",
"html": "<p>E XY 4.430 MPa; tração XY/Z 102/48 MPa; HDT 164 °C. <a href=\"https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf\" target=\"_blank\" rel=\"noopener\">store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf</a></p>",
"busca": "m1 bambu lab pa6-cf, ficha v3.0 e xy 4.430 mpa; tracao xy/z 102/48 mpa; hdt 164 c. store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "M2",
"titulo": "Forward AM Ultrafuse PAHT CF15, ficha v3.5",
"html": "<p>Tração XY/ZX 103,2/18,2 MPa; usado como pior caso de colagem. <a href=\"https://forward-am.com/wp-content/uploads/2024/10/Ultrafuse_PAHT_CF15_TDS_EN_v3.5-1.pdf\" target=\"_blank\" rel=\"noopener\">forward-am.com/wp-content/uploads/2024/10/Ultrafuse_PAHT_CF15_TDS_EN_v3.5-1.pdf</a></p>",
"busca": "m2 forward am ultrafuse paht cf15, ficha v3.5 tracao xy/zx 103,2/18,2 mpa; usado como pior caso de colagem. forward-am.com/wp-content/uploads/2024/10/ultrafuse_paht_cf15_tds_en_v3.5-1.pdf materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "M3",
"titulo": "Eastman Tritan TX1001",
"html": "<p>E 1.548 MPa; ruptura 58 MPa; material da garra atual (resina moldada). &lt;https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&amp;product=71070312&gt;</p>",
"busca": "m3 eastman tritan tx1001 e 1.548 mpa; ruptura 58 mpa; material da garra atual (resina moldada). <https://productcatalog.eastman.com/tds/proddatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312> materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "M4",
"titulo": "Bambu Lab TPU 95A HF, ficha V3.0",
"html": "<p>(PADs). <a href=\"https://store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/Bambu_TPU_95A_HF_Technical_Data_Sheet.pdf\" target=\"_blank\" rel=\"noopener\">store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/Bambu_TPU_95A_HF_Technical_Data_Sheet.pdf</a></p>",
"busca": "m4 bambu lab tpu 95a hf, ficha v3.0 (pads). store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/bambu_tpu_95a_hf_technical_data_sheet.pdf materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "M5",
"titulo": "Lubrizol ESTANE X-595A-11",
"html": "<p>, TPU 97A de referência para os PADs. <a href=\"https://www.lubrizol.com/-/media/Lubrizol/Engineered-Polymers/Documents/Engineered-Polymer-TDS/ESTANE-X595-A11.pdf\" target=\"_blank\" rel=\"noopener\">lubrizol.com/-/media/Lubrizol/Engineered-Polymers/Documents/Engineered-Polymer-TDS/ESTANE-X595-A11.pdf</a></p>",
"busca": "m5 lubrizol estane x-595a-11 , tpu 97a de referencia para os pads. lubrizol.com/-/media/lubrizol/engineered-polymers/documents/engineered-polymer-tds/estane-x595-a11.pdf materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "M6",
"titulo": "Universal Robots UR30, ficha técnica",
"html": "<p>Carga útil de 30 kg; usada para a folga de carga do robô no slide Processo. <a href=\"https://www.universal-robots.com/products/ur30/\" target=\"_blank\" rel=\"noopener\">universal-robots.com/products/ur30</a> · <a href=\"https://www.universal-robots.com/media/1829274/ur30_datasheet_web.pdf\" target=\"_blank\" rel=\"noopener\">universal-robots.com/media/1829274/ur30_datasheet_web.pdf</a></p>",
"busca": "m6 universal robots ur30, ficha tecnica carga util de 30 kg; usada para a folga de carga do robo no slide processo. universal-robots.com/products/ur30 universal-robots.com/media/1829274/ur30_datasheet_web.pdf materiais (fichas tecnicas dos fabricantes)"
},
{
"cod": "",
"titulo": "",
"html": "<ul><li>Cartões de material usados no FE: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/materiais/materiais_R07.json\" target=\"_blank\" rel=\"noopener\"><code>materiais/materiais_R07.json</code></a>.</li></ul>",
"busca": "cartoes de material usados no fe: materiais/materiais_r07.json . materiais (fichas tecnicas dos fabricantes)"
}
]
},
{
"titulo": "Literatura e normas",
"intro": "",
"itens": [
{
"cod": "L1",
"titulo": "",
"html": "<p>GIBSON, L. J.; ASHBY, M. F. <i>Cellular Solids: Structure and Properties</i>. 2. ed. Cambridge University Press, 1997. DOI 10.1017/CBO9781139878326. Fundamenta a lei do giroide homogeneizado.</p>",
"busca": "l1 gibson, l. j.; ashby, m. f. cellular solids: structure and properties . 2. ed. cambridge university press, 1997. doi 10.1017/cbo9781139878326. fundamenta a lei do giroide homogeneizado. literatura e normas"
},
{
"cod": "L2",
"titulo": "",
"html": "<p>MINER, M. A. Cumulative damage in fatigue. <i>Journal of Applied Mechanics</i>, v. 12, p. A159–A164, 1945. DOI 10.1115/1.4009458. Fundamenta a soma de dano da fadiga.</p>",
"busca": "l2 miner, m. a. cumulative damage in fatigue. journal of applied mechanics , v. 12, p. a159a164, 1945. doi 10.1115/1.4009458. fundamenta a soma de dano da fadiga. literatura e normas"
},
{
"cod": "L3",
"titulo": "",
"html": "<p>ARCHARD, J. F. Contact and rubbing of flat surfaces. <i>Journal of Applied Physics</i>, v. 24, p. 981–988, 1953. DOI 10.1063/1.1721448. Fundamenta o desgaste dos furos.</p>",
"busca": "l3 archard, j. f. contact and rubbing of flat surfaces. journal of applied physics , v. 24, p. 981988, 1953. doi 10.1063/1.1721448. fundamenta o desgaste dos furos. literatura e normas"
},
{
"cod": "L4",
"titulo": "",
"html": "<p>NIST. <i>Weld formation during material extrusion additive manufacturing</i> (colagem entre camadas). <a href=\"https://www.nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing\" target=\"_blank\" rel=\"noopener\">nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing</a></p>",
"busca": "l4 nist. weld formation during material extrusion additive manufacturing (colagem entre camadas). nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing literatura e normas"
},
{
"cod": "L5",
"titulo": "",
"html": "<p>NIST IR 8059. <i>Materials testing standards for additive manufacturing of polymer materials</i>. <a href=\"https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8059.pdf\" target=\"_blank\" rel=\"noopener\">nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8059.pdf</a></p>",
"busca": "l5 nist ir 8059. materials testing standards for additive manufacturing of polymer materials . nvlpubs.nist.gov/nistpubs/ir/2015/nist.ir.8059.pdf literatura e normas"
},
{
"cod": "L6",
"titulo": "",
"html": "<p>Estudo de orientação de impressão em polímeros com fibra (PMC11669830). <a href=\"https://pmc.ncbi.nlm.nih.gov/articles/PMC11669830/\" target=\"_blank\" rel=\"noopener\">pmc.ncbi.nlm.nih.gov/articles/PMC11669830</a></p>",
"busca": "l6 estudo de orientacao de impressao em polimeros com fibra (pmc11669830). pmc.ncbi.nlm.nih.gov/articles/pmc11669830 literatura e normas"
},
{
"cod": "L7",
"titulo": "",
"html": "<p>Fluência em peças impressas (arXiv 2302.11240). <a href=\"https://arxiv.org/abs/2302.11240\" target=\"_blank\" rel=\"noopener\">arxiv.org/abs/2302.11240</a></p>",
"busca": "l7 fluencia em pecas impressas (arxiv 2302.11240). arxiv.org/abs/2302.11240 literatura e normas"
},
{
"cod": "N1",
"titulo": "",
"html": "<p>EN 13155. <i>Cranes: Safety. Non-fixed load lifting attachments</i> (dispositivos de içamento, incluindo a vácuo). Usada como referência de critério para o ensaio de carga de prova.</p>",
"busca": "n1 en 13155. cranes: safety. non-fixed load lifting attachments (dispositivos de icamento, incluindo a vacuo). usada como referencia de criterio para o ensaio de carga de prova. literatura e normas"
}
]
},
{
"titulo": "Preços de mercado (slides de Custos e Retorno)",
"intro": "",
"itens": [
{
"cod": "P1",
"titulo": "Entradas do custo real, pesquisadas em nov/2026",
"html": "<p>Cada valor tem a fonte e a data no próprio arquivo: <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json\" target=\"_blank\" rel=\"noopener\"><code>custos/entradas_custo.json</code></a>. Os principais:</p><div class=\"rv-tab\"><table><thead><tr><th>Valor no slide</th><th>Fonte</th></tr></thead><tbody><tr><td>PA6-CF R$ 420/kg</td><td>Voolt3D R$ 420 e Creality Hyper PA6-CF R$ 434</td></tr><tr><td>TPU R$ 158/kg</td><td>equipe; mediana do mercado R$ 159,90 (melhorfilamento.com.br) e Brasfila R$ 158</td></tr><tr><td>Tritan R$ 220/kg</td><td>3DX CPE com certificado NSF 51 (loja3dxfilamentos.com.br)</td></tr><tr><td>Energia R$ 0,70/kWh</td><td>CPFL Paulista, tarifa A4 verde 2026 (REH 3.579/2026), com impostos</td></tr><tr><td>Técnico R$ 30,23/h</td><td>R$ 3.500/mês (Novo CAGED, via salario.com.br) × 1,9 de encargos ÷ 220 h</td></tr><tr><td>Impressora K1 Max R$ 5.500 em 5.000 h</td><td>lojas no Brasil (R$ 4.940 a 6.507); vida de referência de snapmaker.com e all3dp.com</td></tr><tr><td>Bico de aço endurecido</td><td>cerca de R$ 60 a cada 300 h com fibra de carbono</td></tr><tr><td>Refugo de 10% no PA6-CF</td><td>Filamentive, citado em PMC9706623 (hipótese)</td></tr></tbody></table></div><p>Modelo e revisão: <a class=\"rv-x\" href=\"#ref-E6\" data-ref=\"E6\">[E6]</a> e <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md\" target=\"_blank\" rel=\"noopener\"><code>custos/CUSTO_REAL.md</code></a>.</p>",
"busca": "p1 entradas do custo real, pesquisadas em nov/2026 cada valor tem a fonte e a data no proprio arquivo: custos/entradas_custo.json . os principais: valor no slide fonte pa6-cf r$ 420/kg voolt3d r$ 420 e creality hyper pa6-cf r$ 434 tpu r$ 158/kg equipe; mediana do mercado r$ 159,90 (melhorfilamento.com.br) e brasfila r$ 158 tritan r$ 220/kg 3dx cpe com certificado nsf 51 (loja3dxfilamentos.com.br) energia r$ 0,70/kwh cpfl paulista, tarifa a4 verde 2026 (reh 3.579/2026), com impostos tecnico r$ 30,23/h r$ 3.500/mes (novo caged, via salario.com.br) 1,9 de encargos 220 h impressora k1 max r$ 5.500 em 5.000 h lojas no brasil (r$ 4.940 a 6.507); vida de referencia de snapmaker.com e all3dp.com bico de aco endurecido cerca de r$ 60 a cada 300 h com fibra de carbono refugo de 10% no pa6-cf filamentive, citado em pmc9706623 (hipotese) modelo e revisao: [e6] e custos/custo_real.md . precos de mercado (slides de custos e retorno)"
}
]
},
{
"titulo": "Reciclagem (slide Sustentabilidade)",
"intro": "",
"itens": [
{
"cod": "R1",
"titulo": "",
"html": "<p>Política Nacional de Resíduos Sólidos, Lei 12.305/2010 (separação e destinação dos resíduos). <a href=\"https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12305.htm\" target=\"_blank\" rel=\"noopener\">planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12305.htm</a></p>",
"busca": "r1 politica nacional de residuos solidos, lei 12.305/2010 (separacao e destinacao dos residuos). planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12305.htm reciclagem (slide sustentabilidade)"
},
{
"cod": "R2",
"titulo": "",
"html": "<p>BASF, programa CirculAí: recolhe sobras de poliamida PA 6 e PA 66, com ou sem carga, no Brasil. A página não cita fibra de carbono: <b>confirmar com a BASF</b> se aceita PA6-CF. <a href=\"https://download.basf.com/p1/8a80821284d444010184e5e90a2e57d4/pt/CIRCULA%C3%8D_Brochure_South_America_portugu%C3%AAs.pdf?view\" target=\"_blank\" rel=\"noopener\">download.basf.com/p1/8a80821284d444010184e5e90a2e57d4/pt/CIRCULA%C3%8D_Brochure_South_America_portugu%C3%AAs.pdf?view</a></p>",
"busca": "r2 basf, programa circulai: recolhe sobras de poliamida pa 6 e pa 66, com ou sem carga, no brasil. a pagina nao cita fibra de carbono: confirmar com a basf se aceita pa6-cf. download.basf.com/p1/8a80821284d444010184e5e90a2e57d4/pt/circula%c3%8d_brochure_south_america_portugu%c3%aas.pdf?view reciclagem (slide sustentabilidade)"
},
{
"cod": "R3",
"titulo": "",
"html": "<p>Reaproveitamento de refugo de poliuretano em solados de calçado (Ecycle). O texto fala de PU, a família do TPU, e não de TPU impresso: <b>confirmar com um reciclador</b> do polo calçadista. <a href=\"https://www.ecycle.com.br/component/content/article/35-atitude/884-poliuretanoo-desconhecido-muito-presente-no-cotidiano.html\" target=\"_blank\" rel=\"noopener\">ecycle.com.br/component/content/article/35-atitude/884-poliuretanoo-desconhecido-muito-presente-no-cotidiano.html</a></p>",
"busca": "r3 reaproveitamento de refugo de poliuretano em solados de calcado (ecycle). o texto fala de pu, a familia do tpu, e nao de tpu impresso: confirmar com um reciclador do polo calcadista. ecycle.com.br/component/content/article/35-atitude/884-poliuretanoo-desconhecido-muito-presente-no-cotidiano.html reciclagem (slide sustentabilidade)"
},
{
"cod": "",
"titulo": "",
"html": "<p>Os destinos do slide (recicladores do polo calçadista para o TPU e de polímeros de engenharia para o PA6-CF) são <b>proposta da equipe</b>. As fontes acima mostram que a reciclagem é possível, mas nenhum comprador foi contatado.</p>",
"busca": "os destinos do slide (recicladores do polo calcadista para o tpu e de polimeros de engenharia para o pa6-cf) sao proposta da equipe . as fontes acima mostram que a reciclagem e possivel, mas nenhum comprador foi contatado. reciclagem (slide sustentabilidade)"
}
]
},
{
"titulo": "Dados informados pela equipe",
"intro": "",
"itens": [
{
"cod": "Equipe",
"titulo": "Dados informados pela equipe",
"html": "<p>Origem: equipe do projeto, com base na linha da Ajinomoto. Ficam registrados em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/README.md\" target=\"_blank\" rel=\"noopener\"><code>dados/README.md</code></a> e em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json\" target=\"_blank\" rel=\"noopener\"><code>custos/entradas_custo.json</code></a>.</p><ul><li><b>Linha:</b> cerca de 6 caixas por minuto; 2 caixas por ciclo do robô (uma em cada asa); 40 caixas por palete, em 4 camadas de 10; 12 itens e 12 kg por caixa.</li><li><b>Garra instalada:</b> Tritan, 2,834 kg; quebra a cada 3 meses (4 vezes por ano), rompendo na raiz.</li><li><b>Paradas:</b> a troca da garra para a linha 45 min (280 caixas); a troca só dos PADs leva cerca de 20 min (120 caixas, estimativa da equipe). Parada para manuseio a cada 45 min de operação.</li><li><b>Manutenção proposta:</b> garra SAI nova a cada 24 meses e PADs a cada trimestre, com data marcada.</li><li><b>Impressão:</b> a mesma impressora que imprime o Tritan imprime o PA6-CF, trocando o bico (<a class=\"rv-x\" href=\"#ref-O1\" data-ref=\"O1\">[O1]</a>).</li><li><b>Prazos:</b> Tritan importado 15 a 20 dias; PA6-CF nacional 5 a 8 dias úteis.</li><li><b>Matriz de prioridade</b> (slide Ideias anteriores): notas de valor e complexidade de 0 a 10 dadas pela equipe.</li><li><b>Valores da equipe que o modelo de custo trocou ou deixou de usar:</b> PA6-CF R$ 258/kg (o modelo usa R$ 420, preço de mercado), R$ 250 por quebra do Tritan, bico de R$ 23,50 de uma vez e R$ 84.000 por parada. O porquê está em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/CUSTO_REAL.md\" target=\"_blank\" rel=\"noopener\"><code>custos/CUSTO_REAL.md</code></a>.</li></ul>",
"busca": "equipe dados informados pela equipe origem: equipe do projeto, com base na linha da ajinomoto. ficam registrados em dados/readme.md e em custos/entradas_custo.json . linha: cerca de 6 caixas por minuto; 2 caixas por ciclo do robo (uma em cada asa); 40 caixas por palete, em 4 camadas de 10; 12 itens e 12 kg por caixa. garra instalada: tritan, 2,834 kg; quebra a cada 3 meses (4 vezes por ano), rompendo na raiz. paradas: a troca da garra para a linha 45 min (280 caixas); a troca so dos pads leva cerca de 20 min (120 caixas, estimativa da equipe). parada para manuseio a cada 45 min de operacao. manutencao proposta: garra sai nova a cada 24 meses e pads a cada trimestre, com data marcada. impressao: a mesma impressora que imprime o tritan imprime o pa6-cf, trocando o bico ( [o1] ). prazos: tritan importado 15 a 20 dias; pa6-cf nacional 5 a 8 dias uteis. matriz de prioridade (slide ideias anteriores): notas de valor e complexidade de 0 a 10 dadas pela equipe. valores da equipe que o modelo de custo trocou ou deixou de usar: pa6-cf r$ 258/kg (o modelo usa r$ 420, preco de mercado), r$ 250 por quebra do tritan, bico de r$ 23,50 de uma vez e r$ 84.000 por parada. o porque esta em custos/custo_real.md . dados informados pela equipe"
}
]
},
{
"titulo": "Uso de inteligência artificial",
"intro": "",
"itens": [
{
"cod": "C1",
"titulo": "Claude Code (Anthropic): apoio nos testes e na organização dos dados",
"html": "<ul><li>O projeto teve ajuda do Claude Code, assistente de programação com IA da Anthropic, na parte de testes, como a aplicação em Python (<a class=\"rv-x\" href=\"#ref-S3\" data-ref=\"S3\">[S3]</a>, scripts em <a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/tree/main/dados/scripts\" target=\"_blank\" rel=\"noopener\"><code>dados/scripts/</code></a>).</li><li><b>Regra de uso:</b> o Claude Code foi proibido de buscar informações novas e de mudar o modelo sem permissão da equipe.</li><li><b>Para que foi usado:</b><ul><li>organização dos dados;</li><li>validação dos resultados;</li><li>automação dos testes no Autodesk Fusion (<a class=\"rv-x\" href=\"#ref-S1\" data-ref=\"S1\">[S1]</a>);</li><li>identificação de falhas e eventos nos dados.</li></ul></li><li>Exemplo: a conferência byte a byte das imagens do Fusion (<a href=\"https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/scripts/evidencias_fusion.py\" target=\"_blank\" rel=\"noopener\"><code>evidencias_fusion.py</code></a>) achou uma figura corrompida na cópia publicada do relatório <a class=\"rv-x\" href=\"#ref-F1\" data-ref=\"F1\">[F1]</a>, que foi restaurada a partir do arquivo original.</li><li>Produto: <a href=\"https://claude.com/claude-code\" target=\"_blank\" rel=\"noopener\">claude.com/claude-code</a></li></ul>",
"busca": "c1 claude code (anthropic): apoio nos testes e na organizacao dos dados o projeto teve ajuda do claude code, assistente de programacao com ia da anthropic, na parte de testes, como a aplicacao em python ( [s3] , scripts em dados/scripts/ ). regra de uso: o claude code foi proibido de buscar informacoes novas e de mudar o modelo sem permissao da equipe. para que foi usado: organizacao dos dados; validacao dos resultados; automacao dos testes no autodesk fusion ( [s1] ); identificacao de falhas e eventos nos dados. exemplo: a conferencia byte a byte das imagens do fusion ( evidencias_fusion.py ) achou uma figura corrompida na copia publicada do relatorio [f1] , que foi restaurada a partir do arquivo original. produto: claude.com/claude-code uso de inteligencia artificial"
}
]
}
]
};
