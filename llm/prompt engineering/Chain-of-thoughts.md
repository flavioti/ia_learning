#Model-optimization
[[Prompt engineering]]

Is a prompt engineering techinique, to force the model divide a complex problem in intermediary steps, before emit the final answer.

Is linear
## Examples
### Zero-shot
No examples in the prompt
```prompt
PROMPT:

Um servidor web recebe 1.200 requisições por minuto. Cada requisição consome 250 KB de banda. O provedor cobra R$ 0,05 por gigabyte transferido acima da cota gratuita de 500 GB por mês. 

Calcule o custo total estimado de transferência de dados em um mês de 30 dias.

Pense passo a passo:
1. Calcule o volume total de dados gerados por minuto, hora e dia.
2. Converta o total mensal para Gigabytes (GB).
3. Subtraia a cota gratuita para encontrar o tráfego excedente.
4. Aplique a taxa por GB excedente.
5. Apresente o cálculo detalhado de cada etapa e finalize com a resposta.
```
### Few-shot
2 or more examples in the prompt
```prompt
PROMPT:

P: A cafeteria tinha 23 sacos de café. Eles usaram 11 sacos no período da manhã e compraram mais 18 à tarde. Quantos sacos de café eles têm agora?
R: A cafeteria começou com 23 sacos. Usou 11, então 23 - 11 = 12. Depois comprou 18, então 12 + 18 = 30. A resposta é 30.

P: Um galpão tem 5 caixas com 12 lâmpadas em cada uma. O gerente descartou 8 lâmpadas queimadas e depois dividiu o restante igualmente entre 4 salas de escritório. Quantas lâmpadas cada sala recebeu?
R:
```
### Tagged
Use XML or HTML tags to separate visual and structural
```prompt
PROMPT:

Você é um analista de arquitetura de software. Analise o problema abaixo e responda estruturando seu output em duas partes: <raciocinio> para suas etapas de análise e <resposta_final> com a recomendação.

Problema:
Uma aplicação monolítica em Python/Django com banco PostgreSQL está sofrendo com picos de acesso às sextas-feiras. A tabela de 'Pedidos' tem 50 milhões de linhas e as consultas de relatórios do painel administrativo estão travando o banco principal.

Instruções:
- Na tag <raciocinio>, analise as causas-raiz, gargalos de I/O, concorrência e alternativas tecnológicas.
- Na tag <resposta_final>, defina a arquitetura recomendada em ordem de prioridade de implementação (curto, médio e longo prazo).
```
### Self-consistency
Usado em problemas de lógica complexa, onde você orienta o modelo a avaliar múltiplas perspectivas de resolução antes de chegar a um consenso.
```prompt
Determine se a afirmação abaixo é verdadeira ou falsa:

"Se um trem sai da Estação A às 14:00 a 80 km/h e outro sai da Estação B às 14:30 a 100 km/h na mesma linha em sentido contrário, estando as estações separadas por 210 km, eles se cruzarão antes das 15:45."

Para responder:
1. Desenvolva o cálculo usando o método de velocidade relativa.
2. Desenvolva o cálculo usando equações de posição em função do tempo t.
3. Compare os dois caminhos de raciocínio.
4. Se ambos concordarem, declare a resposta final com base no consenso.
```

