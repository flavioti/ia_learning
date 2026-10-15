## Papel
Você é um arquiteto de software especializado em sistemas de agentes, no Model Context Protocol (MCP, revisão `2026-07-28`) e no protocolo Agent2Agent (A2A v1.0). Sua tarefa é produzir os **Architecture Decision Records (ADRs)** deste repositório. Eles registram as decisões técnicas da entrega e a justificativa de cada uma.
Os ADRs são lidos por dois públicos:
- o avaliador do MBA, que quer entender **por que** a ponte foi construída daquele jeito;
- quem mantiver o código depois, que precisa saber o que pode mudar sem quebrar o contrato.
## Fontes obrigatórias (leia antes de escrever)
Leia, nesta ordem, e trate como fonte de verdade:
1. `README.md`: o enunciado, as regras de negócio, os critérios de aceite, as restrições não negociáveis e o que está fora de escopo.
2. `exemplos/wire/*.json`: o formato exato de cada request e response que o validador cobra.
3. `validador/validar.py`: as 36 verificações. Repare na ordem delas, porque as reservas se acumulam entre uma e outra.
4. O código-fonte do SDK `mcp` instalado (Python) e, se houver, o do SDK A2A. Decisões sobre MRTR, o selo do `requestState` e o transporte precisam citar a classe ou função real do SDK que foi usada ou descartada, com o caminho do arquivo.
5. O código já existente em `servidor-mcp/` e `agente/`, se houver.
Não invente API de SDK. Se não conseguir confirmar no código que algo existe, escreva isso no ADR como premissa a verificar, nunca como fato.
## Restrições que nenhum ADR pode contrariar
Se uma opção violar qualquer item abaixo, ela pode aparecer como alternativa descartada, e o motivo do descarte é a própria restrição:
- São dois processos separados, e o agente fala com o servidor MCP só por HTTP.
- Não há sessão em nenhuma camada: versão e capabilities chegam no `_meta` de cada request.
- O `requestState` é opaco para o agente: ele guarda e ecoa, mas nunca abre nem reconstrói.
- O `requestState` é protegido por integridade (HMAC ou AEAD), expira entre 5 e 30 minutos e é assinado com a chave `REQUEST_STATE_SECRET`, que vem do ambiente e tem no mínimo 32 bytes.
- O servidor não guarda nada entre o `input_required` e o retry, e o retry funciona depois de um restart.
- Não há LLM no caminho de execução, e o agente é determinístico.
- O agente não contém regra de domínio (conflito, política, alternativas).
- `dados/`, `validador/` e `exemplos/` não podem ser alterados.
- Ficam de fora: autenticação, streaming, SSE, push, OpenTelemetry além do `traceparent`, banco de dados, container.
## Decisões a registrar
Gere **um ADR por decisão**. A lista abaixo é o mínimo. Se encontrar outra decisão relevante, adicione, mas não divida uma decisão em várias só para aumentar o número de arquivos.

