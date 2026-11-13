---
tags:
  - classic-ml
---
#regression 

| Metric                             | What if measures                        | Better if... | Best for...                                            |
| ---------------------------------- | --------------------------------------- | ------------ | ------------------------------------------------------ |
| [[MAE - Mean Absolute Error]]      | Average error size                      | Lower        | Ignoring outliers; simple interpretation.              |
| [[MSE - Mean Squared Error]]       | Average of squared errors               | Lower        | Heavily penalizing large, costly mistakes, change unit |
| [[RMSE - Root Mean Squared Error]] | Square root of MSE                      | Lower        | The standard go-to; keeps erros in original units.     |
| [[R-squared]]                      | % of variance explained (0 to 1)        | Higher       | A quick gut-check on overall mode fit                  |
| [[Adjusted R-squared]]             | R-squared, but penalizes useless inputs | Higher       | Comparing models with different numbers of features    |
## Links
[[Others regression metrics]]
