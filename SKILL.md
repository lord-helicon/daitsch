---
name: daitsch
description: Deutsche Texte schreiben, prüfen und überarbeiten, ohne dass sie nach KI klingen. Erkennt und ersetzt KI-Floskeln. Use when writing or reviewing German text (E-Mail, LinkedIn-Post, Blogartikel, Bericht, Dokumentation, Pressetext, Angebot), when asked to entfloskeln or to check for Floskeln, KI-Sprech or KI-Sprachmuster, or when a text is described as floskelhaft, generisch, glatt, KI-typisch, or as sounding like ChatGPT.
---

# dAItsch

Deutsche KI-Texte sind an rund 75 wiederkehrenden Mustern erkennbar. Dieser Skill benennt sie als **Floskel** und ersetzt jede durch **Klartext**: eine Aussage, die jemand nachprüfen kann.

Der vollständige Katalog steht in [`references/katalog.md`](references/katalog.md). Jeder Eintrag hat eine Muster-ID, ein Floskel-Beispiel, die Klartext-Fassung und die Fälle, in denen das Muster richtig ist. Der Prüfer `scripts/klartext.py` liest denselben Katalog und meldet Fundstellen mit derselben ID.

<!-- KERN:start -->
## Kernregeln

Diese Griffe decken den größten Teil ab. Alles Weitere steht im Katalog.

| Statt der Floskel | Klartext |
|---|---|
| nicht X, sondern Y | Die Sache benennen, die zutrifft. Den Gegensatz nur, wenn der Leser sonst das Falsche annimmt. |
| nicht nur X, sondern auch Y | Beide Punkte einzeln, jeder mit seiner eigenen Zahl. |
| Mehrwert, Potenziale, Synergien, ganzheitlich, nahtlos, innovativ, robust | Die Verbesserung nennen: was vorher wie lange dauerte und was jetzt. |
| sauber strukturiert, sauber getrennt, sauber gelöst | Sagen, was getrennt ist und wovon. |
| dient als, fungiert als, markiert einen Wendepunkt | ist, zeigt, regelt, erlaubt |
| Lassen Sie uns, Tauchen wir tiefer ein, Schauen wir uns an | Mit der Sache anfangen. |
| Es ist erwähnenswert, Es zeigt sich, Im Kern geht es um | Den Punkt hinschreiben, den die Wendung ankündigt. |
| könnte möglicherweise, dürfte unter Umständen | Eine Abtönung je Aussage. Wenn die Sache ungetestet ist, das schreiben. |
| Experten sind sich einig, Studien zeigen | Quelle, Jahr, Zahl. Ohne Quelle entfällt die Aussage. |
| schnell, sicher und effizient (Dreiergruppen, gleiche Satzanfänge in Serie) | So viele Punkte nennen, wie es gibt. |
| Zusammenfassend lässt sich, Am Ende kommt es auf den Menschen an, Beginnen Sie noch heute | Der Text hört auf, wenn er fertig ist. |
| Gerne, hier ist eine Übersicht … Gerne passe ich den Text an | Kein Rahmen um die Antwort. Weder davor noch danach. |
| Geviertstrich, gerade Anführungszeichen, Pfeile, Emoji als Gliederung, fett beginnende Listenpunkte | Halbgeviertstrich sparsam, deutsche Anführungszeichen, gewöhnliche Sätze und Listen. |

Zwei Regeln stehen über den Mustern:

1. Bedeutung schlägt Musterfreiheit. Eine sachlich nötige Einschränkung bleibt stehen, auch wenn sie wie eine Absicherung aussieht.
2. Die Klartext-Fassung ist nie länger als die Floskel. Wer streicht und nichts Prüfbares einsetzen kann, streicht den Satz.
<!-- KERN:end -->

## Modus Schreiben

Gilt, sobald deutscher Text entsteht: Mail, Post, Artikel, Bericht, Dokumentation, Angebot.

1. Text schreiben, mit den Kernregeln im Kopf.
2. Entwurf in eine Datei legen und prüfen: `python3 scripts/klartext.py entwurf.md`
3. Jeden harten Fund beheben. Zu jedem weichen Fund entscheiden: beheben, oder als zulässig stehen lassen und dabei den Fall aus dem Katalogeintrag nennen.

Fertig ist der Text, wenn kein harter Fund offen ist und jeder weiche Fund entweder behoben oder begründet ist.

## Modus Prüfen

Der Text bleibt unverändert. Der Auftrag lautet: Befund, keine Bearbeitung.

1. `python3 scripts/klartext.py <datei> --json`
2. Zu jedem Fund den Katalogeintrag mit der gemeldeten ID lesen, besonders das Feld Zulässig.
3. Den Katalog zusätzlich nach den Mustern durchgehen, die kein Ausdruck findet (Art `lesen`, etwa Synonymvariation oder die makellose Büromail). `python3 scripts/klartext.py --regeln` listet sie.
4. Befund als Tabelle ausgeben: Zeile, Muster-ID, Fundstelle, Vorschlag.

Fertig ist die Prüfung, wenn jeder gemeldete Fund in der Tabelle steht oder mit Grund verworfen wurde, und die Datei unverändert ist.

## Modus Überarbeiten

1. Prüfen wie oben.
2. Umschreiben, Fund für Fund, nach der Klartext-Spalte des jeweiligen Katalogeintrags.
3. Erneut prüfen.
4. Am Ende in drei Zeilen berichten: was geändert wurde, was bewusst stehen blieb und warum, und welche Stelle inhaltlich unklar war und eine Entscheidung des Autors braucht.

Beim Umschreiben verschwindet die Floskel, nicht die Information. Wo eine Floskel eine fehlende Zahl verdeckt, wird die Lücke benannt statt mit einer anderen Floskel gefüllt.

## Ohne Shell

Agenten ohne Skriptausführung arbeiten den Katalog selbst ab: erst die Kernregeln, dann `references/katalog.md` von oben nach unten, mit besonderem Blick auf die Typografie, weil sie am zuverlässigsten verrät. Die Befunde und die Modi bleiben gleich.

## Grenzen

Der Katalog beschreibt Auffälligkeiten, keine Fehler. Fast jedes Muster ist irgendwo richtig: der Halbgeviertstrich in guter Prosa, „Fazit“ im Gutachten, „es bleibt abzuwarten“ im juristischen Text, der Doppelpunkt-Titel in der Presse, das Ökosystem in der Biologie. Das Feld Zulässig im Katalogeintrag entscheidet, nicht der Fund.

Überkorrektur macht Texte schlechter als die Floskeln, die sie beseitigt. Im Zweifel bleibt der Satz stehen und der Befund wird gemeldet.

## Herkunft

Die Musterlisten beruhen auf „KI-Sprachmuster im Deutschen vermeiden“ von Tobias Voßberg, [www.iplaw.lol/ki-floskeln](https://www.iplaw.lol/ki-floskeln/).
