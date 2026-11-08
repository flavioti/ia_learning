## About

Framework do Apache Kafka para **mover dados entre o Kafka e sistemas externos** (bancos, data lakes, filas, APIs) apenas com configuração, sem escrever código. Por baixo, ele usa [[Apache kafka Producer|producers]] e [[Apache Kafka Consumer|consumers]] do Kafka e cuida de offsets, retries, rebalance e paralelismo.

## Source e Sink

| Tipo de connector | Direção | Usa por baixo | Exemplos |
| --- | --- | --- | --- |
| **Source** | Sistema externo → Kafka | **Producer** | Debezium ([[CDC]]), JDBC source, arquivos |
| **Sink** | Kafka → sistema externo | **Consumer** | S3, Elasticsearch, JDBC sink |

```
Postgres --(Debezium, source)--> Kafka --(S3 sink)--> Data Lake
```

## Relação com consumers

- **Sink connector:** cada task é um consumer, e todas as tasks formam um **consumer group** chamado `connect-<nome-do-connector>`.
  - O offset fica em `__consumer_offsets`, como em qualquer consumer group.
  - As [[Kafka Topic Partition|partições]] são divididas entre as tasks. Se uma task sai, ocorre rebalance.
- **Source connector:** cada task é um producer. O "offset" aqui é a posição na origem (LSN do banco, ponto do arquivo), e não um offset de tópico. O Connect o guarda em um tópico interno (`connect-offsets`, por padrão).

## Componentes

| Componente | O que é |
| --- | --- |
| **Worker** | Processo (JVM) que roda os connectors. Vários workers formam um cluster do Connect, **separado** do [[Kafka cluster]] |
| **Connector** | A configuração da integração (qual tabela, qual tópico, qual destino) |
| **Task** | Unidade que de fato lê ou escreve. É a que se comporta como consumer ou producer. `tasks.max` define quantas existem |
| **Converter** | Serializa e desserializa as mensagens (JSON, Avro, Protobuf) entre o Connect e o Kafka |
| **SMT** (Single Message Transform) | Transformação simples por mensagem (renomear campo, mascarar, rotear) |
| **Dead letter queue** | Tópico para mensagens que falharam (só em sink connectors) |

Os workers guardam seu estado em tópicos internos do Kafka: configuração dos connectors, offsets dos sources e status.

## Paralelismo

Em um sink, o número útil de tasks é limitado pelo **número de partições do tópico**, pela mesma regra de qualquer consumer group (1 partição por consumer). Um tópico com 2 partições aproveita no máximo 2 tasks. Uma terceira ficaria ociosa.

## Modos de execução

| Modo | Uso |
| --- | --- |
| **Standalone** | 1 worker, configuração em arquivo. Bom para desenvolvimento e testes |
| **Distributed** | Vários workers, com tolerância a falhas e rebalance de tasks. Padrão em produção, com connectors gerenciados pela API REST (porta 8083) |

```bash
# criar um connector via API REST (modo distributed)
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "orders-s3-sink",
    "config": {
      "connector.class": "io.confluent.connect.s3.S3SinkConnector",
      "topics": "orders-topic",
      "tasks.max": "2"
    }
  }'
```

O exemplo é ilustrativo: cada connector exige as próprias configurações (bucket, formato, credenciais).

## Connect ou consumer próprio?

| | Kafka Connect | Consumer próprio |
| --- | --- | --- |
| Esforço | Só configuração (JSON) | Código, testes e deploy |
| Offsets, retry e rebalance | Já tratados | Você implementa |
| Conectores | Centenas prontos (JDBC, S3, Debezium) | Você escreve |
| Lógica de negócio | Limitada (transforms simples) | Livre |

Use o Connect para **mover dados** entre sistemas, e um consumer próprio para **processar** com regra de negócio.

## Pontos de atenção

- **CDC e deletes:** o Debezium emite um evento de `delete` e depois um **tombstone** (valor `null`) para a mesma chave. Em tópicos compactados isso remove a chave. Veja [[Kafka Topics]].
- **Falhas de conversão:** por padrão, uma mensagem inválida para o converter derruba a task. Configure `errors.tolerance` e a dead letter queue para decidir o que fazer.
- **Semântica de entrega:** sinks costumam ser *at-least-once*. Para evitar duplicatas, o destino deve ser idempotente (upsert por chave, por exemplo).
- **Recursos:** os workers consomem CPU e memória próprias, fora dos brokers. Dimensione o cluster do Connect separadamente.

## Related

- [[data architecture/Apache Kafka/Apache Kafka Consumer.md|Apache Kafka Consumer]]
- [[data architecture/Apache Kafka/Apache kafka Producer.md|Apache Kafka Producer]]
- [[data architecture/Apache Kafka/Kafka Topics.md|Kafka Topics]]
- [[data architecture/Apache Kafka/Kafka Topic Partition.md|Kafka Topic Partition]]
- [[data architecture/Apache Kafka/Kafka cluster.md|Kafka cluster]]
- [[data architecture/CDC.md|CDC]]
