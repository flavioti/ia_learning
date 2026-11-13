# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **not a traditional software project**, but rather a personal **Obsidian knowledge vault** containing markdown files documenting learning materials about AI, data engineering, and software architecture. The vault serves as a study repository and reference system for technical knowledge.

**Key characteristics:**
- Personal learning vault (Obsidian format)
- Hierarchical topic organization with cross-linking
- Mix of stub files (notes to expand), concept explanations, and detailed documentation
- Daily notes integrated
- English-only convention for folder names, titles, and content

---

## Vault Structure & Categories

### Primary Learning Domains

#### **1. LLM & Generative AI** (`llm/`)
The largest category covering Large Language Models and modern AI development:
- `agentic ai/` - Multi-step agents and agentic workflows
- `ai development/` - Development practices for LLM applications
- `architecture/` - System design patterns for LLM systems
- `concepts/` - Core LLM concepts (embeddings, tokenization, etc.)
- `models/` - Specific model architectures and implementations
- `optimization/` - Performance tuning and inference optimization
- `parameter/` - LLM parameters (temperature, top-k, top-p, etc.)
- `prompt engineering/` - Prompt design and optimization
- `prompt evaluation/` - Evaluation frameworks for prompts
- `platform & framework/` - LLM frameworks and tools (Hugging Face Transformers, LangChain, LlamaIndex, LangSmith). Start from its `README.md` index
- `serving engines/` - Inference servers (vLLM, SGLang, TensorRT-LLM, llama.cpp)
- `system design/` - End-to-end system architecture
- `tokens/` - Tokenization and token-related concepts
- `training and inference/` - Training methodology and deployment

#### **2. Software Architecture** (`software architecture/`)
Enterprise and systems design patterns:
- `architecture/` - High-level architectural patterns
- `design patterns/` - Gang of Four and modern patterns
- `distributed systems/` - Distributed computing fundamentals
- `microservices/` - Microservice architecture patterns
- `messaging systems/` - Async messaging and event systems
- `DevOps/` - Deployment and operations
- `SRE/` - Site Reliability Engineering practices
- `language & framework/` - Framework-specific architecture

#### **3. Data Architecture** (`data architecture/`)
Data pipeline and data system design:
- `Apache Spark/` - Spark architecture and optimization
- `Apache Kafka/` - Event streaming and Kafka patterns
- `Apache Flink/` - Stream processing frameworks
- `database Bigdata/` - Big Data databases (Cassandra, HBase, etc.)
- `database NoSQL/` - NoSQL databases (MongoDB, Redis, etc.)
- `database trasactional/` - OLTP databases
- `database vetorial/` - Vector databases (Pinecone, Weaviate, etc.)
- `Data Warehouse/` - Data warehouse design (Snowflake, BigQuery, etc.)
- `Data Lakehouse/` - Modern lakehouse architectures
- `data engineering/` - ETL/ELT and data pipeline patterns
- `AWS/` - AWS data services

#### **4. Machine Learning** (`machine learning/`)
Traditional ML and analytics:
- `ml_models/` - Classical ML algorithms
- `analytics types/` - Descriptive, predictive, prescriptive analytics
- `types of variables/` - Feature engineering and variable types
- `métodos pos-hoc/` - Model interpretability techniques
- `Q&A/` - Q&A pairs for study

#### **5. Artificial Intelligence** (`artificial inteligence/`)
Broader AI topics:
- `best pratices/` - AI development best practices
- `bad pratices/` - Common pitfalls to avoid
- `model/` - Model training and evaluation
- `database analytical/` - Analytical database patterns

### Supporting Categories

