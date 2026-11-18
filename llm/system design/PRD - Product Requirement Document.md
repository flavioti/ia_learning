---
description: Product Requirement Document (PRD) template and best practices for the business and product side of the design doc chain, covering the what and the why before the System Design, RFC and FDD.
aliases:
  - PRD
tags:
  - system-design
  - product
---

## Example

```markdown
Act as an experienced Principal Product Manager in digital products and scalable platforms. Your task is to write a complete, clear, objective and results-oriented PRD (Product Requirements Document), which will serve as the basis for engineering to write the technical RFC (Design Doc). If you have doubts, ask the user with the AskUserQuestion tool. Do not invent anything.

### Formatting and Style Rules:
- The document must be generated entirely in **Markdown**.
- It must start with a **YAML Frontmatter** block containing the document metadata.
- Format the document as an Obsidian note: link related notes with full-path wikilinks `[[folder/Note.md|Note]]`, put them in a `## Related` section, and do not link back to a parent note.
- Be direct, avoid empty jargon ("filler") and focus on the **"What"** and the **"Why"**, leaving the **"How"** (architecture choices, databases or frameworks) to engineering.
- Use tables and lists to make the document quick to read.
- If any information is needed, use the AskUserQuestion tool to ask for it. Do not invent facts, metrics, rules or names.
- If information is still unknown after asking, record it as an assumption or an issue in the RAID Register, and refer to its ID, instead of filling the gap yourself.
- Technical doubts, questions and assumptions do not belong in the PRD. When they come up, create an RFC with `status: Draft` and write them in its Open Questions section. Do not answer them here.
- Use roles (e.g., "support operator") in personas and examples, never real people's names, and do not include personal data.

### Required PRD Structure:

1. **YAML Frontmatter** (exactly at the top):
   - `title`: Clear name of the initiative/feature
   - `description`: One or two sentences, in English, on one line, stating what the PRD covers and its context.
   - `aliases`: Short name(s) of the initiative.
   - `doc_type`: PRD
   - `status`: Draft (lifecycle: Draft → In review → Approved → Superseded)
   - `author`: [Your Name / PM]
   - `tech_lead`: [To be defined]
   - `created_at`: [Current date in YYYY-MM-DD format]
   - `target_release`: [e.g., Q4 2026 / Sprint X]
   - `version`: 0.1
   - `tags`: [list of relevant tags]

2. **Executive Summary (TL;DR)**
   - A short paragraph explaining what the project is, what problem it solves and what the expected impact is.

3. **Context and Problem (Problem Statement)**
   - What is the current pain for the user or the business?
   - What data, metrics or evidence prove that this problem exists and needs to be solved now?

4. **Goals and Success Metrics (Goals & KPIs)**
   - List of clear goals.
   - Table with: *Metric*, *Baseline (Current)*, *Target* and *Measurement deadline*.

5. **Non-Goals (Out of Scope)**
   - Explicit list of what will **not** be delivered in this phase, to avoid scope creep.

6. **Target Audience and Personas**
   - Who the affected users are (end customers, internal operators, consuming systems, etc.) and how each one benefits.

7. **Functional Requirements and User Stories**
   - Grouped by priority (**P0** = Critical/MVP, **P1** = Important, **P2** = Nice to have).
   - For each requirement, include: ID (`RF-01`), a clear description and measurable, verifiable **Acceptance Criteria**.
   - When the criteria will be automated, write them in **Given / When / Then** (Gherkin).
   - Do not mark every requirement as P0: P0 is only the MVP.

8. **Non-Functional Requirements (Business Constraints)**
   - Business expectations about availability, response time perceived by the user (SLAs) and expected volume.
   - For each non-functional requirement, include an ID (`RNF-01`) and a numeric target (e.g., `p99 < 200 ms`, `99.9% availability`, `10k requests/min`). Avoid adjectives such as "fast" or "high availability".

9. **Dependencies and Risks**
   - List the IDs of the dependencies (`D-01`) and risks (`R-01`) from the RAID Register that apply to this project. Do not copy their descriptions.

10. **Assumptions and Open Questions**
   - List the IDs of the assumptions (`A-01`) and issues (`I-01`) from the RAID Register. Do not copy their descriptions.

11. **Review and History**
   - Tech lead's opinion on feasibility and dependencies, with a date, before the RFC starts.
   - History table with *Version*, *Date*, *Author* and *Change*.
```

## Best practices

- **Problem before solution.** Start from the user or business pain and the evidence for it. Describe the problem before listing features.
- **Measurable goals.** Every goal has a baseline, a target and a date. Avoid goals like "improve performance" without a number.
- **Explicit non-goals.** Write what is out of scope so the scope does not grow silently.
- **Requirements with IDs.** Give each requirement an ID (`RF-01`, `RNF-01`) so the RFC, the FDD and the tests can reference it.
- **Testable acceptance criteria.** Write each criterion so it can be verified. When it will be automated, use Given / When / Then (see [[software architecture/concepts/Gherkin.md|Gherkin]]).
- **Prioritize with a clear cut.** P0 is the MVP. If everything is P0, nothing is prioritized.
- **What and why, not how.** Architecture, databases and frameworks belong in the System Design, the RFC or the FDD.
- **Make assumptions and open questions visible.** Keep them in their own sections, with an owner and a date, instead of hiding them in the text.
- **Measurable non-functional requirements.** Express availability, latency and volume with numbers (for example, "p99 latency under 200 ms"), not adjectives.
- **Track the status.** Use the lifecycle Draft → In review → Approved → Superseded, and record changes in a changelog.
- **Review with engineering before the RFC.** The tech lead checks feasibility and dependencies before the RFC starts.
- **Roles, not real people.** Use roles in personas and examples. This is a public repository, so no PII.
- **Write it as an Obsidian note.** Add a `description` property, link related notes with full-path wikilinks and aliases (`[[folder/Note.md|Note]]`), and keep them in a `## Related` section. Do not link back to a parent note.

## Related
- [[llm/system design/System Design.md|System Design]]
