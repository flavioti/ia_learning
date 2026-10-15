evaluate multiples decision paths in paralel, [[backtracking]] when a viable path is identified.
Is non linear

```
PROMPT / ALGORITMO ToT (Exemplo conceitual do fluxo):

[Etapa 1: Gerar nós iniciais (Próxima entrega)]
- Opção 1.1: Começar por A
- Opção 1.2: Começar por B
- Opção 1.3: Começar por C

[Etapa 2: Avaliar estados intermediários]
- Avaliador (LLM/Algoritmo):
  * Opção 1.1 (Ir para A): Viável. Tempo = 15min. (Nota: 8/10)
  * Opção 1.2 (Ir para B): Inviável. Trânsito intenso no horário. (Nota: 2/10) -> [DESCARTADO]
  * Opção 1.3 (Ir para C): Viável, mas distante. Tempo = 45min. (Nota: 5/10)

[Etapa 3: Expandir os melhores nós (BFS a partir de 1.1)]
- A partir de A -> Testar próxima parada (B ou C):
  * Rota A -> B: Chega a B às 14:00 (Janela de entrega fechada) -> [BACKTRACKING: Beco sem saída]
  * Rota A -> C: Chega a C às 14:15 (Janela aberta, trânsito livre) -> [MANTIDO]

[Etapa 4: Finalizar o caminho válido]
- De C -> Finalizar em B às 15:30 (Janela de B reaberta).

Resultado Final ToT: Rota A -> C -> B (Caminho validado após descartar A -> B).
```