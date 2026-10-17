---
aliases:
  - High Bias
---
# Underfitting

## O que é?

**Underfitting:** Modelo **não aprende bem** os padrões nos dados. O modelo é ruim nos **dados de treino** e também nos **dados novos**. ***High Bias***, ***Too simple***, ***few variables***
## Visualização

```
Train Accuracy: 65%  ← Ruim
Test Accuracy:  63%  ← Ruim
Diferença: 2%        ← Pequena (mas ambos baixos!) ❌
```

**Analogia:** Aluno que não estudou nada. Fracassa tanto nos exercícios quanto na prova.

---

## Causas Comuns

| Causa | Exemplo |
|-------|---------|
| **Modelo muito simples** | Regressão linear para relação não-linear |
| **Poucos features** | Perdeu features importantes |
| **Treino insuficiente** | Poucas épocas, learning rate muito alto |
| **Regularização excessiva** | L2 muito forte, sufoca o modelo |
| **Dados de baixa qualidade** | Noise, erros, features ruins |

---

## Como Detectar?

### Sinais de Alerta

✅ **Train Accuracy baixa (< 60%)**
- Train: 55%, Test: 53% → Modelo não aprende!

✅ **Train Loss não diminui**
```
Epoch 1: Train Loss = 0.8
Epoch 5: Train Loss = 0.75  ← Melhora mínima
Epoch 10: Train Loss = 0.73 ← Estagnado!
```

✅ **Curva de aprendizado plana**
- Treino: ↗️ (melhora lenta)
- Teste: ↗️ (também lenta)
- Ambas ficam presas em nível baixo

---

## Como Corrigir?

| Solução | Efetiva | Complexidade |
|---------|---------|-------------|
| **Modelo mais complexo** | Muito ✅✅✅ | Média |
| **Treinar mais** | Boa ✅✅ | Baixa (fácil) |
| **Adicionar features** | Boa ✅✅ | Média |
| **Diminuir regularização** | Boa ✅✅ | Baixa (fácil) |
| **Learning rate melhor** | Boa ✅✅ | Média |
| **Melhorar dados** | Muito ✅✅✅ | Alta (caro) |
| **Feature engineering** | Boa ✅✅ | Alta (tempo) |

---

## Exemplo em Python

### Detectar Underfitting

```python
# Após treinar
train_accuracy = 0.58  # Ruim
test_accuracy = 0.55   # Ruim
train_loss = 0.75      # Alto

if train_accuracy < 0.6 and train_loss > 0.7:
    print("⚠️ Possível UNDERFITTING!")
    print("Tente: modelo mais complexo, mais features, menos regularização")
```

### Modelo Simples → Complexo

```python
# ❌ Modelo simples demais
from sklearn.linear_model import LinearRegression
modelo_simples = LinearRegression()
# Train Acc: 58%, Test Acc: 55%

# ✅ Modelo mais complexo
from sklearn.ensemble import RandomForest
modelo_complexo = RandomForest(n_estimators=100, max_depth=10)
# Train Acc: 82%, Test Acc: 79% (muito melhor!)
```

### Aumentar Features

```python
# ❌ Poucos features (perde informação)
X_train_small = X_train[['idade', 'renda']]
modelo.fit(X_train_small, y_train)
# Train Acc: 60%

# ✅ Mais features (mais informação)
X_train_full = X_train[['idade', 'renda', 'score', 'histórico', ...]]
modelo.fit(X_train_full, y_train)
# Train Acc: 85% (muito melhor!)
```

### Reduzir Regularização

```python
# ❌ Regularização muito forte
modelo = Ridge(alpha=100)  # Penalidade muito alta
# Train Acc: 62%

# ✅ Regularização moderada
modelo = Ridge(alpha=1.0)  # Penalidade equilibrada
# Train Acc: 85% (melhor!)
```

---

## Visualização: Curva de Aprendizado

```
Accuracy
   |
100|
   |     ╱╱╱ Esperado (bom modelo)
   |   ╱╱
   | ╱╱  ╱─── Observado (underfitting)
  0|___╱_____ Época
       ↑
    Ambos ficam presos em nível baixo
```

---

## Trade-off: Bias vs Variance

**Underfitting = Alto Bias**
- Modelo não consegue capturar padrões (assumptions erradas)
- Será ruim sempre
- Mesmo com mais dados, não melhora muito

**Vs Overfitting = Alto Variance**
- Modelo é muito sensível
- Generaliza mal em dados novos

**Meta:** Balanço entre Bias e Variance ⚖️

---

## Underfitting vs Overfitting

| Aspecto | Underfitting | Overfitting |
|--------|--------------|------------|
| **Train Accuracy** | Baixa (< 60%) | Muito Alta (> 90%) |
| **Test Accuracy** | Baixa (< 60%) | Muito Baixa (< 60%) |
| **Diferença** | Pequena | Grande (> 15%) |
| **Causa** | Modelo simples | Modelo complexo |
| **Solução** | Complexificar | Simplificar/Regularizar |
| **Risco** | Não aprende nada | Decora, falha em novos |

---

## Checklist: Corrigir Underfitting

- ✅ Aumentar complexidade do modelo
- ✅ Adicionar mais features/feature engineering
- ✅ Treinar por mais épocas
- ✅ Reduzir regularização (se existe)
- ✅ Ajustar learning rate
- ✅ Melhorar qualidade dos dados
- ✅ Remover features irrelevantes (às vezes ajuda)
- ✅ Usar validação cruzada para validar mudanças

---

## Resumo

| Aspecto | Underfitting |
|--------|--------------|
| **Problema** | Modelo não aprende padrões |
| **Sintoma** | Train ≈ Test (ambos baixos) |
| **Causa** | Modelo simples, poucos features |
| **Risco** | Desempenho ruim sempre |
| **Solução** | Modelo complexo, mais features |

---

## Diagnosticar: Qual é o Problema?

```
Seus resultados:
├─ Train Acc: 95%, Test Acc: 60% 
│  → OVERFITTING (decora treino)
│
├─ Train Acc: 65%, Test Acc: 63%
│  → UNDERFITTING (não aprende)
│
└─ Train Acc: 85%, Test Acc: 82%
   → BÁLANCE! (modelo bom) ✅
```
