Truncate old messages, if it not fit in the [[Context Management]]
```mermaid
flowchart LR
subgraph OldMessage
	A
	B
end
subgraph RecentMessage
	C
	D
	E
end
OldMessage --> RecentMessage
```
