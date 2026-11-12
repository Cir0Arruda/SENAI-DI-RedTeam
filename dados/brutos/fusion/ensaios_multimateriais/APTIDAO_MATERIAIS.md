# Aptidão dos dados para ensaios no Fusion

Base: pesquisa local `pesquisa_materiais_3d/GUIA_TECNICO_MATERIAIS_FFF.md`. Data: 10/11/2026. Este documento avalia dados disponíveis; não relata resultados de novos solucionadores e não atesta que um tipo de estudo esteja licenciado na conta.

O arquivo `materiais.json` contém oito produtos distintos, fontes e unidades por propriedade. Nenhum campo ausente foi substituído por zero ou pelo valor herdado de um material genérico. As estimativas de massa são analíticas, separadas de simulações.

## Aptidão por produto

| Produto | Estado dos dados mecânicos | Limitação principal |
| --- | --- | --- |
| PETG Polymaker V2.0 | Young, tração e alongamento XY/Z; flexão e impacto | Poisson e constantes de cisalhamento não publicados; sem curva constitutiva térmica ou de longo prazo |
| PCTG 3D-Fuel Pro | Young, tração e alongamento por orientação | Não misturar a tabela impressa com a tabela genérica de resina; Poisson ausente |
| Tritan Eastman TX1001 | Dados de material moldado, incluindo escoamento | Não caracteriza um filamento ou suas interfaces Z; marca comercial não identifica formulação de impressão |
| TPU Bambu 95A HF V3.0 | Young e resistência/alongamento XY/Z | Young linear não descreve grandes deformações; faltam curvas hiperelásticas e viscoelásticas, compressão e rasgo |
| PA6 formulado LEHVOSS 9936 | Dados impressos secos XY/Z | Formulação especial; não representa PA6 puro; faltam constantes completas e dependências ambientais |
| PA12 Fiberlogy | Young, escoamento e alongamento de material | Origem/condicionamento e orientação FFF não estabelecidos; nenhum Z validado |
| PolyMax PC V5.4 | Young, tração e alongamento XY/Z | Ensaio fabricado em ambiente a 90 °C; não transferir os resultados para outra condição de processo |
| PA6-CF Bambu V3.0 | Dados impressos secos XY/Z | Forte anisotropia; não confundir produto PA6-CF com PA-CF genérico; falta caracterização úmida e constitutiva completa |

## Aptidão por ensaio

| Ensaio solicitado | O que já é calculável com os dados pesquisados | O que falta para execução tecnicamente rastreável |
| --- | --- | --- |
| Massa/peso nominal | Massa = densidade × volume geométrico, para os oito produtos | Geometria e volume depositado reais, umidade e densidade do lote; usar gravidade escolhida para força peso |
| Tensão estática linear | Existem E e valores de tração de referência | Poisson; para anisotropia, Ex/Ey/Ez, Gxy/Gxz/Gyz e coeficientes de Poisson consistentes. Apoios e cargas de serviço. TPU restrito a pequena deformação se linear |
| Ruptura/resistência final | Apenas comparação exploratória com resistências de ensaios identificados | Critério de falha apropriado, compressão/cisalhamento, curvas e caracterização interlaminar. Resistência à tração não é escoamento nem compressão |
| Térmico estacionário | HDT/Tg/Vicat ajudam a interpretar, não a alimentar condução | Condutividade k e condições térmicas: temperatura/carga térmica, convecção, radiação/emissividade e contatos |
| Térmico transitório | Densidade disponível | Além de k, calor específico cp e histórico temporal; HDT não fornece cp |
| Termomecânico | E de referência em uma condição | Expansão térmica alpha, Poisson, propriedades em função da temperatura e umidade, temperatura livre de tensão, vínculos |
| Impacto/quedas | Energia potencial ou cinética pode ser calculada quando massa, altura/velocidade forem definidas | Curvas dinâmicas dependentes de taxa/temperatura, plasticidade ou hiperelasticidade, dano/fratura, contato e atrito, alvo e orientação. Charpy/Izod não são uma curva dinâmica constitutiva |
| Desgaste por milhares de horas | Não há previsão de perda dimensional apoiada nos dados atuais | Par de contato, pressão, velocidade/distância, temperatura, lubrificação, rugosidade e coeficiente de desgaste calibrado. Horas sem movimento/carga não determinam desgaste |
| Fluência/relaxação por milhares de horas | Não há modelo temporal identificado | Curvas ensaiadas em tensão/temperatura/umidade e modelo viscoelástico/viscoplástico calibrado. Não extrapolar estático para milhares de horas |
| Fadiga | Não há curva S-N ou epsilon-N identificada | Espectro e razão de carga, frequência, temperatura/umidade, curvas por orientação e regra de dano validada |
| Colagem entre camadas/delaminação | Comparação das resistências de corpos XY/Z | Resistência/energia de fratura em modos I/II/III e lei de interface; modelar corpo homogêneo não reproduz interfaces automaticamente |

## Condições a declarar para testes demonstrativos

Qualquer caso arbitrado para demonstração deve ser chamado de condição assumida de teste, nunca condição de serviço do item. Registrar geometria usada, volume, orientação, preenchimento, apoios/cargas, contato, atrito, duração e valores faltantes que tenham sido aproximados após autorização. Separar dados confirmados de aproximações no material, nome do estudo e relatório.

Para impacto, um exemplo de queda só se torna determinado ao escolher altura, orientação, superfície-alvo e condições de contato. Para longo prazo, definir cenários como 1.000/5.000/10.000 h não cria uma lei física de envelhecimento ou desgaste. Sem dados calibrados, manter esses cálculos como não executados em vez de fabricar resultados.

## Verificação realizada neste cadastro

- Oito identificadores únicos e oito produtos separados.
- Densidade, unidades, origem, condicionamento e URL registrados.
- Lacunas nu, G, k, cp, alpha, fluência, desgaste e fadiga explícitas para todos os registros.
- Escoamento conhecido preservado para PA12 e Tritan; não substituído por UTS nos demais.
- Massa de cubo de 50 mm maciço e com casca de 2 mm/20% interno; massa nominal da esfera de 50 mm incluída.
- Nenhuma atribuição de material ou execução no Fusion foi realizada por este subagente.
