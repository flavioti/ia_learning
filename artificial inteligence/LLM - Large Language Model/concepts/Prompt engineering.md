#ModelOptimization 

- 🟢 Is a In-context learning
- 🔴 Increase token use

## Techniques

[[CoT chain-of-thoughts]]
[[N-shot]]
## Best pratices

### Put instructions at the beginning of the prompt

⛔ Hey, GPT. This is an email I wrote last night. Can you revise it?
✅ Revise the following email to sound more professional.
### Use delimiters

⛔ Revise the following email to sound more professional, but don't change anything else about it: I wanted to check if you had a chance to review the document I sent last week. Let me know what you think.
✅ Revise the following email to sound more professional, but don't change anything else about it. \<email\> I wanted to check if you had a chance to review the document I sent last week. Let me know what you think.\</email\>
### Be very specific
⛔ Write a blog post about prompt engineering.
✅ Write a 500-word blog post about prompt engineering tips. The audience will be beginners, so use a friendly tone and give concrete examples for easier understanding.

### Give the model a persona
⛔ Explain blockchain.
✅ **\<role\>** You are a tech educator who specializes in explaining complex topics in simple, relatable language. Your audience is made up of adults with no technical background – teachers, business owners, and everyday readers curious about new technology. **\</role\>**
**\<task\>** Write a 500-word blog post explaining what blockchain is, how it works at a basic level, and why it matters. Avoid jargon terms. Use a friendly, engaging tone with real-world analogies to keep the explanation easy to follow and interesting.**\</task\>**
### Provide relevant examples
⛔ Write a product description for a new smartwatch.
✅ \<instruction\>Create a product description for a new smartwatch with these specifications: fitness tracking (steps, heart rate, sleep monitoring), GPS navigation, smartphone notifications, music control, contactless payments, and health monitoring (ECG, SPO2). Use the following example as a style guide.\</instruction\>
\<example\>Stay fit and connected with our sleek fitness tracker that monitors your heart rate, tracks your steps, and syncs seamlessly with your devices.\</example\>
### Ask the model to explain the chain of thought
⛔ What’s the best marketing channel for a small bakery?
✅ Help me choose the best marketing channel for the small bakery that I just started. First, list your best picks and explain why they’re good, divide them into \<best-picks\> and \<least-recommended\> XML tags. After that, give your final answer.
### Specify the desired output format
⛔ List SEO tips for beginners.
✅ List five beginner-friendly SEO tips in bullet points. For each tip, include a short explanation to help readers understand why it matters.
### Supply the AI with relevant data
⛔ Summarize our Q1 sales performance.
✅ Summarize the following Q1 sales data in 3 bullet points:  “Q1 revenue: $120k, up 15% YoY. Top product: SmartLamp. Customer growth: +8%.”
### Ask for evidence
⛔ Who is the wealthiest man in the world?
✅ Who is currently the wealthiest person in the world? Provide their most recent net worth and source (Forbes, Bloomberg, etc.)  If up-to-date data is unavailable, say “I don’t know.”
### Prompt in iterations
⛔ Who is the wealthiest man in the world?
✅ 