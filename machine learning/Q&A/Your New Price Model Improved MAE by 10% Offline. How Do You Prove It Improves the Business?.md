#QA #interview-question #model-evaluation #regression

## Question

A new used-car price model reduces the offline MAE by 10% compared with the model in production, using a time-based validation. The product team wants to know if it really improves the business before replacing the current one. How would you design the online evaluation, given that the price set for a car influences whether and when it sells, and that cars in the same marketplace compete for the same buyers?

## Answer

I would treat the offline gain only as a reason to test, since MAE says nothing about margin, days to sell or the share of unsold cars, so I would first run the new model in shadow mode to catch pipeline and feature bugs and to check how much it disagrees with the current one, and then run a randomized experiment ([[A-B testing]], the last stage of a [[champion and challenger]] rollout) whose primary metric is a business outcome such as margin per car with days to sell and unsold rate as secondary metrics, and guardrails such as bias by price band and complaints. Because cars compete for the same buyers, randomizing per listing can contaminate the groups (a cheaper car in one arm pulls demand away from similar cars in the other arm), so I would randomize by a larger unit, such as vehicle segment, region or time blocks with a switchback design, and decide the sample size and the duration in advance with a power calculation, long enough to cover the delayed outcome (the sale can take weeks) and a full weekly cycle, instead of stopping as soon as the result looks good. If the results are positive and the guardrails hold, I would roll out gradually, keep the old model available for rollback, and keep a small holdout priced by the old process, so that I keep an unbiased baseline and can detect [[Model drift]] later.

## Related

- [[Your Used-Car Price Model Has a Low MAE, but the Business Still Loses Money. How Do You Evaluate It?]]
- [[Should You Train a Separate Model for Each Season or Use One Global Model for Used-Car Prices?]]
- [[Model Evaluation]]
