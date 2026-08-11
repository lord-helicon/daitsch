#!/bin/bash
# Installiert den Skill daitsch. Verwendung:
#   bash install.sh                  in den vorhandenen Skill-Ordner
#   bash install.sh --ziel <pfad>    in einen bestimmten Ordner

set -euo pipefail

NAME="daitsch"
QUELLE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIEL=""

while [ $# -gt 0 ]; do
  case "$1" in
    --ziel) ZIEL="$2"; shift 2 ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; exit 2 ;;
  esac
done

AGENTS_DIR="$HOME/.agents/skills"
CLAUDE_DIR="$HOME/.claude/skills"

if [ -z "$ZIEL" ]; then
  if [ -d "$AGENTS_DIR" ]; then
    ZIEL="$AGENTS_DIR/$NAME"
  else
    ZIEL="$CLAUDE_DIR/$NAME"
  fi
fi

mkdir -p "$ZIEL"
rm -rf "${ZIEL:?}/references" "${ZIEL:?}/scripts" "${ZIEL:?}/tests"
cp "$QUELLE/SKILL.md" "$ZIEL/SKILL.md"
cp -R "$QUELLE/references" "$ZIEL/references"
cp -R "$QUELLE/scripts" "$ZIEL/scripts"
cp -R "$QUELLE/tests" "$ZIEL/tests"
echo "Installiert nach $ZIEL"

# Wo Skills unter ~/.agents liegen und ~/.claude/skills darauf verweist, den Verweis nachziehen.
if [ "$ZIEL" = "$AGENTS_DIR/$NAME" ] && [ -d "$CLAUDE_DIR" ] && [ ! -e "$CLAUDE_DIR/$NAME" ]; then
  ln -s "../../.agents/skills/$NAME" "$CLAUDE_DIR/$NAME"
  echo "Verweis angelegt: $CLAUDE_DIR/$NAME"
fi

if command -v python3 >/dev/null 2>&1; then
  echo
  python3 "$ZIEL/scripts/klartext.py" --selbsttest
else
  echo
  echo "python3 nicht gefunden. Der Skill funktioniert auch ohne, dann ohne Prüfskript."
fi

cat <<TEXT

Für andere Agenten liegen fertige Dateien in adapters/:

  adapters/AGENTS.md                     ins Projektwurzelverzeichnis als AGENTS.md
  adapters/CLAUDE.md                     als CLAUDE.md
  adapters/GEMINI.md                     als GEMINI.md
  adapters/cursor/daitsch.mdc            nach .cursor/rules/
  adapters/copilot-instructions.md       nach .github/copilot-instructions.md
  adapters/system-prompt.txt             in den Systemprompt beliebiger Agenten
TEXT
