#observability #monitoring #statistical-distribution #macro-trends #seasonal-behavior

==checks if your data has changed==
==first line defence==

- statistical tests like [[Kolmogorov Smirnov (KS)]]
- metrics like [[Population Stability Index (PSI)]] to quantify the change
	- ~0.15 -> warn
	- >= 0.25 -> model retraining
- compare the [[statistical distribution]] of real-time production data against reference [[training data]]. 
- use observability frameworks or model monitoring services

> When data drift ocurrs, the [[ML model]] must be retrained.