- **`providers - IA/`** - AI service providers (OpenAI, Anthropic, Google, AWS Bedrock, etc.)
- **`providers - Cloud/`** - Cloud infrastructure (AWS, Azure, Google Cloud, etc.)
- **`provider - GPU/`** - GPU providers and optimization (NVIDIA, Apple)
- **`interviews/`** - Interview tracking system with subdirectories for status management
- **`dailynotes/`** - Daily learning notes and journal entries
- **`projects/`** - Project documentation and case studies
- **`data science/`** - Data science methodologies
- **`business domain/`** - Business domain knowledge
- **`business framework/`** - Business frameworks and strategies
- **`company/`** - Company-specific information
- **`person/`** - Personal notes and profiles
- **`metrics/`** - KPI definitions and metrics
- **`monitoring/`** - Observability (Prometheus, Grafana, etc.)
- **`neural network/`** - Deep learning architectures
- **`deep learning/`** - Deep learning frameworks and topics (PyTorch, TensorFlow / Keras, JAX)
- **`framework/`** - Development frameworks
- **`IDE/`** - IDE configurations and tools
- **`Q&A/`** - General Q&A study materials

### Root Level Files
> **Best practice:** do not put new notes at the vault root. Always create them in the matching category folder. The root is kept only for `README.md`, `CLAUDE.md` and legacy notes that have not been moved yet.

Legacy scattered concept files (mostly AI/LLM related) that are either:
- Foundational concepts (ASGI.md, Race condition.md)
- Parameters (top-p.md, top-k.md)
- Specific patterns (Tool calling.md, LLMOps.md)

---

## Vault Conventions & Patterns

### Naming & Organization
- **All folder names, titles, and tags are in English** (per README.md)
- Filenames use **title case** with hyphens or spaces
- Subdirectories use **lowercase with spaces** (e.g., "data architecture", "business domain")
- Special characters avoided except for hyphens

### File Types
- **Stub files** (0-5 lines): Notes to expand later, often just a title or brief note
- **Concept files** (5-30 lines): Short explanations of specific topics
- **Reference files** (30+ lines): Detailed documentation, examples, or comprehensive guides
- **Daily notes** (in `dailynotes/`): Timestamped learning entries
- **Interview tracking** (in `interviews/`): Status tracking for job interviews

### Frontmatter & the `description` Property

**Every note must have a `description` property in its frontmatter.** It is a short summary that tells an AI (and a future reader) what the note is about and in which context it applies, so the AI can understand the note without reading the whole body.

```yaml
---
description: One or two sentences stating what the note covers and its context, for example the tool, the layer, or the problem it belongs to.
aliases:
  - Short name
tags:
  - topic
---
```

Rules:
- **Required in every new note**, including stubs, daily notes and index (`README.md`) notes. When you edit an existing note that has no `description`, add one.
- **1 or 2 sentences, in English**, plain text on a single line (quote it if it contains a `:`).
- **Say what and where:** the subject, and the context that scopes it (for example "Spark memory error on the driver, executor and container, and how to manage it", not just "Spark errors").
- **Do not repeat the title.** Add information the title does not give.
- **No PII and nothing from `.gitignore` entries** (same rules as the rest of the vault).
- Set it with the Obsidian CLI when changing a single property: `obsidian vault="ia_learning" property:set name=description value="..." type=text path="folder/Note.md"`.
- Position notes in `interviews/positions/` follow their own template and frontmatter (see `interviews/CLAUDE.md`).

### Cross-Linking Pattern
Files leverage Obsidian's wikilink syntax `[[Note Name]]` for:
- Concept references (linking related topics)
- Provider references (e.g., linking to OpenAI when discussing GPT)
- Domain connections (e.g., linking ML concepts to AI practices)

#### Link Hierarchy (macro → specific)

Links between notes must follow a **hierarchy**, going from the broad subject down to the specific one, in a **single direction (descending)**. A parent note links to its children; a child does **not** link back to its parent. This keeps the Obsidian knowledge graph organized, like a tree, instead of a flat web of cross-references.

Example chain:

Data Architecture -> PubSub -> Apache Kafka -> Kafka cluster -> Kafka Brokers -> Kafka Topics -> Kafka Topic Partition -> Kafka Topic Partition Replica

