#!/usr/bin/env python3
"""Erzeugt das Bild für die README: ein echter Lauf des Prüfers.

Der Demotext und die Ausgabe entstehen bei jedem Lauf neu, damit das Bild nicht
irgendwann etwas zeigt, was der Prüfer nicht mehr meldet.

    python3 tools/screenshot.py

Braucht Pillow und eine Monospace-Schrift.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow fehlt. Installieren mit: python3 -m pip install Pillow")

WURZEL = Path(__file__).resolve().parent.parent
PRUEFER = WURZEL / "skills" / "daitsch" / "scripts" / "klartext.py"
ZIEL = WURZEL / "docs" / "daitsch-terminal.png"

DEMO = """Gerade in Zeiten des Wandels ist Vertrauen wichtiger denn je. Es geht nicht um
Technologie, sondern um Menschen. Unsere Lösung ist sauber strukturiert und
schafft echten Mehrwert — nahtlos, robust und zukunftssicher.

Lassen Sie uns gemeinsam den nächsten Schritt gehen. Zusammenfassend lässt sich
sagen: Am Ende kommt es auf den Menschen an.
"""

SCHRIFTEN = [
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]

GROESSE, ZH, RAND, BREITE = 21, 32, 44, 1200
HG, PROMPT, TEXT, GEDIMMT = (24, 26, 33), (126, 176, 122), (208, 212, 222), (118, 124, 140)
HART, WEICH, ID, WEISS = (226, 106, 96), (222, 178, 92), (122, 176, 214), (238, 241, 246)


def schrift(groesse: int, fett: bool):
    for pfad in SCHRIFTEN:
        if Path(pfad).exists():
            try:
                return ImageFont.truetype(pfad, groesse, index=1 if fett else 0)
            except OSError:
                return ImageFont.truetype(pfad, groesse)
    raise SystemExit("Keine Monospace-Schrift gefunden.")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        entwurf = Path(tmp) / "entwurf.md"
        entwurf.write_text(DEMO, encoding="utf-8")
        lauf = subprocess.run(
            [sys.executable, str(PRUEFER), entwurf.name],
            cwd=tmp, capture_output=True, text=True,
        )
    ausgabe = [z for z in lauf.stdout.rstrip().splitlines()]
    while ausgabe and not ausgabe[0].strip():
        ausgabe.pop(0)
    if not ausgabe:
        print("Der Prüfer meldete nichts. Demotext prüfen.", file=sys.stderr)
        return 2

    normal, fett = schrift(GROESSE, False), schrift(GROESSE, True)
    zeilen: list[tuple[str, tuple | None, object]] = [("$ cat entwurf.md", PROMPT, fett)]
    zeilen += [(z, TEXT, normal) for z in DEMO.rstrip().splitlines()]
    zeilen += [("", TEXT, normal), ("$ python3 scripts/klartext.py entwurf.md", PROMPT, fett)]
    for i, z in enumerate(ausgabe):
        if i == 0:
            zeilen.append((z, GEDIMMT, normal))
        elif not z.strip():
            zeilen.append(("", TEXT, normal))
        elif z.startswith(" "):
            zeilen.append(("FUND:" + z, None, normal))
        else:
            zeilen.append((z, WEISS, fett))

    hoehe = RAND * 2 + ZH * len(zeilen) + 54
    bild = Image.new("RGB", (BREITE, hoehe), HG)
    d = ImageDraw.Draw(bild)
    y = RAND
    for text, farbe, font in zeilen:
        if farbe is None:
            roh, x = text[5:], RAND
            teile = [
                (roh[:7], normal, GEDIMMT),
                (roh[7:14], fett, HART if "hart" in roh[7:14] else WEICH),
                (roh[14:48], normal, ID),
                (roh[48:], normal, TEXT),
            ]
            for stueck, f, c in teile:
                d.text((x, y), stueck, font=f, fill=c)
                x += d.textlength(stueck, font=normal)
        else:
            d.text((RAND, y), text, font=font, fill=farbe)
        y += ZH
    d.text((RAND, hoehe - RAND - 6), "github.com/lord-helicon/daitsch", font=schrift(17, False), fill=GEDIMMT)

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    bild.save(ZIEL)
    funde = [z for z in ausgabe if z.startswith(" ")]
    print(f"{ZIEL.relative_to(WURZEL)}  {bild.size[0]}x{bild.size[1]}  {len(funde)} Funde")
    return 0


if __name__ == "__main__":
    sys.exit(main())
