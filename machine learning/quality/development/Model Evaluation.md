![[Pasted image 20261016125847.png|648]]

## The Machine Learning Workflow

**[[Data Collection]]:** Gathering the raw data you need to solve the problem
**[[Data Preprocessing]]:** [[Data Cleaning]], Formatting, and preparing the data so an algorithm can understand it.
**[[Model Selection]]:** Choosing the right algorithm for the task.
**[[Training and Validation]]:** Feeding the data to the model so it can learn patterns, and checking its initial performance.
**[[Model Evaluation]]:** Rigorously measuring how accurate the model's guesses actually are on unseen data.
**[[Final Model]]:** Deploying the optimized model to make real-world decisions.

What makes a model "good"?

Evaluating a model is simply comparing **The actual value (ground truth)** and **The Predicted Value**, the difference between these two numbers is your error. The goal is to make that error as close to zero.

![[Parsimonious Model#Parsimonious Model]]

| Training performance                                                      | Validation performance                                          |
| ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 💪 This is how well our model performs on the ==🔵data it used to learn== | 🪓 This is how well our model peforms on new, ==🔵unseen data== |
|                                                                           |                                                                 |
## Overfitting vs. Underfitting

![[Overfitting#O que é?]]

![[Underfitting## O que é?]]

The tradeoff is the balancing act between the two, this is [[Parsimonious Model]]

![[Evaluating regression model metrics]]

## References
[[Linear Regression (regression problems)]]
[[Logistic regression (Classification problems)]]