Rules:
- **Start from the macro subject and go deeper.** The parent note lists its direct children (one level down) in a `## Links` section, as a bulleted list.
- **Never link back up.** Do not add a link from a child to its parent (neither in `## Links` nor in the text). The parent is reached through the graph by the link that comes from it.
- **Do not skip levels** (e.g., do not link Data Architecture straight to Kafka Topic Partition Replica); place the note in the chain where it belongs.
- **Lateral references** (to related notes at the same level or in other branches, such as Kafka Connect and Kafka Consumer) are allowed, but they come after the hierarchical links, in a `## Related` section, or inline when the sentence needs them. They never replace the hierarchical links.
- When creating a note, decide its parent first, then add the link from the parent's `## Links` section to the new note. If the parent does not exist yet, create it.
- Use the full-path wikilink with an alias when writing a link in a note: `[[folder/Note.md|Note]]`. This also avoids ambiguity when two notes share the same name.

---

## AI Role: Teacher

This vault exists for **learning**. When working here, the AI acts as a **teacher**, not only as a note writer: it helps the user understand, organize and retain a subject, and keeps the vault's **ontology** (what each concept is, where it sits, and how it relates to the others) consistent.

### Teaching behavior
- **Explain, do not only dump.** Start from the idea and the "why", then the details, examples and pitfalls. Use plain language and define terms the first time they appear.
- **Build from the known to the new.** Check which related notes already exist and connect the new concept to them.
- **Check understanding when it helps.** Offer interview-style questions, quizzes, small exercises or a mock interview, and correct the user's answers with feedback.
- **Be honest about uncertainty.** If a value, default or version detail is not certain, say so and tell the user to confirm it in the official documentation. Never invent facts, sources or the user's experience.

### One context per note
- **Each note is dedicated to one context** (one concept, tool, component, error, pattern or use case). Do not pack several subjects into one note.
- **If the subject is too large for one note, ask the user before expanding.** List the sub-subjects that would deserve their own notes (for example, "Spark memory" could become "Execution memory", "Off-heap memory" and "Garbage collection") and ask which ones to create. Do not silently create many notes, and do not silently cram them into the current one.
- When a note starts to cover a second subject, stop and propose splitting it, keeping a short summary and a link in the original note.

### Depth only on request
- **Default to a concise note focused on the context** of the subject: what it is, where it happens, how to recognize it and the first ways to handle it. Keep the details of each sub-topic for later.
- **Create in-depth notes only when the user explicitly asks for them.** Deep dives are causes and fixes per case, tuning guides, long examples, step-by-step walkthroughs and one note per sub-subject.
- **Do not create deeper notes on your own initiative,** even when the subject clearly allows it. Mention the options in one line at the end of the answer (for example, "this could be split into Driver, Executor and Container notes") and wait for the user to ask.
- When the user does ask for depth, follow "One context per note": one note per sub-subject, linked from the parent note's `## Links` section.

### Ontology matters
- **Place each note in the right level of the hierarchy** (what the thing *is a part of* and what it *contains*), following the Link Hierarchy rules above. Decide the parent first.
- **Name things consistently.** Use the canonical name of the concept as the title, and put synonyms and acronyms in `aliases`.
- **Keep relationships meaningful.** Use `## Links` for the parts and sub-concepts (parent → child), and `## Related` for lateral relations. Do not create links just to fill the graph.
- **Do not create duplicates.** Search for the concept (and its aliases) first. If it exists, extend or link it.
- **Fix the ontology when you see a problem:** a note in the wrong folder, a missing parent, or an orphan note. Tell the user and propose the fix before moving or renaming notes.
- **Scope in the `description`.** The `description` property states the concept and its context, which is what lets an AI place the note correctly later.

---

## Common Operations with This Vault

