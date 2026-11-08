## Question 1 (Fundamentals: generalization)

You train a model and see 98% accuracy on training data but 71% on the validation set.
1. What is happening, and how do you diagnose it?
2. Walk me through the concrete steps you'd take to fix it, in the order you'd try them.
3. How would your approach change if the training and validation scores were _both_ low?

---
#### Answer to Question 1
1. Overfitting is caused by high variance, data leakage. Use Learning Curve
2. If there are many features, I will begin removing some of them, the model is too complex
3. Simplify model, or get more data, remove features (redo feature selection)

