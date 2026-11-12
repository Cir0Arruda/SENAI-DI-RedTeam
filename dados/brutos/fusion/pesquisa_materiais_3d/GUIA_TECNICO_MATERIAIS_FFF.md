# Materiais de impressão 3D: propriedades e união entre camadas

Pesquisa de 10/11/2026. Escopo: filamentos FFF/FDM PETG, PCTG/Tritan, TPU 95A, PA6, PA12, PC e PA-CF. As fontes principais são fichas dos fabricantes e pesquisas experimentais. Os números são valores típicos dos produtos identificados, não limites garantidos de toda a família.

## 1. O que significa cada propriedade

| Propriedade | Significado prático |
| --- | --- |
| Resistência à tração, MPa | Tensão suportada no ensaio. Distinguir escoamento, máximo e ruptura. Não é a força em kg que uma peça qualquer suporta. 1 MPa = 1 N/mm². |
| Módulo de Young, MPa ou GPa | Rigidez inicial em tração: maior módulo significa menor deformação elástica para a mesma tensão. Não mede tenacidade. 1 GPa = 1.000 MPa. |
| Alongamento na ruptura, % | Deformação antes de romper, nas condições do ensaio. Ajuda a avaliar ductilidade, mas não informa quanto dessa deformação é recuperável. |
| Tenacidade | Energia absorvida até a fratura; depende da curva tensão-deformação, entalhes, velocidade e temperatura. |
| Resistência ao impacto | Energia num ensaio dinâmico específico. Comparar apenas o mesmo método, entalhe, geometria, temperatura e direção. |
| Dureza Shore | Resistência à indentação superficial. 95A não significa 95 MPa nem determina sozinho rigidez, desgaste ou temperatura de uso. |
| Fluência | Deformação que cresce com o tempo sob carga constante. |
| Relaxação | Queda de força quando uma deformação é mantida. Relevante para presilhas e vedações. |
| Fadiga | Dano por ciclos repetidos; não se deduz do ensaio estático ou de impacto. |

XY identifica aqui tração predominantemente no plano de impressão. Z/ZX identifica o corpo de prova vertical, com a carga separando camadas. As definições exatas dos fabricantes e os trajetos internos devem ser conferidos. Mesmo em XY pode haver anisotropia entre direções dos cordões.

## 2. Comparação mecânica de produtos identificados

Valores médios arredondados. São corpos de prova impressos, exceto a linha PA12, cuja ficha não estabelece orientação nem demonstra que os valores foram medidos em peças FFF. NR = não reportado nessa fonte; não é zero.

| Produto de referência | Tração XY / Z, MPa | Young XY / Z, MPa | Alongamento na ruptura XY / Z | Preparação ou ressalva |
| --- | --- | --- | --- | --- |
| Polymaker PETG V2.0 | 47,96 / 45,71 | 2.311 / 2.203 | 9,33% / 3,54% | Corpos 100% preenchidos, bico 240 °C e ventilação desligada no ensaio |
| 3D-Fuel Pro PCTG, tabela por orientação | 44,0 / 45,0 | 1.810 / 1.860 | 130% / 3,9% | Dados de peças impressas, distintos da tabela genérica de propriedades da resina |
| Bambu TPU 95A HF V3.0 | 27,3 / 22,3 | 9,8 / 7,4 | >650% / >480% | 100% de preenchimento; fabricante condicionou termicamente/secou os corpos a 70 °C por 12 h |
| LEHVOSS LUVOCOM 3F PAHT 9936 BK/L | 79 / 41 | 3.050 / 2.800 | 4,1% / 1,6% | PA6 formulado/modificado e sem reforço estrutural, conforme fabricante; seco, sem recozimento; não representa PA6 puro genérico |
| Fiberlogy Nylon PA12 | 45 no escoamento; Z NR | 1.400; Z NR | >50%; Z NR | Valores da ficha de material, sem orientação FFF declarada |
| Polymaker PolyMax PC V5.4 | 53,44 / 41,43 | 2.435 / 2.149 | 4,53% / 2,79% | Corpos fabricados em ambiente a 90 °C; ficha também recomenda recozimento |
| Bambu PA6-CF V3.0 | 102 / 48 | 4.430 / 2.170 | 5,8% / 3,7% | 100% preenchido, seco e tratado a 80 °C por 12 h antes do ensaio |

