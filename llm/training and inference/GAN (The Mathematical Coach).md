In a **GAN (Generative Adversarial Network)**, the "Judge" (Discriminator) does not just output a text review or a grade to the "Forger" (Generator). They are tethered together by a mathematical umbilical cord called **[[Backpropagation]]**.

- **How it works:** The Generator creates a piece of data. The Discriminator analyzes it and calculates a strict mathematical error value (e.g., _"Incorrect by a margin of 0.45"_).
- **Does the brain change?** **Yes, instantly.** This error value travels backward through the deep layers of the Generator, **actively altering its Soft Weights** on the fly. The Generator changes its internal mathematical structures so that its very next attempt (which happens in milliseconds) is mathematically superior. It is a **closed-loop training system**, like a coach micro-adjusting an athlete's physical posture every single second of training.

![[Backpropagation]]
