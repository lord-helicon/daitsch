#!/usr/bin/env python3
"""Packt den Skill für die Ziele, die keinen Zugriff auf das Dateisystem haben.

Claude Code holt sich das Plugin über den Marktplatz aus dem Repository. Cowork
und der Claude-Chat laufen dagegen auf fremden Rechnern und brauchen eine Datei.

    python3 tools/paket.py

Erzeugt in dist/:
    daitsch.plugin       für Cowork, in den Chat ziehen und annehmen
    daitsch-skill.zip    für den Claude-Chat, in den Einstellungen hochladen
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "dist"
NAME = "daitsch"

# Was in die .plugin-Datei gehört. Werkzeuge, Tests des Repositorys und die
# Adapterdateien bleiben draußen, sie helfen dem Plugin nicht.
PLUGIN_INHALT = [
    ".claude-plugin/plugin.json",
    "skills",
    "README.md",
    "LICENSE",
    "LICENSE-CONTENT.md",
]

AUSGESCHLOSSEN = {"__pycache__", ".DS_Store"}


def dateien(pfad: Path):
    if pfad.is_file():
        yield pfad
        return
    for eintrag in sorted(pfad.rglob("*")):
        if eintrag.is_file() and not any(teil in AUSGESCHLOSSEN for teil in eintrag.parts):
            yield eintrag


def packen(quellen: list[Path], basis: Path, ziel: Path) -> int:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    anzahl = 0
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as archiv:
        for quelle in quellen:
            for datei in dateien(quelle):
                archiv.write(datei, datei.relative_to(basis))
                anzahl += 1
    return anzahl


def main() -> int:
    manifest = json.loads((WURZEL / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]

    fehlend = [p for p in PLUGIN_INHALT if not (WURZEL / p).exists()]
    if fehlend:
        print("Fehlt im Repository: " + ", ".join(fehlend), file=sys.stderr)
        return 2

    plugin = ZIEL / f"{NAME}.plugin"
    n = packen([WURZEL / p for p in PLUGIN_INHALT], WURZEL, plugin)
    print(f"  {plugin.relative_to(WURZEL)}  {n} Dateien  {plugin.stat().st_size // 1024} KB  (Cowork)")

    skillzip = ZIEL / f"{NAME}-skill.zip"
    n = packen([WURZEL / "skills" / NAME], WURZEL / "skills", skillzip)
    print(f"  {skillzip.relative_to(WURZEL)}  {n} Dateien  {skillzip.stat().st_size // 1024} KB  (Claude-Chat)")

    # Nachweis, dass das Paket für sich allein läuft.
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(skillzip) as archiv:
            archiv.extractall(tmp)
        pruefer = Path(tmp) / NAME / "scripts" / "klartext.py"
        if not pruefer.exists():
            print("Im Zip fehlt der Prüfer.", file=sys.stderr)
            return 2

    print(f"\nVersion {version}. Beide Pakete liegen in dist/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
