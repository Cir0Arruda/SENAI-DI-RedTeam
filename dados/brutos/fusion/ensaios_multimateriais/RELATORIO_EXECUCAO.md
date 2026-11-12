# Auditoria intermediária dos ensaios multimateriais no Fusion

Data: 10/11/2026. Este relatório registra preparação, cadastro documental e impedimentos observados. **Não é um relatório de novos resultados de elementos finitos nem uma conclusão sobre vida útil.**

## 1. Item efetivamente aberto e preservação

O documento ativo verificado no Autodesk Fusion foi **Modelo referência**, contendo o sólido **Corpo1**. O material físico permanece **aço**. O item inspecionado não é a esfera nem o cubo de exemplo da pesquisa anterior.

| Medida | Valor observado |
| --- | --- |
| Volume sólido | 692,4420971293735 cm³ |
| Dimensões da caixa envolvente | 125 × 250 × 50 mm |
| Corpo | Corpo1 |
| Material físico atualmente atribuído | Aço |

As dimensões da caixa envolvente não significam que a peça seja um bloco maciço dessas dimensões. As estimativas de massa usam o volume real do sólido inspecionado.

Antes da preparação, foi preservada a cópia `Modelo_referencia_ANTES_ENSAIOS.f3d`, na pasta raiz FUSION. A exportação após a preparação foi verificada com retorno `True`: `ensaios_multimateriais/Modelo_referencia_ENSAIOS_INICIAIS.f3d`.

## 2. Cadastro realizado: dados documentais, não materiais constitutivos completos

Foram registrados oito produtos no catálogo de atributos **FFF_MATERIAL_CATALOG**, no componente raiz do Design. O arquivo `materiais.json` guarda propriedades, unidades, fontes, direções e lacunas. O cadastro não equivale a oito materiais físicos calculáveis atribuídos ao solucionador.

**O aço não foi convertido automaticamente em polímero, e nenhum estudo novo foi resolvido com os polímeros.** Não foi completado um campo ausente com zero nem mantido um valor herdado de aço para representar uma propriedade desconhecida do filamento.

| Produto | Dados existentes e limites relevantes |
| --- | --- |
| Polymaker PETG V2.0 | Valores impressos XY/Z. Faltam Poisson, cisalhamento completo e leis térmicas/temporais. |
| 3D-Fuel Pro PCTG | Dados por orientação separados dos valores genéricos da resina. Não confundir alta resistência XY/Z com igual ductilidade. |
| Eastman Tritan TX1001 | Propriedades de produto moldado; não caracterizam por si só filamento e união entre camadas FFF. |
| Bambu TPU 95A HF V3.0 | Dados XY/Z; grandes deformações exigem caracterização hiperelástica/viscoelástica, não apenas Young linear. |
| LEHVOSS LUVOCOM 3F PAHT 9936 BK/L | Formulação especial de PA6, sem reforço estrutural. Não é referência universal para PA6 puro. |
| Fiberlogy Nylon PA12 | Propriedades sem direção FFF estabelecida na ficha consultada; não há resistência Z validada nesse cadastro. |
| Polymaker PolyMax PC V5.4 | Dados por direção e condições específicas de fabricação; é necessário reproduzir o estado térmico e de processo. |
| Bambu PA6-CF V3.0 | Dados secos XY/Z com anisotropia; PA6-CF não representa qualquer PA-CF genérico. |

O detalhamento das fontes e das propriedades está em `../pesquisa_materiais_3d/GUIA_TECNICO_MATERIAIS_FFF.md`. A avaliação de aptidão de cada campo para análise está em `APTIDAO_MATERIAIS.md`.

## 3. Estudos iniciados na interface

| Estudo observado | Tipo e configuração inicial | Estado verificável |
| --- | --- | --- |
| 01 Impacto - PENDENTE DADOS E CONTATOS | Dynamic Event Simulation; duração padrão 1 ms e 25 intervalos | Estrutura inicial criada; sem definição das cargas, contatos e materiais de polímeros. Não enviado ao solucionador. |
| Estudo 2 - Térmico | Thermal | Estrutura inicial criada. A verificação prévia reportou **“nenhuma carga com base na temperatura definida”**. Não enviado ao solucionador. |

Esses estudos não constituem ensaios completos. **Nenhum novo cálculo FEA foi enviado, nenhum resultado novo de tensão, temperatura, impacto ou vida útil foi gerado e nenhum crédito de cálculo foi consumido nesta preparação.** O resultado estático anterior da esfera não é resultado deste Corpo1.

