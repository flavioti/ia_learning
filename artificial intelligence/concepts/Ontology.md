---
description: Simple definition of an ontology, a formal map of the concepts of a subject and how they relate, used in knowledge graphs, data modeling and AI systems.
aliases:
  - Ontologies
tags:
  - ontology
  - knowledge-representation
---

# Ontology

An **ontology** is a map of a subject: the **things** that exist in it, how they are **grouped**, and how they **relate** to each other.

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    subgraph Classes ["Classes (concepts)"]
        Person
        Engineer
        DataEngineer["Data Engineer"]
        Company
        Skill
    end
    subgraph Individuals ["Individuals (real things)"]
        Alice["Ana Alice"]
        Acme["Acme Corp"]
        Python
    end
    Engineer -- "is a kind of" --> Person
    DataEngineer -- "is a kind of" --> Engineer
    Person -- "works at" --> Company
    DataEngineer -- "needs skill" --> Skill
    Alice -. "instance of" .-> DataEngineer
    Alice -- "works at" --> Acme
    Acme -. "instance of" .-> Company
    Alice -- "has skill" --> Python
    Python -. "instance of" .-> Skill

    classDef cls fill:#1e3a8a,stroke:#93c5fd,color:#f1f5f9
    classDef ind fill:#14532d,stroke:#86efac,color:#f1f5f9
    class Person,Engineer,DataEngineer,Company,Skill cls
    class Alice,Acme,Python ind
    style Classes fill:#0f172a,stroke:#475569,color:#cbd5e1
    style Individuals fill:#0f172a,stroke:#475569,color:#cbd5e1
    linkStyle 0,1,2,3 stroke:#93c5fd,stroke-width:2px
    linkStyle 5,7 stroke:#86efac,stroke-width:2px
    linkStyle 4,6,8 stroke:#fbbf24,stroke-width:2px,stroke-dasharray:5 5
```

## Idea

Imagine a shared dictionary plus the rules to use it. It answers three questions:

1. **What exists?** (concepts, e.g. `Person`, `Company`, `Job`)
2. **How are they grouped?** (`Engineer` is a kind of `Person`)
3. **How do they relate?** (`Person` *works at* `Company`)

## Example

Read the diagram above as follows:

- **Classes** are the concepts (the top box). A *Data Engineer* is a kind of *Engineer*, and an *Engineer* is a kind of *Person*. A *Data Engineer* needs a *Skill*, and *Python* is an instance of *Skill*.
- **Individuals** are real things that belong to a class (the bottom box). *Alice* is an instance of *Data Engineer*, and *Acme Corp* is an instance of *Company*.
- **Relations** connect things: *Alice* *works at* *Acme Corp* and *has skill* *Python*.
- Dotted orange arrows (*instance of*) link an individual to its class.
- Colors: blue = classes, green = individuals.

## Why it matters

- It gives people and machines the **same meaning** for the same words.
- It makes data **easier to connect and search**.
- It is the base of **knowledge graphs**, used to ground AI answers (see [[llm/concepts/RAG.md|RAG]]).

## Ontology vs. taxonomy

- A **taxonomy** is only a hierarchy ("is a kind of").
- An **ontology** is a taxonomy plus **relationships** and **rules**.

## Related

- [[llm/concepts/RAG.md|RAG]]
