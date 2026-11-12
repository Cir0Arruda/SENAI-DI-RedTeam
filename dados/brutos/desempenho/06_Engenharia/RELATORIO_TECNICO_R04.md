# Relatório técnico SAMI R04


## SAMI R04 | Exterior original, reforços internos


**Regra obrigatória: ALTERAÇÕES EXTERNAS DA GARRA SÃO PROIBIDAS.** As cores representam regiões internas de preenchimento. Nenhuma união das máscaras ao sólido externo foi realizada. Os PADs existentes ficam em componentes e STL próprios; não modificam o BRep da garra.

Escala nominal 1:1. Garra PA-CF: cinco perímetros, TPMS-D 20% na base, 30% amarelo, 50% azul e 70% rosa. PAD TPU95A: núcleo 40%, separado. Vídeo pausado por solicitação do usuário.

| Dado calculado | Resultado | Abrangência |
| --- | --- | --- |
| Massa de PA-CF nas três partes | 1.618,98 g | Sem suportes e sem ferragens |
| Massa dos oito meios-PAD | 93,06 g | Peças TPU95A |
| Massa polimérica montada | 1.712,04 g | PA-CF + TPU; exclui ferragens e ventosas |
| Consumo total de filamento | 2.068,66 g | Inclui suportes e adesão |
| Impacto, térmico, falha e vida útil | Não resolvidos | Sem novos resultados de solver Fusion |

![GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO](desempenho\01_Fusion\GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.png)

Preparação nativa Fusion: três corpos PA originais + oito metades de PAD, zero máscaras como corpos físicos. Nenhum novo job de simulação foi enviado. A imagem é geometria nominal, sem deformação calculada.


---



## 1 | Conferência da geometria e preenchimento


Os STL imprimíveis foram comparados com a tesselação dos BReps nativos antes da exportação, descontando apenas a translação para a mesa. Maior diferença de coordenada: 0,00000763 mm, de arredondamento do STL. Não houve escala, mudança de superfície, engrossamento externo ou modificação dos furos.

| Região | Densidade do núcleo | Implementação |
| --- | --- | --- |
| Garra geral | 20% | TPMS-D; corpo original contínuo |
| Amarelo | 30% | Modificador interno; não constitui peça adicional |
| Azul | 50% | Corredores internos de reforço |
| Rosa | 70% | Regiões internas locais, inclusive sob PADs |
| PAD TPU95A | 40% | Gyroid, hipótese de padrão mantida; não é parte da garra |

As máscaras são volumes de seleção do slicer, recortados automaticamente dentro da peça. Podem ultrapassar visualmente a superfície no modo Preparar, mas não acrescentam volume imprimível. Classificação conferida nos 3MF: um normal_part e três modifier_part por corpo. Prioridade geométrica: 70 &gt; 50 &gt; 30 &gt; 20. Larguras/profundidades das regiões são hipóteses dimensionadas a partir da pintura 2D, não cotas fornecidas.

![CAMADAS_REAIS_INTERNO](desempenho\06_Engenharia\CAMADAS_REAIS_INTERNO.png)

Vista de camadas reais Z=12, 25 e 45 mm do corpo superior, extraídas do G-code. Paredes em escuro e interior em verde. Suportes omitidos para mostrar a estrutura interna. Esta figura não representa tensão, absorção ou deformação.


---



## 2 | Massa, consumo e fabricação em escala real


| Caso | Peças (g) | Suportes (g) | Adesão/outros (g) | Total Orca (g) | Filamento (m) | Tempo estimado |
| --- | --- | --- | --- | --- | --- | --- |
| SUPERIOR | 780,33 | 112,46 | 2,58 | 895,37 | 341,51 | 39h 44min |
| INFERIOR_ESQ | 419,34 | 96,23 | 1,56 | 517,13 | 197,25 | 21h 50min |
| INFERIOR_DIR | 419,32 | 96,28 | 1,56 | 517,15 | 197,25 | 21h 50min |
| PAD | 93,06 | 45,95 | 0,00 | 139,01 | 47,37 | 11h 01min |

