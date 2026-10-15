Ollama lets you use [[open source models]] with your coding agents so you can spend less while keeping your data private.

https://ollama.com/

## Info
- [[Context Management]] is enabled by default, when using terminal.
[[Session context]]
[[Modelfile]]
## Commands

`--temperature`: 0.1 is pragmatic, 1 is imaginative
`/set parameter num_ctx 16384`:  Increase embedding length ([[Context Management]]) limit to 16,384 tokens


```bash
ollama list # List installed models
ollama run llama3:latest
ollama run llama3-mini --optimized # run faster
llama-3 --parallel --batch-size 2 --sequence-length 128 --temperature 0.5
llama-3 --optimized --batch-size 2 --sequence-length 128 --temperature 0.3
llama-3-small --batch-size 1 --sequence-length 256 --temperature 0.5 --optimized
```

## Models

[[LLaMA-3]]
[[Nimble 9b]]
[[Tev1 4b]]


## Links

[[IA model]]

