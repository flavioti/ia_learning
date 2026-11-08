---
aliases:
  - RL-LLM
---
## Description

Is the phase where a pre-trained [[LLM]]—which is initially focused only on predicting the next token—is refined to follow instructions, reason, and align with specific preferences or rules.

## The Basic RL Loop in Post-Training
1. **Generation (Trajectory/Policy):** The model (policy π) receives a prompt and generates a full response (a sequence of tokens).
2. **Reward:** A score is assigned to the generated response. This can come from:
    - **Verifiable Rewards:** Objective checks (e.g., an exact math answer key, code unit tests).
    - **Learned Rewards (Reward Model):** A model trained to mimic human preferences regarding helpfulness, safety, and style.
    - **Self-Feedback:** The model itself evaluates its confidence or generates reasoning traces to score its own performance.
3. **Policy Optimization:** The model's parameters are updated to increase the probability of generating responses that received high scores.

## Key Algorithms and Approaches

- **[[RLHF]]:** Uses a reward model trained on human preference data and optimizes the LLM using algorithms like **[[PPO]]**.
- **[[DPO]]:** Simplifies [[RLHF]] by embedding the preferences directly into the loss function, skipping the need to train a separate reward model.
- **[[GRPO]]:** A group-based [[Reinforced Learning]] algorithm widely used in reasoning models (like DeepSeek-R1) to evaluate multiple response attempts for the same prompt relative to one another.