Totais: PA-CF nas peças 1.618,98 g; TPU nos PADs 93,06 g; suportes 350,92 g; adesão/outros 5,69 g. Tempo somado de máquina: 94h 26min. Os arredondamentos por linha podem diferir do total em centésimos de grama.

Método: massa do filamento por função, a partir da extrusão E positiva em movimentos XY do G-code, diâmetro nominal 1,75 mm e densidades de 1,09 g/cm³ PA6-CF e 1,22 g/cm³ TPU. Retrações e purga E pura excluídas. A soma foi conferida contra o total do Orca: diferença absoluta menor que 0,02 g em cada caso. Nenhuma dessas massas foi medida em balança; macros externos da impressora podem acrescentar purga não quantificada.

Referência de mesa: K1 Max 300 x 300 x 300 mm, bico 0,4 mm; peça superior aproximadamente 261 x 248,5 x 85 mm; cada suporte 203 x 288 x 72,7 mm. Camada nominal 0,20 mm, linha assumida 0,40 mm; cinco perímetros equivalem a cerca de 2,0 mm nominais, sem garantia de espessura constante em Arachne. Topo/fundo: seis camadas, 1,2 mm. PAD: três perímetros, 1,2 mm, topo/fundo 1,2 mm. Núcleo parcial não significa a mesma porcentagem na massa total.

**Perfis para estimar consumo, não liberados para impressão.** O Orca reportou aviso de dureza do bico em todos os casos e aviso de temperatura da mesa no PAD. O perfil de referência declara bico de latão; PA-CF requer seleção e verificação de bico resistente à abrasão. Os avisos ficam preservados nos JSON. Nenhum arquivo foi enviado à impressora. Tempo também depende dos limites reais, acelerações, macros, suportes e perfil aprovado.

Comparação apenas por densidade: mantendo exatamente o mesmo volume depositado da garra, Tritan TX1001 (1,18 g/cm³, resina moldada de referência) corresponderia a 1.752,66 g; diferença de 133,68 g em favor do PA6-CF. Isso não prevê resistência nem economia da montagem instalada de 2,834/3,03 kg, cuja massa de ferragens e composição real não foram confirmadas.


---



## 3 | Fichas técnicas e limites de transferência


| Propriedade | Bambu PA6-CF V3.0 | PolyFlex TPU95 V5.4 | Aplicabilidade |
| --- | --- | --- | --- |
| Densidade | 1,09 g/cm³ | 1,20-1,24; adotado 1,22 g/cm³ | Massa do filamento; não densidade do núcleo poroso |
| Módulo de tração | XY 4.430; Z 2.170 MPa | XY 33,6 ± 0,9 MPa | Corpos de prova da ficha, não lei efetiva zonal |
| Resistência de tração | XY 102; Z 48 MPa | Tensão a 100%: 11,1 ± 0,3 MPa | Tensão a 100% não é resistência última |
| Alongamento na ruptura | XY 5,8%; Z 3,7% | XY 551,2 ± 23,5% | Não transferir ao PAD40% sem ensaio |
| Flexão | Resistência XY151/Z80 MPa; módulo XY5460/Z2240 MPa | Não informado na ficha usada | Não substituir módulo de tração por flexão |
| Impacto | ISO179 entalhado XY13,4 kJ/m² | Curva de compressão/descarga dinâmica não fornecida | Energia Charpy não é energia admissível da garra |
| Temperatura | Tg68°C; HDT186°C a0,45MPa e164°C a1,8MPa | Bico210-230°C; mesa25-60°C: processo | HDT e temperatura de impressão não são limites de uso24/7 |
| Dureza e grande deformação | Não usada como lei de dano | 95 ShoreA; tensão200/300/400%:15,0/21,0/25,8 MPa | Dureza não determina amortecimento ou curva hiperlástica |

A fibra curta tende a orientar-se ao longo do cordão; a resistência entre camadas depende de fusão, difusão, umidade, temperatura, resfriamento e vazios. Reforçar o preenchimento não elimina a anisotropia nem garante resistência transversal. PA6-CF deve ser caracterizado na condição de umidade e pós-processamento de uso. TPU é a referência termoplástica imprimível, não um PU termofixo genérico nem uma média estatística de fornecedores.

