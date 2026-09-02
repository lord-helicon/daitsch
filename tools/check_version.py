#!/usr/bin/env python3
"""Hält die Versionsangaben zusammen.

Zwei Stellen tragen eine Version: der Git-Tag und .codex-plugin/plugin.json.
Laufen sie auseinander, installiert jemand über Codex eine andere Fassung als
die, die das Release verspricht.

    python3 tools/check_version.py            # gegen den neuesten Tag
    python3 tools/check_version.py v1.2.0     # gegen einen geplanten Tag
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
MANIFEST = WURZEL / ".codex-plugin" / "plugin.json"


def neuester_tag() -> str | None:
    try:
        ergebnis = subprocess.run(
            ["git", "-C", str(WURZEL), "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return None
    tag = ergebnis.stdout.strip()
    return tag or None


def main(argv: list[str]) -> int:
    if not MANIFEST.exists():
        print(f"Kein Manifest unter {MANIFEST}", file=sys.stderr)
        return 2

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as fehler:
        print(f"plugin.json ist kein gültiges JSON: {fehler}", file=sys.stderr)
        return 2

    fehler: list[str] = []

    for feld in ("name", "version", "description", "skills"):
        if not manifest.get(feld):
            fehler.append(f"plugin.json: Feld {feld} fehlt oder ist leer.")

    name = manifest.get("name", "")
    if name and not (WURZEL / "skills" / name / "SKILL.md").exists():
        fehler.append(f"plugin.json nennt {name!r}, aber skills/{name}/SKILL.md gibt es nicht.")

    version = str(manifest.get("version", ""))
    ausdruecklich = len(argv) > 1
    tag = argv[1] if ausdruecklich else neuester_tag()
    hinweis = ""

    if tag is None:
        hinweis = f"plugin.json steht auf {version}. Noch kein Tag vorhanden, nichts zu vergleichen."
    elif version != tag.lstrip("v"):
        satz = f"Tag {tag} und plugin.json {version} passen nicht zusammen."
        if ausdruecklich:
            # Beim Taggen ist die Abweichung ein Fehler.
            fehler.append(satz)
        else:
            # Zwischen Versionssprung und Tag ist sie der normale Zustand.
            hinweis = f"{satz} Solange der Tag noch fehlt, ist das erwartet."

    if fehler:
        print("Versionsprüfung fehlgeschlagen:\n", file=sys.stderr)
        for eintrag in fehler:
            print(f"  - {eintrag}", file=sys.stderr)
        return 1

    if hinweis:
        print(hinweis)
    elif tag is not None:
        print(f"Versionsprüfung bestanden: Tag {tag} und plugin.json {version} passen zusammen.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
