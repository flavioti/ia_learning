## 1. Semântica de Offsets, Liderança e Replicação

### 🟢 Questão 1 — Retomada de Consumer Group e Offsets

A Kafka consumer group committed [[Offset]] 42 for a partition before stopping. The offset is still valid and retained. Where should the group resume for that partition?

**Resposta Correta:** At [[Offset]] 43, because the committed offset identifies the last processed record.

**Justificativa:** Os commits de offset são persistidos no tópico interno de offsets do Kafka (`__consumer_offsets`) e sobrevivem ao reinício do grupo. Ao retomar o consumo, o grupo inicia a leitura no registro imediatamente posterior ao último registro processado e confirmado (offset 43).

---

### 🟢 Questão 2 — Eleição de Líder de Partição

A [[Partition|partition leader]] broker fails. Another [[Partition|partition replica]] is in the in-sync replica set and is eligible for leadership; the [[Controllers|cluster controller]] remains available. What permits that partition to resume writes?

**Resposta Correta:** The [[Controllers|cluster controller]] elects an eligible in-sync [[Partition|partition replica]] as the new [[Partition|partition leader]].

**Justificativa:** O [[KRaft]] do [[Cluster]] monitora a disponibilidade dos [[Brokers]]. Ao detectar a falha do [[Partition|partition leader]], ele promove automaticamente uma das [[Partition|partition replica]] sincronizadas (In-Sync Replicas — ISR) elegíveis para assumir a liderança, restabelecendo a capacidade de escrita e leitura.

---

### Questão 3 — Garantia de Durabilidade e ISR

A topic has `replication.factor=3` and `min.insync.replicas=2`. A producer uses `acks=all`. Only the leader remains in sync. What should happen to new writes while that condition persists?

**Resposta Correta:** They fail to meet the required ISR count rather than being acknowledged as successful.

**Justificativa:** Com `min.insync.replicas=2` e `acks=all`, o broker exige a confirmação de pelo menos duas réplicas sincronizadas antes de confirmar a escrita ao produtor. Como apenas o líder está ativo no ISR, as novas gravações falham (gerando `NotEnoughReplicasException`) para evitar perda potencial de dados.

---

## 2. Integração, Segurança e Particionamento

### Questão 4 — Ingestão de Dados via CDC

A team wants to ingest database changes into Kafka using an available supported CDC connector rather than writing its own capture service. Which deployment fits?

**Resposta Correta:** Run the connector as a Kafka Connect source connector publishing to Kafka.

**Justificativa:** Na arquitetura do Kafka Connect, conectores de origem (*source connectors*) são responsáveis por capturar alterações de sistemas externos (como logs de transação de bancos de dados via CDC) e publicá-las em tópicos do Kafka, enquanto conectores de destino (*sink connectors*) exportam dados do Kafka para outros sistemas.

### Questão 5 — Diagnóstico de Autorização (ACLs)

A client successfully authenticates to Kafka but receives a topic-authorization error when reading `orders`. What should be checked first?

**Resposta Correta:** Whether the authenticated principal is authorized to read the `orders` topic.

**Justificativa:** Como a autenticação foi concluída com êxito, as credenciais são válidas. O erro indica falha na etapa de autorização, exigindo a verificação das políticas de controle de acesso (ACLs) para confirmar se a identidade autenticada (*principal*) possui permissão de leitura (`Read`) no tópico `orders`.

### Questão 6 — Ordenação de Eventos por Chave

A topic has a fixed partition count. One producer sends each customer's events in order, and consumers process each partition sequentially. How should records be partitioned to preserve per-customer order?

**Resposta Correta:** Use customer ID as a key with consistent key-based partitioning.

**Justificativa:** O Kafka garante a ordenação estrita dos registros apenas dentro de uma mesma partição. Ao definir o customer ID como chave da mensagem, o particionador padrão aplica um hash consistente que direciona todos os eventos de um mesmo cliente para a mesma partição.

---

## 3. Gerenciamento de Consumidores e Processamento de Streams

