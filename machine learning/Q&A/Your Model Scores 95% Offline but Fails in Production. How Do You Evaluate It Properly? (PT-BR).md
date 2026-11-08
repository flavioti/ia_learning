#QA #interview-question #model-evaluation
## Pergunta

Você construiu um classificador binário para detectar transações fraudulentas (cerca de **0,5% de positivos**). No conjunto de teste (hold-out), ele atinge **99,4% de [[Accuracy|acurácia]]** e **0,95 de [[ROC-AUC]]**. Após o deploy, a equipe de fraude diz que o modelo deixa passar fraudes demais e sinaliza clientes legítimos demais.

1. Por que esses números offline podem parecer ótimos enquanto o resultado de negócio é ruim?
2. Quais métricas você reportaria no lugar, e por quê?
3. Como você escolheria o limiar de decisão (threshold)?
4. Quais erros de avaliação (divisão dos dados, vazamento, tempo) você descartaria antes de confiar em qualquer número?
5. Como continuar avaliando o modelo depois que ele está em produção?

---

## O que uma boa resposta cobre

- **Acurácia não faz sentido com classes desbalanceadas.** Prever "não é fraude" para tudo já dá 99,5%. Veja [[Imbalanced classes]] e [[Accuracy]].
- **As métricas devem refletir o custo de cada erro.** Leia primeiro a [[Confusion Matrix|matriz de confusão]] e depois escolha [[Precision]], [[Recall]], [[F1-Score]] ou [[PR-AUC]].
- **O modelo pontua; o limiar decide.** Métricas como [[ROC-AUC]] independem do limiar, mas a produção usa um único ponto de operação.
- **A divisão dos dados deve imitar a produção.** [[K-Fold Cross-Validation|K-fold]] aleatório em dados ordenados no tempo vaza o futuro; use divisão temporal ([[Backtest]]).
- **Descarte [[Data Leakage|vazamento de dados]]** antes de comemorar uma pontuação alta.
- **A avaliação não termina no deploy.** Veja [[Monitor Accuracy in Production Continuously]] e [[Model drift]].

---

## Resposta modelo

### 1. Por que o offline parece bom e a produção não

- **Desbalanceamento de classes:** com 0,5% de positivos, 99,5% de acurácia é o baseline de um modelo que nunca sinaliza nada. 99,4% é na verdade *pior* que esse baseline.
- **O ROC-AUC é otimista com positivos raros:** a taxa de falsos positivos tem um denominador enorme (todas as transações boas), então mesmo muitos alarmes falsos mal mexem na curva ROC. O [[PR-AUC]] os expõe, pois a precisão usa os falsos positivos diretamente.
- **Distribuição diferente:** o conjunto de teste pode não se parecer com o tráfego real (período diferente, novos padrões de fraude, [[Model drift|drift]]).
- **Vazamento:** uma variável que só é conhecida *depois* que a fraude é confirmada (por exemplo, "flag de chargeback" ou "conta bloqueada") infla todas as métricas offline.

![Curva ROC do detector de fraude com AUC = 0,95 e o ponto de operação com FPR de 5%](fraud_roc_curve.png)

Como ler o gráfico (curva sintética, apenas ilustrativa): a curva fica colada no canto superior esquerdo, por isso o [[ROC-AUC]] é 0,95. Mas, no ponto de operação com **FPR = 5%** e **recall ≈ 75%**, a precisão é de apenas **≈ 7%**: com 0,5% de fraudes, os 5% de transações boas sinalizadas por engano superam em muito as fraudes capturadas, e cerca de 13 de cada 14 alertas são falsos. A curva ROC não mostra isso, porque o eixo X divide pelo total de transações boas (um denominador enorme). Por isso, para classes raras, acompanhe também a curva [[PR-AUC|precisão-recall]].

![Curva precisão-recall do mesmo detector de fraude, com PR-AUC de 0,30 e o ponto de operação com precisão de 7%|760](fraud_pr_curve.png)

O mesmo modelo, visto na curva precisão-recall (mesma curva sintética, com 0,5% de fraudes): o **PR-AUC é ≈ 0,30**, bem longe dos 0,95 do ROC-AUC. A linha tracejada é o baseline de um modelo aleatório: sua precisão é igual à prevalência (0,5%), e não 50% como na diagonal do ROC. O ponto de operação (recall ≈ 75%, precisão ≈ 7%) fica na parte baixa da curva, onde o ganho de recall custa muita precisão. Aqui o problema fica visível, e é por isso que o [[PR-AUC]] é a métrica mais honesta para esse caso.

### 2. Métricas a reportar

