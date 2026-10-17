#machine-learning #forecasting #time-series #regression-like

**Time series forecasting** is a [[task]]. It ***predicts future*** values from ***past values*** where the ***order*** of the data matters. 
The target is usually a number (sales, energy use, traffic), and the data has trend, seasonality and noise, as described in your note.

>[!tip] Predicting **future values from past values**, where the data is ordered by time.

| Item           | Time series forecasting          |
| -------------- | -------------------------------- |
| What it is     | A problem/task                   |
| Output         | Future value(s) over time        |
| Data order     | Order and time dependence matter |
| Typical target | Continuous (usually)             |
## Simple example

| Jan | Feb | Mar | Apr   |
| --- | --- | --- | ----- |
| 100 | 110 | 120 | ==?== |
***Sales grow by about 10 each month, so the forecast for April is about **130**.***

## What a "time series" is

A series of data points collected at regular intervals (per hour, day, month, etc.). The order matters, because yesterday influences today.
## Patterns the models look for

| Pattern | Meaning | Example |
|---------|---------|---------|
| **Trend** | Long-term direction (up or down) | Sales growing year after year |
| **Seasonality** | Repeats on a schedule | More sales every December |
| **Noise** | Random variation | A one-off spike with no reason |

## Common uses
- Demand and sales forecasting
- Stock levels in inventory
- Energy consumption
- Website traffic
- Weather and prices
## Common approaches

| Approach              | Examples                                     |
| --------------------- | -------------------------------------------- |
| Statistical (classic) | Moving average, [[ARIMA]], Exponential Smoothing |
| Machine Learning      | [[Gradient boosting]], Prophet               |
| Deep Learning         | LSTM, Transformers                           |
