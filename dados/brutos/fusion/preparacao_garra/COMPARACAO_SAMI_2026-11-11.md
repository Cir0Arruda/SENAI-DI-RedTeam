# Garra SAMI — comparação de materiais e campanha Fusion

**Data:** 11/11/2026. **Estado:** dois estudos estáticos resolvidos; candidato PA12-CF bloqueado no pré-check. Impacto, PAD, temperatura, fadiga, fluência e desgaste não têm resultados calculados nesta campanha.

## 1. Conclusão da etapa

No modelo elástico exploratório do corpo superior maciço, Bambu PA6-CF apresentou aproximadamente 65% menos deslocamento que a referência Tritan TX1001, sob a mesma carga. A massa analítica desse corpo cai aproximadamente 125 g. Isso demonstra maior rigidez no modelo adotado, sem demonstrar superioridade ao impacto ou vida industrial.

Como alternativa para a próxima caracterização, foi selecionado **Polymaker Fiberon PA12-CF10 V1.1**, por densidade baixa e menor sensibilidade à umidade declarada frente a PA6/66. A seleção é condicional: o PA12-CF não é superior em todos os critérios. O cadastro documental e a ficha exploratória foram criados; o Fusion rejeitou o material no pré-check. Nenhum resultado foi gerado para esse estudo e nenhum valor de escoamento foi inventado para liberar o cálculo.

Interpretação de “trio”: Tritan, conforme o objetivo anterior. Os três candidatos estruturais documentados são Tritan TX1001, Bambu PA6-CF e Fiberon PA12-CF10. O PU é um quarto material, dedicado aos PADs, sem substituir automaticamente o corpo da garra.

## 2. Escopo real do modelo

Arquivo original: `Montagem_Geral_Garra.stp`, preservado. Documento de trabalho: **SAMI PA6CF - CORPO SUPERIOR - EXPLORATORIO 24kg**. Foi extraído o corpo `Corpo Supor`, com volume de **1.391,190996 cm³**, 2.676 faces e seção CAD maciça. A montagem completa tem componentes, fixadores e ventosas que não estão representados por esse corpo isolado.

As quatro faces inferiores das interfaces destacadas nas imagens receberam carga simultânea. Cada face tem aproximadamente 779,42 mm². Restrições XYZ foram aplicadas às paredes cilíndricas dos seis furos da flange, raio 4,2 mm. Apoios rígidos representam uma idealização da ligação ao robô.

Hipótese operacional: duas caixas totalizando 24 kg, gravidade 9,80665 m/s² e aceleração vertical adicional de 5 m/s². A força é 24 × (9,80665 + 5) = **355,3596 N**, igualmente distribuída: **88,8399 N por interface**, na direção −Z. Essa aceleração não foi medida na célula. Pressão média nominal em cada face: 0,114 MPa; não equivale à tensão local máxima.

Não estão incluídos: peso próprio, massa e inércia dos braços inferiores, torque/excentricidade adicional, pré-carga dos parafusos, flexibilidade da flange do robô, contato real das interfaces, distribuição desigual, perda de ventosas, PADs e impactos. Os 24 kg transportados não são automaticamente a massa efetiva de uma colisão do robô.

## 3. Resultados efetivamente resolvidos

| Grandeza | Estudo 1 — PA6-CF | Estudo 2 — Tritan |
|---|---:|---:|
| Estado | Resolvido | Resolvido |
| Módulo E usado, MPa | 4.430 | 1.548 |
| Poisson usado | 0,39, proxy | 0,38, proxy |
| Referência de resistência última, MPa | 102 | 58 |
| von Mises máxima, MPa | 3,232 | 3,222 |
| Primeira principal máxima, MPa | 5,163 | 5,025 |
| Deslocamento máximo, mm | ≈0,080 | ≈0,230 |
| Fator de segurança mínimo de referência | 19,755 | 11,542 |
| Nós / elementos | 498.261 / 339.001 | 498.261 / 339.001 |

Critério exibido pelo Fusion nos dois estudos: **resistência máxima à tração**. O fator de segurança depende desse critério e das propriedades atribuídas; não é uma carga admissível certificada e não deve ser reconstruído usando simplesmente resistência/von Mises. A referência Tritan é resina moldada; o PA6-CF usa dados de corpos FFF XY. Portanto a comparação de margem não é uma comparação caracterizada entre duas peças impressas equivalentes.

As tensões são próximas porque o caso é predominantemente controlado por força e geometria. A maior rigidez do PA6-CF reduz a deformação. Isso não implica maior ductilidade ou maior energia absorvida antes da ruptura. Diferenças de Poisson também alteram a distribuição local.

