# Ensaio Fusion — acompanhamento de 11/11/2026

## Resultado concluído — baseline exploratória

| Grandeza | Resultado do Fusion |
|---|---:|
| Tensão de von Mises máxima | 3,232 MPa |
| Primeira tensão principal máxima | 5,163 MPa |
| Deslocamento total máximo | aproximadamente 0,080 mm |
| Fator de segurança mínimo, referência de tração XY | 19,755 |
| Nós / elementos parabólicos | 498.261 / 339.001 |
| Refinamentos adaptativos | 0 |

Valores transcritos das legendas e configurações do relatório nativo; a exportação deixou células numéricas do resumo vazias, por isso as figuras exportadas constituem a evidência dos extremos. Figuras 14, 15 e 17 mostram von Mises, primeira principal e deslocamento. O HTML contém também textos genéricos de recomendações do template, que não substituem os campos numéricos deste estudo.

O máximo de primeira principal aparece junto aos furos da flange; as interfaces dos braços apresentam os maiores deslocamentos. Localização qualitativa pela imagem, sem coordenada nodal extraída. A escala de deformação não foi documentada no exportado: interpretar o deslocamento pela legenda, não pela aparência da forma.

**O caso calculado não demonstrou a resistência a impacto dos quatro pontos, eficácia do PAD, vida 24/7 ou comportamento térmico.** É a resposta elástica do corpo superior maciço sob uma hipótese de carga. Não extrapolar o fator de segurança para massa admissível, durabilidade, preenchimentos menores ou resistência Z. Não houve verificação global de soma de reações nem estudo de convergência: a baseline permanece exploratória.

Arquivos: `SAMI_PA6CF_24kg_Relatorio_Fusion.html` (evidência nativa), `Fusion_SAMI_figura_15.png`, `Fusion_SAMI_figura_17.png`, `SAMI_PA6CF_RESULTADO_ESTATICO_2026-11-11.f3d` (arquivo final com integridade CRC verificada). A recuperação completa dos resultados de nuvem pode depender do documento/account original: `urn:adsk.wipprod:dm.lineage:qGiN74eQQtSYmI4lNtmWQA`.

## Caso efetivamente configurado

Documento separado: **SAMI PA6CF - CORPO SUPERIOR - EXPLORATORIO 24kg**. Geometria original do componente `Corpo Supor`, maciça, 1.391,191 cm³ e 2.676 faces. Não representa os braços inferiores, fixadores, ventosas nem PADs. Não foram resolvidos preenchimentos de 30/40/60% nesta etapa.

Fixação XYZ nas paredes dos seis furos de raio 4,2 mm da flange. Carga vertical de −88,8399 N em cada uma das quatro faces inferiores das interfaces destacadas, de 779,42 mm² cada. Total nominal: −355,3596 N = 24 × (9,80665 + 5). Aceleração de 5 m/s² e repartição igual são hipóteses, não dados medidos da célula. As quatro interfaces são carregadas simultaneamente. Pressão média nominal em cada face: aproximadamente 0,114 MPa; isso não é tensão máxima na peça.

Material candidato Bambu PA6-CF V3.0: elasticidade isotrópica exploratória, E=4.430 MPa, ν=0,39 como proxy de outra matriz PA6; densidade 1.090 kg/m³. A resistência última XY de 102 MPa é apenas referência no campo de fator de segurança. Esse fator não caracteriza falha anisotrópica, delaminação ou impacto. As direções Z e condição úmida não estão reproduzidas. Não comparar a margem exibida com uma certificação de carga.

Malha inicial alvo 3 mm. A verificação prévia passou. O job foi concluído com sucesso no Fusion. A tela de pós-processamento mostrou tensão máxima de von Mises de **3,232 MPa** e fator de segurança mínimo de **19,755** com critério de resistência máxima à tração. Não deduzir esse fator dividindo a resistência por von Mises sem conferir o critério utilizado. A malha ainda não passou por estudo de convergência. O registro `campanha_2026-11-11.json` acompanha o estado e os dados extraídos.

Peso próprio, inércia dos braços, excentricidades adicionais, pré-carga dos parafusos, perda de ventosa e deformabilidade da flange não estão incluídos. Resultados deste corpo isolado não homologam a montagem.

## Impacto nos quatro pontos

O ensaio quase estático não determina pico de impacto. Um evento de impacto precisa de corpo impactante, massa efetiva, velocidade, direção, contato e evolução temporal. O Fusion possui estudo de evento dinâmico, que considera inércia e contatos; eliminação de elementos exige um limite de deformação apropriado, não um valor inventado. [Autodesk](https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM).

Para montar uma matriz demonstrativa reprodutível, considerar separadamente A1…A4, sem PAD e com PAD, com massa efetiva explicitamente hipotética. Exemplo analítico: 1 kg a 0,25 / 0,5 / 1 m/s corresponde a 0,03125 / 0,125 / 0,5 J. Para 24 kg, as mesmas velocidades correspondem a 0,75 / 3 / 12 J. Esses números são energia cinética calculada, não resultados de impacto, e 24 kg não é automaticamente a massa efetiva de colisão de um robô.

Não converter energia diretamente em força máxima sem curso e resposta do contato. O PAD pode reduzir pico, mas sua geometria, confinamento, pré-compressão e histerese precisam ser representados. Dureza PU97A não fornece uma lei hiperelástica/viscoelástica. A análise sem esses dados pode comparar hipóteses elásticas, mas não provar absorção real, ruptura ou vida do encaixe.

## Temperatura e trabalho contínuo

Definir inicialmente ambientes hipotéticos de 23, 40 e 60 °C e um caso excepcional de 80 °C, sem tratá-los como temperaturas reais da célula. Para resultado térmico quantitativo faltam condutividade, condições de troca e propriedades mecânicas em cada temperatura do produto escolhido. Não usar propriedades de PA6 não reforçado como se fossem medidas do PA6-CF.

A ficha candidata relata Tg de 68 °C e HDT de 164 °C a 1,8 MPa; HDT não é limite de serviço contínuo sob carga. A resistência à tração varia com direção: XY 102 MPa e Z 48 MPa. Esses valores de corpos de prova não certificam as interfaces da garra. [Ficha Bambu V3.0](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf).

24/7 representa exposição, não uma lei de degradação. Para ciclo hipotético de 10 s: 8.640 ciclos/dia, 259.200 ciclos em 30 dias e 3.153.600 ciclos/ano de 365 dias. São contagens operacionais, não vida prevista. Precisam ser separados: fadiga dos braços/interfaces, fluência sob carga, relaxação da pré-carga, deformação permanente dos PADs, envelhecimento e abrasão onde houver deslizamento. Sem curvas e espectro, não calcular “horas até quebrar” nem porcentagens de desgaste.

## Massa do componente isolado

Com a geometria CAD maciça e densidades candidatas: PA6-CF aproximadamente 1,516 kg; Tritan TX1001 aproximadamente 1,642 kg; redução analítica aproximadamente 125,21 g neste corpo superior. Não inclui ferragens, braços ou PADs. Não é pesagem nem previsão do componente impresso com preenchimento parcial. O Tritan instalado continua sem produto/condição identificados.
