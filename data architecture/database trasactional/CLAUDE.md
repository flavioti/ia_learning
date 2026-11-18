# Database transactional: organization rules

Rules for the notes in this folder. They complement the vault-wide `CLAUDE.md`.

## Structure

| Item | Location | Purpose |
|---|---|---|
| Product notes | `Postgres.md`, `MySQL.md`, ... | History and product facts. They link down to the dialect notes |
| SQL topic notes | `SQL Pitfalls.md`, `SQL EXPLAIN.md`, `Basic SQL Examples.md`, `Window *.md`, `Basic SQL Examples.md` | One context each, child of [[SQL Language]] (at the vault root) |
| Dialect hub | `SQL Dialects/SQL Dialects.md` | Compares commands that change between engines. Parent of the dialect notes |
| Dialect notes | `SQL Dialects/SQL Dialect - <Engine>.md` | One note per engine, only the syntax and commands of that engine |
| Drawings | `*.excalidraw.md` next to the note that embeds them | Excalidraw files, following the vault rules |

## Naming

- Topic and dialect notes are in English titles, with Portuguese content, as in the rest of the SQL notes.
- Dialect notes use the prefix `SQL Dialect - ` and the engine's official name: `PostgreSQL`, `MySQL`, `SQL Server`, `Oracle`, `Spark SQL`.
- Window notes share the prefix `Window`: `Window Ranking Functions`, `Window Aggregate Functions`, `Window Offset Functions`, `Window Frame Clause`.

## Link hierarchy

Follow the vault hierarchy (parent to child, no links back up):

- [[SQL Language]] → `SQL Dialects` hub → dialect notes.
- `Postgres.md` and `MySQL.md` link down to their dialect note. The dialect note does not link back to the product note in its `## Links`, only in the text.
- Topic notes link to [[SQL Language]] in `## Related`. Lateral links between topics go in `## Related`.

## Dialect note template

Each dialect note has the same sections, in this order:

1. **Estatísticas:** the command that collects statistics.
2. **Plano de execução:** `EXPLAIN` and its variants.
3. **Limite e paginação:** `LIMIT`, `TOP`, `FETCH` or equivalent.
4. **Upsert:** the merge or insert-on-conflict syntax.
5. **Transações:** how a transaction starts and ends.
6. **Identificadores:** quoting rules.
7. **Armadilhas:** only differences that cause errors or wrong results.

If an engine has no equivalent of a command, say so in the section instead of leaving it out.

## Version caveats

- Mark version-dependent syntax (for example `EXPLAIN ANALYZE` in MySQL 8.0.18+, or `FETCH FIRST` in Oracle 12c+) and tell the user to confirm it in the official documentation.
- The examples were not run against a live database. Say so when presenting them.

## Hub rules

- The hub `SQL Dialects.md` only compares. Engine-specific detail goes in the dialect notes.
- A new engine gets a new dialect note and a new column in the hub table.

## Checklist

- [ ] Every dialect note has the seven sections of the template
- [ ] Every dialect note is linked from the hub
- [ ] The hub is linked from [[SQL Language]] in `## Dialetos`
- [ ] Product notes (`Postgres.md`, `MySQL.md`) link to their dialect note under `## Related`
- [ ] Each note has a `description` in the frontmatter
