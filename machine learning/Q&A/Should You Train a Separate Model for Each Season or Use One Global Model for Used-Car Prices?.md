#QA #interview-question #model-evaluation #regression

## Question

You have a used-car price model that works well on average, but the business notices that it is biased around Christmas and in winter, when prices behave differently. A teammate proposes training one general model for the whole year plus specialized models for Christmas and for winter, and serving all of them in production. Would you do it, and how would you decide?

## Answer

I would start with a single global model that receives calendar and market features (month, week of the year, holidays, recent price trend, interest rate, stock level), validate it with a time-based split such as a [[Backtest]], and measure the bias per season and per vehicle segment before creating anything new, because a seasonal effect is usually a shift in price level or demand that one model can learn, including its interaction with the vehicle type (convertibles gain value in spring, 4x4 and SUVs in winter). Specialized models have real costs: Christmas happens once a year, so a few years of history give only a handful of examples and the specialist tends to [[Overfitting|overfit]] ([[High variance]]); routing by date creates price jumps at the boundary (30 Nov versus 1 Dec); and every extra model adds a pipeline to retrain and monitor against [[Model drift]]. So I would first try cheaper fixes (more features, higher weight for recent data, or a residual model on top of the global one) and only keep a specialist if it beats the global model consistently on the same slices in a leave-one-year-out validation, blending the two smoothly over the calendar instead of switching, and serving it in shadow mode and then in an A/B test ([[champion and challenger]]) judged on margin and days to sell, not only on MAE.

## Related

- [[Your Used-Car Price Model Has a Low MAE, but the Business Still Loses Money. How Do You Evaluate It?]]
- [[Distribution shift]]
- [[Model Evaluation]]
