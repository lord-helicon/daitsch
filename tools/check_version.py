#!/usr/bin/env python3
"""Hält die Versionsangaben zusammen.

Vier Stellen tragen eine Version: der Git-Tag, das Codex-Manifest, das
Plugin-Manifest und der Marktplatzeintrag. Laufen sie auseinander, installiert
jemand eine andere Fassung als die, die das Release verspricht.

    python3 tools/check_version.py            # gegen den neuesten Tag
    python3 tools/check_version.py v1.2.0     # gegen einen geplanten Tag
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent


def lesen(pfad: Path):
    return json.loads(pfad.read_text(encoding="utf-8"))


def versionen(fehler: list[str]) -> dict[str, str]:
    """Sammelt jede Stelle, die eine Version trägt."""
    gefunden: dict[str, str] = {}

    codex = WURZEL / ".codex-plugin" / "plugin.json"
    plugin = WURZEL / ".claude-plugin" / "plugin.json"
    markt = WURZEL / ".claude-plugin" / "marketplace.json"

    for pfad, schluessel in ((codex, "Codex-Manifest"), (plugin, "Plugin-Manifest")):
        if not pfad.exists():
            fehler.append(f"{schluessel} fehlt: {pfad.relative_to(WURZEL)}")
            continue
        try:
            daten = lesen(pfad)
        except json.JSONDecodeError as e:
            fehler.append(f"{schluessel} ist kein gültiges JSON: {e}")
            continue
        for feld in ("name", "version", "description"):
            if not daten.get(feld):
                fehler.append(f"{schluessel}: Feld {feld} fehlt oder ist leer.")
        gefunden[schluessel] = str(daten.get("version", ""))
        name = daten.get("name", "")
        if name and not (WURZEL / "skills" / name / "SKILL.md").exists():
            fehler.append(f"{schluessel} nennt {name!r}, aber skills/{name}/SKILL.md gibt es nicht.")

    if markt.exists():
        try:
            daten = lesen(markt)
            gefunden["Marktplatz"] = str(daten.get("metadata", {}).get("version", ""))
            for eintrag in daten.get("plugins", []):
                gefunden[f"Marktplatz/{eintrag.get('name')}"] = str(eintrag.get("version", ""))
                quelle = WURZEL / eintrag.get("source", ".")
                if not (quelle / ".claude-plugin" / "plugin.json").exists():
                    fehler.append(f"Marktplatz zeigt auf {eintrag.get('source')!r}, dort fehlt plugin.json.")
        except json.JSONDecodeError as e:
            fehler.append(f"Marktplatz ist kein gültiges JSON: {e}")

    return gefunden


def neuester_tag() -> str | None:
    try:
        ergebnis = subprocess.run(
            ["git", "-C", str(WURZEL), "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return None
    return ergebnis.stdout.strip() or None


def main(argv: list[str]) -> int:
    fehler: list[str] = []
    gefunden = versionen(fehler)

    einzigartig = set(gefunden.values())
    if len(einzigartig) > 1:
        aufstellung = ", ".join(f"{k} {v}" for k, v in sorted(gefunden.items()))
        fehler.append(f"Die Manifeste widersprechen sich: {aufstellung}")

    version = next(iter(einzigartig), "")
    ausdruecklich = len(argv) > 1
    tag = argv[1] if ausdruecklich else neuester_tag()
    hinweis = ""

    if tag is None:
        hinweis = f"Alle Stellen stehen auf {version}. Noch kein Tag vorhanden."
    elif len(einzigartig) == 1 and version != tag.lstrip("v"):
        satz = f"Tag {tag} und Manifeste {version} passen nicht zusammen."
        if ausdruecklich:
            fehler.append(satz)
        else:
            hinweis = f"{satz} Solange der Tag noch fehlt, ist das erwartet."

    if fehler:
        print("Versionsprüfung fehlgeschlagen:\n", file=sys.stderr)
        for eintrag in fehler:
            print(f"  - {eintrag}", file=sys.stderr)
        return 1

    if hinweis:
        print(hinweis)
    else:
        print(f"Versionsprüfung bestanden: Tag {tag} und {len(gefunden)} Stellen stehen auf {version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
