Are [[semantic fragments]] of text.

- In English, 1 token roughly equals **0.75 words** or **4 characters**
- 8,192 tokens =  ~6.000 words.  12 to 15 text pages
- 1.33 tokens per word

Portuguese uses 1.2x more tokens, than english.
- 1 token = 0,55 words | 2,4 to 3 characters

| Language   |                  | Characters | Tokens |                                           |
| ---------- | ---------------- | ---------- | ------ | ----------------------------------------- |
| English    | I am learning AI | 15         | 4      | `['I', ' am', ' learning', ' AI']`        |
| Portuguese |                  | 19         | 5-6    | `['Est', 'ou', ' aprend', 'endo', ' IA']` |

Com base na incidência é feita a decisão da quebra de token, a palavra `cachorro` pode ser fragmentada de diversas formas baseado no conteúdo usado no treinamento, sem tem mais ocorrências das combinações `cacho` e nenhuma para `orro`, esse token será considerado forte, pois não temos a palavra `orro`, mas como temos a palavra `casa`, pode ser que o token seja ['ca', 'chorro'] e outro token ['ca', 'sa'].
Isso é uma simplificação extrema, o algorítimo irá decidir como será a fragmentação.
