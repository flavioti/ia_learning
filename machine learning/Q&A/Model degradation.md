#interview-question 

Foi detectado pelo cliente que o numero de vendas cairam nos últimos 6 meses, usando a base offline estava tudo certo, o problema estava na predição em real-time, qual a melhor forma de lidar com esse problema?

## Solução
Job de Avaliação Assíncrono (Reativo - Usando $Y$ ([[Rotulo real]]) quando disponível:
- À medida que os resultados reais do negócio são consolidados no _Data Lake_ / _Feature Store_, execute um job batch agendado (ex: diário ou semanal).
- Faça o _join_ dos logs de predição com os rótulos reais consolidados e calcule o F1-score, Precision e Recall reais.
- _Objetivo:_ Confirmar o [[Concept Drift]] e servir de gatilho oficial de retreinamento automatizado ([[Continuous Training - CT]]).
## Outras soluções menos viáveis
- Feedback Imediato
	- Usar métricas como [[F1-Score]], [[Recall]] e [[Precision]] somente são úteis em produção se existir o rótulo.
		- Exemplo: Um pipeline de dados (streaming com Kafka/Flink) faz o _join_ entre a predição e a ação do usuário, calcula o F1-score em janelas móveis (ex: a cada hora) e dispara um alerta ou pipeline de retreinamento se a métrica cair abaixo de um limite aceitável.

![[machine learning/Rotulo real]]

