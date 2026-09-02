#!/usr/bin/env python3
"""Prüft deutsche Texte auf KI-Floskeln.

Die Regeln stehen in references/katalog.md und werden beim Start gelesen.
Das Skript ändert nie eine geprüfte Datei; es meldet nur.

    python3 scripts/klartext.py text.md
    python3 scripts/klartext.py text.md --json
    python3 scripts/klartext.py --haerte hart *.md
    python3 scripts/klartext.py --regeln
    python3 scripts/klartext.py --selbsttest
    cat text.txt | python3 scripts/klartext.py -
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
KATALOG_STANDARD = WURZEL / "references" / "katalog.md"

# Der Prüfer gilt für Fließtext. In Quelltext sind gerade Anführungszeichen und
# Pfeile richtig, dort meldet er sonst nur Rauschen.
FLIESSTEXT = {".md", ".markdown", ".mdx", ".txt", ".text", ".rst", ".adoc", ""}


# ---------------------------------------------------------------- Datenmodell


@dataclass
class Regel:
    muster: str
    haerte: str = "weich"
    erkennung: str = ""
    zulaessig: str = ""
    floskel: str = ""
    klartext: str = ""
    metrik: str = ""
    quellen: list[str] = field(default_factory=list)
    ausdruecke: list[re.Pattern] = field(default_factory=list)

    @property
    def art(self) -> str:
        if self.ausdruecke:
            return "ausdruck"
        if self.metrik:
            return "metrik"
        return "lesen"


@dataclass
class Fund:
    muster: str
    haerte: str
    zeile: int
    spalte: int
    fundstelle: str
    erkennung: str


# ------------------------------------------------------------- Katalog lesen


FELD = re.compile(r"^\*\*(Erkennung|Härte|Metrik|Floskel|Klartext|Zulässig):\*\*\s*(.*)$", re.MULTILINE)
BLOCK = re.compile(r"^```(\w+)[ \t]*\n(.*?)\n```", re.MULTILINE | re.DOTALL)


def wortliste_zu_ausdruck(zeilen: list[str]) -> str:
    teile = []
    for zeile in zeilen:
        woerter = zeile.split()
        if not woerter:
            continue
        stuecke = []
        for wort in woerter:
            if wort.endswith("*"):
                stuecke.append(re.escape(wort[:-1]) + r"\w*")
            else:
                stuecke.append(re.escape(wort))
        teile.append(r"\b" + r"\s+".join(stuecke) + r"\b")
    teile.sort(key=len, reverse=True)
    return "(?i)(?:" + "|".join(teile) + ")"


def katalog_lesen(pfad: Path) -> list[Regel]:
    text = pfad.read_text(encoding="utf-8")
    stuecke = re.split(r"^### +(.+?)\s*$", text, flags=re.MULTILINE)
    regeln: list[Regel] = []

    for i in range(1, len(stuecke), 2):
        muster = stuecke[i].strip()
        rumpf = stuecke[i + 1]
        regel = Regel(muster=muster)

        bloecke: dict[str, list[str]] = {}
        for treffer in BLOCK.finditer(rumpf):
            bloecke.setdefault(treffer.group(1), []).append(treffer.group(2))

        ohne_bloecke = BLOCK.sub("", rumpf)
        for feld, wert in FELD.findall(ohne_bloecke):
            wert = wert.strip()
            if feld == "Erkennung":
                regel.erkennung = wert
            elif feld == "Härte":
                regel.haerte = wert.lower()
            elif feld == "Metrik":
                regel.metrik = wert
            elif feld == "Floskel":
                regel.floskel = wert
            elif feld == "Klartext":
                regel.klartext = wert
            elif feld == "Zulässig":
                regel.zulaessig = wert

        if "floskel" in bloecke:
            regel.floskel = bloecke["floskel"][0]
        if "klartext" in bloecke:
            regel.klartext = bloecke["klartext"][0]

        for roh in bloecke.get("regex", []):
            regel.quellen.append(roh.strip())
        for roh in bloecke.get("wortliste", []):
            regel.quellen.append(wortliste_zu_ausdruck(roh.splitlines()))

        for quelle in regel.quellen:
            try:
                regel.ausdruecke.append(re.compile(quelle, re.MULTILINE))
            except re.error as fehler:
                raise SystemExit(f"Katalogfehler in {muster}: {fehler}\n  {quelle}")

        if regel.haerte not in ("hart", "weich"):
            raise SystemExit(f"Katalogfehler in {muster}: Härte ist {regel.haerte!r}")

        regeln.append(regel)

    if not regeln:
        raise SystemExit(f"Keine Regeln in {pfad} gefunden.")
    return regeln


# ------------------------------------------------------------------ Maskieren


FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
CODEBLOCK = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINECODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://\S+")
LINKZIEL = re.compile(r"\]\([^)]*\)")


def maskieren(text: str) -> str:
    zeichen = list(text)

    def leeren(anfang: int, ende: int) -> None:
        for i in range(anfang, ende):
            if zeichen[i] != "\n":
                zeichen[i] = " "

    for ausdruck in (FRONTMATTER, CODEBLOCK, INLINECODE, URL, LINKZIEL):
        for treffer in ausdruck.finditer(text):
            leeren(treffer.start(), treffer.end())

    return "".join(zeichen)


# -------------------------------------------------------------------- Metriken


UEBERGAENGE = (
    "Zudem", "Darüber hinaus", "Außerdem", "Gleichzeitig", "Dabei",
    "In diesem Zusammenhang", "Vor diesem Hintergrund", "Nicht zuletzt",
    "Ferner", "Zugleich", "Insofern", "Somit", "Folglich", "Des Weiteren",
)
DEMONSTRATIVE = ("Dies", "Dabei", "Dadurch", "Damit", "Auf diese Weise", "So wird", "So entsteht")
METAPHERN = re.compile(
    r"(?i)\b(?:Reise|Etappe|Kompass|Wegweiser|Fundament|Baustein|Säule|Architektur|"
    r"Navigation|Horizont|Terrain|Landschaft|Leuchtturm|Anker)\w*\b"
)
KONDITIONAL = re.compile(r"(?i)^(?:Sollten?|Falls|Sofern|Wenn|Für den Fall)\b")
FETT = re.compile(r"\*\*[^*\n]+\*\*")
DREIERGRUPPE = re.compile(r"\b[\wäöüß]{3,},\s+[\wäöüß]{3,}\s+und\s+[\wäöüß]{3,}\b")


LISTENZEILE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


def _ist_liste(block: str) -> bool:
    """Eine Aufzählung ist zu Recht gleichförmig und zählt nicht als Absatz."""
    zeilen = [z for z in block.splitlines() if z.strip()]
    if not zeilen:
        return False
    return sum(bool(LISTENZEILE.match(z)) for z in zeilen) * 2 >= len(zeilen)


def absaetze_von(text: str) -> list[tuple[int, str]]:
    """Absätze als (Zeilennummer, Text). Überschriften, Tabellen und Listen bleiben draußen."""
    ergebnis = []
    zeile = 1
    for block in re.split(r"\n\s*\n", text):
        inhalt = block.strip()
        if inhalt and not inhalt.startswith("#") and not inhalt.startswith("|") and not _ist_liste(inhalt):
            versatz = block.index(inhalt.split("\n")[0])
            ergebnis.append((zeile + block[:versatz].count("\n"), inhalt))
        zeile += block.count("\n") + 2
    return ergebnis


def saetze_von(text: str) -> list[str]:
    roh = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in roh if s.strip()]


def woerter_von(text: str) -> list[str]:
    return re.findall(r"[\wäöüßÄÖÜ]+", text)


def _je_tausend(anzahl: int, woerter: int) -> float:
    return anzahl * 1000 / max(woerter, 1)


def metrik_uebergangsdichte(text, absaetze, saetze, woerter):
    if len(absaetze) < 4:
        return None
    treffer = [(z, a) for z, a in absaetze if a.lstrip().startswith(UEBERGAENGE)]
    anteil = len(treffer) / len(absaetze)
    if anteil > 0.30:
        return treffer[0][0], f"{len(treffer)} von {len(absaetze)} Absätzen beginnen mit einem Übergangswort (Schwelle 30 Prozent)"
    return None


def metrik_demonstrativkette(text, absaetze, saetze, woerter):
    lauf = 0
    beginn = ""
    for satz in saetze:
        if satz.startswith(DEMONSTRATIVE):
            if lauf == 0:
                beginn = satz
            lauf += 1
            if lauf >= 3:
                return _zeile_von(text, beginn), f"{lauf} Sätze in Folge beginnen mit Dies, Dabei, Dadurch oder Damit (Schwelle 3)"
        else:
            lauf = 0
    return None


def metrik_dreiergruppen(text, absaetze, saetze, woerter):
    treffer = DREIERGRUPPE.findall(text)
    dichte = _je_tausend(len(treffer), len(woerter))
    if len(treffer) >= 3 and dichte > 4:
        return 0, f"{len(treffer)} Dreiergruppen, {dichte:.1f} je 1000 Wörter (Schwelle 4)"
    return None


def metrik_gedankenstrich_dichte(text, absaetze, saetze, woerter):
    anzahl = text.count("–")
    dichte = _je_tausend(anzahl, len(woerter))
    if anzahl >= 3 and dichte > 3:
        return 0, f"{anzahl} Halbgeviertstriche, {dichte:.1f} je 1000 Wörter (Schwelle 3)"
    return None


def metrik_fettdruck_dichte(text, absaetze, saetze, woerter):
    betroffen = [(z, a) for z, a in absaetze if len(FETT.findall(a)) >= 2]
    if len(betroffen) >= 2:
        return betroffen[0][0], f"{len(betroffen)} Absätze mit zwei oder mehr fetten Stellen (Schwelle 2)"
    return None


def metrik_kurzabsatz_anteil(text, absaetze, saetze, woerter):
    if len(absaetze) < 5:
        return None
    kurz = [(z, a) for z, a in absaetze if len(woerter_von(a)) < 8]
    anteil = len(kurz) / len(absaetze)
    if anteil > 0.40:
        return kurz[0][0], f"{len(kurz)} von {len(absaetze)} Absätzen sind kürzer als acht Wörter (Schwelle 40 Prozent)"
    return None


def metrik_flughoehe(text, absaetze, saetze, woerter):
    laengen = [len(woerter_von(a)) for _, a in absaetze]
    if len(laengen) < 5 or statistics.mean(laengen) < 15:
        return None
    streuung = statistics.pstdev(laengen) / statistics.mean(laengen)
    if streuung < 0.25:
        return absaetze[0][0], f"Alle Absätze sind fast gleich lang, Streuung {streuung:.2f} (Schwelle 0.25)"
    return None


def metrik_anapher(text, absaetze, saetze, woerter):
    lauf = 1
    vorher = ""
    for satz in saetze:
        anfang = " ".join(satz.lower().split()[:2])
        if anfang and anfang == vorher:
            lauf += 1
            if lauf >= 3:
                return _zeile_von(text, satz), f"{lauf} Sätze in Folge beginnen mit {anfang!r} (Schwelle 3)"
        else:
            lauf = 1
        vorher = anfang
    return None


def metrik_metapherndichte(text, absaetze, saetze, woerter):
    treffer = METAPHERN.findall(text)
    dichte = _je_tausend(len(treffer), len(woerter))
    if len(treffer) >= 4 and dichte > 6:
        return 0, f"{len(treffer)} Bildwörter derselben Welt, {dichte:.1f} je 1000 Wörter (Schwelle 6)"
    return None


def metrik_konditional_haeufung(text, absaetze, saetze, woerter):
    for zeile, absatz in absaetze:
        treffer = [s for s in saetze_von(absatz) if KONDITIONAL.match(s)]
        if len(treffer) >= 3:
            return zeile, f"{len(treffer)} Konditionalsätze in einem Absatz (Schwelle 3)"
    return None


def metrik_doppelung(text, absaetze, saetze, woerter):
    normal = []
    for zeile, absatz in absaetze:
        kern = re.sub(r"[^\wäöüß ]", "", absatz.lower())
        kern = " ".join(kern.split())
        if len(kern) >= 40:
            normal.append((zeile, kern))
    for i in range(len(normal)):
        for j in range(i + 1, len(normal)):
            aehnlich = difflib.SequenceMatcher(None, normal[i][1], normal[j][1]).ratio()
            if aehnlich > 0.90:
                return normal[j][0], f"Absatz in Zeile {normal[j][0]} wiederholt Zeile {normal[i][0]} zu {aehnlich * 100:.0f} Prozent"
    return None


METRIKEN = {
    "uebergangsdichte": metrik_uebergangsdichte,
    "demonstrativkette": metrik_demonstrativkette,
    "dreiergruppen": metrik_dreiergruppen,
    "gedankenstrich_dichte": metrik_gedankenstrich_dichte,
    "fettdruck_dichte": metrik_fettdruck_dichte,
    "kurzabsatz_anteil": metrik_kurzabsatz_anteil,
    "flughoehe": metrik_flughoehe,
    "anapher": metrik_anapher,
    "metapherndichte": metrik_metapherndichte,
    "konditional_haeufung": metrik_konditional_haeufung,
    "doppelung": metrik_doppelung,
}


def _zeile_von(text: str, stueck: str) -> int:
    stelle = text.find(stueck[:60])
    return text.count("\n", 0, stelle) + 1 if stelle >= 0 else 0


# --------------------------------------------------------------------- Prüfen


def pruefen(text: str, regeln: list[Regel], nur_ausdruecke: bool = False) -> list[Fund]:
    maskiert = maskieren(text)
    funde: list[Fund] = []
    gesehen: set[tuple[str, int]] = set()

    for regel in regeln:
        for ausdruck in regel.ausdruecke:
            for treffer in ausdruck.finditer(maskiert):
                if treffer.start() in [s for m, s in gesehen if m == regel.muster]:
                    continue
                gesehen.add((regel.muster, treffer.start()))
                zeile = maskiert.count("\n", 0, treffer.start()) + 1
                spalte = treffer.start() - (maskiert.rfind("\n", 0, treffer.start()) + 1) + 1
                roh = text[treffer.start():treffer.end()]
                fundstelle = " ".join(roh.split())[:70]
                funde.append(Fund(regel.muster, regel.haerte, zeile, spalte, fundstelle, regel.erkennung))

    if not nur_ausdruecke:
        absaetze = absaetze_von(maskiert)
        saetze = saetze_von(maskiert)
        woerter = woerter_von(maskiert)
        for regel in regeln:
            if not regel.metrik:
                continue
            funktion = METRIKEN.get(regel.metrik)
            if funktion is None:
                raise SystemExit(f"Katalogfehler in {regel.muster}: Metrik {regel.metrik!r} kennt das Skript nicht.")
            ergebnis = funktion(maskiert, absaetze, saetze, woerter)
            if ergebnis:
                zeile, beschreibung = ergebnis
                funde.append(Fund(regel.muster, regel.haerte, zeile, 1, beschreibung, regel.erkennung))

    funde.sort(key=lambda f: (f.zeile, f.spalte, f.muster))
    return funde


def filtern(funde: list[Fund], haerte: str) -> list[Fund]:
    if haerte == "alle":
        return funde
    return [f for f in funde if f.haerte == haerte]


# -------------------------------------------------------------------- Ausgabe


def ausgeben_text(ergebnisse: list[tuple[str, list[Fund]]]) -> None:
    hart = weich = 0
    for name, funde in ergebnisse:
        if not funde:
            continue
        print(f"\n{name}")
        for fund in funde:
            hart += fund.haerte == "hart"
            weich += fund.haerte == "weich"
            ort = f"{fund.zeile}" if fund.zeile else "-"
            print(f"  {ort:>5}  {fund.haerte:<5}  {fund.muster:<32}  {fund.fundstelle}")

    if hart or weich:
        print(f"\n{hart} harte, {weich} weiche Funde. Erklärungen in references/katalog.md.")
    else:
        print("Keine Funde.")


def ausgeben_json(ergebnisse: list[tuple[str, list[Fund]]]) -> None:
    daten = {
        "dateien": [
            {
                "datei": name,
                "funde": [
                    {
                        "muster": f.muster,
                        "haerte": f.haerte,
                        "zeile": f.zeile,
                        "spalte": f.spalte,
                        "fundstelle": f.fundstelle,
                        "erkennung": f.erkennung,
                    }
                    for f in funde
                ],
            }
            for name, funde in ergebnisse
        ],
    }
    daten["zusammenfassung"] = {
        "hart": sum(1 for _, fs in ergebnisse for f in fs if f.haerte == "hart"),
        "weich": sum(1 for _, fs in ergebnisse for f in fs if f.haerte == "weich"),
    }
    print(json.dumps(daten, ensure_ascii=False, indent=2))


def ausgeben_regeln(regeln: list[Regel]) -> None:
    print(f"{len(regeln)} Muster in {KATALOG_STANDARD.name}\n")
    for regel in sorted(regeln, key=lambda r: (r.haerte, r.muster)):
        print(f"  {regel.haerte:<5}  {regel.art:<8}  {regel.muster:<32}  {regel.erkennung[:70]}")


# ----------------------------------------------------------------- Selbsttest


def selbsttest(regeln: list[Regel]) -> int:
    fehler: list[str] = []

    if len(regeln) < 60:
        fehler.append(f"Nur {len(regeln)} Regeln geparst, erwartet mindestens 60.")

    ohne_beispiel = [r.muster for r in regeln if not r.floskel or not r.klartext]
    if ohne_beispiel:
        fehler.append("Ohne Floskel- oder Klartext-Beispiel: " + ", ".join(ohne_beispiel))

    for regel in regeln:
        if not regel.ausdruecke:
            continue
        if not any(a.search(regel.floskel) for a in regel.ausdruecke):
            fehler.append(f"{regel.muster}: findet das eigene Floskel-Beispiel nicht.")

    for regel in regeln:
        if not regel.klartext:
            continue
        treffer = filtern(pruefen(regel.klartext, regeln, nur_ausdruecke=True), "hart")
        if treffer:
            namen = ", ".join(sorted({f.muster for f in treffer}))
            fehler.append(f"{regel.muster}: Klartext-Beispiel löst harte Funde aus ({namen}).")

    schlecht = WURZEL / "tests" / "floskelig.md"
    gut = WURZEL / "tests" / "klartext.md"
    getroffen: set[str] = set()

    if schlecht.exists():
        funde = pruefen(schlecht.read_text(encoding="utf-8"), regeln)
        muster = {f.muster for f in funde}
        getroffen |= muster
        if len(muster) < 25:
            fehler.append(f"tests/floskelig.md löst nur {len(muster)} Muster aus, erwartet mindestens 25.")
        if not any(f.haerte == "weich" for f in funde):
            fehler.append("tests/floskelig.md löst keinen weichen Fund aus.")
    else:
        fehler.append("tests/floskelig.md fehlt.")

    for datei in sorted((WURZEL / "tests" / "metriken").glob("*.md")):
        getroffen |= {f.muster for f in pruefen(datei.read_text(encoding="utf-8"), regeln)}

    unerprobt = sorted(r.muster for r in regeln if r.metrik and r.muster not in getroffen)
    if unerprobt:
        fehler.append("Metriken, die kein Testtext auslöst: " + ", ".join(unerprobt))

    if gut.exists():
        funde = pruefen(gut.read_text(encoding="utf-8"), regeln)
        if funde:
            zeilen = ", ".join(f"{f.muster} (Zeile {f.zeile})" for f in funde)
            fehler.append(f"tests/klartext.md ist nicht sauber: {zeilen}")
    else:
        fehler.append("tests/klartext.md fehlt.")

    if fehler:
        print("Selbsttest fehlgeschlagen:\n")
        for eintrag in fehler:
            print(f"  - {eintrag}")
        return 2

    mit_ausdruck = sum(1 for r in regeln if r.ausdruecke)
    mit_metrik = sum(1 for r in regeln if r.metrik)
    print(
        f"Selbsttest bestanden: {len(regeln)} Muster, davon {mit_ausdruck} mit Ausdruck "
        f"und {mit_metrik} mit Metrik. Beide Testtexte verhalten sich wie erwartet."
    )
    return 0


# ---------------------------------------------------------------------- Start


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="klartext",
        description="Prüft deutsche Texte auf KI-Floskeln. Ändert nichts.",
    )
    parser.add_argument("dateien", nargs="*", help="Dateien, oder - für stdin")
    parser.add_argument("--json", action="store_true", help="maschinenlesbare Ausgabe")
    parser.add_argument("--haerte", choices=("hart", "weich", "alle"), default="alle")
    parser.add_argument("--regeln", action="store_true", help="alle Muster auflisten")
    parser.add_argument("--selbsttest", action="store_true", help="Katalog und Testtexte prüfen")
    parser.add_argument("--erzwingen", action="store_true", help="auch Dateien prüfen, die nach Quelltext aussehen")
    parser.add_argument("--katalog", type=Path, default=None, help="anderer Musterkatalog")
    args = parser.parse_args(argv)

    pfad = args.katalog or Path(os.environ.get("KLARTEXT_KATALOG", KATALOG_STANDARD))
    if not pfad.exists():
        print(f"Musterkatalog nicht gefunden: {pfad}", file=sys.stderr)
        return 2
    regeln = katalog_lesen(pfad)

    if args.regeln:
        ausgeben_regeln(regeln)
        return 0

    if args.selbsttest:
        return selbsttest(regeln)

    if not args.dateien:
        parser.print_help()
        return 2

    ergebnisse: list[tuple[str, list[Fund]]] = []
    for name in args.dateien:
        if name == "-":
            text, anzeige = sys.stdin.read(), "stdin"
        else:
            datei = Path(name)
            if not datei.exists():
                print(f"Datei nicht gefunden: {name}", file=sys.stderr)
                return 2
            if datei.suffix.lower() not in FLIESSTEXT and not args.erzwingen:
                print(f"Übersprungen, sieht nach Quelltext aus: {name} (mit --erzwingen trotzdem prüfen)", file=sys.stderr)
                continue
            text, anzeige = datei.read_text(encoding="utf-8"), name
        ergebnisse.append((anzeige, filtern(pruefen(text, regeln), args.haerte)))

    if args.json:
        ausgeben_json(ergebnisse)
    else:
        ausgeben_text(ergebnisse)

    return 1 if any(funde for _, funde in ergebnisse) else 0


if __name__ == "__main__":
    sys.exit(main())
