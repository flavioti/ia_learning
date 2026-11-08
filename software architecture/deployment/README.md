How to release new versions of software (and models) to production safely: strategies for shipping a change while limiting risk and downtime. The overview of the strategies is in [[deployment strategies]]; this folder holds the detailed notes.

## Core idea

Every release strategy balances the same trade-offs:

- **Risk exposure:** how many users see a bad version before it is caught
- **Rollback speed:** how fast you can undo it
- **Cost:** how much extra infrastructure it needs
- **Downtime:** whether users notice the release

## Notes in this folder

| Note | What it covers | Status |
|---|---|---|
| [[canary deployment]] | Release to a small share of real traffic first, widen in steps, roll back if unhealthy | Detailed |
| [[A-B testing]] | Randomized experiment comparing versions on a business metric, with sample size and pitfalls | Detailed |
| [[shadow deployment]] | Mirror live traffic to the new version and discard its responses, with zero user impact | Detailed |

## Strategies at a glance

| Strategy       | Idea                                                           | Question it answers                                         |
| -------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| **Canary**     | Gradually shift a small share of traffic to the new version    | Is this version safe to release? ([[canary deployment]])    |
| **A/B test**   | Split users randomly and compare a metric                      | Which version is better for the business? ([[A-B testing]]) |
| **Blue-green** | Run a full second environment and switch all traffic at once   | Can I release with instant rollback?                        |
| **Rolling**    | Replace instances one by one                                   | Can I release with no extra environment?                    |
| **Shadow**     | Copy live traffic to the new version and discard its responses | Does it behave well on real inputs, with no user impact? ([[shadow deployment]]) |

Canary and A/B testing look similar but differ in intent and in how they are judged, so they are separate notes. They are often combined: a canary confirms the version is safe, then an A/B test measures whether it is better.

## Choosing a strategy

- Need to confirm safety with limited exposure: canary
- Need to measure business impact with statistical confidence: A/B test
- Need instant rollback and can afford a duplicate environment: blue-green
- Simple stateless service with low risk: rolling
- Need to validate on real inputs without any user impact (for instance a new model): shadow

## In machine learning

The same strategies apply to model releases, usually as a sequence: offline evaluation, shadow, canary or A/B, then full promotion. See [[champion and challenger]] and [[Model drift]].

## To do

- Write notes for blue-green and rolling deployments (the [[deployment strategies]] overview still points to a missing `Blue-Green deployment` note)
- Add feature flags and progressive delivery

## Related

- [[deployment strategies]]
- [[CICD]]
- [[DevOps]]
- [[champion and challenger]]
- [[Model drift]]
