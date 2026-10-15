The Dictionary Creator

Before you even turn on the neural networks of the LLM, you run a purely statistical algorithm (like BPE) over your dataset.

- **The Goal:** To discover the most common words, syllables, and characters in that specific language.
- **The Output:** It generates a fixed catalog/vocabulary. Once trained, **the tokenizer is frozen**. It never changes again.

## Links
https://platform.openai.com/tokenizer