Faltam leis efetivas direcionais para TPMS-D20/30/50/70%, ligadas às cinco paredes e transições; lei compressiva e descarregamento do PAD40% versus taxa e temperatura; dados térmicos aplicáveis, falha, fluência, fadiga e desgaste. Poisson0,49 no cadastro anterior do TPU era hipótese, não medição. Nenhuma curva foi completada com valores inventados.

Fontes primárias e revisões estão nos JSON de fichas e na página de referências. Tritan TX1001 é resina moldada; não caracteriza a impressão Tritan instalada. Não há base para concluir nesta revisão que PA-CF é mais resistente ao impacto que o Tritan real.


---



## 4 | Impacto e temperatura: modelo e resultados pendentes


**Status: preparação geométrica concluída; solver de impacto e térmico não resolvidos.** A antiga hipótese A1/R02 foi bloqueada por propriedades inválidas e falta de contatos. O campo inválido específico não foi exposto. Não foi repetido o pré-check sem mudança técnica justificável; seus módulos equivalentes de30%/Hexa15% não são cartões válidos do novo TPMS-D zonal.

Campanha necessária: mesma geometria externa, cinemática e energia, comparando com e sem PAD. Fixação e conectores devem representar flange, parafusos, braços e ventosas; não fixar superfícies arbitrárias nem remover modos rígidos para esconder falta de apoio. Incluir contato entre impactor, PAD e garra, folgas, retenção e atrito; validar malha e passos de tempo por convergência da força, deformação e energia.

| Saída solicitada | Como calcular/medir | Situação |
| --- | --- | --- |
| Pico de força e deformação | Evento transiente, curvas F(t), deslocamento e deformações direcionais | Não calculado |
| Absorção e proteção do PAD | Energia dissipada da histerese, rebote, força transmitida e tensões na garra | Não calculado; elasticidade sozinha não dissipa energia |
| Ruptura/delaminação | Critérios de falha por direção, interfaces e dano calibrados | Dados de falha insuficientes |
| Temperatura de trabalho | Transiente com k, cp, densidade, contato, convecção e ambiente reais | Não calculado |
| Efeito de temperatura na resistência | E(T), resistência(T), umidade e fluência, vinculados ao cálculo mecânico | Não caracterizado |

Relações para planejar o ensaio, sem afirmar resultados: energia cinética E=0,5 m_eff v²; impulso=integral F dt; trabalho de compressão=integral F dδ; perda por ciclo=área entre carga e descarga. m_eff depende do robô, postura e controle; 24kg de carga transportada não são automaticamente a massa efetiva do choque. Por exemplo, somente como cenário: impactor1kg a0,5m/s possui0,125J; a1m/s,0,5J. A força real e o curso de compressão ainda precisam ser calculados, não inferidos desses números.

Elevar a densidade pode aumentar a rigidez e a força de contato. Amarelo30% não garante absorção superior, e o PAD95A40% não garante redução de pico sem sua lei de compressão. Não existe percentual de melhoria de impacto disponível nesta revisão; o63% ilustrativo do modelo1D antigo não se aplica.


---



## 5 | Uso24/7, desgaste e durabilidade


24/7 significa8.760h por ano apenas como tempo de calendário. Número de ciclos depende da cadência: com um ciclo a cada5s, seriam6.307.200 ciclos/ano; a10s,3.153.600. Esses valores são contagem, não vida útil. O espectro deve separar operação normal, aceleração, paradas, colisões leves e eventos excepcionais.