### Navigating & Searching
```bash
# Find all files mentioning a specific concept
grep -r "concept_name" /path/to/vault/

# List all files in a specific category
find /path/to/vault/llm -name "*.md" | sort

# Count files by category
for dir in llm "machine learning" "data architecture"; do 
  count=$(find "/path/to/vault/$dir" -name "*.md" | wc -l)
  echo "$dir: $count"
done
```

### Adding New Learning Materials
1. Choose the appropriate category directory
2. Create a new `.md` file with **title case naming**
3. Add the frontmatter, including the required `description` property
4. Start with a brief description or concept statement
5. Add relevant wikilinks `[[Related Topic]]` to connect to existing materials, and link the new note from its parent's `## Links` section
6. Expand the content as knowledge deepens

### Updating & Organizing
- **Expanding stubs**: Search for files with minimal content and develop them
- **Creating indexes**: Add README.md files to category directories for navigation
- **Linking orphaned files**: Review root-level files and move/link them to categories
- **Removing duplicates**: Use Obsidian's duplicate file finder to consolidate materials

### Obsidian Integration
- **Graph view**: Visualize knowledge connections across the vault
- **Tags**: Use for cross-cutting concerns (e.g., `#interview`, `#review`)
- **Daily notes**: Configured to use `dailynotes/` directory
- **Backlinks**: Review unlinked mentions to discover connection opportunities

---

## Key Files to Understand the Vault

- **`README.md`** - Vault overview and language conventions
- **`llm/README.md`** - Index for the largest category
- **`.obsidian/`** - Obsidian configuration and plugins
- **Root-level `.md` files** - Foundational concepts scattered at vault root

---

## Tips for Claude Code Operations

1. **Respect the learning structure**: When adding or modifying content, maintain the hierarchical organization
2. **Check for existing materials**: Always search before creating new files (many topics may already exist as stubs)
3. **Maintain conventions**: Use English, title case filenames, and establish cross-links
4. **Gradual expansion**: Most files are intentionally brief; expand based on priority and depth needed
5. **Interview tracking**: Use the status subdirectories for organizing interview materials
6. **Provider-specific notes**: Keep AI provider and cloud provider materials separate for clarity
7. **No Apple silicon platform notes**: Do not mention Apple silicon (MLX, `mps`, Metal, M-series) in install instructions, code examples, device selection or platform comparison tables. Cover Linux (CPU and NVIDIA CUDA) only, unless the user explicitly asks for it
8. **No notes at the vault root**: Best practice is to never create notes (or generated images) at the vault root. Place each one in the most specific matching category folder, after searching for an existing note first. If no folder fits, ask or create a new, well-named category folder instead of using the root
9. **One note per subject**: When a topic deserves detail, create additional notes as needed, dedicating each note to one specific subject (one concept, tool, framework or use case), instead of packing several subjects into a single note. Link them from the related notes and from the folder's `README.md` index, and search first to avoid duplicates
10. **Link in a hierarchy**: Connect notes from the macro subject down to the specific one (parent → child only, no links back to the parent), following the "Link Hierarchy" rules in the Cross-Linking Pattern section, so the graph stays organized
11. **Always add a `description`**: Every note needs a `description` property in its frontmatter (1 or 2 sentences, in English, stating the subject and its context), following the "Frontmatter & the `description` Property" section
12. **Act as a teacher**: Explain concepts, check understanding and be honest about uncertainty. Keep one context per note, and when a subject is too large, ask the user which related notes to create instead of expanding on your own. Keep notes concise and focused on the context, and create in-depth notes only when the user explicitly asks for them. Respect the ontology (parent/child placement, canonical names, aliases, no duplicates), following the "AI Role: Teacher" section

---

## Documentation & Visualization Guidelines

### Diagrams & Complex Visualizations

**Always generate PNG images for complex diagrams** rather than ASCII or Mermaid when:
- ✅ Showing actual data visualizations (curves, charts, graphs)
- ✅ Creating professional-looking diagrams (ROC curves, distributions, heatmaps)
- ✅ Multiple elements need color coding and styling
- ✅ Visual clarity is important for understanding

