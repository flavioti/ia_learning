Nominal: categorias sem ordem (cor, país, porto).
- One-hot encoding (para nominais): cria uma coluna 0/1 para cada categoria.
Ordinal: categorias com ordem natural (classe da passagem, escolaridade, “baixo/médio/alto”).
- Ordinal encoding (para ordinais): mapeia as categorias para números que respeitam a ordem.

| Coluna        | Tipo                   | Por quê                                                                     |
| ------------- | ---------------------- | --------------------------------------------------------------------------- |
| `Sex`         | categórica nominal     | male/female, sem ordem                                                      |
| `Embarked`    | categórica nominal     | portos C, Q, S, sem ordem                                                   |
| `Pclass`      | categórica **ordinal** | 1ª > 2ª > 3ª classe: tem ordem, mas a “distância” entre elas não é numérica |
| `Age`, `Fare` | numéricas              | quantidades de verdade                                                      |
