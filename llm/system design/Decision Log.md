---
description: Index of the Architecture Decision Records (ADRs) of the design doc chain, listing each decision with its number, title, status and date so the current and superseded decisions can be found.
aliases:
  - ADR Index
  - Decision Log
tags:
  - system-design
  - adr
---

The decision log is an index of the ADRs. Each ADR remains the source of truth for its decision, and this log only lists them and shows their status.

## Rules
- **Append only:** add a row for each new ADR, and never delete a row.
- **Immutable ADRs:** the body of an ADR is not edited. The only change allowed is its status, for example to Superseded, when a new ADR replaces it.
- **Full-path links:** each ADR is linked with its full path and alias.

## Decisions

| ID | Title | Status | Date |
|---|---|---|---|

## Example

This prompt creates or updates the decision log from the ADRs of a project.

```markdown
Act as a technical lead who keeps the architecture decision history of a project. Your task is to create or update the Decision Log: an index of the ADRs (Architecture Decision Records) listed below, showing each one's number, title, status and date. If you have doubts, ask the user with the AskUserQuestion tool. Do not invent anything.

### Formatting and Style Rules:
- The document must be generated entirely in **Markdown**.
- It must start with a **YAML frontmatter** block with `description` (one or two sentences, on one line), `aliases` and `tags`.
- Format the document as an Obsidian note: link each ADR with a full-path wikilink and alias (`[[folder/ADR - Title.md|ADR - Title]]`).
- Ontology matters: the Decision Log is the parent of the ADRs, so it links down to them and is not linked back from them.
- Do not copy the content of the ADRs. The log only lists them, because each ADR is the source of truth for its decision.
- Never edit an ADR's body. The only change allowed is its status, for example to Superseded, when a new ADR replaces it.
- Do not put personal data in the log, and use roles instead of real names.

### Required Decision Log Structure:
1. **Frontmatter:** `description`, `aliases` and `tags`.
2. **Rules:** append-only, immutable ADR bodies, and full-path links.
3. **Decisions table:** one row per ADR, in the order of their numbers, with the columns ID, Title, Status (Proposed, Accepted or Superseded) and Date (YYYY-MM-DD).
4. **Superseded by:** for each superseded ADR, the ID of the ADR that replaces it.
5. **Related:** links to the ADR template note.
```

## Related
- [[llm/system design/ADR - Architecture Decision Record.md|ADR - Architecture Decision Record]]