Malha alvo de 3 mm, elementos parabólicos curvos, zero refinamento adaptativo. Não foi executado estudo de convergência nem balanço global da soma de reações. Picos perto dos apoios rígidos e furos precisam dessa verificação antes de decisões de dimensionamento.

Evidência: relatórios nativos `SAMI_PA6CF_24kg_Relatorio_Fusion.html` e `SAMI_TRITAN_24kg_Relatorio_Fusion.html`. A exportação deixou células de extremos vazias; os números foram transcritos das legendas das figuras 14 (von Mises), 15 (primeira principal) e 17 (deslocamento). O fator de segurança foi conferido na interface de resultados. O arquivo F3D final tem integridade ZIP/CRC verificada; recuperar resultados de nuvem pode exigir documento e conta originais.

## 4. Fichas e rastreabilidade

### Referências estruturais já calculadas

**Bambu PA6-CF V3.0:** densidade 1,09 g/cm³; E XY 4.430 MPa; resistência à tração XY/Z 102/48 MPa; Tg 68 °C; HDT a 1,8 MPa 164 °C. Corpos de prova secos, 100% de preenchimento, tratamento de 80 °C por 12 h. O cálculo usa XY como isotrópico e ν=0,39 de outra matriz PA6. Z, umidade, temperatura variável e falha interlaminar não são representados. [Ficha do fabricante](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf).

**Eastman Tritan TX1001:** densidade 1,18 g/cm³; E 1.548 MPa; escoamento 43 MPa; resistência na ruptura 58 MPa; alongamento na ruptura 185%; flexão 59 MPa, módulo 1.495 MPa; Izod entalhado ISO 180: 93 kJ/m² a 23 °C e 20 kJ/m² a −40 °C; HDT 85 °C a 1,82 MPa e 99 °C a 0,455 MPa. Dados de resina moldada, sem direção FFF; ν=0,38 é proxy. Não caracterizam o “Triton” instalado enquanto fabricante, composição e processo permanecerem desconhecidos. [Ficha Eastman](https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312).

### Candidato industrial: Fiberon PA12-CF10 V1.1

Valores típicos da ficha Polymaker; corpos recozidos a 100 °C por 16 h. Condição úmida: adicionalmente imersos a 60 °C por 48 h, teor médio de umidade 2,92%.

| Propriedade | Seco XY / Z | Úmido XY / Z |
|---|---:|---:|
| E, MPa | 3.311,2 / 1.806,6 | 3.131,7 / 1.622,0 |
| Resistência à tração, MPa | 77,4 / 52,2 | 71,7 / 42,1 |
| Alongamento, % | 4,2 / 5,0 | Não transcrito |

Densidade 1,06 g/cm³; flexão seca: módulo XY/Z 2.886,5/1.452,8 MPa e resistência 112,4/69,8 MPa. Charpy seco: entalhado XY 9,9 kJ/m²; sem entalhe XY/Z 33,7/27,6 kJ/m². Tg 55 °C; fusão 171 °C; HDT 105 °C a 1,8 MPa e 131 °C a 0,45 MPa. Manter seco durante a impressão, abaixo de 20% UR; usar bico resistente à abrasão. [TDS oficial V1.1](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/TDS_FIBERON_PA12-CF10_V1.1_EN.pdf?v=1740427088), cópia PDF arquivada em `fontes_industriais`.

