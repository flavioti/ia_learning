#softwareengineering
# Formal Definition of a Graph: $G = (V, E)$

In graph theory, the notation **$G = (V, E)$** mathematically defines a graph, which is a structure used to model relationships between pairs of objects.
## Components

* **$G$**: The graph itself.
* **$V$**: The set of **vertices** (or nodes). It represents the elements or points in the system.
  * *Constraint:* $V \neq \emptyset$ (the set cannot be empty).
* **$E$**: The set of **edges**. It represents the connections or relationships between the vertices.
  * *Constraint:* $E \subseteq \{\{u, v\} \mid u, v \in V\}$ (for undirected graphs).
---
## Practical Example

Imagine a simple map with 3 cities (**A**, **B**, and **C**), where there are roads connecting **A to B** and **A to C**.

The mathematical representation of this graph is:

* **Set of Vertices:** $V = \{A, B, C\}$
* **Set of Edges:** $E = \{\{A, B\}, \{A, C\}\}$
