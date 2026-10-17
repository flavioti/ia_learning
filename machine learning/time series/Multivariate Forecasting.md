**Multivariate forecasting** predicts future values using **more than one variable** observed over time. It contrasts with **univariate forecasting**, which uses only the history of the series being predicted.

>[!tip] predicts future values using **more than one variable**
## Univariate vs. multivariate

|Univariate|Multivariate|
|---|---|---|
|Inputs|Only the past of the target|Past of the target **plus** other variables|
|Example|Forecast sales from past sales|Forecast sales from past sales, price, promotions, weather, holidays|
|Question answered|"What did this series do before?"|"What do this series _and its drivers_ suggest?"|

## Example

|Month|Sales|Ad spend|Avg. temperature|Holiday|
|---|---|---|---|---|
|Jan|100|10|5|0|
|Feb|110|12|6|0|
|Mar|120|15|10|0|
|Apr|?|20 (planned)|14 (forecast)|1|

A univariate model only sees the sales column and extrapolates the trend. A multivariate model also uses ad spend, temperature and holiday information to explain _why_ sales move, so it can react to changes like a bigger ad budget.