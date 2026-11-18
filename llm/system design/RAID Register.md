---
description: Single RAID register (Risks, Assumptions, Issues, Dependencies) for the design doc chain, where each entry has an ID that the PRD, RFC and SDD reference instead of repeating it.
aliases:
  - RAID Register
  - RAID Log
tags:
  - system-design
  - raid
---

The RAID register is the one place where risks, assumptions, issues and dependencies are recorded. The PRD, RFC and SDD refer to entries by ID and do not repeat them.

## ID prefixes
- `R-01` **Risk:** a possible event that would hurt the project. Needs a probability, an impact and a mitigation.
- `A-01` **Assumption:** something taken as true without verification. Needs a verification plan and a due date.
- `I-01` **Issue:** a problem that is happening now. Needs an action.
- `D-01` **Dependency:** something the work relies on that another team or system controls.

## Rules
- **One entry, one ID.** Documents link to the ID and never copy the entry.
- **Append only.** Close an entry by changing its status, and never delete it.
- **Assumptions are not facts.** An assumption stays open until it is verified or closed. A document may use it only as an assumption.
- **Every entry has an owner and a due date.**

## Register

| ID | Type | Description | Owner | Due | Status | Mitigation or verification |
|---|---|---|---|---|---|---|

## Example

This prompt creates or updates the RAID register from the risks, assumptions, issues and dependencies of a project.

```markdown
Act as a project manager who keeps the RAID register of a software project. Your task is to create or update the register below from the information provided. Each entry must have a type, an ID, an owner and a due date. If you have doubts, ask the user with the AskUserQuestion tool. Do not invent anything.

### Formatting and Style Rules:
- The document must be generated entirely in **Markdown**.
- It must start with a **YAML frontmatter** block with `description` (one or two sentences, on one line), `aliases` and `tags`.
- Format the document as an Obsidian note, with full-path wikilinks and aliases for related notes, and no link back to the parent note.
- Use the ID prefixes: `R-01` for risks, `A-01` for assumptions, `I-01` for issues, `D-01` for dependencies. Number them in order and never reuse a number.
- Risks need a probability, an impact and a mitigation. Assumptions need a verification plan. Issues need an action. Dependencies need the team or system that controls them.
- Do not delete entries. To close one, change its status.
- An assumption is not a fact. Keep it open until it is verified, and label it as an assumption everywhere it is used.
- Do not put personal data in the register, and use roles instead of real names.
- Other documents (PRD, RFC, SDD) must refer only to IDs that exist in this register.

### Required RAID Register Structure:
1. **Frontmatter:** `description`, `aliases` and `tags`.
2. **ID prefixes and rules:** a short summary of the four types and the rules above.
3. **Register table:** one row per entry, with the columns ID, Type, Description, Owner, Due (YYYY-MM-DD), Status (Open, Closed or Superseded) and Mitigation or verification.
4. **Related:** links to the Decision Log.
```

## Related
- [[llm/system design/Decision Log.md|Decision Log]]
