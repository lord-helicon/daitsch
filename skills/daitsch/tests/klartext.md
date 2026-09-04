# Import der Nebenkostenabrechnung, Stand 14. April

Der nächtliche Import läuft seit dem 3. April wieder durch. Vorher brach er in acht von zehn Nächten ab, weil zwei Objekte im Stammdatensatz doppelt geführt wurden. Der Fehler stammt aus der Migration im Januar. Wir haben die Dubletten am 2. April zusammengeführt und prüfen die Objektnummern jetzt schon beim Einlesen auf Eindeutigkeit.

Ungeklärt bleiben die Leerstandsflächen. Im Altsystem tragen sie keine Kostenstelle, im neuen ist das Feld verpflichtend. Für die 41 betroffenen Flächen setzen wir vorläufig die Kostenstelle des Objekts ein und markieren sie, damit die Abrechnung sie nicht stillschweigend umlegt. Frau Weber aus der Buchhaltung hält das für vertretbar, solange die Markierung in der Auswertung sichtbar bleibt. Eine dauerhafte Regel braucht die Zustimmung der Fondsbuchhaltung.

Der Lauf dauert jetzt 22 Minuten statt der geplanten zehn.

Der Engpass sitzt in der Umlageberechnung. Sie setzt je Fläche eine eigene Abfrage ab: 38.000 Abfragen im Lauf, davon 31.000 mit identischem Ergebnis. Ein Zwischenspeicher drückt den Lauf nach unserer Messung auf gut sechs Minuten. Der Umbau kostet etwa drei Tage, und er berührt die Umlagelogik, die im Sommer ohnehin auf die neue Fassung umgestellt wird. Wer beides zusammenlegt, spart einen zweiten Test der Abrechnung.

Zwei Punkte brauchen eine Entscheidung aus dem Fachbereich. Ob die drei Tage in den Zwischenspeicher fließen oder ob 22 Minuten je Nacht hinnehmbar sind, kann ich nicht beurteilen. Wie die Leerstandsflächen dauerhaft behandelt werden, ebenfalls nicht.

Die Optimierung der Abfragen wirkt am stärksten bei den großen Objekten. Abbildung 2 im Anhang zeigt die Laufzeiten je Fläche. Die Begleitung durch die Fachabteilung ist bis Ende Oktober zugesagt, die Förderung für das Vorhaben läuft bis März.

Bis dahin läuft der Import unverändert weiter. Ich melde mich, wenn er zweimal hintereinander abbricht.
