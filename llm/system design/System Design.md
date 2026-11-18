---
description: General system design, the plan for a whole software solution (components, integrations, data flow, deployment and trade-offs) that starts together with the RFC and the downstream design documents.
aliases:
  - Solution Design
tags:
  - system-design
---

System design is the plan for the entire solution: how the parts of a system fit together to meet the requirements defined in the PRD. It answers what the components are, how they talk to each other, where they run, and why the solution is built this way.

## What it covers
- Components and their responsibilities
- Integrations and interfaces between them
- Data flow and storage
- Deployment and infrastructure
- Non-functional requirements (scale, availability, latency, cost, security)
- Trade-offs and the reasons behind each choice

## Position in the design documents
System design is developed in parallel with the RFC, not one after another. The overall chain is described in the parent note.

## Links
- [[llm/system design/AI Context Design.md|AI Context Design]]

## Related
- [[llm/system design/C4 diagrams.md|C4 diagrams]]
