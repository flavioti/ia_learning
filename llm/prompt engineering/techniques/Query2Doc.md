#queryenrichment 

Similar to RAG, LLM generate more content, to do a serch, and them return the result

1. Receive user short query
2. few-shot prompt to LLM model asking a objective mini-document about the subject
3. Concat document with original query
4. [[Lexical Search]] using [[Okapi BM25]]
5. Return shards
6. Generate final answer

**Example**
```text
Escreva um texto informativo e neutro, de 100 a 150 palavras que explique o tópico abaixo. Inclua definições, termos técnicos, sinônimos e contexto relacionado, mas não dê uma resposta direta se for uma pergunta.

Tópico: "{query}"
```


[[Prompt engineering]]