| Métrica                                                            | Por que é útil aqui                                              |
| ------------------------------------------------------------------ | ---------------------------------------------------------------- |
| [[Recall]] (fraudes capturadas)                                    | Fraude não detectada custa dinheiro diretamente                  |
| [[Precision]] (sinalizados que são fraude de fato)                 | Alarmes falsos incomodam clientes e consomem tempo dos analistas |
| [[PR-AUC]]                                                         | Independe do limiar e é sensível à classe minoritária            |
| [[F1-Score]] ou F-beta                                             | Número único; use F2 se o recall importa mais que a precisão     |
| Precisão com recall fixo (ou recall com orçamento fixo de revisão) | Reflete como a equipe de fraude realmente trabalha               |
| Custo esperado                                                     | `FN × custo da fraude + FP × custo de revisão/atrito`            |

Sempre reporte a [[Confusion Matrix|matriz de confusão]] no limiar escolhido, além de um **baseline ingênuo** (sempre "não é fraude", ou uma regra simples) para comparação.

![Matriz de confusão do detector de fraude no limiar com FPR de 5%: 376 VP, 124 FN, 4.975 FP e 94.525 VN](fraud_confusion_matrix.png)

Matriz de confusão do mesmo limiar dos gráficos anteriores (FPR = 5%), aplicado a 100.000 transações sintéticas com 0,5% de fraudes (500 fraudes e 99.500 legítimas):

- **VP = 376:** fraudes capturadas (recall de 75,2%).
- **FN = 124:** fraudes que passaram sem ser detectadas.
- **FP = 4.975:** clientes legítimos sinalizados por engano. São quase **13 vezes mais** que as fraudes capturadas, por isso a precisão é de apenas 7,0%.
- **VN = 94.525:** legítimas aprovadas corretamente.

Neste limiar a acurácia seria de 94,9%, abaixo do baseline ingênuo de 99,5% (aprovar tudo). Os 99,4% da pergunta correspondem a um limiar mais conservador, que sinaliza menos transações: números ilustrativos, mas a lição é a mesma. A acurácia não revela nem os 124 FN nem os 4.975 FP; só a matriz mostra os dois tipos de erro, que têm custos diferentes.

### 3. Escolhendo o limiar

1. Obtenha **probabilidades**, não apenas rótulos (verifique a calibração de probabilidades se os escores forem usados como estimativa de risco).
2. Calcule precisão, recall e custo esperado para cada limiar em um conjunto de **validação**, nunca no conjunto de teste.
3. Escolha o limiar que minimiza o custo esperado, ou que atende a uma restrição de negócio (por exemplo, "revisar no máximo 1.000 casos por dia").
4. Confirme uma única vez no conjunto de teste intocado e revise o limiar conforme a taxa de fraude mudar.

### 4. Erros de avaliação a descartar

- **Divisão aleatória em dados temporais:** treine no passado, valide no futuro (divisão temporal, ou [[Backtest]] com origem móvel).
- **Mesmo cliente em treino e teste:** agrupe a divisão pelo id do cliente/conta.
- **[[Data Leakage|Vazamento de dados]]:** variáveis indisponíveis no momento da predição; pré-processamento (normalização, reamostragem) ajustado antes da divisão.
- **Reamostrar o conjunto de teste:** faça oversampling/undersampling apenas nos folds de treino; mantenha validação e teste com a taxa real de fraude.
- **Ajustar hiperparâmetros no conjunto de teste:** use validação aninhada ou um hold-out final usado uma única vez.
- **Divisão única:** com tão poucos positivos, use [[K-Fold Cross-Validation]] estratificado (ou repetido) e reporte a **variância / intervalo de confiança**, não um único número.

### 5. Depois do deploy

- **Rótulos atrasados:** a fraude confirmada pode levar semanas, então o recall real só é conhecido depois. Enquanto isso, acompanhe proxies: distribuição dos escores, [[Population Stability Index (PSI)|PSI]], taxa de alertas.
- Compare com o modelo atual usando [[champion and challenger]] (modo sombra ou teste A/B).
- Fique atento ao [[concept drift]]: fraudadores se adaptam, então o desempenho decai.
- Registre cada predição com id, timestamp e versão do modelo para juntar os rótulos depois ([[Ground Truth]]).

---

## Armadilhas comuns (perguntas de acompanhamento)

- "Por que não fazer oversampling da classe fraude até balancear?" Isso altera a probabilidade a priori: as probabilidades ficam descalibradas, e avaliar em dados reamostrados está errado.
- "O ROC-AUC subiu, mas o PR-AUC caiu. Em qual você confia?" No PR-AUC, para positivos raros.
- "A precisão é 90% e o recall é 10%. Bom ou ruim?" Depende do custo: é seguro para os clientes, mas deixa passar 90% das fraudes.

## Relacionados

- [[quality/development/README|Qualidade do modelo em desenvolvimento]]
- [[Model Evaluation]]
- [[Evaluation classification model metrics]]
- [[Mock Senior ML Interview]]