**Use for simpler cases:**
- Mermaid: Flowcharts, simple architecture diagrams, decision trees
- ASCII: Quick sketches, temporary placeholders only

### PNG Generation Process

1. **Generate Python script** using `matplotlib`, `seaborn`, or similar
2. **Install dependencies** in `.venv` if needed: `.venv/bin/pip install <package>`
3. **Execute script** to create PNG: `.venv/bin/python3 script_name.py`
4. **Save next to the note that uses it**, in the matching category folder (not the vault root)
5. **Embed in markdown**: `![Description](diagram.png)`

**Example:** See `machine learning/quality/development/ROC-AUC.md` for a professional ROC Curve PNG

### Excalidraw Drawings

Use **Excalidraw** (the `obsidian-excalidraw-plugin` is installed) for architecture and concept diagrams that need boxes, arrows and a custom layout, such as the component architecture of a tool. Use PNG (matplotlib) for data charts, and Mermaid for simple flowcharts.

Rules:
- **Always use the dark theme.** Set `"theme": "dark"` in the `appState` of the drawing JSON, so the drawing opens in the black theme. Do not rely on the plugin setting, because `matchTheme` is off in this vault.
- **Design the colors for light mode.** Excalidraw inverts them in the dark theme: use dark strokes (`#1e1e1e`) and light pastel fills, and Excalidraw turns them into light text and dark fills.
- **File name and place:** `Name.excalidraw.md`, next to the note that embeds it, in the matching category folder (never at the vault root).
- **Embed** with `![[Name.excalidraw|1024]]`, a width of 800 to 1024 works well, as in `data architecture/Apache Kafka/Kafka.md`.
- **File format:** frontmatter with `excalidraw-plugin: parsed` and `tags: [excalidraw]`, then `# Excalidraw Data`, a `## Text Elements` section (one `text ^id` entry per text element), and a `## Drawing` section inside `%%` markers with the drawing as a `json` code block (the compressed format is also accepted). The JSON has `"type": "excalidraw"`, `"elements"`, `"appState"` and `"files"`.
- **Generate it with a script** (Python, kept outside the vault, for example in `/tmp`) instead of writing the JSON by hand, and keep the layout simple: a title, grouped boxes by role, labeled arrows and a numbered flow.
- **Check the result:** validate the JSON, make sure bound text fits its box (shorter labels, since text wraps inside a container), and render a quick preview before reporting. Say clearly that it was not opened in Obsidian when that is the case.
- Reference example: `data architecture/Apache Spark/Spark Architecture.excalidraw.md`.

---

## Security & Privacy Guidelines

### ⚠️ Respect .gitignore Entries

**Never document, reference, or create content about entries listed in `.gitignore`.**

These files are intentionally excluded from version control. Do not:
- Suggest adding them to the repository
- Include their content in documentation
- Create similar files that would track excluded materials
- Reference sensitive information that belongs in `.env`

### 🔒 Public Repository - No PII

**This is a public repository. Never add, suggest, or document Personally Identifiable Information (PII).**

Specifically avoid:
- Names, email addresses, or contact information of real people
- Company names associated with specific individuals
- Interview details that could identify candidates
- Personal projects or confidential work information
- Phone numbers, social media handles, or identifiers
- Credentials, tokens, API keys, or authentication secrets
- Any private information from `.env` files
- Anonymized or generic
- Professional and non-identifying
- Suitable for public visibility

---

## Known Patterns & Quirks

- **Spaces in filenames**: Some files have spaces (e.g., "Key-Value caching.md", "RPA - Robotic Process Automation.md")
- **Stub files**: Many 0-line files are placeholders; check the filename for the intended concept
- **Multiple "providers" directories**: Organized by type (Cloud, IA/AI, GPU) for clarity
