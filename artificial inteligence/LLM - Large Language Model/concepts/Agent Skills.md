#ai 
Is a collection of markdown files, instructions for change the model behavior.
> Isn't a endpoint, function or code

Agent skills isn't a proprietary resource, but a file structure convention.

## Why it should be used?

| Without skill                                        | With skill                                                                 |
| ---------------------------------------------------- | -------------------------------------------------------------------------- |
| Every prompt, you need to give context to LLM.       | LLM always read the instructions, without need to take context every time. |
| The knowledge stay on each dev mind.                 | The knowlege is versioned on GIT server, reviewed on PR                    |
| Each developer works in their own way.               | Consistent results across sessions and individuals                         |
| Deterministic steps performed with improvisation     | Same entry instructions, always                                            |
| Hard to onboard new coworker, because there's no doc | Easy way to onboard new coworkers                                          |
## Where is usefull?

- Reuse - When the model behavior or context must be used several times
- Process - Naming conventions, clear purpose, team standards, essential steps hierarchy.
- Stability - Rules must follow every time

> [!SECURIY WARNING] Not use skill for
> secrets, credentials, PII or live data. Skill are always statics inside a context.

## Use cases

| Item                                                      | Use                                                         |                                                                                                                                                                       |
| --------------------------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Not obvius and repeatable process                         | Agent Skill                                                 |                                                                                                                                                                       |
| Project fact (we use poetry, not pip)                     | Markdown                                                    |                                                                                                                                                                       |
| Code format                                               | Linter / Formatter                                          |                                                                                                                                                                       |
| Data access or system access                              | [[MCP]] / Tool                                              |                                                                                                                                                                       |
| Volatile fact (some package version)                      | Web search                                                  |                                                                                                                                                                       |
| Explicit action with colateral effects ([[CD - Continuous deployment]] deploy) | Skill (with dilable-model-invocation, [[YAML frontmatter]]) | Prevents your coding agent from automatically discovering and loading the skill into its context window, restricting its execution to explicit manual slash commands. |
|                                                           |                                                             |                                                                                                                                                                       |

