# Ensaios da esfera de 50 mm — SUNLU ABS-Like

> Registro histórico da etapa anterior. O material foi posteriormente pesquisado e o ensaio estático foi resolvido. Consulte `RESULTADOS_ESFERA_SUNLU.md` para o estado atual e as limitações das aproximações.

Estado: estudos configurados no Autodesk Fusion; cálculos não executados.

## Ficha técnica registrada; material de cálculo pendente

Material identificado: SUNLU ABS-Like padrão. Foi consultada a TDS oficial SL-TE-WI-100, versão A/0, arquivada em `SUNLU_ABS_Like_TDS_SL-TE-WI-100.pdf`. Por escolha do usuário, foram registrados somente dados confirmados, sem estimativas para os campos ausentes. A pós-cura efetivamente usada não foi informada.

Os dados estão em 14 parâmetros de usuário `SUNLU_` e em atributos da esfera e do componente raiz. Os parâmetros numéricos são registros sem unidade dimensional no Fusion; os nomes e comentários especificam as unidades físicas. Eles não alimentam automaticamente o solucionador.

| Propriedade confirmada | Valor |
| --- | --- |
| Densidade sólida | 1.190 ± 30 kg/m³ |
| Resistência à tração, Z | 28 MPa |
| Resistência à flexão, Z | 36 MPa |
| Módulo de flexão, Z | 980 MPa |
| Alongamento na ruptura, Z | 25% |
| Izod com entalhe, Z | 70 J/m |
| Dureza | 80 Shore D |
| Expansão térmica | 101 × 10⁻⁶ K⁻¹ |
| HDT, ensaio a 0,45 MPa | 50 °C |
| Tg | 44 °C |
| Contração de moldagem | 8% |

O módulo de flexão não foi convertido em módulo de Young. A resistência à tração não foi tratada como escoamento. Faltam módulo de Young, Poisson e condutividade térmica, além de dados constitutivos com temperatura e resistência à compressão para interpretar esses ensaios. Calor específico também não consta na ficha, embora não determine o resultado térmico estacionário.

Não foi criado nem atribuído um material físico calculável com valores herdados de outra resina. O material físico do solucionador continua sendo o aço padrão do documento, que não representa a SUNLU. Portanto, todos os cálculos permanecem pendentes.

## Geometria

- Esfera sólida de diâmetro 50 mm, centrada na origem.
- Volume verificado: 65,44984695 cm³.
- Superfície dividida em três regiões nos planos z = -20 mm e z = +20 mm, sem remoção de material.
- Calotas inferior e superior: área superficial de 785,398 mm² cada.
- Faixa intermediária: área de 6.283,185 mm².

## Estudos preparados

1. **Estudo 1 — Tensão estática:** calota inferior fixa nos três eixos; força distribuída na calota superior com Fx = 0 N, Fy = 0 N e Fz = -100 N. Apoio idealizado, sem modelagem de contato com pratos de compressão.
2. **Estudo 2 — Térmico:** temperatura de 80 °C na calota superior; convecção na faixa intermediária com coeficiente assumido de 10 W/(m²·K) e ar a 20 °C. Calota inferior sem carga térmica explícita (adiabática). Regime estacionário.
3. **03 Termomecanico 80C — PENDENTE RESINA:** clone do estudo térmico convertido em tensão térmica, com as cargas térmicas anteriores, referência sem tensão de 20 °C e calota inferior fixa nos três eixos. Sem força mecânica adicional.

As cargas e temperaturas são condições demonstrativas para explorar o comportamento do modelo; não constituem limites certificados da resina. A condição de 80 °C foi preservada como configuração anterior não resolvida e ultrapassa a Tg e a HDT declaradas: sem dados adicionais, ela não valida o comportamento mecânico da resina aquecida. Não foram configurados os casos adicionais de 500 N e 1.000 N mencionados durante a preparação.

## Arquivo

`Esfera_50mm_SUNLU_ABS_Like_DADOS_CONFIRMADOS.f3d` é a cópia local atualizada com a ficha registrada e os três estudos pendentes. `SUNLU_ABS_Like_DADOS_CONFIRMADOS.json` contém o registro estruturado e as lacunas identificadas. A cópia anterior `Esfera_50mm_Estudos_PENDENTE_RESINA.f3d` foi preservada. O documento original permanece aberto e sem salvar na nuvem.

## Próximos passos

1. Obter as propriedades faltantes e a condição real de pós-cura.
2. Atribuir o material correto ao modelo e conferir as atribuições de cada estudo.
3. Configurar e gerar a malha; verificar refinamento e convergência nas regiões de apoio e carga.
4. Conferir o custo exibido pelo Fusion antes de resolver cada estudo na nuvem.
5. Resolver e registrar deslocamentos, tensões principais, critério de resistência aplicável, temperaturas e fluxo térmico. Ainda não há resultados numéricos de simulação.

## Referências

- TDS SUNLU: https://media.sunlu.com/prod/20260331/cdd6ab82-85d8-49ea-b432-12c6c9c5c005.pdf?filename=TDS
- Tipos de estudo do Fusion: https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-8CC26683-A6DD-4FDC-80BD-0DC40D7ACAF2.htm
- Materiais dependentes de temperatura: https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/SIM-TEMP-DEP-MATERIALS-CONCEPT.htm
