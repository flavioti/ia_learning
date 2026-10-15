## Encoder-only
Encoder-only é a versão do transformer que mantém apenas o bloco de codificação. Seu foco não é gerar texto token a token, mas construir uma representação contextualizada da entrada inteira. Isso o torna especialmente adequado para tarefas de compreensão, como classificação, extração de informação e transformação de frases em vetores. Em troca, ele tende a ser mais leve, mais rápido e mais barato do que arquiteturas voltadas à geração.
## Decoder-only
Decoder-only é a variação do Transformer especializada em geração textual passo a passo. Em vez de processar a sequência inteira com visão bidirecional, ele restringe o cálculo ao histórico disponível para prever o próximo token. Essa escolha reduz complexidade para tarefas generativas e alinha a arquitetura ao problema central de completar texto, responder e continuar sequências de forma coerente.
## Encoder-Decoder
