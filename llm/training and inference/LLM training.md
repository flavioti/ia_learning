## ==🔵The Dictionary Creator - Tokenization==

After the text is completely transformed into a mountain of **Numerical IDs**, by [[Tokenizer training]], these IDs are, in fact, the **input** for the LLM training. The LLM never sees a single physical letter during its own training process; it only receives sequences of numbers and tries to mathematically predict what the next number in the sequence should be.

- At the begining of training, [[embeddings]] receive aleatory weights
- [[tokens]] receive a [[hard weight]], at the end of training
## ==🟣The Learning Phase - LLM==

During training, the goal is to tweak the AI's internal numbers so it becomes smarter.
- **[[soft weight]] (Malleable Weights):** At the beginning of training, the AI's weights are _soft_. This means the computer can alter them freely. If the AI guesses a word incorrectly, the algorithm goes in and adjusts these soft weights to correct the mistake. They change every single second.
- **[[hard weight]] (Frozen Weights):** Imagine you want to teach an AI about _Medicine_, but it already knows how to speak _English perfectly_. You don't want to risk it unlearning English while learning medicine. So, you **freeze** the language layers of its brain (they become **Hard Weights**). The computer is strictly forbidden from touching them. You leave only the new layers as **Soft Weights**, which is where the AI will store its new medical knowledge.

| **LLM Stage**       | **What are [[hard weight]]?**                                                             | **What are [[soft weight]]?**                                                              |
| ------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **During Training** | The parts of the AI's brain that you **locked** so it won't forget what it already knows. | The parts of the brain that are **actively being modified** right now to learn new things. |

>[!WARNING] Built-in "judge": This technique mimic a [[GAN (The Mathematical Coach)]] , this is done through advanced alignment techniques like **RLAIF** (Reinforcement Learning from AI Feedback) or **DPO** (Direct Preference Optimization). This is **not about llm-as-a-judge**💡, but a internal process created by researchs
