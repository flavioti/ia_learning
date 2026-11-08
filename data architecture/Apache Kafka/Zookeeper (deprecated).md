#deprecated

Removido do kafka na versão 4.0, substituido por [[KRaft]]

## Por que o Zookeeper saiu

Antes, o Kafka precisava de um cluster Zookeeper separado para guardar os metadados e coordenar o cluster. Isso trazia vários problemas:

- **Dois sistemas para operar:** deploy, monitoramento, segurança e upgrade eram feitos duas vezes.
- **Limite de escala:** a recuperação de um novo controller exigia ler todos os metadados do Zookeeper, e isso ficava lento com centenas de milhares de partições.
- **Fonte de verdade dividida:** o estado do cluster ficava no Zookeeper, e cada broker mantinha um cache que podia ficar inconsistente.
- **Modelo de propagação ineficiente:** o controller enviava atualizações de metadados aos brokers por RPCs.