A razão resistência Z/XY seca é aproximadamente 67%; úmida, 59%. Isso evidencia anisotropia dos corpos de prova, sem ser um ensaio de adesão pura da interface. A ficha não fornece constantes ortotrópicas completas, escoamento, condutividade, calor específico, expansão, fadiga, fluência, falha dependente da velocidade ou dissipação. O cartão linear usa E XY e ν=0,39 de outra modelagem de PA12, explicitamente proxy, não medição desse composto. Fonte do proxy: [estudo PA12](https://pmc.ncbi.nlm.nih.gov/articles/PMC10023978/).

**Estudo 3 bloqueado:** “Alguns componentes estão usando um material com propriedades inválidas.” E, densidade, ν, cisalhamento e resistência última foram auditados; o critério de resistência última foi confirmado após reabrir. O pré-check continuou rejeitando a ficha. A causa interna específica não foi exposta; não atribuir com certeza o bloqueio apenas ao escoamento ausente. Campos térmicos/escoamento numericamente zero representam ausência, não resultados medidos. Nenhum job desse estudo foi enviado.

**Alternativa avaliada:** Forward AM Ultrafuse PAHT CF15. Ficha oficial acessada com cabeçalho V4.0, 09/05/2023: densidade condicionada 1,203 g/cm³, E seco XY/ZX 8.386/3.532 MPa, resistência 103,2/18,2 MPa. Não foi escolhido automaticamente: o benefício de rigidez XY acompanha baixa resistência ZX nessa ficha e não oferece redução de densidade contra TX1001. Não usar ν condicionado 0,51 em elasticidade isotrópica estável. [TDS Forward AM](https://forward-am.com/wp-content/uploads/2024/10/Ultrafuse_PAHT_CF15_TDS_EN_v3.5-1.pdf).

## 5. PADs PU 97A e impacto nas interfaces

Referência documental de 97A: **Lubrizol ESTANE X-595A-11**, TPU de poliéster para extrusão. A ficha declara densidade 1,22 g/cm³; dureza 97 Shore A; tensão a 100%/300% de alongamento 135/240 kgf/cm², equivalentes a 13,24/23,54 MPa; resistência última 500 kgf/cm² ≈49,03 MPa; alongamento 550%; rasgamento Die C 130 kgf/cm ≈127,49 kN/m. Compression set: 20% a 23 °C/22 h e 50% a 70 °C/22 h; Vicat 115 °C. Valores típicos com recozimento informado na ficha. [TDS Lubrizol](https://www.lubrizol.com/-/media/Lubrizol/Engineered-Polymers/Documents/Engineered-Polymer-TDS/ESTANE-X595-A11.pdf).

Essa é referência para consulta ao fornecedor, não uma especificação de compra nem filamento FFF validado. Confirmar disponibilidade atual, rota de fabricação, ambiente químico e resistência à hidrólise. As tensões a 100% e 300% não são módulos de Young nem tensões de escoamento. Compression set não é porcentagem de energia absorvida ou desgaste. Vicat não é temperatura contínua admissível.

O PAD precisa de espessura útil de compressão, área, folga, retenção, pré-compressão e posição de contato. Confinamento lateral aumenta a rigidez aparente; um PAD duro e muito fino pode transmitir alto pico. Absorção depende da integral da curva força × deslocamento e da histerese, não somente da dureza. Evitar que um fim de curso rígido elimine o curso do amortecedor. Conferir também esmagamento do polímero e rasgamento/arrancamento dos encaixes e parafusos.

O Fusion possui estudo de evento dinâmico com massa, velocidade, inércia, amortecimento e contato variável. Ruptura por eliminação de elementos exige deformação limite caracterizada. [Documentação Autodesk](https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM). Nesta campanha não há modelo PU hiperelástico/viscoelástico calibrado nem evento resolvido.

Matriz preparada conceitualmente: interfaces A1–A4 individualmente, impacto normal e tangencial, sem/com PAD, velocidades demonstrativas 0,25/0,5/1 m/s. Para massa efetiva hipotética de 1 kg: energias 0,03125/0,125/0,5 J; para 24 kg: 0,75/3/12 J. São cálculos cinéticos, não simulações. A força máxima requer curso, contato e lei constitutiva; não dividir energia por uma distância arbitrária para relatar pico real.

Saídas necessárias para aceitar o estudo futuro: força e impulso de contato no tempo, tensões principais, deformação plástica/limite adequado, curso do PAD, energia interna/dissipada/cinética, rebote, estabilidade temporal e convergência de malha/contato. Instrumentar a célula e o protótipo para confrontar essas saídas.

## 6. Temperatura, união das camadas e serviço 24/7

Na FFF, a união acontece por contato das trilhas quentes, molhamento e difusão de cadeias antes do resfriamento. Em poliamidas, cristalização e histórico térmico também influenciam a resposta. Fibra curta tende a alinhar com a extrusão e não constitui reforço contínuo atravessando as camadas. Umidade, vazios, temperatura, tempo entre camadas, ventilação e pressão de deposição alteram a união. A foto de dano não basta para distinguir impacto, delaminação, porosidade ou falha de retenção.

Registrar orientação e linhas de deposição em relação à tração principal nos quatro pontos. Avaliar corpos XY e Z produzidos na mesma máquina, lote e ciclo térmico; medir umidade e massa após condicionamento. Não transportar a resistência de um corpo recozido para peça não recozida ou de preenchimento parcial.

Ambientes propostos para ensaio: 23/40/60 °C contínuos e 80 °C como excursão separada. São hipóteses. HDT e Tg não fornecem automaticamente E(T), limite de serviço ou resistência residual. Para temperatura quantitativa faltam k, calor específico no transiente, convecção, contato térmico e fontes de calor; para tensão térmica, expansão e curvas mecânicas por temperatura. Não houve solve térmico.

Operação 24/7 precisa de espectro: tempo carregado, ciclos, aceleração, reversões, choque e paradas. Um ciclo hipotético de 10 s gera 8.640 ciclos/dia, 259.200/30 dias e 3.153.600/ano de 365 dias. Isso é exposição, sem previsão de vida. Fadiga requer curvas aplicáveis e tensão média; fluência requer curvas por tensão, tempo, temperatura e umidade; relaxação altera pré-carga; desgaste requer contato deslizante, velocidade, contraparte, lubrificação e lei experimental. Não foram calculadas horas até ruptura nem perdas por milhares de horas.

Plano de validação: ensaios de tração XY/Z e impacto com condicionamento seco/úmido; compressão cíclica e relaxação dos PADs em temperatura; protótipo instrumentado com retenção de carga protegida; inspeção de trincas e deformação nas interfaces ao longo dos ciclos. Fixar antes os limites de deflexão, deformação residual, força transmitida e temperatura. A ficha estática isolada não estabelece esses limites.

## 7. Massa: corpo real e cubo de exemplo

Para o mesmo volume depositado, m = ρV. Ferragens e demais componentes permanecem separados. Valores sem PAD:

| Material | Massa do corpo superior maciço | Economia contra Tritan |
|---|---:|---:|
| Tritan, 1,18 g/cm³ | 1.641,61 g | Referência |
| PA6-CF, 1,09 g/cm³ | 1.516,40 g | 125,21 g / 7,63% do polímero |
| PA12-CF10, 1,06 g/cm³ | 1.474,66 g | 166,94 g / 10,17% do polímero |

As imagens informam 2,834 kg e aproximadamente 3,03 kg para conjuntos distintos, diferença de 196 g ainda não reconciliada. Não aplicar a redução percentual do polímero a todo esse conjunto. A massa final requer identificação dos corpos substituíveis, ocorrências, ferragens, volume de PAD e volume realmente extrudado. PAD documental: cada 10 cm³ acrescenta cerca de 12,2 g, caso a densidade e o processo sejam equivalentes.

Cubo demonstrativo de **50 × 50 × 50 mm**, com casca ideal uniforme de **2 mm**, inclusive tampas. Vexterno=125 cm³; Vnúcleo=97,336 cm³; Vcasca=27,664 cm³. Fórmula m=ρ[Vcasca+fVnúcleo]. Tabela de massa analítica, sem suportes, sobre-extrusão ou retração:

| Preenchimento do núcleo | Tritan, g | PA6-CF, g | PA12-CF10, g |
|---|---:|---:|---:|
| 30% | 67,10 | 61,98 | 60,28 |
| 40% | 78,59 | 72,59 | 70,59 |
| 60% | 101,56 | 93,81 | 91,23 |
| 100% | 147,50 | 136,25 | 132,50 |

Casca real, perímetros, reforços ao redor de furos e padrão de preenchimento exigem volume do fatiador. Não multiplicar simplesmente a massa maciça por 30/40/60%; não escalar E e resistência linearmente pela porcentagem. Esses preenchimentos não foram simulados nesta garra.

## 8. Ambiente preparado e próximos bloqueios

Servidor MCP compacto operacional, com seis ferramentas, sem chamadas internas a modelos de linguagem e sem envio automático de solver. Fichas e respostas grandes ficam em disco. Foi ampliado para consultar PA12-CF e estimar massas com densidades explícitas, mantendo o padrão anterior; teste de protocolo, validação e conexão Fusion passou. Não há porcentagem garantida de economia de tokens: isso depende das interações. Usar registro de estado e recuperar somente os campos necessários evita repetir pesquisa e jobs.

| Caso | Estado e requisito restante |
|---|---|
| PA6-CF e Tritan, estático maciço | Resolvidos exploratoriamente; verificar convergência, reações e apoios |
| PA12-CF10 | Cadastrado; bloqueado pelo pré-check, causa específica não exposta |
| 30/40/60% | Não resolvidos; requer casca e núcleo representativos do fatiador |
| Impacto sem/com PAD | Não resolvido; requer geometria, contato e curvas calibradas |
| Temperatura | Não resolvido; dados térmicos e condições de contorno incompletos |
| Fadiga/fluência/desgaste 24/7 | Não resolvido; faltam leis e espectro experimental |

Arquivo final preservado: `SAMI_COMPARACAO_PA6CF_TRITAN_PA12CF_2026-11-11.f3d`. O estudo bloqueado está incluído para diagnóstico; não é apresentado como resultado.
