#observability #monitoring #correct #clean #complete

==checks if your data is broken==
==second line defense==
## Metrics

| Metric                | [[data evaluation]]               | [[threshold]]                 |
| --------------------- | --------------------------------- | ----------------------------- |
| completeness          | Null or empty values              | tolerancy 5%                  |
| schema and type check | schema, type and range compliance | age is an integer,            |
| uniqueness            | prevent duplication               | tolerancy 0%                  |
| freshness             | prevent receive old data          | date must be greater than D-2 |
## Frameworks
[[Great expectations]]
[[AWS Deequ]]
