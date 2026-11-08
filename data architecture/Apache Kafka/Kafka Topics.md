## About

Named log of records, split into partitions for parallelism

## Setup

| Config                    | Descrição                                                                                                                                                              | Requisitos                                                                      | Default               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------- |
| min.insync.replicas       | Mínimo de réplicas em sincronia (ISR), contando o líder, que precisam confirmar uma escrita. Abaixo disso o broker rejeita a escrita (`NotEnoughReplicas`)             | Só tem efeito com `acks=all` no producer. Comum: RF 3 e `min.insync.replicas=2` | 1                     |
| cleanup.policy=delete     | Expurga segmentos com base em tempo ou tamanho (`retention.ms` e `retention.bytes`)                                                                                    |                                                                                 | `delete`              |
| retention.ms              | Quanto tempo as mensagens ficam no log. Apaga os segmentos mais antigos que esse tempo. `-1` = sem limite                                                              | Tópicos com `cleanup.policy=delete` ou `compact,delete`                         | 7 dias (604800000 ms) |
| retention.bytes           | Expurga por tamanho. Limite **por partição**: apaga os segmentos mais antigos quando a partição passa desse valor                                                      | Tópicos com `cleanup.policy=delete` ou `compact,delete`                         | -1 (sem limite)       |
| cleanup.policy=compact    | Deduplica por chave, mantém o registro inserido por último (faz um update por ID). ==Não é imediato, consumers podem ler versões antigas por um tempo==                 | Toda mensagem precisa ter chave                                                 |                       |
| min.cleanable.dirty.ratio | Define quanto do log precisa estar "sujo" (chaves ainda não compactadas) para a compactação rodar                                                                      | Tópicos com `cleanup.policy=compact`                                            | 0.5                   |
| segment.ms, segment.bytes | Fazem o segmento rolar mais rápido, o que permite compactar (ou expurgar) mais cedo. O segmento ativo nunca é compactado nem apagado                                    |                                                                                 | 7 dias e 1 GB         |
| min.compaction.lag.ms     | Garante que uma mensagem fique um tempo sem ser compactada                                                                                                             | Tópicos com `cleanup.policy=compact`                                            | 0                     |
| delete.retention.ms       | Quanto tempo os **tombstones** (mensagens com valor `null`) ficam em um tópico compactado. Depois desse tempo, o tombstone é removido junto com a chave                | Tópicos com `cleanup.policy=compact`                                            | 1 dia (86400000 ms)   |

***log cleaner***: Roda nos brokers em threads, aplicando compactação.

***tombstone***: Producer envia uma mensagem com a chave e valor `null` para apagar a chave. A deleção de fato acontece com base em `delete.retention.ms`.

## Links

- [[data architecture/Apache Kafka/Kafka Topic Partition.md|Kafka Topic Partition]]
