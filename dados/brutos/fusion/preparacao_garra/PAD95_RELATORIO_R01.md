# SAMI — PADs de proteção PU/TPU 95A, revisão R01

**11/11/2026 — protótipo CAD criado, estudo de evento iniciado e não resolvido.**

![PADs laranja montados na geometria real](SAMI_PAD95_MONTAGEM_R01.png)

## Entrega e alcance

Foram criadas quatro capas nas regiões A1–A4 correspondentes aos quatro encontros entre o corpo superior e os suportes inferiores destacados em vermelho. Cada capa é dividida em duas metades: oito peças independentes, removíveis e propostas como itens de sacrifício. A montagem original e os resultados estáticos anteriores foram preservados. Não foi reutilizada a meia-lua ilustrativa como geometria da garra.

Os PADs acompanham o contorno cilíndrico das interfaces e recebem recortes derivados do corpo real e dos componentes vizinhos do STEP. O exterior tem transições cônicas para reduzir saliências; isso é um tratamento geométrico de contorno, sem estudo aerodinâmico. As capas protegem a faixa lateral das interfaces, não toda a superfície superior dos braços.

Arquivos: montagem nativa `SAMI_PAD95_CONFORMAL_R01.f3d`; montagem intercambiável `SAMI_PAD95_MONTAGEM_R01.step`; oito STL de impressão no pacote; estudo separado `SAMI_PAD95_EVENTO_A1_ESTUDO_PENDENTE.f3d`. O Fusion foi deixado com a montagem completa aberta. Os arquivos locais são a entrega recuperável; não foi confirmado salvamento adicional no projeto de nuvem.

Os STL de impressão foram centralizados em XY e apoiados em Z=0, em milímetros. A verificação encontrou e removeu pares de triângulos coincidentes opostos de espessura zero na tesselação nativa, sem alterar o CAD. Os oito arquivos finais passaram na checagem de bordas fechadas/orientadas; diferença máxima de volume entre malha e BRep: 0,085%. Integridade dos arquivos F3D e do pacote ZIP verificada. Isso não substitui a prévia de camadas no fatiador.

## Geometria e retenção

| Item | R01 |
|---|---:|
| Regiões / metades por região | 4 / 2 |
| Raio nominal da flange | 31 mm |
| Raio interno nominal do PAD na faixa cilíndrica | 31,5 mm |
| Raio externo máximo | 39 mm |
| Espessura radial máxima nominal | 7,5 mm |
| Altura axial do envelope | 20,5 mm |
| Abertura entre metades | 0,8 mm |
| Canal para cinta de retenção | largura 3,5 mm / profundidade 1,2 mm |

A fixação proposta é um colar bipartido com cinta substituível no canal, aproveitando a geometria existente. Não há PU interposto na superfície de aperto dos parafusos da junta. Material, fecho, pré-tensão e resistência da cinta ainda precisam ser especificados; a cinta não foi modelada nem ensaiada. A retenção por atrito e o risco de arrancamento permanecem pendentes.

A folga radial de 0,5 mm vale para a região cilíndrica. Nas transições, o alívio foi obtido por subtração de uma cópia local ampliada da geometria, e não por um offset normal uniforme; a folga local precisa de conferência no protótipo. Não interpretar o desenho como encaixe aprovado para fabricação em série.

Verificação por interseção de sólidos no Fusion: oito corpos sólidos, cada um com uma única região conectada; nenhuma interpenetração volumétrica detectada contra o corpo superior e os dois suportes inferiores, com tolerância de verificação de 10⁻⁸ cm³. Isso verifica a posição estática no CAD. Não verifica articulação em todo o curso, mangueiras flexíveis, acesso de ferramentas, tolerâncias de impressão ou comportamento sob impacto.

## Material de referência e preenchimento

PU abrange diferentes poliuretanos. Como o pedido inclui impressão e preenchimento de 40%, adotou-se **TPU 95A para FFF**, referência **Polymaker PolyFlex TPU95 V5.4**, mantendo a possibilidade de substituir o fornecedor após caracterização. Não é uma média estatística de fornecedores nem um PU termofixo fundido.

