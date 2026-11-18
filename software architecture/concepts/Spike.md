---
description: Spike, a time-boxed investigation that answers a technical or functional question before a design or implementation is committed, in software development, with its output feeding the RFC, the ADR and the RAID register.
aliases:
  - Technical Spike
  - Research Spike
tags:
  - software-engineering
  - agile
---

A spike is a time-boxed investigation that answers a question or reduces uncertainty before the team commits to a design or an implementation. The term comes from Extreme Programming. Teams define it differently, so check how yours uses it.

## Types
- **Technical spike:** checks whether an approach works, for example a prototype of a library, an integration with an external API, or a performance test.
- **Functional spike:** clarifies what users need, for example a rough prototype or user interviews about a workflow.

## Characteristics
- **Time-boxed:** it stops when the time runs out, whether or not the question is answered.
- **Output is knowledge, not production code:** the prototype is usually thrown away. What is kept is the answer and the evidence.
- **Feeds the design docs:** its findings support the [[llm/system design/RFC - Request for comments.md|RFC]]. A decision it settles is recorded as an [[llm/system design/ADR - Architecture Decision Record.md|ADR]].
- **Verifies assumptions:** a spike can confirm an assumption, so the matching `A-` entry in the [[llm/system design/RAID Register.md|RAID Register]] can be closed.

## Output
A short write-up with:
- the question
- the approach and the time spent
- the evidence (measurements, test results, observations)
- the recommendation
- links to the affected RFC, ADR and RAID entries
