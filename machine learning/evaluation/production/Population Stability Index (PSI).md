# Population Stability Index (PSI)

## O que é

O **PSI** mede o quanto a distribuição de uma variável mudou entre uma amostra de **referência** (em geral, o treino) e uma amostra **atual** (produção). Ele não precisa de ground truth, por isso é usado para detectar [[Data Drift]] de forma rápida.

A variável é dividida em faixas (bins) e, para cada faixa, compara-se a proporção de registros na referência (`p`) com a da amostra atual (`q`):

```
PSI = Σ (q − p) · ln(q / p)
```

Quanto maior o PSI, maior a mudança na distribuição. Funciona para variáveis contínuas (após o binning) e categóricas.

## Interpretação

Por convenção, PSI < 0,1 é estável, 0,1 a 0,25 é moderado e > 0,25 é mudança significativa.

| PSI | Interpretação |
|---|---|
| < 0,1 | Estável |
| 0,1 a 0,25 | Mudança moderada |
| > 0,25 | Mudança significativa |
