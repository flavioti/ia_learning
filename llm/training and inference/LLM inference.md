#generator
## During INFERENCE (The AI Answering the User)

When you download a model (like Llama) onto your computer or use ChatGPT, the training is already done. This is the Inference phase.
- **[[hard weight]] (The Static Brain):** All the core knowledge the AI already possesses comes packed in a giant file of several Gigabytes. These are the **Hard Weights**. They are loaded directly into your graphics card (GPU) memory and **never change**, no matter what you ask. Whether you type _"What is 2+2?"_ or _"Write me a poem"_, the Hard Weights retain the exact same numerical values. They are the AI's "fixed encyclopedia."
- **[[soft weight]] (The Dynamic Context):** As the AI reads your prompt, it has to decide which words in your sentence are the most important. To do this, it calculates temporary numbers on the fly called "attention weights." For example, in the sentence _"The river bank was muddy"_, the AI calculates a dynamic weight to connect the word "bank" to "river" (and not to a financial bank). These numbers change with every new word you type. They are **Soft Weights** because they only last for the millisecond required to generate the response. As soon as you close the chat, they disappear.

| **LLM Stage**        | **What are [[hard weight]]?**                                                                  | **What are [[soft weight]]?**                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **During Inference** | The **fixed model file** (e.g., language rules, logic) that sits statically in the GPU memory. | The **temporary mathematical calculations** the AI makes on the fly to understand your prompt's context. |
