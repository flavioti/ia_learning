
| Metric                                  | What if measures                         | Rule of thumb    | Best for...                                            |
| --------------------------------------- | ---------------------------------------- | ---------------- | ------------------------------------------------------ |
| [[MAE - Mean Absolute Error]]           | Average error size                       | Lower is better  | Ignoring outliers; simple interpretation.              |
| [[MSE - Mean Squared Error]]            | Average of squared errors                | Lower is better  | Heavily penalizing large, costly mistakes, change unit |
| [[RMSE - Root Mean Squared Error]]      | Square root of MSE                       | Lower is better  | The standard go-to; keeps erros in original units.     |
| [[R-squared]]                           | % of variance explained (0 to 1)         | Higher is better | A quick gut-check on overall mode fit                  |
| [[Adjusted R-squared]]                  | R-squared, but penalizes useless inputs  | Higher is better | Comparing models with different numbers of features    |
| [[Akaike Information Criterion\|AIC]]   | Balances accuracy vs. complexity         | Lower is better  | Finding the "sweet spot" between fit and simplicity    |
| [[Bayesian Information Criterion\|BIC]] | Stricter penalty for complexity than AIC | Lower is better  | Forcing the simplest effective model on large datasets |
