[[Design patterns]]

**Problem**:

**Solution**: In event-driven systems, to ensure that events will be processed, needs to write the message in a table (on the database), then, other process will consume

```mermaid
flowchart LR
start((start))
end_((end))
subgraph Microservices
	A[producer]
	B[consumer]
end
subgraph Database
	C1[(table 1 - user)]
	C2[(table 2 - user_outbox)]
end
D[Outbox Consumer]
subgraph Kafka
	E[Topic]
end

start-->A
A--event-->B
B--write-->C1
B--write-->C2
D--polling-->C2
D--write-->E
E-->end_
```

