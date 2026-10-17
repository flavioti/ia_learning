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
- `serving engines/` - Inference servers (vLLM, TensorRT, etc.)
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
- **`framework/`** - Development frameworks
- **`IDE/`** - IDE configurations and tools
- **`Q&A/`** - General Q&A study materials

### Root Level Files
Scattered concept files (mostly AI/LLM related) that are either:
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

### Cross-Linking Pattern
Files leverage Obsidian's wikilink syntax `[[Note Name]]` for:
- Concept references (linking related topics)
- Provider references (e.g., linking to OpenAI when discussing GPT)
- Domain connections (e.g., linking ML concepts to AI practices)

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
3. Start with a brief description or concept statement
4. Add relevant wikilinks `[[Related Topic]]` to connect to existing materials
5. Expand the content as knowledge deepens

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
4. **Save to vault root** or appropriate folder
5. **Embed in markdown**: `![Description](diagram.png)`

**Example:** See `[[machine learning/quality/development/ROC-AUC.md]]` for a professional ROC Curve PNG

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
