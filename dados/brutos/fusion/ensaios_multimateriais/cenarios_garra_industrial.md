# Plano demonstrativo: mordente de garra industrial

Estado: **cenários definidos; nenhum cálculo Fusion foi executado por este subagente**. Geometria informada pelo agente principal: ModeloReferencia, caixa envolvente 125 × 250 × 50 mm, volume CAD sólido 692,442 cm³ e duas furações de montagem. A caixa envolvente não deve substituir o volume real. A localização das interfaces ainda precisa ser conferida no CAD.

## Operação e cargas assumidas

Este é um cenário de comparação, não o histórico real de uma máquina nem uma especificação certificada. Adota dois mordentes opostos prendendo uma carga de 2 kg por atrito. Cada mordente recebe normal de 100 N; a aceleração vertical para cima é 5 m/s². Gravidade 9,80665 m/s². O coeficiente de atrito nominal é **assumido em 0,30**, com sensibilidade em 0,15 e 0,50; ele não é uma propriedade universal de qualquer um dos oito plásticos.

A Robotiq fornece o dimensionamento por atrito W = 2Fμ/S e destaca aceleração e medição do atrito. Seu exemplo μ = 0,30 se refere a ponta específica de NBR sobre aço lubrificado: não valida um par de contato de plástico impresso. [Manual primário Robotiq](https://assets.robotiq.com/website-assets/support_documents/document/2F-85_2F-140_General_PDF_20200211.pdf).

Para as hipóteses escolhidas:

- Peso estático da carga: 19,6133 N; contribuição tangencial em cada mordente: 9,80665 N.
- Carga efetiva acelerando: m(g+a) = 29,6133 N; contribuição por mordente: 14,80665 N.
- Atrito disponível nos dois contatos: 2 × 100 × 0,30 = 60 N.
- Margem nominal contra deslizamento: 60/29,6133 = **2,026**. Não é fator de segurança estrutural do mordente.
- Em μ = 0,15, a margem cai para 1,013; em μ = 0,50, sobe para 3,377. Essa incerteza é relevante.
- Contato demonstrativo de 40 × 40 mm: pressão média nominal 0,0625 MPa. A pressão real pode ser muito não uniforme.
- Braço demonstrativo de 200 mm entre montagem e centro do contato: normal gera 20 N·m e tangencial acelerada gera 2,9613 N·m em eixos conforme orientação real. Não somar escalarmente momentos de eixos diferentes.

O peso próprio de cada mordente deve entrar separadamente, com sua massa e orientação reais. A carga de 2 kg é a peça manipulada, não a massa do mordente. Não se presume que o modelo seja compatível com um atuador Robotiq: a documentação foi usada para o princípio físico, não para certificar montagem, curso ou capacidade.

## Matriz mínima de estudos

| Caso | Definição | Evidência procurada |
| --- | --- | --- |
| S01 | Normal 100 N e tangencial 9,80665 N por mordente | Deflexão da ponta, tensões, reações e deformações na retenção estática |
| S02 | Normal 100 N e tangencial 14,80665 N por mordente | Mesmo conjunto durante aceleração, em aproximação estática equivalente |
| S03 | Sensibilidade da normal 50/100/150 N e atrito 0,15/0,30/0,50 | Estrutura e margem antideslizamento, sem confundir as duas |
| T01 | Contato a 40 °C, ambiente 25 °C, h = 10 W/(m²·K) assumido | Campo térmico e expansão com referência sem tensão a 25 °C |
| T02 | Mesmo cenário com contato a 60 °C | Sensibilidade térmica; propriedades constantes não comprovam rigidez real a 60 °C |
| I01 | Impactador rígido efetivo de 2 kg a 0,25 m/s no contato funcional | Evento de energia cinética 0,0625 J; deformação/contato dependem da caracterização dinâmica |
| L01 | Checkpoints 1.000/5.000/10.000 h | Agenda de exposição/ciclos; vida e desgaste permanecem pendentes sem leis calibradas |

A fixação preliminar pode idealizar a base rígida, mas deve usar faces e furações confirmadas no CAD. Para resultados de projeto, incluir parafusos/arruelas, pré-carga, folgas e complacência do atuador. Tensões singulares junto a vínculos rígidos não devem ser anunciadas como ruptura física comprovada.

## Ciclos e impacto ocasional

Ciclo hipotético de 10 s: 4 s preso/carregado, 6 s liberado/retorno. Equivale a 360 ciclos/h, sem disponibilidade ou paradas deduzidas.

| Tempo acumulado | Ciclos comandados | Tempo acumulado preso |
| --- | --- | --- |
| 1.000 h | 360.000 | 400 h |
| 5.000 h | 1.800.000 | 2.000 h |
| 10.000 h | 3.600.000 | 4.000 h |

Esses números são conversões de agenda, não vida prevista. Fluência exige curva/modelo temporal; fadiga exige espectro e curva S–N ou ε–N; desgaste exige tribopar, deslizamento e coeficiente calibrado. Não converter horas diretamente em perda de material.

O impacto escolhido equivale à energia de queda livre de cerca de 3,19 mm para a mesma massa. O rótulo moderado descreve a hipótese, não uma classe normalizada de severidade. Ensaiar primeiro um evento; uma série de 100 eventos seria um caso adicional de durabilidade, não substituto de fadiga validada. A energia não determina o pico da força sem rigidez, contato e tempo de desaceleração. Não adotar 100 N como força de impacto deduzida dessa energia. A rampa numérica de 10 ms no JSON é uma hipótese de carregamento, não tempo de contato medido.

## Preenchimentos 30%, 40%, 60% e 100%

Comparar arquitetura real do fatiador, mantendo a mesma estratégia de paredes, tampas e trajetória, ou usar propriedades efetivas ortotrópicas calibradas em corpos de prova correspondentes. São quatro geometrias/processos, não apenas quatro densidades de um sólido idêntico.

Não multiplicar E e resistência pelo percentual e chamar isso de dado confirmado. Alterar só densidade representa alteração de massa, não a rigidez do preenchimento. O limite inferior frouxo fρV e o superior ρV podem ajudar uma triagem de massa; a massa correta exige o volume depositado, pois as cascas consomem material.

## Proxies pesquisados para completar análises exploratórias

Todos os valores abaixo pertencem a **outro grau ou processo**. Não são dados confirmados dos oito filamentos e não foram inseridos no cadastro confirmado. O JSON contém unidades, fonte e classificação por campo.

| Família | ν candidato | k, W/(m·K) | cp, J/(kg·K) | α, K⁻¹ | Origem |
| --- | --- | --- | --- | --- | --- |
| PA6 | 0,39, literatura com grau não resolvido | 0,37 | 1.600 | 97 × 10⁻⁶ | Térmicos de TECAMID 6 natural; α longitudinal 23–60 °C |
| PA12 | 0,39, entrada de modelo FFF publicado | 0,30 | 1.800 | 150 × 10⁻⁶ | Térmicos de TECAMID 12 natural; α longitudinal 23–60 °C |
| PC | 0,37, corpo experimental de PC | 0,25 | 1.300 | 80 × 10⁻⁶ | Térmicos de TECANAT natural; α longitudinal 23–60 °C |
| TPU | 0,40 ±0,01, medido em outro TPU95A impresso | 0,19–0,25 | 1.700–2.300 | Pendente de leitura de curva por grau/temperatura | Térmicos representam a família BASF Elastollan, não Bambu95AHF |

Para TPU, um modelo publicado também assume ν = 0,49 para quase incompressibilidade, mas isso é uma escolha constitutiva e não medição universal. Não substituir automaticamente o valor experimental de outra formulação por 0,49. A grande dispersão entre formulações reforça a necessidade de ensaios para uma análise de grandes deformações. [Estudo TNM TPU95A](https://www.mdpi.com/2073-4360/18/21/2752).

Fontes primárias dos proxies:

- [Ensinger TECAMID 6 natural](https://www.ensinger-online.com/modules/public/sheet/createsheet.php?FILENAME=TECAMID+6+natural.PDF&FL=0&SID=2133). Há outra edição regional com α = 120 × 10⁻⁶; o valor não é invariável nem do PA6 LEHVOSS.
- [Ensinger TECAMID 12 natural](https://www.ensingerplastics.com/en/shapes/pa12-tecamid-12-natural).
- [Ensinger TECANAT natural](https://www.ensinger-online.com/modules/public/sheet/createsheet.php?FILENAME=TECANAT_natural_0.PDF&FL=0&SID=1346&ZOOM=1.2).
- [Dissertação ISEP, matriz PA6, tabela de propriedades dos produtores](https://recipp.ipp.pt/bitstreams/d975a4ec-e230-4160-a03c-17ec170fca87/download). Grau exato não estabelecido nesta pesquisa.
- [Alzyod e Ficzere, modelo FFF de PA12](https://pmc.ncbi.nlm.nih.gov/articles/PMC10023978/). ν é entrada do modelo, não medição independente deste filamento.
- [Pesquisa experimental com tubo de PC, tabela 4-1](https://api.lib.kyushu-u.ac.jp/opac_download_md/6787558/eng3267.pdf).
- [Haid 2024, caracterização TPU, tabela 4.3](https://shura.shu.ac.uk/33603/1/Haid_2024_PhD_TowardsConcussionPrevention.pdf).
- [BASF Elastollan: térmicos representativos, tabela 1](https://download.basf.com/p1/8a8082587fd4b608017ff4e900830157/en/Elastollan).
- [BASF: curvas de expansão por dureza e temperatura](https://www.basf.com/dam/jcr%3A19c11827-1bc0-3b0f-a3f4-4fc2b986d54f/Elastollan_Properties-Physical-Properties.pdf). Não foi feita digitalização numérica dessas curvas.

G pode ser derivado de E/[2(1+ν)] somente em uma aproximação isotrópica declarada. Isso não produz os módulos de cisalhamento ortotrópicos reais de uma impressão preenchida. Não transferir os proxies do PA6 sem fibra para PA6-CF como se fossem caracterização do compósito.