## 4. Massa nominal do item aberto

As massas abaixo são **cálculos analíticos**, usando `massa = volume sólido × densidade`. Não são resultados do solucionador nem pesagens. O peso é força, calculada com gravidade convencional de 9,80665 m/s².

| Produto | Densidade, g/cm³ | Massa maciça nominal, g | Força peso, N |
| --- | --- | --- | --- |
| PETG Polymaker | 1,30 | 900,17 | 8,828 |
| PCTG 3D-Fuel | 1,23 | 851,70 | 8,352 |
| Tritan TX1001 | 1,18 | 817,08 | 8,013 |
| TPU 95A HF Bambu | 1,22 | 844,78 | 8,284 |
| PA6 formulado LEHVOSS 9936 | 1,25 | 865,55 | 8,488 |
| PA12 Fiberlogy | 1,01 | 699,37 | 6,858 |
| PC PolyMax | 1,19 | 824,01 | 8,081 |
| PA6-CF Bambu | 1,09 | 754,76 | 7,402 |

Base numérica: `massas_item_aberto.json`, volume 692,4420971293735 cm³. A precisão das casas decimais expressa o cálculo, não a incerteza física. Preenchimento parcial, vazios, umidade, pigmentos e densidade do lote alteram a massa impressa. É necessário obter o volume depositado no fatiador para estimar uma peça com infill e cascas reais; não basta multiplicar a massa maciça pela porcentagem de infill.

As massas também foram registradas no atributo **AnalyticalMasses** do projeto. O documento foi salvo com Ctrl+S; o desaparecimento do asterisco de modificação foi observado. Isso confirma o salvamento do estado preparado, não a execução de um solucionador.

## 5. O que falta para impacto e temperatura

### Impacto

Definir altura de queda ou velocidade/energia incidente, orientação, alvo, sua rigidez/material, contatos, atrito, condições iniciais e restrições. O modelo material precisa de curvas de tensão-deformação apropriadas ao estado, temperatura e taxa de deformação, além de hipóteses de plasticidade, hiperelasticidade ou dano quando pertinentes. Valores Charpy/Izod não substituem essas curvas.

Dynamic Event Simulation considera massa, inércia, contato e deformação dinâmica. O caso padrão dura 1 ms. O limite computacional de execução informado pela Autodesk é de 12 horas; isso é tempo de cálculo, não horas de serviço simuladas. Posicionar corpos quase em contato evita desperdiçar passos calculando voo livre. Fontes: [estudo dinâmico](https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM), [configuração](https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-HOW-TO), [limite de execução](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Can-the-setting-default-value-be-increased-from-0-001-seconds-in-Fusion-Simulation.html), [eficiência da duração](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/SIM-DYN-ES-RED-DURATN-CONCEPT.htm).

### Temperatura e termomecânica

Definir temperaturas impostas, fontes de calor, ambiente, convecção, radiação quando aplicável e contatos térmicos. Condutividade térmica é necessária para condução; expansão térmica e temperatura sem tensão são necessárias para termotensão. Para comportamento estrutural aquecido, são necessárias propriedades dependentes de temperatura e umidade. HDT, Tg e Vicat não fornecem condutividade, calor específico ou expansão.

O estudo Thermal documentado no Fusion é **estacionário**. Não prevê automaticamente evolução térmica, degradação ou envelhecimento durante milhares de horas. [Tipos de estudo oficiais](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-8CC26683-A6DD-4FDC-80BD-0DC40D7ACAF2.htm).

## 6. Milhares de horas: ensaios distintos e dados faltantes

| Fenômeno | Dados que tornam a previsão determinada | Estado atual |
| --- | --- | --- |
| Desgaste por contato | Par de materiais, rugosidade, pressão, movimento, distância/velocidade, lubrificação, temperatura e coeficiente/lei de desgaste calibrados | Não calculado. Não identificado estudo dedicado na lista oficial atual do Fusion. Contato com atrito não prova implementação de perda de material. |
| Fluência | Carga sustentada, temperatura/umidade, curvas de fluência e lei viscoelástica/viscoplástica calibrada | Não calculada. A menção genérica a creep como não linearidade na ajuda não comprova disponibilidade de uma lei temporal específica no solver. |
| Relaxação | Deformação mantida, tempo, ambiente e curvas de relaxação | Não calculada. |
| Fadiga | Espectro, razão e frequência de carga, direção, ambiente, curvas S-N/epsilon-N e regra de dano validada | Não calculada. Respostas oficiais de funcionários Autodesk apontam ausência de cálculo de fadiga no Fusion e alternativa Inventor Nastran. |
| Envelhecimento térmico/UV/químico | Histórico ambiental e cinética de degradação calibrada por ensaios | Não calculado. |

