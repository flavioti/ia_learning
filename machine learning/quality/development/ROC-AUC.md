#binary-classification 
# ROC-AUC

## O que é?

**ROC-AUC** (*Receiver Operating Characteristic – Area Under the Curve*) é uma métrica de avaliação para classificação binária. Ela mede a capacidade do modelo de **ranquear instâncias positivas acima das negativas**, considerando todos os limiares de decisão possíveis.

- **ROC** = curva que mostra o trade-off entre acertos e falsos alarmes
- **AUC** = área sob a curva (0 a 1, quanto maior melhor)

---

## Resumo Rápido

```
ROC-AUC = 0.50  →  Aleatório (modelo não aprende) ❌
ROC-AUC = 0.70  →  Bom (modelo diferencia) ✅
ROC-AUC = 0.90  →  Excelente (muito bom) ✅✅
ROC-AUC = 1.00  →  Perfeito (praticamente impossível em dados reais) 🎯
```

---

## Como a Curva ROC é construída

A curva é traçada variando o limiar de decisão de 1,0 até 0,0 e plotando dois valores:

- **TPR** (True Positive Rate, Recall ou Sensibilidade), no eixo **y**:

  $$\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

- **FPR** (False Positive Rate, ou 1 − Especificidade), no eixo **x**:

  $$\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$

Quanto mais o limiar baixa, mais amostras são classificadas como positivas, e tanto os verdadeiros positivos quanto os falsos positivos aumentam. A curva mostra esse trade-off em todos os limiares.

---

## ROC Curve: Visualização

![ROC Curve](roc_curve.png)

**Interpretação:**
- ➖ **Diagonal (preta)** = Aleatório (AUC = 0.50), modelo sem valor
- 🔴 **Curva Vermelha** = Modelo Fraco (AUC ≈ 0.5), quase não diferencia as classes
- 🟠 **Curva Laranja** = Modelo Bom (AUC ≈ 0.7), diferencia de forma aceitável
- 🟢 **Curva Verde** = Modelo Excelente (AUC ≈ 0.9), diferencia muito bem

**Regra:** quanto mais acima e à esquerda, melhor o modelo. 📈

---

## Interpretação do AUC

| AUC | Qualidade |
|-----|-----------|
| **0.90-1.00** | Excelente |
| **0.80-0.90** | Muito bom |
| **0.70-0.80** | Bom |
| **0.60-0.70** | Regular |
| **0.50-0.60** | Fraco |
| **0.50** | Aleatório (sem valor) |
| **< 0.50** | Pior que o acaso (costuma indicar rótulos invertidos) |

### Interpretação probabilística

O AUC é a probabilidade de uma amostra positiva escolhida ao acaso receber um score maior que o de uma amostra negativa escolhida ao acaso:

$$P(\hat{y}_{\text{pos}} > \hat{y}_{\text{neg}})$$

---

## Propriedades

| Propriedade | Explicação |
|-------------|-----------|
| **Independe do threshold** | Avalia o ranqueamento geral, sem fixar um ponto de corte (ex.: 0,5) |
| **Invariante à escala** | Mede a ordenação das previsões, não as probabilidades calibradas. Transformações monotônicas dos scores não mudam o AUC |
| **Comparação justa** | Permite comparar modelos de forma objetiva |

---

## ROC-AUC vs Acurácia

| Métrica | Usa | Problema |
|---------|-----|----------|
| **Acurácia** | Threshold fixo (50%) | Enganosa com dados desbalanceados |
| **ROC-AUC** | Todos os thresholds | Mostra a capacidade real de separar as classes |

**Exemplo:** dataset com 95% de negativos
- Modelo que prevê sempre "negativo" → 95% de acurácia ❌ (enganoso!)
- Mesmo modelo → ROC-AUC = 0.50 ✅ (revela que é ruim)

---

## Limitação: dados muito desbalanceados

Com **desbalanceamento severo** (ex.: fraude, doenças raras), o ROC-AUC pode dar uma impressão **otimista demais**.

O denominador do FPR inclui todos os verdadeiros negativos (TN + FP). Com muitos negativos, o FPR fica baixo mesmo quando o modelo gera muitos falsos positivos em relação à pequena classe positiva.

> **Regra prática:** com desbalanceamento severo, prefira o [[PR-AUC]] (área sob a curva Precision-Recall), já que a Precision reflete diretamente os falsos positivos contra a classe minoritária.

---

## Exemplo em Python

```python
from sklearn.metrics import roc_auc_score

# Após fazer previsões
y_true = [0, 1, 1, 0, 1, 1]
y_pred_proba = [0.1, 0.8, 0.9, 0.2, 0.7, 0.15]

roc_auc = roc_auc_score(y_true, y_pred_proba)
print(f"ROC-AUC: {roc_auc:.2f}")
# Output: ROC-AUC: 0.88
```

---

## Quando Usar?

✅ **USE:**
- Classificação binária
- Comparar modelos
- Avaliar em diferentes thresholds
- Dados com desbalanceamento moderado

❌ **NÃO use (ou prefira outra métrica):**
- Regressão (não é classificação)
- Desbalanceamento severo, onde o [[PR-AUC]] é mais informativo
- Quando o threshold é fixo e importante

---

## Resumo

**ROC-AUC = métrica robusta que mede a capacidade de ranquear positivos acima de negativos, independente do threshold usado.** Em desbalanceamento severo, confirme também com o PR-AUC.

[[ML metrics]]
