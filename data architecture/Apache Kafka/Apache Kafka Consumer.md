- Can be a consumer group, several clients can read the same message

Para o ***consumer group*** saber de onde parou, o Kafka usa ==🟣offsets==, que automaticamente registram a ultima leitura.

Um consumer group é um grupo de consumidores lendo o mesmo tópico, mas recebendo eventos distindos, se conectam a [[Kafka Topic Partition]]