Referências: [não linearidade, documentação Fusion](https://help.autodesk.com/view/fusion360/ENU/?contextId=SIM-NONLIN-STATIC-STRESS), [resposta de suporte sobre fadiga](https://forums.autodesk.com/t5/fusion-design-validate-document/fatigue-analysis-in-fusion-360/m-p/10798133/highlight/true), [resposta de engenheiro Autodesk](https://forums.autodesk.com/t5/fusion-support-forum/fatigue-analysis/td-p/11100277). As respostas de fadiga são de 2021/2022 e foram confrontadas com a lista atual de estudos; não foi presumido suporte novo sem comprovação.

Portanto, cenários de 1.000, 5.000 ou 10.000 horas podem ser definidos como requisitos de investigação, mas ainda não têm resultados previstos. Não é válido extrapolar uma tensão estática, HDT ou ensaio de impacto para uma vida útil em horas. Uma carga estática sem dano explícito não simula desgaste.

## 7. Créditos e acesso

Nenhuma cobrança ocorreu nesta etapa. A documentação geral da Autodesk informa estático linear incluído, Thermal/Thermal Stress com 3 tokens por estudo e Event Simulation com 6. A disponibilidade e o custo reais devem ser observados na conta e no diálogo de execução antes de enviar cada estudo. [Tabela oficial](https://help.autodesk.com/view/fusion360/ENU/?contextId=CC-SIMULATION).

Uma resposta de funcionário Autodesk de 2022 orienta usuários Educação a verificar se Simulation Tasks usa o contrato Education/Unlimited em Preferences > Tokens and Cloud Credits. É apenas um diagnóstico a conferir na interface atual, não prova de que a conta atual tenha créditos ilimitados. [Fonte](https://forums.autodesk.com/t5/fusion-educators-read-only/fusion-360-student-license-cloud-credit/td-p/11154470).

## 8. Skills e coordenação de agentes

A skill local **fusion-material-testing** foi criada, validada e instalada para descoberta na próxima interação. Sua finalidade é reutilizar o fluxo de inspeção, rastreabilidade, preparação, execução e auditoria, distinguindo campos documentais de propriedades usadas pelo solver. Apenas um agente deve controlar a interface/projeto de cada vez; os demais podem pesquisar dados e revisar resultados sem disputar a sessão.

O candidato externo `porameht/pi-autodesk-fusion` foi baixado para revisão como `SKILL_EXTERNA_REVISAO_NAO_INSTALADA.md`. Ele depende da extensão Pi e não foi instalado como se fosse compatível diretamente com esta sessão. Outros servidores MCP pesquisados duplicariam a conexão nativa existente sem comprovar capacidade adicional de análise. [Skill externa revisada](https://raw.githubusercontent.com/porameht/pi-autodesk-fusion/main/skills/autodesk-fusion/SKILL.md).

O [plugin comunitário de interoperabilidade](https://github.com/openai/community-plugins/blob/main/plugins/autodesk-fusion/README.md) declara estado preview e deixa Simulation fora do subconjunto gerenciado. Testes de protocolo ou fixtures não demonstram execução licenciada do kernel/solucionador. Nenhuma dependência externa foi tratada como fonte de dados materiais ou validação de engenharia.

## 9. Critério para continuar e relatar resultados

1. Fixar uso do Corpo1, orientação de impressão, preenchimento, apoios, esforços e ambiente.
2. Completar as lacunas constitutivas por fonte apropriada ou separar aproximações autorizadas de dados medidos.
3. Criar materiais físicos com conferência de cada campo e unidade, evitando herança silenciosa do aço.
4. Definir contatos/cargas; obter verificação prévia sem erros e conferir custo/licença.
5. Executar os estudos suportados, observar conclusão do solver e registrar malha, reações, unidades, escalas, convergência e limitações.
6. Exportar evidências dos resultados efetivamente gerados. Ensaios não executados continuam marcados como pendentes ou indisponíveis.

**Estado final desta auditoria intermediária:** geometria preservada, catálogo documental de oito produtos registrado, massas maciças estimadas e duas estruturas iniciais de estudo criadas. Impacto, temperatura e vida útil permanecem sem novos resultados FEA.
