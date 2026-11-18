---
description: Security design doc that records the threat model, data classification, authentication and authorization, secrets handling and risks of a system or feature, written alongside the System Design when the risk is high.
aliases:
  - Security Design Doc
  - SDD
tags:
  - system-design
  - security
---

A Security Design Doc describes how a system or feature protects its data and its users: what can go wrong, and what is done to prevent or limit it.

## When to write it
- The system handles personal data, credentials, payments or other sensitive data.
- It exposes APIs or integrates with external systems.
- It lets an AI model call tools or read untrusted input, for example through prompt injection.
- For a small internal change, a security section in the System Design or the RFC is usually enough.

## Typical sections
- **Scope and assets:** what is being protected.
- **Data classification:** what kind of data is handled and where it is stored.
- **Threat model:** what can go wrong. A common method is STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege).
- **Authentication and authorization:** who the actors are, and how they prove their identity and get access.
- **Secrets handling:** where keys and tokens are stored and how they are rotated.
- **Risks and mitigations:** each risk with its mitigation and an owner.
- **Open questions:** unresolved items, with an owner and a date.

## Example

```markdown
Act as an experienced security architect for software systems. Your task is to write a Security Design Doc (SDD) for the system or feature described below. The SDD is written alongside the System Design and the RFC, and its threats and controls must inform them. If you have doubts, ask the user interactively and assume only the obvious.

### Formatting and Style Rules:
- The document must be generated entirely in **Markdown**.
- It must start with a **YAML frontmatter** block with `description` (one or two sentences, on one line), `aliases` and `tags`.
- Focus on **what** is protected, **which** threats exist and **which** controls reduce them. Leave the product and library choices to the RFC or the FDD.
- Use tables and lists to make the document quick to read.
- If information is missing, record it in the RAID Register and refer to its ID instead of inventing controls or data classifications.
- Use roles (e.g., "external client") instead of real names. Do not include personal data.
- **CLAUDE.md must never contain PII or security risks.** Record security risks only in this document.
- **Ontology matters.** Use the canonical name of the concept as the title, and put synonyms and acronyms in `aliases`. Place the document in the right level of the design doc chain, and state which documents it depends on (System Design, RFC, FDD).
- **Write it as an Obsidian note.** Link related notes with full-path wikilinks and aliases (`[[folder/Note.md|Note]]`), and keep them in a `## Related` section. Do not link back to a parent note.

### Required SDD Structure:

1. **Scope and Assets:** what is protected and why it matters.
2. **Data Classification:** the types of data handled, their sensitivity, where they are stored and for how long.
3. **Threat Model:** threats per component and data flow, using STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege). Give each threat an ID (`T-01`).
4. **Authentication and Authorization:** the actors, how each one proves its identity, and what each role can access.
5. **Secrets Handling:** where keys and tokens are stored, how they are rotated and who can access them.
6. **Controls and Risks:** for each threat, the mitigation and the control. Record residual risks in the RAID Register and refer to their IDs (`R-01`).
7. **Assumptions and Open Questions:** list the IDs of the relevant assumptions and issues from the RAID Register.
8. **Review and History:** the security review status and a changelog table.
```

## Related
- [[llm/system design/System Design.md|System Design]]
