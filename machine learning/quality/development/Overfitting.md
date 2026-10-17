---
aliases:
  - High variance
---
# Overfitting

## O que é?

 **Overfitting:** Modelo **decora os dados de treino** em vez de aprender padrões generalizáveis. O modelo é bom nos **dados que viu**, mas ruim em **dados novos**. ***High variance***, ***Too complex***, ***Many variables***
## Visualização

```
Train Accuracy: 95%  ← Muito bom
Test Accuracy:  60%  ← Muito ruim
Diferença: 35%       ← PROBLEMA! ❌
```

**Analogia:** Aluno que decora a prova anterior inteira, mas não entende nada. Na prova nova, fracassa.
## Causas Comuns

| Causa                     | Exemplo                                               |
| ------------------------- | ----------------------------------------------------- |
| **Modelo muito complexo** | Rede neural gigante para dataset pequeno              |
| **Treino muito longo**    | Muitas épocas até overfitting total                   |
| **Poucos dados**          | 100 amostras, 1000 features                           |
| **Sem regularização**     | Sem regularization\|L1/L2 para penalizar complexidade |
| **Features demais**       | Incluir todas as colunas sem seleção                  |
## Como Detectar?

### Sinais de Alerta

✅ **Train Accuracy >> Test Accuracy**
- Train: 90%, Test: 60% → Overfitting!

✅ **Loss em treino diminui, loss em teste aumenta**
```
Epoch 1: Train Loss = 0.5, Test Loss = 0.5
Epoch 5: Train Loss = 0.1, Test Loss = 0.8  ← Problema!
```

✅ **Curva de aprendizado diverge**
- Treino: ↓↓↓ (melhora)
- Teste: ↑↑↑ (piora)

---

## Como Evitar/Corrigir?

| Solução | Efetiva | Complexidade |
|---------|---------|-------------|
| **Mais dados** | Muito ✅✅✅ | Alta (caro) |
| **Regularização** (L1/L2) | Muito ✅✅✅ | Baixa (fácil) |
| **Early stopping** | Boa ✅✅ | Baixa (fácil) |
| **Dropout** | Boa ✅✅ | Média |
| **Data augmentation** | Média ✅ | Média |
| **Modelo mais simples** | Média ✅ | Média |
| **Feature selection** | Boa ✅✅ | Média |
## Checklist: Evitar Overfitting

- ✅ Validar com [[train dataset and test dataset|train/test split]] ou cross-validation
- ✅ Monitorar [[machine learning/quality/development/Accuracy|train vs test accuracy]]
- ✅ Usar regularização (L1/L2)
- ✅ Aplicar early stopping
- ✅ Aumentar dados (data augmentation)
- ✅ Simplificar modelo se necessário
- ✅ Feature selection (menos features = menos overfitting)
- ✅ Usar validation set para ajustar hyperparameters
## Resumo

| Aspecto      | Overfitting                               |
| ------------ | ----------------------------------------- |
| **Problema** | Modelo decora treino                      |
| **Sintoma**  | Train >> Test                             |
| **Causa**    | Modelo muito complexo, poucos dados       |
| **Risco**    | Falha total em dados novos                |
| **Solução**  | Regularização, mais dados, modelo simples |
