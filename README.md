# dAItsch

Ein Skill für KI-Agenten, der deutsche Texte davon abhält, nach KI zu klingen. Herstellerneutral: eine Quelle, daraus Adapterdateien für die verbreiteten Agentenformate.

Die Musterlisten beruhen auf „KI-Sprachmuster im Deutschen vermeiden“ von **Tobias Voßberg**, [www.iplaw.lol/ki-floskeln](https://www.iplaw.lol/ki-floskeln/). Von dort stammen die rund 75 Muster. Hinzugekommen sind hier die Klartext-Fassungen, die Ausnahmen und der Prüfer.

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
python3 scripts/build_adapters.py
```

## Prüfer

```bash
python3 scripts/klartext.py text.md              # Befund, Exit 1 bei Funden
python3 scripts/klartext.py text.md --json       # maschinenlesbar für Agenten
python3 scripts/klartext.py --haerte hart *.md   # nur eindeutige Funde
python3 scripts/klartext.py --regeln             # alle Muster auflisten
python3 scripts/klartext.py --selbsttest         # Katalog und Testtexte prüfen
cat text.txt | python3 scripts/klartext.py -     # aus der Standardeingabe
```

Nur Standardbibliothek, kein pip. Das Skript ändert nie eine geprüfte Datei; es meldet, der Agent formuliert um.

Geprüft wird Fließtext. Dateien, die nach Quelltext aussehen, überspringt der Prüfer, weil gerade Anführungszeichen und Pfeile dort richtig sind. Mit `--erzwingen` prüft er sie trotzdem. In Markdown bleiben Codeblöcke, Inline-Code, URLs und Frontmatter ohnehin außen vor.

Harte Funde sind eindeutig und ohne Kontexturteil zu beheben, etwa Geviertstriche, gerade Anführungszeichen oder feste Wendungen. Weiche Funde sind Dichtebefunde und kontextabhängige Muster, über die der Agent entscheidet und die Entscheidung begründet.

## Katalog erweitern

Alle Regeln stehen in `references/katalog.md`, auch die des Prüfers. Er liest die Datei beim Start und hat keine eigene Wortliste, deshalb wird eine neue Floskel an genau einer Stelle ergänzt. Der Aufbau eines Eintrags steht oben in derselben Datei.

Der Selbsttest fängt kaputte Einträge ab. Er prüft, dass jeder Ausdruck kompiliert, dass jede Regel ihr eigenes Floskel-Beispiel findet, dass kein Klartext-Beispiel einen harten Fund auslöst, dass jede Metrik von einem Testtext ausgelöst wird und dass `tests/klartext.md` ohne Fund bleibt.

```bash
python3 scripts/klartext.py --selbsttest
```

## Lizenz

Der Code (`scripts/`, `install.sh`, `install.ps1`) steht unter der MIT-Lizenz, siehe [LICENSE](LICENSE).

Die Textteile (`SKILL.md`, `references/`, `adapters/`, `tests/`) stehen unter CC BY 4.0, siehe [LICENSE-CONTENT.md](LICENSE-CONTENT.md). Die zugrunde liegende Mustersammlung stammt von Tobias Voßberg; Veröffentlichung und Lizenzwahl erfolgen mit seiner Zustimmung.

## Aufbau

```
SKILL.md                  Kanonische Quelle im offenen Agent-Skills-Format
references/katalog.md     Rund 75 Muster, zugleich Regelquelle des Prüfers
scripts/klartext.py       Prüfer
scripts/build_adapters.py Erzeugt adapters/ aus dem KERN-Block
tests/                    Testtexte für den Selbsttest
adapters/                 Erzeugt, eingecheckt
```