Ficha: densidade 1,20–1,24 g/cm³, valor central adotado 1,22; E XY 33,6 ± 0,9 MPa; tensão a 100/200/300/400% de alongamento 11,1/15,0/21,0/25,8 MPa; alongamento na ruptura 551,2 ± 23,5%; dureza 95A. Corpos de prova a 100% de preenchimento, bico 230 °C, mesa 50 °C, duas paredes e três camadas de topo/base. [TDS oficial V5.4](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyFlex_TPU95_TDS_EN_V5.4.pdf?v=1731956391), cópia arquivada em `fontes_industriais`.

No cadastro básico do Fusion: densidade 1.220 kg/m³ e E 33,6 MPa; ν=0,49 é **hipótese de quase incompressibilidade**, não valor confirmado desse filamento. O cartão está identificado como não calibrado para 40%. Campos de resistência última, escoamento e propriedades térmicas sem dados aplicáveis ficaram ausentes no registro documental; zeros exigidos pelo cadastro não representam medições. O cadastro básico não contém uma lei válida de impacto do PAD.

Configuração inicial de fabricação proposta: núcleo gyroid a 40%, linha 0,4 mm, três perímetros (parede nominal 1,2 mm), camada 0,2 mm, seis camadas de topo e base (1,2 mm). São escolhas de projeto, não condições equivalentes aos corpos de prova da ficha. Confirmar a impressora, orientação, fluxo e dimensões. Os STL são envelopes fechados: **o gyroid ainda deve ser gerado no fatiador**. Não há malha interna gyroid explícita nos estudos.

