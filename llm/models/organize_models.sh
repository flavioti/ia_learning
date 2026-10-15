#!/usr/bin/env bash
# Organizes the notes in llm/models into provider subfolders.
# File names are kept unchanged, so Obsidian [[wikilinks]] keep resolving.
# mv -n never overwrites an existing file. Safe to run more than once.
set -euo pipefail
cd "$(dirname "$0")"

move() {  # move <folder> <file>...
  local dir="$1"; shift
  mkdir -p "$dir"
  for f in "$@"; do
    [ -e "$f" ] && mv -n -- "$f" "$dir/" && echo "  $f -> $dir/"
  done
  return 0
}

move "Anthropic" \
  "Anthropic - Fable 5.x.md" "Opus 5.x.md" "Sonnet 5.5.md" \
  "Haiku 5.5.md" "Haiku 4.5.md" "Claude 3.5 Sonnet.md"

move "Google" \
  "Google - Gemini 3.1 Flash.md" "Google - Gemini 3.7 Flash.md" \
  "Gemini 3.5 Flash-Lite.md"

move "OpenAI"  "GPT-6 Luna.md"
move "Alibaba" "Qwen3.5 4b.md"

move "_Concepts" "IA model.md" "Text-based model.md"

# Comparison.md stays at the top level as the index.
echo "Done. You can delete this script now."
