---
description: Request for Comments (RFC), the technical proposal that turns the PRD into a solution, gathers review feedback and links to the ADRs that record its decisions; written in parallel with the System Design.
aliases:
  - RFC
  - Design Doc
tags:
  - system-design
decisions: []
related:
  - "[[llm/system design/System Design.md|System Design]]"
  - "[[llm/system design/SDD - Security Design Doc.md|SDD - Security Design Doc]]"
---

An RFC proposes a technical solution to a problem, opens it to review, and records the outcome. It starts from the requirements in the [[llm/system design/PRD - Product Requirement Document.md|PRD]] and is written in parallel with the [[llm/system design/System Design.md|System Design]].

## Lifecycle
Draft → In review → Accepted, Rejected or Withdrawn

## Typical sections
- **Summary:** the proposal in a few sentences.
- **Context and motivation:** the problem, with links to the PRD requirements by ID (for example `RF-01`).
- **Proposal:** the design, at the level of components and interactions.
- **Alternatives considered:** each option with its trade-offs, and why it was not chosen.
- **Decisions:** links to the [[llm/system design/ADR - Architecture Decision Record.md|ADRs]] that record the decisions made during review.
- **Impact:** cost, performance, operations and security (link to the [[llm/system design/SDD - Security Design Doc.md|SDD]] when it exists).
- **Rollout and migration:** how the change reaches production and how to go back.
- **Open questions:** each with an owner and a date.

## Best practices
- **Cite the ADRs in detail.** The RFC links to the decisions and explains the context, but does not copy the ADR text. Without this, the RFC becomes a copy of the ADR and loses its value.
- **Start from the requirements.** Reference PRD requirement IDs so each part of the proposal can be traced back to a need.
- **Compare real alternatives.** Show at least two options, with trade-offs, and state why the chosen one won.
- **Keep one proposal per RFC.** If the document covers two decisions, split it so each can be accepted or rejected on its own.
- **Set a review deadline and an owner.** An RFC without a deadline stays in review forever.
- **Record decisions as ADRs.** A decision that exists only in comments is lost. The ADR is written during review and linked from the RFC.
- **Leave detailed behavior to the FDD.** The RFC describes the proposal; the FDD specifies how the feature is built.
- **Ask, do not invent.** When the author lacks information (metrics, constraints, owners), the gap goes into Open questions, not into invented facts.

## Example
This example is the prompt used to write an RFC, following the same pattern as the PRD and SDD notes.

```markdown
Act as a principal software engineer who writes technical proposals. Your task is to write an RFC (Request for Comments) for the problem and the PRD requirements provided below. The RFC is written in parallel with the System Design, and it must cite the ADRs that record its decisions. If you have doubts, ask the user with the AskUserQuestion tool. Do not invent anything.

### Formatting and Style Rules:
- The document must be generated entirely in **Markdown**.
- The RFC **must have a YAML frontmatter** block at the very top, with `description` (one or two sentences, on one line), `aliases` and `tags`. A document without frontmatter is not valid.
- Add links to other documents in the frontmatter when they exist: `decisions` for the ADRs that record its decisions, and `related` for lateral notes such as the System Design and the SDD. Write each link as a quoted full-path wikilink, for example `"[[folder/Note.md|Note]]"`. Do not put the parent note in the frontmatter.
- Format the document as an Obsidian note: link related notes with full-path wikilinks and aliases (`[[folder/Note.md|Note]]`), keep them in a `## Related` section, and do not link back to a parent note.
- The RFC **must follow the ontology** of the design doc chain. Ontology matters: use the canonical name as the title, put synonyms and acronyms in `aliases`, and state which documents the RFC depends on (PRD, System Design) and which depend on it (FDD, ADR).
- Use tables and lists to make the document quick to read.
- Use roles instead of real names. Do not include personal data.
- If any information is needed, use the AskUserQuestion tool to ask for it. If it is still unknown, record it in the RAID Register and refer to its ID instead of filling the gap.

### Required RFC Structure:
1. **Summary:** the proposal in a few sentences.
2. **Context and Motivation:** the problem, with the PRD requirement IDs it addresses.
3. **Proposal:** the design, at the level of components and their interactions.
4. **Alternatives Considered:** at least two options, each with trade-offs and the reason it was not chosen.
5. **Decisions:** links to the ADRs that record each decision.
6. **Impact:** cost, performance, operations and security.
7. **Rollout and Migration:** how the change reaches production and how to roll it back.
8. **Open Questions:** list the IDs of the open issues and assumptions from the RAID Register that affect this RFC.
9. **Review and Status:** the lifecycle status, the review deadline and a changelog table.
```

## Related
- [[llm/system design/FDD - Feature Design Doc.md|FDD - Feature Design Doc]]
