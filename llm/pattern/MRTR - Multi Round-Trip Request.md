#stateless #pattern 
## O que é o MRTR no [[MCP]]?
- **Definição:** É um padrão projetado para obter informações adicionais do cliente (como a aprovação humana de uma ação, conhecida como [[Human-in-the-Loop]]) durante uma operação iniciada pelo cliente, **sem a necessidade de manter uma sessão de protocolo bidirecional aberta**.
## Como funciona o MRTR
- **Primeira Rodada (Requisição Inicial):** O cliente envia uma chamada (como `tools/call`, `prompts/get` ou `resources/read`) para o servidor.
- **Resposta Intermediária (`input_required`):** Se o servidor precisar de informações adicionais do cliente (por exemplo, elicitação de dados, aprovação do usuário ou listagem de raízes), ele encerra a conexão HTTP imediatamente e retorna um resultado do tipo `input_required`, acompanhado de um token opaco chamado `requestState` e um mapa de solicitações (`inputRequests`). 
- **Segunda Rodada (Retentativa):** O cliente coleta a entrada necessária do usuário ou do ambiente, cria uma nova requisição com um ID distinto e repete a chamada original enviando o `requestState` guardado e as respostas em `inputResponses`.
- **Conclusão (`complete`):** O servidor valida o estado opaco, processa o restante da operação de forma independente e retorna um resultado final com `resultType: "complete"`.
### Vantagens Principais
- **Eliminação de Conexões Longas:** Dispensa o uso de fluxos persistentes complexos como [[Server-Sent Events (SSE)]] ou sessões stateful em balanceadores de carga para pedidos intermediários.
- **Escalabilidade Web-Scale:** Permite que servidores MCP operem sobre infraestruturas HTTP comuns e sem estado, onde cada chamada é tratada de forma isolada.
- **Arquitetura Desacoplada:** Transforma interações que antes dependiam de fluxos bidirecionais complexos em requisições/respostas independentes encadeadas por um identificador de estado seguro (`requestState`)
## Links
https://modelcontextprotocol.io/specification/draft/basic/patterns/mrtr