| Mecanismo | Dados indispensáveis | Verificação proposta |
| --- | --- | --- |
| Fluência e perda de aperto | Tensão, temperatura, umidade, tempo; curvas direcionais de fluência | Carga sustentada, deslocamento residual e pré-carga das fixações |
| Fadiga da garra | Espectro de tensões, razãoR, orientação, condicionamento; curvas de fadiga | Ensaios em corpos de prova e subcomponente, correlação com FEA |
| Desgaste/rasgo do PAD | Par de contato, carga, curso, rugosidade, atrito, ambiente e lei experimental | Massa/volume perdido, trincas, deslocamento e perda de retenção |
| Aquecimento por histerese | Energia dissipada/ciclo e frequência, transferência térmica | Potência média P=E_perdida*f; equilíbrio térmico instrumentado |
| Dano após impactos repetidos | Força transmitida, rebote, deformação permanente, temperatura e ciclos | Comparar PAD novo/usado e condição sem PAD; inspeções intervaladas |

O PAD é sacrificial por intenção de projeto; ainda não há intervalo de troca em horas ou ciclos tecnicamente demonstrado. Definir limites funcionais medidos: folga/escorregamento admissível, espessura mínima, deformação permanente máxima e início de trinca. Não multiplicar resistência estática por fatores arbitrários de envelhecimento para fabricar uma previsão.

Para liberar a campanha: confirmar material/lote, orientação e condição de impressão; caracterizar shell/core nas regiões e interfaces; obter velocidade/massa efetiva e restrições reais; calibrar compressão/descarga do PAD40%; obter dados térmicos/viscoelásticos e de falha; gerar malha adequada; conferir custos antes do envio ao solver. As duas estáticas antigas maciças permanecem históricas e não validam este projeto.

**Conclusão sustentada:** a distribuição interna solicitada foi preparada e fatiada, com exterior original preservado e estimativa de massa/consumo extraída. A melhora de proteção, temperatura admissível, ruptura, desgaste e vida útil continuam sem resultado numérico de simulação.


---



## 6 | Arquivos, reprodução e continuidade


| Pasta/arquivo | Uso correto |
| --- | --- |
| 01_Fusion/GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.f3d | Geometria limpa para preparar estudos; não é uma simulação resolvida nem malha explícita do núcleo |
| 02_STL_PAD/PADs_STL_INDIVIDUAIS.zip | Oito STL individuais dos PADs, em mm; preenchimento é definido no slicer |
| 03_STL_Garra +04_Modificadores | Três envelopes e máscaras separadas. Máscaras são seletores não imprimíveis, não inserts físicos |
| 05_Orca/*K1MAX_ESCALA_REAL.3mf | Abrir como projeto para preservar classificação modifier_part e20/30/50/70%; PAD separado40% |
| 05_Orca/Resultado_*_K1MAX | G-code e3MF de fatiamento com dados reais de consumo; não são arquivos liberados para impressão |
| 06_Engenharia | Massas CSV/JSON, auditorias, camadas reais, fichas e este relatório |
| 00_Continuar +CLAUDE.md | Estado e instruções para continuação; vídeo pausado, sem resultados físicos inventados |

Não importar as máscaras como objetos imprimíveis independentes. STL não armazena porcentagem de preenchimento, material ou estudo mecânico; usar3MF para manter o projeto. Arquivos CAD de ferramentas em FERRAMENTAS_NAO_SIMULAR contêm máscaras ocultas para edição e não devem ser tratados como montagem física para FEA.

Fonte geométrica: Montagem_Geral_Garra.stp, SHA256169cafb686de98662e14d105a4298ace43a7fca4905cb891eb76a38473f6d26f. Nenhuma conversão automática da malha STL original de1.566.676 triângulos foi realizada. Os STL desta revisão foram exportados dos BReps nativos.

Bambu PA6-CF V3.0: https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf

Polymaker PolyFlex TPU95 V5.4: https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyFlex_TPU95_TDS_EN_V5.4.pdf?v=1731956391

Eastman Tritan TX1001: https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312

OrcaSlicer - padrões eTPMS-D: https://github.com/OrcaSlicer/OrcaSlicer/wiki/strength_settings_patterns

OrcaSlicer - CLI: https://github.com/OrcaSlicer/OrcaSlicer/wiki/cli_mode

Perfis oficiais CrealityK1Max: https://github.com/OrcaSlicer/OrcaSlicer/tree/main/resources/profiles/Creality