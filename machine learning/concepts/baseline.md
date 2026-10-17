## O que é Baseline?

Um **baseline** é um **modelo simples**, treinado com base em um **dataset** (treino), usado na **comparação de futuros modelos** mais complexos.
## Fluxo

```
1. Train dataset ──────────┐
                           ├─→ Treina Baseline (modelo simples)
                           │
                           └─→ Treina Modelo Complexo

2. Avalia ambos no mesmo Test Set

3. Compara resultados:
   ├─ Baseline: 70% accuracy
   └─ Seu Modelo: 85% accuracy
   
4. Diferença: +15% → Justifica a complexidade ✅
```
## Exemplos de Baselines Simples

| Tipo               | Baseline                            |
| ------------------ | ----------------------------------- |
| **Classificação**  | Sempre predizer a classe mais comum |
| **Regressão**      | Predizer a média dos valores        |
| **Série Temporal** | Predizer o último valor observado   |
