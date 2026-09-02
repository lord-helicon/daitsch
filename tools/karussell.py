#!/usr/bin/env python3
"""Erzeugt aus dem Musterkatalog ein PDF-Karussell für LinkedIn.

Die Folien entstehen aus references/katalog.md, damit sie nie etwas anderes
behaupten können als der Katalog selbst.

    python3 tools/karussell.py
    python3 tools/karussell.py --muster sauber,nutzenwoerter --ziel raus.pdf
    python3 tools/karussell.py --liste

Braucht Pillow. Alles andere ist Standardbibliothek.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow fehlt. Installieren mit: python3 -m pip install Pillow")

WURZEL = Path(__file__).resolve().parent.parent
KATALOG = WURZEL / "skills" / "daitsch" / "references" / "katalog.md"

BREITE, HOEHE = 1080, 1350
RAND = 96
PAPIER = (250, 249, 246)
DUNKEL = (26, 26, 28)
GRAU = (132, 132, 138)
ROT = (170, 62, 52)
LINIE = (218, 216, 210)

SCHRIFTEN = [
    ("/System/Library/Fonts/Supplemental/Georgia.ttf", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"),
    ("/System/Library/Fonts/NewYork.ttf", "/System/Library/Fonts/NewYork.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
]

STANDARD = [
    "negativ-parallelismus",
    "nutzenwoerter",
    "sauber",
    "vage-zuschreibung",
    "lehrerrolle",
    "hohler-schluss",
]


def schriftpaar() -> tuple[str, str]:
    for normal, fett in SCHRIFTEN:
        if Path(normal).exists() and Path(fett).exists():
            return normal, fett
    raise SystemExit("Keine geeignete Schrift gefunden. Mit --schrift einen Pfad angeben.")


def katalog_lesen() -> dict[str, dict[str, str]]:
    text = KATALOG.read_text(encoding="utf-8")
    stuecke = re.split(r"^### +(.+?)\s*$", text, flags=re.MULTILINE)
    eintraege: dict[str, dict[str, str]] = {}
    for i in range(1, len(stuecke), 2):
        rumpf = stuecke[i + 1]
        felder = dict(re.findall(r"^\*\*(Floskel|Klartext|Zulässig|Erkennung):\*\* (.+)$", rumpf, re.MULTILINE))
        if felder.get("Floskel") and felder.get("Klartext"):
            eintraege[stuecke[i].strip()] = felder
    return eintraege


def umbrechen(d, text: str, font, maxbreite: int) -> list[str]:
    zeilen, aktuell = [], ""
    for wort in text.split():
        versuch = f"{aktuell} {wort}".strip()
        if d.textlength(versuch, font=font) <= maxbreite:
            aktuell = versuch
        else:
            if aktuell:
                zeilen.append(aktuell)
            aktuell = wort
    if aktuell:
        zeilen.append(aktuell)
    return zeilen


def setzen(d, text: str, pfad: str, groesse: int, maxhoehe: int):
    """Bricht Text um und verkleinert ihn, bis er in maxhoehe passt."""
    while True:
        font = ImageFont.truetype(pfad, groesse)
        zeilen = umbrechen(d, text, font, BREITE - 2 * RAND)
        zh = int(groesse * 1.34)
        if len(zeilen) * zh <= maxhoehe or groesse <= 26:
            return font, zeilen, zh, len(zeilen) * zh
        groesse -= 3


def zeichnen_block(d, zeilen, font, zh: int, y: int, farbe) -> int:
    for zeile in zeilen:
        d.text((RAND, y), zeile, font=font, fill=farbe)
        y += zh
    return y


def block(d, text: str, pfad: str, y: int, groesse: int, farbe, maxhoehe: int) -> int:
    font, zeilen, zh, _ = setzen(d, text, pfad, groesse, maxhoehe)
    return zeichnen_block(d, zeilen, font, zh, y, farbe)


def seite(zeichnen) -> Image.Image:
    bild = Image.new("RGB", (BREITE, HOEHE), PAPIER)
    zeichnen(ImageDraw.Draw(bild))
    return bild


def bauen(muster: list[str], ziel: Path, normal: str, fett: str) -> None:
    eintraege = katalog_lesen()
    fehlend = [m for m in muster if m not in eintraege]
    if fehlend:
        raise SystemExit("Nicht im Katalog: " + ", ".join(fehlend))

    seiten: list[Image.Image] = []

    def titel(d):
        d.text((RAND, 300), "Mein Werkzeug gegen", font=ImageFont.truetype(normal, 62), fill=GRAU)
        d.text((RAND, 380), "KI-Floskeln hat als", font=ImageFont.truetype(normal, 62), fill=GRAU)
        d.text((RAND, 460), "Erstes meinen", font=ImageFont.truetype(fett, 66), fill=DUNKEL)
        d.text((RAND, 542), "eigenen Text", font=ImageFont.truetype(fett, 66), fill=DUNKEL)
        d.text((RAND, 624), "verrissen.", font=ImageFont.truetype(fett, 66), fill=DUNKEL)
        d.line([(RAND, 760), (BREITE - RAND, 760)], fill=LINIE, width=2)
        d.text((RAND, 800), "74 deutsche Muster, jedes mit", font=ImageFont.truetype(normal, 38), fill=GRAU)
        d.text((RAND, 852), "brauchbarer Gegenfassung.", font=ImageFont.truetype(normal, 38), fill=GRAU)
    seiten.append(seite(titel))

    for nummer, name in enumerate(muster, start=1):
        eintrag = eintraege[name]

        def musterseite(d, eintrag=eintrag, name=name, nummer=nummer):
            etikett = ImageFont.truetype(fett, 30)
            f_font, f_zeilen, f_zh, f_hoehe = setzen(d, eintrag["Floskel"], normal, 56, 340)
            k_font, k_zeilen, k_zh, k_hoehe = setzen(d, eintrag["Klartext"], fett, 56, 460)
            # Etikett 68, Trennlinie 142, Etikett 68 zwischen den Blöcken
            gesamt = 68 + f_hoehe + 142 + 68 + k_hoehe
            y = int((HOEHE - gesamt) / 2 - 40)   # etwas über der Mitte wirkt ruhiger

            d.text((RAND, y), "FLOSKEL", font=etikett, fill=ROT)
            y = zeichnen_block(d, f_zeilen, f_font, f_zh, y + 68, GRAU)
            d.line([(RAND, y + 46), (BREITE - RAND, y + 46)], fill=LINIE, width=2)
            d.text((RAND, y + 96), "KLARTEXT", font=etikett, fill=DUNKEL)
            zeichnen_block(d, k_zeilen, k_font, k_zh, y + 164, DUNKEL)
            d.text((RAND, HOEHE - RAND - 30), name, font=ImageFont.truetype(normal, 26), fill=LINIE)
            d.text((BREITE - RAND - 60, HOEHE - RAND - 30), f"{nummer}/{len(muster)}",
                   font=ImageFont.truetype(normal, 26), fill=LINIE)
        seiten.append(seite(musterseite))

    def ausnahmen(d):
        d.text((RAND, 300), "UND JETZT DAS WICHTIGE", font=ImageFont.truetype(fett, 30), fill=ROT)
        y = block(d, "Fast jedes dieser Muster ist irgendwo richtig.", fett, 376, 58, DUNKEL, 260)
        y = block(d, "Der Halbgeviertstrich ist korrektes Deutsch. Ein Fazit gehört ins Gutachten. "
                     "Es bleibt abzuwarten steht zu Recht in juristischen Texten.",
                  normal, y + 50, 42, GRAU, 420)
        block(d, "Deshalb steht in jedem Katalogeintrag auch, wann das Muster bleiben darf. "
                 "Ohne das streicht ein Agent stur nach Liste, und der Text ist hinterher "
                 "glatter als vorher.", normal, y + 50, 42, DUNKEL, 420)
    seiten.append(seite(ausnahmen))

    def schluss(d):
        d.text((RAND, 420), "Katalog, Prüfskript", font=ImageFont.truetype(fett, 60), fill=DUNKEL)
        d.text((RAND, 500), "und Skill:", font=ImageFont.truetype(fett, 60), fill=DUNKEL)
        d.text((RAND, 620), "github.com/lord-helicon/daitsch", font=ImageFont.truetype(normal, 40), fill=ROT)
        d.line([(RAND, 720), (BREITE - RAND, 720)], fill=LINIE, width=2)
        d.text((RAND, 760), "Mustersammlung von Tobias Voßberg", font=ImageFont.truetype(normal, 32), fill=GRAU)
        d.text((RAND, 806), "(iplaw.lol), verwendet mit seiner Zustimmung.", font=ImageFont.truetype(normal, 32), fill=GRAU)
    seiten.append(seite(schluss))

    seiten[0].save(ziel, save_all=True, append_images=seiten[1:], resolution=144.0)
    print(f"{ziel}  {len(seiten)} Seiten  {BREITE}x{HOEHE}")


def main() -> int:
    p = argparse.ArgumentParser(description="Baut ein PDF-Karussell aus dem Musterkatalog.")
    p.add_argument("--muster", default=",".join(STANDARD), help="Muster-IDs, mit Komma getrennt")
    p.add_argument("--ziel", type=Path, default=WURZEL / "karussell.pdf")
    p.add_argument("--schrift", nargs=2, metavar=("NORMAL", "FETT"))
    p.add_argument("--liste", action="store_true", help="alle Muster mit Beispielpaar auflisten")
    a = p.parse_args()

    if a.liste:
        for name, e in katalog_lesen().items():
            print(f"{name}\n   {e['Floskel']}\n   {e['Klartext']}\n")
        return 0

    normal, fett = tuple(a.schrift) if a.schrift else schriftpaar()
    bauen([m.strip() for m in a.muster.split(",") if m.strip()], a.ziel, normal, fett)
    return 0


if __name__ == "__main__":
    sys.exit(main())
