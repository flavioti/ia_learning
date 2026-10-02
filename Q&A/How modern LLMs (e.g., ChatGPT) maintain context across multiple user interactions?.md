#memory #in-context_learning 
## Intro

> **Answer**: It uses [[Context window]].

Modern LLMs maintain context across multiple interactions not by possessing persistent internal memory, but by receiving the entire conversation history re-submitted alongside every new message in a single prompt payload.

> [!NOTE] TLDR
> Every new message, has the entire conversation history.

At the API level, models like GPT-4, Claude, or Gemini are [[stateless]] - They process each input independently and forget everything immediately after returning a response. the illusion of the continous conversation is generated through a combination of application-level history management, attention mechanisms, and context caching.

## Payload resubmission (Conversation history)
Every time a user sends a message, the chat application (e.g., ChatGPT's front-end) collects all previous turn from the session database and constructs a unified sequence to send to the model backend:

```json
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "Hi, my name is Alex and I am learning Python."},
  {"role": "assistant", "content": "Hello Alex! Python is a great language to learn. What are you building?"},
  {"role": "user", "content": "What was my name again?"}
]
```
Because the full exchange is included in the prompt, the model uses its self-attention mechanism to attend back to earlier tokens (e.g., linking "my name" to "Alex")

## Attention & key-value (KV) caching

To avoid the computational cost of re-processing every historical token from scratch on every turn, modern LLM inference engines use **[[Key-Value caching]]:
- **[[Self-Attention]]:** During inference, the [[Transformer]] calculates attention matrices determining how [[tokens]] relate to one another across the entire prompt sequence.
- **[[Key-Value caching]]:** The system stores the intermediate key and value vectors of past conversation tokens in GPU memory. When a new turn is sent, the model reuses the cached representations for previous messages and only computes activations for the newly added tokens.
## The End-to-End Multi-Turn Workflow

1. **User action:** User submits a new query.
    
2. **Payload build:** System retrieves conversation history from DB and appends the new message.
    
3. **Inference with KV Cache:** Prompt is routed to the model; cached states of previous turns accelerate token generation.
    
4. **Response generation:** Model generates output using attention over the full sequence.
    
5. **State persist:** Both user message and assistant response are saved to the database for turn $N+1$.