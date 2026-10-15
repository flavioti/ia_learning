#queryenrichment 

Hypothetical Document Embeddings. Ideal for [[Vector Search]]

1. Receive user query
2. Prompt to generate document
3. Concat document and original query
4. Generate embeddings
5. [[Semantic search]]
6. Return shards
7. Generate final answer

**Example**
```text
Escreva uma parágrafo conciso que responda de forma clara à pergunta abaixo. A resposta deve parecer um documento real, com datas, fatos ou descrições prováveis, mesmo que hipotéticas. Não use linguagem especulativa (não diga "talvez" ou "possivelmente").

Pergunta: "{query}"
```

[[Prompt engineering]]
