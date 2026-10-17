# Train Dataset and Test Dataset

## O que é?

**Separamos o dataset em dois conjuntos:**
- **Train Dataset** = Treina o modelo (70%)
- **Test Dataset** = Avalia o modelo (30%)
## Por que Separar?

```
┌─────────────────────────────────────┐
│        Dataset Original             │
├──────────────────┬──────────────────┤
│  Train (70%)     │  Test (30%)      │
├──────────────────┼──────────────────┤
│ • Modelo aprende │ • Avalia novo    │
│   com esses      │   desempenho     │
│   dados          │                  │
└──────────────────┴──────────────────┘
```

**Motivos:**
- ✅ Modelo aprende com train, avalia com dados "novos" (test)
- ✅ Detecta **overfitting** (modelo decora treino, falha no teste)
- ✅ Simula desempenho real em dados nunca vistos
- ✅ Avalia modelo de forma justa

## Por que 70/30?

Não é obrigatório! Mas 70/30 é um **padrão prático** porque:

| Proporção | Vantagem                     | Desvantagem                |
| --------- | ---------------------------- | -------------------------- |
| **60/40** | Mais teste para validação    | Menos dados para treino    |
| **70/30** | Balanço entre treino e teste | Padrão prático             |
| **80/20** | Mais treino para aprender    | Menos teste para validação |
| **90/10** | Máximo aprendizado           | Validação fraca            |

**Escolha depende de:**
- Tamanho do dataset (pequeno → % treino maior)
- Complexidade do modelo (complexo → % treino maior)
- Variabilidade dos dados

---

## Qual Acurácia Importa?

**✅ Test Accuracy é a métrica REAL.**
[[machine learning/quality/development/Accuracy|Accuracy]] é usada apenas para **diagnóstico** (detectar problemas).

| Métrica | Propósito | Importância |
|---------|----------|------------|
| **Train Accuracy** | Diagnóstico (detectar overfitting) | Apenas para análise |
| **Test Accuracy** | Desempenho REAL do modelo | É a que reportamos! ✅ |

---

## [[Overfitting]] vs [[Underfitting]]

```
Train Accuracy: 95% | Test Accuracy: 60%
      ↓
   DIAGNÓSTICO: OVERFITTING detectado ❌
   MAS a acurácia REAL é 60% (test)

Train Accuracy: 65% | Test Accuracy: 63%
      ↓
   DIAGNÓSTICO: UNDERFITTING detectado ❌
   A acurácia REAL é 63% (test)

Train Accuracy: 85% | Test Accuracy: 82%
      ↓
   DIAGNÓSTICO: Modelo generalizou bem ✅
   A acurácia REAL é 82% (test)

CONCLUSÃO: Reporte sempre Test Accuracy!
```

## Validação Adicional: Cross-Validation

Para datasets pequenos, use [[k-fold cross-validation]] em vez de apenas 70/30:

```
Dataset ─┬─ Fold 1: Train com 4, Test com 1
         ├─ Fold 2: Train com 4, Test com 1
         ├─ Fold 3: Train com 4, Test com 1
         ├─ Fold 4: Train com 4, Test com 1
         └─ Fold 5: Train com 4, Test com 1

Resultado: Média de 5 avaliações (mais robusta)
```
## Resumo

| Etapa | Ação |
|-------|------|
| 1 | Dividir dados (70% treino, 30% teste) |
| 2 | Treinar modelo com train dataset |
| 3 | Avaliar modelo com test dataset |
| 4 | Comparar métricas (treino vs teste) |
| 5 | Detectar overfitting/underfitting |
