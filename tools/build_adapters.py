#!/usr/bin/env python3
"""Erzeugt aus dem KERN-Block in SKILL.md die Adapterdateien für andere Agenten.

    python3 tools/build_adapters.py

Die erzeugten Dateien liegen in adapters/ und sind eingecheckt, damit sie ohne
Python benutzbar sind. Geändert wird immer SKILL.md, nie ein Adapter.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
SKILL = WURZEL / "skills" / "daitsch" / "SKILL.md"
ZIEL = WURZEL / "adapters"

HINWEIS = "<!-- Erzeugt aus SKILL.md durch scripts/build_adapters.py. Änderungen gehören in SKILL.md. -->"
HERKUNFT = (
    "Die Musterlisten beruhen auf „KI-Sprachmuster im Deutschen vermeiden“ von Tobias Voßberg, "
    "www.iplaw.lol/ki-floskeln, verwendet mit seiner Zustimmung. Diese Datei steht unter CC BY 4.0; "
    "bei Weitergabe bitte beide Quellen nennen."
)
EINSATZ = (
    "Gilt für jeden deutschen Text, der hier entsteht oder überarbeitet wird: Commit-Nachricht, "
    "Dokumentation, README, Mail, Beitrag, Bericht. Für Code und englische Texte gilt sie nicht."
)


def kern_lesen() -> str:
    text = SKILL.read_text(encoding="utf-8")
    treffer = re.search(r"<!-- KERN:start -->\n(.*?)\n<!-- KERN:end -->", text, re.DOTALL)
    if not treffer:
        raise SystemExit("KERN-Block in SKILL.md nicht gefunden.")
    return treffer.group(1).strip()


def ohne_markdown(kern: str) -> str:
    """Tabelle in Textzeilen wandeln, für Systemprompts ohne Markdown-Darstellung."""
    zeilen = []
    for zeile in kern.splitlines():
        roh = zeile.strip()
        if not roh or set(roh) <= set("|-: "):
            continue
        if roh.startswith("|"):
            spalten = [s.strip() for s in roh.strip("|").split("|")]
            if len(spalten) == 2 and spalten[0] != "Statt der Floskel":
                zeilen.append(f"- Statt {spalten[0]}: {spalten[1]}")
            continue
        if roh.startswith("#"):
            zeilen.append("")
            zeilen.append(roh.lstrip("# ").upper())
            continue
        zeilen.append(roh)
    return "\n".join(zeilen).strip()


def schreiben(pfad: Path, inhalt: str) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(inhalt.rstrip() + "\n", encoding="utf-8")
    print(f"  {pfad.relative_to(WURZEL)}")


def main() -> int:
    if not SKILL.exists():
        print("SKILL.md fehlt.", file=sys.stderr)
        return 2
    kern = kern_lesen()

    rumpf = f"""{HINWEIS}

# Deutsche Texte ohne KI-Floskeln

{EINSATZ}

{kern}

Der vollständige Katalog mit rund 75 Mustern, den Ausnahmen und einem Prüfskript steht im Skill
`daitsch` (references/katalog.md, scripts/klartext.py im Skillordner). Wo das Skript vorhanden ist:
`python3 skills/daitsch/scripts/klartext.py <datei>` vor der Abgabe laufen lassen und jeden harten Fund beheben.

{HERKUNFT}
"""

    print("Erzeugt:")
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        schreiben(ZIEL / name, rumpf)

    schreiben(
        ZIEL / "copilot-instructions.md",
        rumpf.replace("# Deutsche Texte ohne KI-Floskeln", "# Deutsche Texte ohne KI-Floskeln\n\nZiel: `.github/copilot-instructions.md`"),
    )

    cursor = f"""---
description: Deutsche Texte ohne KI-Floskeln schreiben und überarbeiten
globs: ["**/*.md", "**/*.mdx", "**/*.txt"]
alwaysApply: false
---

{rumpf}
"""
    schreiben(ZIEL / "cursor" / "daitsch.mdc", cursor)

    prompt = f"""Du schreibst und überarbeitest deutsche Texte so, dass sie nicht nach KI klingen.
Jede Floskel wird durch eine Aussage ersetzt, die jemand nachprüfen kann.

{ohne_markdown(kern)}

Fast jedes dieser Muster ist irgendwo richtig: der Halbgeviertstrich in guter Prosa, das Fazit im
Gutachten, der Doppelpunkt-Titel in der Presse. Im Zweifel bleibt der Satz stehen.

{HERKUNFT}
"""
    schreiben(ZIEL / "system-prompt.txt", prompt.replace(HINWEIS, "").strip())

    return 0


if __name__ == "__main__":
    sys.exit(main())