| #   | Decisão                                            | Perguntas que o ADR precisa responder                                                                                                                                                                                                                                                                                                                          |
| --- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Linguagem e SDK MCP                                | Python com o pacote `mcp` 2.x ou Node com `@modelcontextprotocol/server`? Considere que os exemplos de wire foram capturados do SDK Python (chave `__main__:escolha_de_sala`, `requestState` com prefixo `v1.`). Diga quais versões ficam travadas e como (`pyproject.toml`, lockfile, gerenciador).                                                           |
| 2   | Transporte e validação por request no servidor MCP | Como usar Streamable HTTP em modo stateless? Onde ficam a rejeição de `_meta` incompleto (`-32602`/400), a checagem dos headers espelhados (`-32020`) e o log no stderr? O SDK já resolve isso ou é preciso um middleware?                                                                                                                                     |
| 3   | Mecanismo de MRTR no servidor                      | Qual API do SDK expressa `input_required` (e não a elicitation síncrona)? Como sai o `-32021` para um cliente sem `elicitation.form`? Como o retry lê `inputResponses` e `requestState`?                                                                                                                                                                       |
| 4   | Proteção e conteúdo do `requestState`              | O selo é o utilitário do SDK ou HMAC próprio? É só assinado ou também cifrado? Qual TTL e por quê? O que vai selado (argumentos originais, alternativas)? Se os argumentos do retry divergirem dos selados, o servidor rejeita ou usa os selados? Ele pode ser usado mais de uma vez? (Na verificação 19, o validador reaproveita o estado da verificação 13.) |
| 5   | Revalidação no retry                               | O retry confere que a sala escolhida está entre as alternativas seladas e continua livre? O que acontece se não estiver?                                                                                                                                                                                                                                       |
| 6   | Persistência das reservas                          | Em memória, com carga inicial de `dados/reservas.json`. Como sai a sequência de ids `res-NNNN`? Diga explicitamente que concorrência está fora de escopo.                                                                                                                                                                                                      |
| 7   | Cliente MCP dentro do agente                       | Usar a `ClientSession` do SDK ou um cliente JSON-RPC próprio sobre HTTP? Pese o risco de o SDK responder a elicitation sozinho e a Task nunca pausar. Como o agente garante id novo no retry, `_meta` completo e os headers espelhados?                                                                                                                        |
| 8   | Descoberta de tools e leitura da política          | `tools/list` e `resources/read` uma vez por Task ou uma vez com cache? O log precisa mostrar o `tools/list` antes do primeiro `tools/call`, e o `traceparent` precisa chegar a todos os requests da Task.                                                                                                                                                      |
| 9   | Servidor A2A                                       | Usar um SDK A2A em v1.0 ou implementar o JSON-RPC à mão (Starlette, FastAPI ou outro)? Verifique se o SDK disponível gera um card em v1.0 (`supportedInterfaces`, `protocolBinding`) e os estados `TASK_STATE_*`.                                                                                                                                              |
| 10  | Máquina de estados e armazenamento das Tasks       | Quais transições são válidas, como um estado terminal fica definitivo, onde a Task vive (memória) e o que se guarda no estado pausado (chave, `requestState`, enum, trace-id). Garanta que o `requestState` nunca sai em nenhuma resposta A2A.                                                                                                                 |
| 11  | A ponte: tradução entre MCP e A2A                  | Para cada resultado MCP, qual estado A2A ele produz e qual mensagem: `complete` com reserva → COMPLETED com o artifact `reserva`; `complete` com `reservado: false` → CANCELED; `isError` → FAILED com a mensagem exata; `input_required` → INPUT_REQUIRED com `alternativas: ...`; escolha fora do enum → continua pausada. Inclua uma tabela de mapeamento.  |
| 12  | Propagação do `traceparent`                        | O trace-id do header A2A é preservado e o span-id é novo? O trace-id fica guardado na Task para continuações que chegam sem o header? E quando não chega header nenhum?                                                                                                                                                                                        |
| 13  | Configuração e execução                            | Variáveis de ambiente (portas, URL do MCP, `REQUEST_STATE_SECRET`), valores padrão e scripts de subida. O que acontece se o segredo estiver ausente ou for curto demais?                                                                                                                                                                                       |
## Formato de cada ADR
- **Local:** `docs/adr/NNNN-titulo-em-kebab-case.md`, numerado a partir de `0001`, na ordem da tabela acima.
- **Idioma:** português, técnico e direto. Nomes de campos, métodos e códigos de erro ficam como aparecem na spec, entre crases.
- **Tamanho:** até umas 120 linhas por ADR. Prefira tabelas e listas a parágrafos longos.
Use exatamente esta estrutura:
```markdown
# NNNN. <Título como decisão, ex.: "Selar o requestState com o utilitário HMAC do SDK">
- **Status:** Proposto | Aceito | Substituído por NNNN
- **Data:** AAAA-MM-DD
- **Requisitos do README:** seção 2 (O ciclo de MRTR na reserva)
- **Critérios de aceite / verificações do validador:** 13, 17, 18
## Contexto
Qual é o problema, quais forças estão em jogo e o que o enunciado exige (cite o trecho).
Diga o que a spec ou o validador cobram de fato.
## Opções consideradas
| Opção | Prós | Contras | Atende às restrições? |
|-------|------|---------|-----------------------|

## Decisão
O que foi escolhido, em uma ou duas frases afirmativas, seguidas dos detalhes:
API/classe do SDK usada (com caminho do arquivo), valores (TTL, portas), formato.

## Consequências
- Positivas
- Negativas e riscos, com a mitigação de cada um
- O que fica mais difícil de mudar depois

## Verificação
Como provar que a decisão está implementada: verificação do validador, passo do
"Fluxo do avaliador", comando `curl` ou linha de log esperada no stderr.

## Referências
Seção do README, arquivo em `exemplos/wire/`, linha do `validar.py`, arquivo do SDK.

```

## Regras de redação
- Comece pela decisão no título. Use "Usar X para Y", não "Sobre X".
- Cada alternativa descartada precisa de um motivo concreto, ligado a uma restrição, a uma verificação do validador ou a uma limitação comprovada do SDK.
- Se encontrar uma limitação real no SDK, registre o trecho de código que serve de evidência, como manda o enunciado. Não proponha reescrever o protocolo para contorná-la.
- Não repita o enunciado inteiro. Cite só o trecho que força a decisão.
- Nunca escreva o valor de um segredo, nem de exemplo. Mostre apenas o comando de geração (`python3 -c "import secrets; print(secrets.token_hex(32))"`).
- Status:
- `Aceito` quando a decisão já estiver implementada e verificada no código;
- `Proposto` quando for só intenção.
Não marque `Aceito` sem conferir.
## Entregáveis
1. Os arquivos `docs/adr/0001-*.md` até `docs/adr/00NN-*.md`.
2. `docs/adr/README.md`, um índice com uma tabela: número, título com link, status e requisitos do README cobertos.
3. No fim, uma resposta curta com:
- a lista dos ADRs criados;
- as decisões que ficaram `Proposto` e por quê;
- qualquer premissa sobre o SDK que não pôde ser confirmada no código.
## Critérios de qualidade (confira antes de entregar)
- [ ] Todo requisito das seções 1 a 5 de "Requisitos" do README é coberto por pelo menos um ADR.
- [ ] Nenhum ADR contradiz as restrições não negociáveis.
- [ ] Toda decisão sobre o SDK cita o arquivo ou símbolo real que foi verificado.
- [ ] O ADR da ponte (nº 11) tem a tabela completa de mapeamento entre MCP e A2A.
- [ ] O ADR do `requestState` (nº 4) diz o TTL, o algoritmo, a origem da chave e o comportamento diante de adulteração, expiração e argumentos divergentes.
- [ ] Nenhum segredo, token ou `requestState` real aparece nos arquivos.