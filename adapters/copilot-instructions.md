<!-- Erzeugt aus SKILL.md durch scripts/build_adapters.py. Änderungen gehören in SKILL.md. -->

# Deutsche Texte ohne KI-Floskeln

Ziel: `.github/copilot-instructions.md`

Gilt für jeden deutschen Text, der hier entsteht oder überarbeitet wird: Commit-Nachricht, Dokumentation, README, Mail, Beitrag, Bericht. Für Code und englische Texte gilt sie nicht.

## Kernregeln

Diese Griffe decken den größten Teil ab. Alles Weitere steht im Katalog.

| Statt der Floskel | Klartext |
|---|---|
| nicht X, sondern Y, auch als Kurzform X, nicht Y | Die Sache benennen, die zutrifft. Den Gegensatz nur, wenn der Leser sonst das Falsche annimmt. |
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

Drei Regeln stehen über den Mustern:

1. Bedeutung schlägt Musterfreiheit. Eine sachlich nötige Einschränkung bleibt stehen, auch wenn sie wie eine Absicherung aussieht.
2. Die Klartext-Fassung ist nie länger als die Floskel. Wer streicht und nichts Prüfbares einsetzen kann, streicht den Satz.
3. Der Portabilitätstest fängt, was keine Liste kennt: Passt ein Satz unverändert auf eine andere Firma, eine andere Person oder ein anderes Produkt, ist er Füllung. Dann muss eine Tatsache, ein Beispiel, eine Folge oder ein Urteil hinein, das nur hierher passt.

Der vollständige Katalog mit rund 75 Mustern, den Ausnahmen und einem Prüfskript steht im Skill
`daitsch` (references/katalog.md, scripts/klartext.py im Skillordner). Wo das Skript vorhanden ist:
`python3 skills/daitsch/scripts/klartext.py <datei>` vor der Abgabe laufen lassen und jeden harten Fund beheben.

Die Musterlisten beruhen auf „KI-Sprachmuster im Deutschen vermeiden“ von Tobias Voßberg, www.iplaw.lol/ki-floskeln, verwendet mit seiner Zustimmung. Diese Datei steht unter CC BY 4.0; bei Weitergabe bitte beide Quellen nennen.
