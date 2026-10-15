Is a foundational sub-layer that sits inside every single block of a [[Transformer]] architecture, right after the [[Self-Attention]] mechanism.
[[MLP (Multilayer Perceptron)]]  processes each token completely independently and in parallel. It acts as the "individual thinking space" and primary knowledge storage of the model.

**The Bulk of the Parameters:** Because of the massive 4× matrix expansion, the MLP blocks are incredibly dense. They actually hold roughly **66% (two-thirds) of an LLM's total parameters**, meaning most of the model's physical size is dedicated to the MLP, not the attention mechanism

Currently envolving to [[Mixture of Experts (MoE)]]

## References
[[Position-wise Feedforward layers]]