O preenchimento descreve a estrutura interna, não uma propriedade química. A rigidez, a compressão e a densificação dependem do padrão, células, paredes e processo. Usar E × 0,40 ou densidade × 0,40 em todo o envelope omite cascas e não caracteriza o PAD. Um artigo primário sobre compressão de TPU foi arquivado para referência, mas seus corpos são a 100% e não foram transplantados para representar o núcleo desta peça. [Sardinha et al., 2025](https://doi.org/10.1108/RPJ-06-2024-0241).

## Impacto e distorção: o que foi preparado

Foi criado um documento reduzido com o corpo superior PA6-CF, oito metades de PAD e uma esfera impactante de aço. Também foi criado no Fusion o estudo **“A1 PAD95 40pct - PENDENTE CALIBRACAO”**, do tipo evento dinâmico, com duração proposta de 20 ms e 40 intervalos de saída.

| Hipótese de bancada para A1 | Valor |
|---|---:|
| Esfera de aço / densidade | raio 20 mm / 7.850 kg/m³ |
| Massa geométrica | 0,263056 kg |
| Folga inicial | 1 mm |
| Velocidades propostas | 0,5 / 1 / 2 m/s |
| Energias cinéticas correspondentes | 0,03288 / 0,13153 / 0,52611 J |

As energias foram calculadas por ½mv²; não são resultados do solver. O plano de velocidade aponta radialmente para A1. As velocidades, os apoios da flange e os contatos estão documentados como próximos itens de configuração; não estão aplicados e validados no estudo. Os braços inferiores não entram nesse submodelo. A massa efetiva real de colisão do robô pode ser muito diferente da esfera e não se resume à carga transportada.

O pré-check realizado bloqueou o cálculo: material com propriedades inválidas e ausência de contatos/conectores entre corpos independentes. Não houve job enviado, malha calculada ou solve novo. O aviso de duração informa que eventos típicos são menores que 1 ms e que cálculos acima de 12 horas são cancelados; a duração precisa ser revista a partir da resposta física e custo previsto, antes de qualquer envio.

Para comparar sem/com PAD, manter o mesmo impactor, energia, geometria, apoio e temperatura. Comparar força de contato versus tempo, impulso, tensão/deformação na PA-CF, compressão e retorno do PAD, eventual contato direto do impactor com a garra, arrancamento e balanço de energia. A geometria da peça sem PAD deve permitir o contato com o mesmo alvo, sem introduzir diferenças indevidas na energia inicial.

O Fusion aceita hiperelasticidade Mooney–Rivlin com duas constantes e parâmetro volumétrico derivados de ensaios. O modelo hiperelástico isolado é recuperável e não representa deformação permanente por desgaste. Uma curva de tração de material cheio não caracteriza compressão, histerese, taxa de deformação e densificação de um gyroid a 40%. [Modelo Autodesk](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/SIM-HYPERELASTIC-MATERIALS-CONCEPT.htm), [teoria e ajuste de constantes](https://help.autodesk.com/view/fusion360/ENU/?contextId=SIM-HYPERELASTIC-MATERIAL).

Consequentemente, **não foram calculados pico de impacto, porcentagem de proteção, distorção máxima do novo conjunto, ruptura ou energia dissipada**. O deslocamento de 0,080 mm do relatório anterior pertence ao corpo superior maciço sem esses PADs, sob outra carga estática; não é resultado desta revisão.

## Durabilidade e peça de sacrifício

Não existe estimativa defensável em horas ou impactos até a troca a partir de Shore 95A e E. Faltam curvas de compressão/descarga do PAD impresso, resposta cíclica e térmica, deformação permanente, rasgamento da retenção e desgaste nas contrapartes reais. A garra PA-CF também precisa de fadiga/fluência e dados de direção, umidade e temperatura. Não foi gerada uma vida útil numérica.

Plano de caracterização que permite estimar a durabilidade:

1. Imprimir amostras e PADs com a configuração entregue; registrar lote, umidade, massa, orientação e dimensão. Verificar montagem e retenção antes dos choques.
2. Medir compressão e descarga em 23/40/60 °C como ambientes de ensaio propostos. Obter força × curso, histerese e espessura residual; repetir após estabilização cíclica.
3. Ensaiar as três energias propostas separadamente, inicialmente em A1. Medir força transmitida e observar batimento direto na PA-CF; repetir nas demais interfaces quando o primeiro caso estiver calibrado.
4. Nos ensaios cíclicos, registrar dano e curso residual em marcos como 100, 1.000 e 10.000 impactos, ampliando o teste conforme o comportamento medido. Esses marcos são pontos de inspeção, não intervalos de substituição aprovados.
5. Ajustar lei cíclica/desgaste somente com dados de carga, percurso, temperatura e contraparte correspondentes. Fadiga da garra e substituição do PAD são critérios distintos.

Critérios propostos para desenvolvimento: trocar o PAD se expuser a garra ao contato, romper/soltar a retenção ou perder o curso protetor especificado no ensaio. O limite quantitativo precisa ser definido antes da validação. Ser sacrificial não garante que a garra permaneça sem dano em qualquer choque.

Para exposição 24/7, um ciclo de máquina hipotético de 10 s significa 8.640 ciclos/dia. Só converter ciclos de máquina em impactos quando a frequência de choques estiver medida. Horas de operação, ciclos de aperto e eventos de colisão não são a mesma variável.

## Massa

Volume total dos oito envelopes CAD: **72,6882 cm³**. Na densidade nominal 1,22 g/cm³, seriam **88,68 g se maciços**. O piso matemático sem cascas, apenas 40% desse volume, seria 35,47 g. A massa real de núcleo a 40% com paredes fica acima desse piso; deve vir do volume extrudado no fatiador e depois da balança. Não declarar 35,47 g como peso do projeto. Cintas e suportes de impressão não estão incluídos.

No cenário anterior, a troca de densidade no corpo superior maciço Tritan→PA6-CF economizava 125,21 g. Acrescentar esses PADs reduz a economia líquida; com os limites geométricos nominais acima, ela ficaria entre 36,53 e 89,74 g **apenas nessa comparação do corpo superior**, antes das cintas. Isso não estima a massa total da montagem nem confirma o Tritan instalado.

## Apresentação e economia de uso

A imagem entregue é uma visualização CAD, sem deformações simuladas. O Fusion oferece gravação AVI para resultados de evento resolvidos; ainda não há resultados para gravar uma animação física de impacto. Não foi criada uma animação ilustrativa com aparência de resultado calculado. [Gravação no Fusion](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-8185D3C3-D076-4CA4-8303-9E22E4107E98.htm).

Geometria, fontes, estado e casos foram gravados em disco para continuar pelo MCP compacto, sem refazer os estudos estáticos. Nenhum agente paralelo nem job de nuvem foi iniciado nesta revisão. Primeiro calibrar e resolver um caso A1; só depois expandir A2–A4 e temperaturas. Não há acesso ao saldo de uso do plano para garantir consumo dentro da janela de cinco horas.
