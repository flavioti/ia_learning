---
description: Tungsten, the Spark execution engine that stores data in a binary format outside the JVM heap and generates optimized code for each stage, with its three pillars (memory management, cache-friendly binary layout and whole-stage code generation), and why it matters for DataFrames and Datasets. Child of Apache Spark, used with the Catalyst note to explain Spark performance.
aliases:
  - Project Tungsten
  - Spark Tungsten
  - Whole-stage code generation
tags:
  - spark
  - performance
  - tungsten
  - interview
---
# Tungsten

**Tungsten** é o motor de execução do Spark. Ele decide **como** os dados ficam na memória e como as operações rodam no processador. O [[Catalyst (plan builder)|Catalyst (plan]] decide **o que** fazer, criando o plano. Juntos, eles explicam por que DataFrame e Dataset são mais rápidos que RDD. Ver [[data architecture/Apache Spark/Apache Spark|Apache Spark]].

O projeto começou em 2015, na Databricks, para melhorar a eficiência de CPU e memória do Spark.

## Problema que resolve

Objetos Java têm custo alto:
- cada objeto tem cabeçalho e ponteiros, o que aumenta o uso de memória;
- muitos objetos pressionam o coletor de lixo (GC), que pausa a execução;
- cada acesso a um campo pode gerar cache misses, porque os objetos ficam espalhados na memória.

O Tungsten trata esses três pontos com três pilares.

## Pilar 1: memória gerenciada fora do heap

- Os dados ficam em blocos de memória binária, administrados pelo próprio Spark.
- O coletor de lixo da JVM vê poucos objetos, então as pausas diminuem.
- Operações como ordenação e agregação trabalham sobre esses blocos.

## Pilar 2: formato binário compacto

- Cada linha é um registro binário com campos em posições conhecidas.
- O Spark lê um campo específico sem desserializar a linha inteira.
- Os dados ficam contíguos na memória, o que favorece o cache da CPU.

Exemplo conceitual: para somar a coluna `valor`, o Spark acessa só o trecho daquele campo em cada linha, em vez de criar um objeto por linha.

## Pilar 3: geração de código (whole-stage code generation)

- Em vez de interpretar o plano linha por linha, o Spark gera código Java para um estágio inteiro, compila e executa.
- Isso remove chamadas de função intermediárias e deixa o laço de processamento mais justo para a CPU.
- Os estágios são separados nas fronteiras de shuffle, então cada estágio vira uma função compilada.

Quando o código não pode ser gerado (por exemplo, certos tipos de operação ou muitas colunas), o Spark usa um caminho interpretado.

## Onde o Tungsten se aplica

| API | Usa Tungsten |
|---|---|
| RDD | Não. Trabalha com objetos Java |
| DataFrame | Sim |
| Dataset | Sim |
| SQL | Sim, pelo mesmo caminho do DataFrame |

Por isso, o conselho de usar DataFrame e funções nativas vem também dele. Ver [[data architecture/Apache Spark/core concepts/Spark RDD DataFrame Dataset|Spark RDD, DataFrame and Dataset]].

## Como observar

- `df.explain()` mostra o plano físico. Operadores com `*` no início, como `*(1) Filter`, indicam que houve geração de código por estágio.
- Na Spark UI, a aba SQL mostra o plano com as etapas executadas.

## Armadilhas

- **UDFs em Python** saem do formato binário para o Python e voltam. Isso quebra parte dos ganhos. Ver [[data architecture/Apache Spark/sql and optimization/Spark UDFs|Spark UDFs]].
- **Lambdas em Dataset** não são visíveis para o Catalyst, e o código gerado não cobre o trecho lambda da mesma forma.
- **Muitos tipos complexos** (structs profundas, mapas grandes) podem reduzir a eficiência do formato binário.
- **Tungsten não resolve shuffle caro.** Ele acelera a execução de cada estágio, mas a troca de dados entre executores continua cara. Ver [[data architecture/Apache Spark/core concepts/Spark Shuffle|Spark Shuffle]].

## Pergunta de entrevista

"O que é o Tungsten e por que DataFrame é mais rápido que RDD?"

Resposta curta: o Tungsten guarda os dados em formato binário fora do heap da JVM, reduz o custo do GC e gera código otimizado por estágio. RDD trabalha com objetos Java e não se beneficia disso. Com o Catalyst, que escolhe o plano, o DataFrame aproveita as duas camadas.

## Related

- [[data architecture/Apache Spark/Apache Spark|Apache Spark]]
- [[Catalyst (plan builder)|Catalyst (plan]]
- [[data architecture/Apache Spark/core concepts/Spark RDD DataFrame Dataset|Spark RDD, DataFrame and Dataset]]
