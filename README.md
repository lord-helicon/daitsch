# dAItsch

Ein Skill für KI-Agenten, der deutsche Texte davon abhält, nach KI zu klingen. Herstellerneutral: eine Quelle, daraus Adapterdateien für die verbreiteten Agentenformate.

Die Musterlisten beruhen auf „KI-Sprachmuster im Deutschen vermeiden“ von **Tobias Voßberg**, [www.iplaw.lol/ki-floskeln](https://www.iplaw.lol/ki-floskeln/), verwendet mit seiner Zustimmung. Seine Sammlung geht ihrerseits auf [tropes.fyi](https://tropes.fyi/) von Ossama zurück, ins Deutsche übertragen und um deutsche Muster ergänzt.

Hinzugekommen sind hier die Klartext-Fassungen, die Angaben dazu, wann ein Muster zulässig ist, die maschinenlesbaren Erkennungsregeln und der Prüfer.

![Ein Lauf des Prüfers auf einem Absatz voller Floskeln](https://raw.githubusercontent.com/lord-helicon/daitsch/main/docs/daitsch-terminal.png)

**Nur die Liste lesen?** Die 74 Muster stehen mit Beispiel, Gegenfassung und Ausnahmen in [references/katalog.md](skills/daitsch/references/katalog.md). Dafür ist nichts zu installieren.

## In English

German text written by an LLM is recognizable by a set of recurring patterns, and the German ones differ from the English ones. This repository catalogues 74 of them and ships a checker that finds them by line number.

What makes it more than a banlist: every entry carries three things, the phrase to avoid, a plain-language replacement, and **the cases where the pattern is correct**. A dash is proper German typography, a section called Fazit belongs in a legal opinion, and hedged endings are right in a court filing. An agent that deletes by list alone leaves the text smoother and emptier than it found it, so the exceptions took more work than the patterns.

Everything is in German, because the patterns are. If you write German with an LLM, this is for you.

It installs as a Claude Code plugin, as a skill folder for Codex, Cursor, Gemini CLI and others, or as a plain instruction block for any system prompt. The checker needs Python and nothing else.

The pattern collection comes from [Tobias Voßberg](https://www.iplaw.lol/ki-floskeln/), used with his permission, and goes back to [tropes.fyi](https://tropes.fyi/) by Ossama, which does the same job for English.

## Zum Namen

Die pfälzische Wikipedia beginnt ihren Artikel über die deutsche Sprache mit den Worten: „Die Daitsch Sprooch (kerz: Daitsch) is e germanische Sprooch.“<sup>[1]</sup>

Aus diesem Daitsch und dem AI in der Mitte wird dAItsch.

<sup>[1]</sup> [Deutsche Sprache](https://pfl.wikipedia.org/wiki/Deutsche_Sprache), Pälzische Wikipedia, CC BY-SA 4.0.

## Was der Skill tut

Er kennt drei Modi. Beim Schreiben hält er die Muster von vornherein aus dem Text. Beim Prüfen meldet er Fundstellen mit Muster-ID, ohne die Datei anzufassen. Beim Überarbeiten schreibt er um und berichtet am Ende, was er bewusst stehen ließ.

Die Vorlage ist eine Verbotsliste. Verbote allein steuern Sprachmodelle schlecht, deshalb steht in jedem Katalogeintrag die Floskel und die brauchbare Fassung nebeneinander, dazu die Fälle, in denen das Muster richtig ist. Der Halbgeviertstrich ist korrektes Deutsch, „Fazit“ gehört ins Gutachten, „es bleibt abzuwarten“ steht zu Recht im juristischen Text. Ohne diese Ausnahmen überkorrigiert ein Agent und macht Texte schlechter als die Floskeln, die er beseitigt.

## Aufruf

In Claude Code und überall sonst, wo Skills als `SKILL.md` gelesen werden:

```
/daitsch prüfe entwurf.md
/daitsch überarbeite den Text und sag mir, was du stehen lässt
```

Ohne Aufruf greift der Skill selbst, sobald die Beschreibung passt: bei deutschen Texten und wenn jemand sagt, etwas klinge nach KI. Bei den Adapterdateien gibt es keinen Aufruf. `AGENTS.md`, `CLAUDE.md` und `GEMINI.md` gelten immer, sobald sie im Projekt liegen; die Cursor-Regel hängt sich an Markdown- und Textdateien.

## Installation

Wo der Agent auf deinem Rechner läuft, liest er den Skill aus einem Ordner. Wo er in der Cloud läuft, braucht er eine Datei. Deshalb je Ziel ein eigener Weg.

### Claude Code

```
/plugin marketplace add lord-helicon/daitsch
/plugin install daitsch@daitsch
```

`daitsch@daitsch` ist kein Tippfehler. Vor dem Klammeraffen steht das Plugin, dahinter der Marktplatz, und beide heißen hier gleich.

Aktualisieren später mit `/plugin update daitsch`. Wenn etwas klemmt, steht der Fall unter [Wenn es nicht klappt](#wenn-es-nicht-klappt).

### Cowork

`dist/daitsch.plugin` in den Chat ziehen und annehmen. Die Datei entsteht mit `python3 tools/paket.py`, oder sie liegt fertig am [neuesten Release](https://github.com/lord-helicon/daitsch/releases/latest).

Geprüft mit 1.2.1: Cowork führt auch das Prüfskript aus, der Befund kommt dort mit Zeilennummern.

### Claude im Browser und in der App

`dist/daitsch-skill.zip` in den Einstellungen unter Skills hochladen. Der Chat läuft auf fremden Rechnern und kann keinen Ordner auf deinem Gerät lesen, deshalb der Umweg über die Datei.

### Codex, Cursor, Copilot, Gemini CLI und weitere

Diesen Satz in den Agenten einfügen:

```text
Installiere den Skill daitsch global von https://github.com/lord-helicon/daitsch
```

Oder über den Skill-Installer, ohne das Repository zu klonen:

```bash
npx skills add lord-helicon/daitsch --skill daitsch --global --yes
```

Oder aus dem geklonten Repository:

```bash
bash install.sh
```

```powershell
.\install.ps1
```

Beide Skripte legen den Skill im vorhandenen Skill-Ordner ab (`~/.agents/skills/` oder `~/.claude/skills/`) und lassen anschließend den Selbsttest laufen. Mit `--ziel <pfad>` beziehungsweise `-Ziel <pfad>` geht es in einen beliebigen anderen Ordner.

## Andere Agenten

Die Dateien in `adapters/` sind aus dem KERN-Block von `SKILL.md` erzeugt und eingecheckt. Kopieren genügt, Python wird dafür nicht gebraucht.

| Datei | Ziel |
|---|---|
| `adapters/AGENTS.md` | `AGENTS.md` im Projektwurzelverzeichnis, gelesen von Codex, Cursor, Gemini CLI, Zed, Jules und weiteren |
| `adapters/CLAUDE.md` | `CLAUDE.md` |
| `adapters/GEMINI.md` | `GEMINI.md` |
| `adapters/cursor/daitsch.mdc` | `.cursor/rules/` |
| `adapters/copilot-instructions.md` | `.github/copilot-instructions.md` |
| `adapters/system-prompt.txt` | Systemprompt eigener Agenten, GPTs, n8n-Nodes |

Nach einer Änderung an `SKILL.md`:

```bash
python3 tools/build_adapters.py
```

## Prüfer

```bash
python3 skills/daitsch/scripts/klartext.py text.md              # Befund, Exit 1 bei Funden
python3 skills/daitsch/scripts/klartext.py text.md --json       # maschinenlesbar für Agenten
python3 skills/daitsch/scripts/klartext.py --haerte hart *.md   # nur eindeutige Funde
python3 skills/daitsch/scripts/klartext.py --regeln             # alle Muster auflisten
python3 skills/daitsch/scripts/klartext.py --selbsttest         # Katalog und Testtexte prüfen
cat text.txt | python3 skills/daitsch/scripts/klartext.py -     # aus der Standardeingabe
```

Nur Standardbibliothek, kein pip. Das Skript ändert nie eine geprüfte Datei; es meldet, der Agent formuliert um.

Geprüft wird Fließtext. Dateien, die nach Quelltext aussehen, überspringt der Prüfer, weil gerade Anführungszeichen und Pfeile dort richtig sind. Mit `--erzwingen` prüft er sie trotzdem. In Markdown bleiben Codeblöcke, Inline-Code, URLs und Frontmatter ohnehin außen vor.

Harte Funde sind eindeutig und ohne Kontexturteil zu beheben, etwa Geviertstriche, gerade Anführungszeichen oder feste Wendungen. Weiche Funde sind Dichtebefunde und kontextabhängige Muster, über die der Agent entscheidet und die Entscheidung begründet.

## Katalog erweitern

Alle Regeln stehen in [`skills/daitsch/references/katalog.md`](skills/daitsch/references/katalog.md), auch die des Prüfers. Er liest die Datei beim Start und hat keine eigene Wortliste, deshalb wird eine neue Floskel an genau einer Stelle ergänzt. Der Aufbau eines Eintrags steht oben in derselben Datei.

Der Selbsttest fängt kaputte Einträge ab. Er prüft, dass jeder Ausdruck kompiliert, dass jede Regel ihr eigenes Floskel-Beispiel findet, dass kein Klartext-Beispiel einen harten Fund auslöst, dass jede Metrik von einem Testtext ausgelöst wird und dass `tests/klartext.md` im Skillordner ohne Fund bleibt.

```bash
python3 skills/daitsch/scripts/klartext.py --selbsttest
```

Dieselben Prüfungen laufen bei jedem Push über GitHub Actions, unter Python 3.9 und 3.12. Dazu wird geprüft, ob `adapters/` noch zu `SKILL.md` passt.

Vier Stellen tragen eine Versionsnummer: der Git-Tag, das Codex-Manifest, das Plugin-Manifest und der Marktplatzeintrag. `tools/check_version.py` hält sie zusammen und schlägt an, sobald eine abweicht. Vor einem Release von Hand:

```bash
python3 tools/check_version.py v1.2.3
```

## Folien aus dem Katalog

Für Beiträge auf LinkedIn erzeugt `tools/karussell.py` ein PDF, das dort als blätterbares Dokument läuft. Eine Seite je Muster, oben die Floskel, unten die Klartext-Fassung.

```bash
python3 tools/karussell.py
python3 tools/karussell.py --muster sauber,dient-als --ziel folien.pdf
python3 tools/karussell.py --liste
```

Die Folien entstehen aus `katalog.md` und können deshalb nichts behaupten, was dort nicht steht. Verbessert jemand eine Klartext-Fassung, ist der nächste Lauf aktuell. Das Skript braucht Pillow; der Skill selbst kommt weiterhin ohne Fremdpakete aus.

## Wenn es nicht klappt

**Der Marktplatz lässt sich nicht hinzufügen.** Die Kurzform `lord-helicon/daitsch` klont über SSH und verlangt einen Schlüssel bei GitHub. Mit der vollständigen Adresse geht es ohne:

```
/plugin marketplace add https://github.com/lord-helicon/daitsch.git
```

**Git kommt nicht nach außen.** Dann `daitsch-skill.zip` aus dem [neuesten Release](https://github.com/lord-helicon/daitsch/releases/latest) herunterladen, auspacken und den Ordner `daitsch` nach `~/.claude/skills/` legen. Kein Git, kein Python, kein Konto.

**Der Skill reagiert nicht oder doppelt.** Wer ihn vorher über `npx skills add` oder ein Installationsskript eingerichtet hat, hat ihn zweimal. Welcher gewinnt, ist nicht vorhersagbar, und ein Update erwischt womöglich nur eine Kopie:

```bash
rm -rf ~/.agents/skills/daitsch ~/.claude/skills/daitsch
```

**Der Prüfer findet seinen Katalog nicht.** Er sucht ihn über den eigenen Pfad, also `../references/katalog.md` neben `scripts/`. Wer nur die Skriptdatei kopiert, muss den Katalog mit `--katalog <pfad>` nachweisen.

**Nach der Installation ist der Skill noch nicht da.** Sitzung neu starten.

## Anregungen

Der Aufbau als Skill mit Prüfliste, der Gedanke, beim Überarbeiten zuerst die Stimme des Autors zu sichern, und der Portabilitätstest stammen aus [no-ai-slop](https://github.com/petergyang/no-ai-slop) von Peter Yang (MIT). Übernommen sind die Gedanken, nicht der Text.

## Lizenz

Der Code (`skills/daitsch/scripts/`, `tools/`, `install.sh`, `install.ps1`) steht unter der MIT-Lizenz, siehe [LICENSE](LICENSE).

Die Textteile (`SKILL.md`, `references/`, `adapters/`, `tests/`) stehen unter CC BY 4.0, siehe [LICENSE-CONTENT.md](LICENSE-CONTENT.md). Die zugrunde liegende Mustersammlung stammt von Tobias Voßberg; Veröffentlichung und Lizenzwahl erfolgen mit seiner Zustimmung.

## Aufbau

```
skills/daitsch/
  SKILL.md                Kanonische Quelle im offenen Agent-Skills-Format
  references/katalog.md   74 Muster, zugleich Regelquelle des Prüfers
  references/pruefliste.md  Fragen nach dem Überarbeiten, die kein Ausdruck stellt
  scripts/klartext.py     Prüfer
  tests/                  Testtexte für den Selbsttest
adapters/                 Erzeugt, eingecheckt
tools/build_adapters.py   Erzeugt adapters/ aus dem KERN-Block
tools/check_version.py    Hält Tag und Codex-Manifest zusammen
tools/karussell.py        Erzeugt PDF-Folien aus dem Katalog
tools/paket.py            Packt Plugin und Skill-Zip nach dist/
tools/screenshot.py       Erzeugt das Bild oben aus einem echten Lauf
.codex-plugin/            Plugin-Manifest für Codex
```
