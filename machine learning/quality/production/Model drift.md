# Model Drift

Model Drift =  [[data drift]] and [[context drift]]

## O que é?

**Model Drift** = perda de desempenho do modelo em produção porque o mundo (dados ou relações entre variáveis) mudou depois do treino. Não é bug de código: o modelo continua executando igual, mas o que ele aprendeu deixa de valer.

Diferente de software convencional, o modelo **envelhece** mesmo sem nenhuma alteração.

> **Drift ≠ degradação.** Drift é a *mudança* (nos dados ou no conceito); degradação é a *consequência* (queda de métrica). Pode haver data drift sem queda de desempenho, por isso monitorar só a métrica final é insuficiente.

**Exemplos:**
- 🏠 Preço de imóveis: modelo treinado antes de uma alta forte de preços
- 📱 Fraude: fraudadores mudam de técnica
- 💰 Score de crédito: a economia muda e os padrões de pagamento mudam
- 📊 Previsão de vendas: mercado e concorrência evoluem
## Como Detectar?

A detecção tem duas camadas. Os sinais **sem ground truth** são rápidos e funcionam como alerta; os sinais **com ground truth** são lentos e servem como confirmação (veja [[Monitorar accuracy em produção continuamente]]).
### Camada 1: Sinais rápidos (sem [[machine learning/concepts/Ground Truth|Ground Truth]])

| Sinal                          | O que observar                                         | Velocidade         |
| ------------------------------ | ------------------------------------------------------ | ------------------ |
| **Distribuição das features**  | KS-test (contínuas), qui-quadrado ou PSI (categóricas) | ⚡ Segundos/minutos |
| **Distribuição das previsões** | Proporção de cada classe prevista mudou                | ⚡ Minutos          |
| **Confiança do modelo**        | Probabilidade máxima média caiu                        | ⚡ Segundos         |
| **Intervalo das features**     | Valores fora do min/max do treino                      | ⚡ Segundos         |

```python
from scipy.stats import ks_2samp

# Data drift em uma feature contínua
estatistica, pvalue = ks_2samp(X_train["idade"], X_prod["idade"])
if pvalue < 0.05:
    print("⚠️ Possível Data Drift em 'idade'")

# Valores fora do intervalo visto no treino
fora = (X_prod["preco"] < X_train["preco"].min()) | (X_prod["preco"] > X_train["preco"].max())
if fora.mean() > 0.01:  # mais de 1% das linhas
    print("⚠️ Feature 'preco' fora do intervalo de treino")
```

**Cuidados com o KS-test:**
- Com amostras muito grandes, o p-value fica minúsculo mesmo para diferenças irrelevantes. Combine com um tamanho de efeito (estatística KS) ou PSI.
- Testando muitas features, alguns alarmes falsos são esperados. Ajuste o limiar (ex.: Bonferroni) ou priorize as features mais importantes.

### Camada 2: Confirmação (com ground truth)

Só é possível quando o rótulo real aparece, o que pode levar dias ou semanas.

| Métrica                                                     | Observação                             |
| ----------------------------------------------------------- | -------------------------------------- |
| [[machine learning/quality/development/Accuracy\|Accuracy]] | Boa para classes balanceadas           |
| [[Precision]] / [[Recall]] / [[F1-Score]]                   | Preferíveis com classes desbalanceadas |
| [[ROC-AUC]]                                                 | Independe do threshold                 |

```python
baseline = 0.85  # accuracy medida no teste, no momento do deploy

acuracias = {"dia_1": 0.85, "dia_30": 0.82, "dia_60": 0.78, "dia_90": 0.71}

if acuracias["dia_90"] < baseline * 0.95:  # queda relativa > 5%
    print("❌ Degradação confirmada")
```

---

## Impacto

Ilustrativo, os números variam por problema:

```
Tempo        Accuracy
  ├─ Dia 1:    85% ✅
  ├─ Mês 1:    82% ✅
  ├─ 3 Meses:  75% ⚠️ (drift começou)
  ├─ 6 Meses:  65% ❌ (perto ou abaixo do baseline)
  └─ 1 Ano:    55% ❌ (inutilizável)

ROI cai progressivamente.
```

---

## Como Mitigar?

### 1. Retraining periódico
Retreinar com dados recentes e só promover o novo modelo se ele superar o atual em um teste atualizado.

```python
novo = treinar(X_recente, y_recente)
if avaliar(novo, X_teste_recente, y_teste_recente) > avaliar(atual, X_teste_recente, y_teste_recente):
    deploy(novo)
```

- ✅ Adapta o modelo ao novo padrão
- ❌ Caro (coletar dados, retreinar, validar)

### 2. Champion-Challenger
Treinar um *challenger* em ciclo fixo (ex.: semanal) e compará-lo ao *champion* em produção. Detalhes em [[Monitorar accuracy em produção continuamente]].

- ✅ Automático, adapta-se sozinho
- ❌ Custo recorrente de retreino; precisa de um conjunto de avaliação confiável e recente

### 3. Online learning
O modelo é atualizado incrementalmente com os dados que chegam.

```python
for batch in streaming_data:
    modelo.partial_fit(batch.X, batch.y)
```

- ✅ Adaptação rápida
- ❌ Pode degradar com dados ruins ou rótulos atrasados; difícil de auditar

### 4. Monitoramento contínuo com gatilho de retreino
Alertar quando um sinal ultrapassa o limiar e disparar o retreino ([[Continuous Training - CT]]). Retreinar automaticamente a partir de um único sinal rápido é arriscado; prefira usar o sinal para investigar e a confirmação (ground truth) para decidir.

### 5. Features estáveis
Preferir variáveis que mudam devagar.

```
❌ "preço do Bitcoin" (muda a toda hora)
✅ "categoria do produto" (estável)
```

---

## Quando Retreinar?

| Frequência | Use quando |
|-----------|-----------|
| **Diária** | Ambiente muito dinâmico (fraude, preço) |
| **Semanal** | Mudança moderada (score de crédito) |
| **Mensal** | Mudança lenta |
| **Sob demanda** | Drift detectado e confirmado (melhor prática) |

---

## Checklist

- ✅ [[Monitorar accuracy em produção continuamente]]
- ✅ Monitorar distribuição das features e das previsões
- ✅ Monitorar confiança do modelo
- ✅ Registrar previsões para cruzar depois com o ground truth
- ✅ Alertar quando a métrica cair além do limiar (ex.: 5%)
- ✅ Retreino automatizado com validação antes do deploy
- ✅ Manter histórico de modelos para rollback

---

## Model Drift vs [[Overfitting]]

| Aspecto | Model Drift | Overfitting |
|--------|-------------|-------------|
| **Quando ocorre** | Em produção, ao longo do tempo | Durante o treino |
| **Causa** | O mundo mudou | O modelo memorizou o treino |
| **Sinal** | Métrica em produção cai com o tempo | Train >> Test |
| **Solução** | Monitorar e retreinar | Regularizar, simplificar |

---

## Resumo

| Aspecto | Descrição |
|--------|-----------|
| **Problema** | Desempenho cai porque dados/conceito mudaram |
| **Tipos** | Data Drift, Target Drift, Concept Drift |
| **Detecção rápida** | Distribuição de features/previsões, confiança |
| **Confirmação** | Accuracy, F1, Precision, Recall com ground truth |
| **Mitigação** | Retraining, Champion-Challenger, online learning |

Modelos não são "set and forget": planeje monitoramento e retreino desde o deploy.

[[ML metrics]]