Fontes de cada linha: [PETG](https://polymaker.com/wp-content/uploads/lana-downloads/TDS_Polymaker_PETG_V2.0_2025-11-17.pdf), [PCTG impresso](https://www.3dfuel.com/pages/pctg), [TPU](https://store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/Bambu_TPU_95A_HF_Technical_Data_Sheet.pdf), [PA6 formulado](https://www.lehvoss.de/fileadmin/Compounds/PDFs/LUVOCOM_3F/LUVOCOM_3F_PAHT_9936_BK_L/Datasheet_LUVOCOM_R__3F_PAHT_9936_BK_L_Filament.pdf), [PA12](https://fiberlogy.com/app/uploads/2026/05/FIBERLOGY_NYLONPA12_TDS.pdf), [PC](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyMax_PC_TDS_EN_V5.4.pdf), [PA6-CF](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf).

O quociente calculado resistência Z/XY é aproximadamente 95% no PETG, 102% no PCTG, 82% no TPU, 52% no PA6 formulado, 78% no PC e 47% no PA6-CF. Isso é uma comparação entre resultados dos corpos de prova, não uma medição de 'porcentagem de cola'. O valor ligeiramente acima de 100% no PCTG é compatível com a dispersão reportada e com diferenças de trajetória. Não permite afirmar isotropia: o alongamento desse mesmo produto muda muito com a direção.

### Flexão e impacto

| Referência | Flexão: resistência XY / Z, MPa | Flexão: módulo XY / Z, MPa | Impacto reportado |
| --- | --- | --- | --- |
| PETG Polymaker | 80,08 / 57,65 | 2.277 / 1.959 | Charpy XY com entalhe 4,95; sem entalhe XY 20,24 e Z 15,74 kJ/m² |
| PCTG 3D-Fuel, impresso | 72,7 / 71,5 | 1.780 / 1.720 | Izod com entalhe: XY 7,5 e ZX 4,7 kJ/m² |
| TPU Bambu | NR | NR | ISO 179: XY 123,2 e Z 86,3 kJ/m²; a tabela não especifica entalhe nesses valores |
| PA6 formulado LEHVOSS, seco | 115 / 65 | 2.730 / 2.470 | XY 89 e ZX 6 kJ/m²; folha identifica '1eU' e ISO 180; confirmar geometria/método antes de comparar diretamente |
| PA12 Fiberlogy | NR | NR | Charpy com entalhe a 23 °C: 12 kJ/m²; direção não declarada |
| PolyMax PC | 81,29 / NR | 2.050 / NR | Charpy com entalhe XY 21,28 kJ/m²; a −30 °C, 9,2 kJ/m² |
| PA6-CF Bambu | 151 / 80 | 5.460 / 2.240 | ISO 179: XY 40,3 sem indicação de entalhe, XY entalhado 13,4 e Z 15,5 kJ/m² |

Fontes: mesmas fichas e tabela por orientação acima. Os resultados não formam um ranking universal porque os ensaios diferem. J/m e kJ/m² não têm conversão direta sem geometria e definição da área. 'Não rompeu' também não é resistência infinita.

## 3. Temperatura: quatro conceitos diferentes

- **Tg:** transição vítrea, associada à mudança de mobilidade da fase amorfa. Em polímeros semicristalinos, os cristais ainda sustentam parte da estrutura acima da Tg.
- **Tm:** fusão dos cristais. Não é temperatura admissível de serviço. Nos amorfos, como PC e muitos copoliésteres, não há pico de fusão cristalina equivalente.
- **HDT:** temperatura de deflexão num ensaio curto com geometria, carga e taxa de aquecimento definidas. Não é limite contínuo de trabalho.
- **Vicat:** amolecimento por penetração de uma ponta sob carga. Não equivale a HDT, Tg ou perda completa de resistência.

| Produto | Densidade, g/cm³ | Tg / Tm, °C | HDT a 0,45 MPa / 1,8 MPa, °C | Outro dado |
| --- | --- | --- | --- | --- |
| PETG Polymaker | 1,30 | 71,24 / NR | 69 / 65 | Vicat 75 °C |
| PCTG 3D-Fuel | 1,23 | 84 / não usar como Tm cristalina | 76 / 64, pela tabela ISO | Dureza 76D; propriedades térmicas da ficha não discriminam orientação |
| TPU Bambu | 1,22 | Tg NR / 183 | NR / NR | Não inferir temperatura de serviço a partir da fusão |
| PA6 formulado LEHVOSS | 1,25 | 80 / 235 | NR / 90 | Formulação especial; valores não representam todo PA6 |
| PA12 Fiberlogy | 1,01 | Tg NR / 178 | 135 / 55 | Vicat 145 °C |
| PolyMax PC | 1,19 | 113 / não aplicável na ficha | 114 / 99 | Vicat 117 °C |
| PA6-CF Bambu | 1,09 | 68 / 223 | 186 / 164 | Vicat 212 °C; cristalização 185 °C |

Fontes: fichas vinculadas na seção 2 e [TDS Pro PCTG, tabela ISO](https://cdn.shopify.com/s/files/1/0027/5339/6848/files/3D-Fuel_Pro_PCTG_TDS_9-2-25.pdf?v=1756827548). Na tabela ASTM desse PCTG, o fabricante informa HDT 74/64 °C; aqui mantive a tabela ISO, sem combinar métodos.

O PA12 é um bom exemplo da influência da carga: a ficha mostra 135 °C a 0,45 MPa, mas 55 °C a 1,8 MPa. Divulgar apenas o primeiro número esconderia uma diferença relevante. A literatura experimental também mostra fluência em termoplásticos impressos bem abaixo da Tg; o estudo citado foi realizado em PLA, não fornece curvas desses sete filamentos. [Pesquisa sobre fluência](https://arxiv.org/abs/2302.11240).

## 4. Como as camadas ficam juntas

A união em FFF ocorre principalmente por **soldagem térmica do próprio polímero**. O cordão quente faz contato com o anterior, aquece a região de contato e permite que cadeias moleculares atravessem a interface por difusão e recuperem entrelaçamentos. No resfriamento, essa mobilidade diminui. É um processo dependente do tempo e da temperatura da interface, não apenas do valor configurado no bico. [Experimentos do NIST sobre formação da solda](https://www.nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing).

Cordões não preenchem perfeitamente todo o espaço. Vazios, área de contato, trajetória e tensões residuais alteram a transferência de carga e a propagação de trincas. Uma peça com 100% de preenchimento programado ainda pode conter poros. [NISTIR 8059](https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8059.pdf).

No PA-CF convencional, fibras curtas ficam embebidas na matriz de nylon e tendem a acompanhar a direção de deposição. A matriz transfere carga às fibras; falhas podem ocorrer por descolamento fibra-matriz, arrancamento, quebra de fibra e trinca da matriz. O reforço em XY não cria uma armadura contínua atravessando cada interface Z. [Estudo de orientação](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669830/) e [estudo de dano interlaminar em PA6-CF15](https://www.sciencedirect.com/science/article/pii/S2238785425018782).

### Variáveis que mudam essa soldagem

| Variável | Efeito a investigar no processo |
| --- | --- |
| Temperatura real da interface | Define mobilidade das cadeias e o tempo disponível para soldagem |
| Câmara, ventilação e intervalo entre camadas | Alteram histórico de resfriamento e tensões residuais |
| Vazão, largura e altura do cordão | Mudam contato, porosidade e geometria da interface |
| Umidade no filamento | Pode gerar defeitos no processamento; o efeito depende do polímero |
| Trajetória e direção de carga | Alteram quais interfaces recebem tração, cisalhamento e abertura de trinca |
| Cristalização e pós-tratamento | Podem alterar rigidez, contração, tensões residuais e coesão |

Essas relações orientam experimentos; não existe configuração universal. Aumentar temperatura ou fluxo indefinidamente não garante resistência. Em um estudo com PA-CF, elevar a vazão até 120% não aumentou densidade ou propriedades no equipamento ensaiado. [Belei e Amancio-Filho](https://pmc.ncbi.nlm.nih.gov/articles/PMC11669830/).

## 5. Particularidades de cada família

**PETG:** copoliéster que oferece fabricação relativamente simples e propriedades úteis para peças funcionais. Neste produto, a resistência à tração em Z se aproxima da XY, mas a ductilidade em Z é menor. Para peças carregadas em ambiente quente, o HDT na faixa de 65–69 °C desse grau e a fluência exigem avaliação específica. A ficha classifica resistência a óleos/graxas e ácidos fracos como boa; ácidos e bases fortes como ruim. Isso não substitui ensaio com produto químico e tensão reais. [TDS PETG](https://polymaker.com/wp-content/uploads/lana-downloads/TDS_Polymaker_PETG_V2.0_2025-11-17.pdf).

**PCTG e Tritan:** não são nomes intercambiáveis de um único grau. Tritan é uma família comercial da Eastman; é preciso identificar o código e o fabricante do filamento. Como contraste, a Eastman publica para o Tritan TX1001 moldado: resistência ISO no escoamento/ruptura 43/58 MPa, módulo 1.548 MPa, alongamento na ruptura 185%, Izod entalhado 93 kJ/m² a 23 °C e 20 kJ/m² a −40 °C, HDT ASTM 99/85 °C a 0,455/1,82 MPa. Esses dados não são propriedades Z de impressão. [Eastman TX1001](https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312).

**TPU 95A:** elastômero termoplástico; segmentos flexíveis e rígidos formam uma estrutura que permite deformação e recuperação. A razão entre os segmentos, a química e o processamento mudam o comportamento. Dois TPUs 95A podem ter respostas diferentes. Alongamento até romper não equivale a alongamento repetível sem deformação permanente. Para vedações e amortecedores, também interessam compression set, resistência ao rasgo, histerese e relaxação, ausentes na ficha Bambu consultada. [Estrutura do TPU, Covestro](https://solutions.covestro.com/en/highlights/articles/theme/product-technology/chemical-physical-structure-tpu).

**PA6:** nylon semicristalino, mas grau puro, copoliamida e formulação modificada precisam ser identificados. O exemplo LEHVOSS da tabela é uma formulação especial, não uma média do PA6. A absorção de umidade precisa entrar no projeto. O comparativo do fabricante de polímeros mostra que PA6/PA66 absorvem mais água que PA12, afetando dimensão e propriedades. [Daicel-Evonik](https://www.evonik.daicel.com/english/product/).

**PA12:** costuma ser escolhido quando estabilidade com umidade e flexibilidade são relevantes. A absorção menor não elimina a necessidade de secar o filamento antes da impressão. Também não torna dados SLS/MJF intercambiáveis com FFF. A ficha Fiberlogy apresenta propriedades sem orientação; portanto não permite calcular a resistência entre camadas desse filamento. [PA12 Fiberlogy](https://fiberlogy.com/en/filaments/nylon-en/nylon-pa12-en/).

**PC:** pode combinar resistência térmica e tenacidade, mas graus de impressão são formulados de maneiras diferentes. O PolyMax PC usado aqui foi ensaiado em câmara a 90 °C, uma condição relevante para reproduzir a coesão. O impacto entalhado cai de 21,28 para 9,2 kJ/m² a −30 °C, mostrando por que o ensaio à temperatura ambiente não descreve todo o uso. [PolyMax PC](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyMax_PC_TDS_EN_V5.4.pdf).

**PA-CF / PA6-CF:** PA-CF significa poliamida com fibra de carbono; a matriz pode ser PA6, PA12, PA612 ou outra formulação. Percentual e comprimento das fibras também importam. No Bambu PA6-CF consultado, a rigidez de tração XY é aproximadamente o dobro da Z. Isso favorece aplicações que precisam limitar deflexão no plano de impressão, mas não garante resistência a choques, rasgo ou abertura entre camadas. A ficha informa redução de desempenho em ambiente úmido e condiciona os números ao estado seco. [TDS PA6-CF](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf).

## 6. Umidade: antes e depois de imprimir

Secar para processar e condicionar uma peça para uso são operações diferentes. Uma peça de nylon absorvendo água depois de impressa pode ficar menos rígida e mais dúctil. Isso não é necessariamente a mesma coisa que imprimir com filamento úmido e produzir defeitos.

Exemplo documentado: Ultrafuse PA é uma **copoliamida 6/66**, não PA6 puro. Em XY, sua ficha mostra:

| Estado | Tração, MPa | Young, MPa | Alongamento na ruptura |
| --- | --- | --- | --- |
| Seco | 61,4 | 2.419 | 9,6% |
| Condicionado | 32,2 | 395 | 143,3% |

Os corpos secos foram mantidos a 80 °C por 504 h; os condicionados a 70 °C e 62% UR por 336 h. São condições de laboratório da caracterização, não uma receita universal de secagem. [TDS Ultrafuse PA](https://move.forward-am.com/hubfs/AES%20Documentation/Engineering%20Filaments/PA/TDS/Ultrafuse_PA_TDS_EN_v2.2.pdf) e [identificação da copoliamida](https://forward-am.com/wp-content/uploads/2021/07/BASF_Ultrafuse-PA_Product_Onepager_13-11-19_RZ.pdf).

## 7. Parâmetros publicados de impressão e secagem

Estas são recomendações de cada produto, não configurações já validadas para a impressora do usuário. Bico, vazão, cor e equipamento podem exigir ajustes.

| Produto | Bico / mesa, °C | Câmara | Secagem do filamento |
| --- | --- | --- | --- |
| PETG Polymaker | 240–260 / 60–70 | Não exigida pela ficha | 55 °C, 6 h |
| PCTG 3D-Fuel | 250–280 / cerca de 80 | Não obrigatória no guia | 70 °C, 6–8 h, ou 65 °C, 8–12 h |
| TPU Bambu 95A HF | 220–240 / 30–35 | 25–45 °C | 70 °C, 8 h |
| PA6 formulado LEHVOSS 9936 | 300–350 / 70 | Pode dispensar aquecimento ativo, segundo ficha | 90 °C, mínimo 24 h; manter seco |
| PA12 Fiberlogy | 255–270 / PDF 100; página atual 110 | Fechada; recomendada aquecida | Página atual: 70 °C, 4 h |
| PolyMax PC | 250–270 / 90–105 | Ficha: 70–100 °C | 75 °C, 6 h |
| PA6-CF Bambu | 260–290 / 80–100 | 45–60 °C | 80 °C, 8–12 h |

Fontes: fichas e páginas vinculadas anteriormente. Recozimento muda dimensões e não deve ser confundido com secagem. O TPU Bambu teve tratamento no ensaio, mas o fabricante desaconselha recozer peças TPU de geometrias complexas porque podem deformar. A presença de fibra exige avaliar desgaste e compatibilidade do bico; seguir o produto específico.

## 8. Dados ainda necessários para engenharia e simulação

'Todos os dados' depende do grau e do uso. As fichas públicas consultadas não fornecem uma caracterização constitutiva completa de cada filamento. Permanecem lacunas como:

- Curvas tensão-deformação em X, Y e Z, incluindo temperaturas e velocidades relevantes.
- Resistência ao escoamento quando não publicada, compressão, cisalhamento e propriedades após envelhecimento.
- Módulos de cisalhamento e Poisson por direção; não foram preenchidos por analogia com outro plástico.
- Condutividade térmica, calor específico e expansão térmica, incluindo anisotropia e dependência da temperatura.
- Curvas de fluência, relaxação e fadiga para umidade e temperatura de serviço.
- Energia de fratura interlaminar e sensibilidade a entalhes.
- Para TPU: resposta hiperelástica/viscoelástica, compression set, rasgo e recuperação cíclica.
- Para PA-CF: matriz exata, fração/comprimento das fibras, porosidade e orientação.
- Resistência química sob tensão, envelhecimento UV e variação de cor/lote.

Para levar esses dados ao Fusion, selecionar primeiro marca, grau, orientação e estado de umidade. Usar um modelo isotrópico com um único E ignora parte da anisotropia do FFF. Uma análise linear de pequena deformação também não descreve a deformação de centenas de porcento do TPU. Tração, impacto e HDT não são parâmetros substitutos entre si. A presente pesquisa não alterou os materiais nem os estudos do projeto Fusion anterior.

Uma caracterização prática deve registrar impressora, bico, temperaturas, vazão, altura, largura de cordão, paredes, preenchimento, trajetórias, orientação, secagem, umidade de ensaio e pós-tratamento. Ensaios XY e Z com repetição permitem avaliar dispersão e modo de falha. A escolha de normas e geometrias deve acompanhar a propriedade procurada. [NIST: caracterização de polímeros fabricados aditivamente](https://nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8059.pdf).

## 9. Massa estimada de um cubo de exemplo

Cubo externo de **50 × 50 × 50 mm**, equivalente a **125 cm³**. A massa maciça nominal é calculada por **massa (g) = densidade (g/cm³) × volume (cm³)**, usando os produtos e fontes identificados nesta pesquisa.

Para ilustrar uma peça com preenchimento parcial, a segunda estimativa adota paredes, tampa e fundo com **2 mm de espessura**, todos maciços, e **20% do volume interno** ocupado por material. É uma aproximação geométrica, não o resultado de um fatiador. O volume interno é 46³ mm³ = 97,336 cm³; o volume total de material fica em 27,664 + 0,20 × 97,336 = **47,1312 cm³**.

| Material / produto | Densidade, g/cm³ | Cubo maciço, g | Cubo com 20% interno e casca de 2 mm, g |
| --- | --- | --- | --- |
| PETG Polymaker | 1,30 | 162,50 | 61,27 |
| PCTG 3D-Fuel | 1,23 | 153,75 | 57,97 |
| Tritan TX1001 Eastman | 1,18 | 147,50 | 55,61 |
| TPU 95A HF Bambu | 1,22 | 152,50 | 57,50 |
| PA6 formulado LEHVOSS 9936 | 1,25 | 156,25 | 58,91 |
| PA12 Fiberlogy | 1,01 | 126,25 | 47,60 |
| PC Polymaker PolyMax | 1,19 | 148,75 | 56,09 |
| PA6-CF Bambu, referência para PA-CF | 1,09 | 136,25 | 51,37 |

São massas nominais calculadas, não medições. As casas decimais apenas apresentam a conta. Porosidade, umidade, pigmentos, composição, dimensões reais e trajetórias do fatiador alteram o resultado. Suportes, brim e purga não entram na massa do cubo desta tabela. Em particular, 20% de preenchimento interno não significa 20% da massa maciça, pois as paredes e tampas também consomem material. O PA6 formulado e o Tritan TX1001 são referências específicas; não transferir suas densidades para qualquer PA6 ou filamento vendido como Tritan.

Para outro lado L em milímetros, a massa do cubo maciço é **m = ρ × (L/10)³**. Mantendo o material e a geometria maciça, dobrar o lado multiplica a massa por oito.

## 9. Peso estimado da esfera do projeto

Objeto considerado: esfera maciça de diâmetro externo 50 mm, sem cavidades, com o volume geométrico de 65,44984695 cm³. A divisão da superfície em calotas não remove material. Cálculo: massa [g] = volume [cm³] × densidade [g/cm³]. Os valores abaixo representam massa, chamada usualmente de peso, e foram arredondados para 0,1 g.

| Material de referência | Densidade usada, g/cm³ | Massa da esfera maciça |
| --- | --- | --- |
| PETG Polymaker | 1,30 | 85,1 g |
| PCTG 3D-Fuel Pro | 1,23 | 80,5 g |
| Tritan Eastman TX1001 | 1,18 | 77,2 g |
| TPU Bambu 95A HF | 1,22 | 79,8 g |
| PA6 formulado LEHVOSS 9936 | 1,25 | 81,8 g |
| PA12 Fiberlogy | 1,01 | 66,1 g |
| PC Polymaker PolyMax | 1,19 | 77,9 g |
| PA6-CF Bambu | 1,09 | 71,3 g |
| Resina SUNLU ABS-Like do estudo anterior | 1,19 | 77,9 g |

Densidades: fichas dos respectivos graus já citadas neste relatório; SUNLU: [TDS SL-TE-WI-100 A/0](https://media.sunlu.com/prod/20260331/cdd6ab82-85d8-49ea-b432-12c6c9c5c005.pdf?filename=TDS). PA6 formulado não representa a densidade de todo PA6, e o exemplo PA6-CF não representa todo PA-CF.

Estas são estimativas geométricas, não pesagem de peças fabricadas. Não incluem suportes, brim, purga ou outros descartes. Porosidade, tolerância dimensional, densidade específica da marca/cor e umidade podem alterar a massa real. Para peça oca ou impressão com preenchimento parcial, calcular o volume efetivamente depositado: não basta multiplicar a massa maciça pelo percentual de preenchimento, pois paredes e superfícies também consomem material. A estimativa do fatiador deve usar a densidade do filamento correto.