### Questão 7 — Prevenção de Rebalanceamentos por Processamento Lento

With the classic group protocol and no static membership, a consumer keeps heartbeating but processing a batch takes longer than `max.poll.interval.ms`. Rebalances follow. Which change addresses this cause?

**Resposta Correta:** Reduce work per poll or tune the poll interval to the measured processing time while preserving processing correctness.

**Justificativa:** Os heartbeats são enviados por uma thread em segundo plano, mantendo a sessão ativa, mas o parâmetro `max.poll.interval.ms` limita o intervalo máximo entre chamadas ao método `poll()`. Se o lote demorar mais que esse limite para ser processado, o consumidor é removido do grupo. Reduzir `max.poll.records` ou ajustar o intervalo resolve a causa raiz.

### Questão 8 — Janelas Temporais e Grace Period no Kafka Streams

A Kafka Streams job uses event-time windows with a five-minute grace period. A record arrives after stream-time has passed its window's end plus grace. What should be expected for that windowed aggregation?

**Resposta Correta:** The record is considered late and is not applied to that closed window.

**Justificativa:** O período de carência (*grace period*) define o tempo extra que uma janela baseada no tempo do evento (*event-time*) aguarda por registros atrasados. Quando o *stream-time* ultrapassa o fim da janela somado ao grace period, a janela é fechada definitivamente e registros posteriores são descartados como tardios.

---

## 4. Transações, Idempotência e Recuperação de Desastres

### Questão 9 — Escrita Atômica e Isolamento de Leitura

A producer must publish related records to two topics atomically. Downstream consumers must exclude aborted writes. Which combination provides the required visibility?

**Resposta Correta:** Write both records in one Kafka transaction and use `read_committed` consumers.

**Justificativa:** As transações do Kafka garantem que múltiplas mensagens enviadas a diferentes tópicos ou partições sejam confirmadas ou abortadas de forma atômica. Para que consumidores a jusante ignorem mensagens de transações abortadas ou em andamento, devem ser configurados com `isolation.level=read_committed`.

### Questão 10 — Efeitos Externos e Chaves de Idempotência

A consumer loses its assignment while an external request is still running. A new owner can process the same record before the old request finishes. Which design protects a non-repeatable external effect?

**Resposta Correta:** Use an atomic idempotency key at the external service so both owners' requests resolve to one effect.

**Justificativa:** Durante rebalanceamentos, a perda de atribuição de partição pode fazer com que dois consumidores processem a mesma mensagem concorrentemente (entrega *at-least-once*). Utilizar uma chave de idempotência atômica no serviço de destino assegura que requisições duplicadas resultem em uma única execução efetiva.

### Questão 11 — Compactação de Logs e Tombstones

A service rebuilds entity state by replaying a compacted topic. It was offline long enough to miss a deletion tombstone that has since been cleaned up. Its old local state still contains that entity. What is the safe recovery approach?

**Resposta Correta:** Rebuild from an empty or otherwise authoritative baseline and bound future recovery lag relative to tombstone retention.

**Justificativa:** Em tópicos compactados, os marcadores de exclusão (*tombstones*) são removidos após o prazo definido por `delete.retention.ms`. Se um consumidor ficar offline além desse período, o replay incremental não removerá registros excluídos do estado local antigo, exigindo a reconstrução total a partir de uma base limpa.

### Questão 12 — Replicação Assíncrona e Plano de Failover

A Kafka application replicates asynchronously to another region. Source and target offsets differ, and the replication link is ten minutes behind when the source region fails. What must the failover plan account for?

**Resposta Correta:** Possible loss of unreplicated events and translated or checkpointed consumer positions, with duplicate-safe processing.

**Justificativa:** Na replicação assíncrona entre regiões, uma falha na origem implica a perda potencial dos eventos que estavam na janela de atraso da replicação (10 minutos). Como os offsets numéricos não são idênticos entre clusters distintos, o failover exige tradução de offsets (via checkpoints) e consumidores preparados para lidar com reprocessamentos duplicados.
