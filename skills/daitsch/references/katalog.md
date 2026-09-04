# Musterkatalog

Rund 75 Muster, an denen deutsche KI-Texte erkennbar sind. Jeder Eintrag nennt die Floskel und die Klartext-Fassung daneben, dazu die Fälle, in denen das Muster richtig ist.

Diese Datei ist zugleich die Regelquelle für `scripts/klartext.py`. Der Prüfer liest sie beim Start. Wer eine Floskel ergänzt, ergänzt sie hier, und nur hier.

## Aufbau eines Eintrags

Die Überschrift ist die Muster-ID, die der Prüfer meldet. Darunter:

- `**Erkennung:**`: woran das Muster zu erkennen ist
- `**Härte:**`: `hart` für eindeutige Funde, `weich` für Befunde, die ein Urteil verlangen
- ein Codeblock `regex` oder `wortliste`, oder `**Metrik:**` für Dichtebefunde über den ganzen Text, oder nichts, wenn nur Lesen hilft
- `**Floskel:**` und `**Klartext:**`: dasselbe zweimal, einmal als Muster, einmal brauchbar
- `**Zulässig:**`: wann das Muster stehen bleibt

In der Wortliste steht eine Wendung je Zeile, Groß- und Kleinschreibung wird ignoriert. `*` am Wortende deckt die Beugung ab: `innovativ*` findet auch `innovative` und `innovativen`.

Ein `regex`-Block wird zeilenweise verankert (`^` und `$` gelten je Zeile) und achtet auf Groß- und Kleinschreibung. Wo sie egal ist, steht `(?i)` am Anfang des Ausdrucks.

---

## Parallelismen

### negativ-parallelismus

**Erkennung:** Eine Aussage wird verneint, damit die folgende wie eine Erkenntnis wirkt.

**Härte:** hart

```regex
(?i)\bnicht\s+(?!nur\b)[^.!?;]{2,60},\s*sondern
```

**Floskel:** Es geht nicht um Technologie, sondern um Menschen.

**Klartext:** Die Software läuft seit März. Benutzt hat sie bisher niemand.

**Zulässig:** Wenn der Leser sonst tatsächlich das Falsche annimmt und der Gegensatz die Korrektur trägt.

### nicht-nur-sondern-auch

**Erkennung:** Eine Addition wird als Steigerung inszeniert.

**Härte:** hart

```regex
(?i)\bnicht\s+nur\b[^.!?;]{2,80}\bsondern\b[^.!?;]{0,40}\bauch\b
```

**Floskel:** Die Lösung spart nicht nur Zeit, sondern verbessert auch die Qualität.

**Klartext:** Die Lösung spart vier Minuten je Vorgang. Die Fehlerquote fiel von sechs auf zwei Prozent.

**Zulässig:** Wenn der zweite Punkt wirklich überrascht, weil der erste ihn ausschließen würde.

### verneinungs-dreiklang

**Erkennung:** Mehrere Möglichkeiten werden verneint, bevor der angeblich wahre Punkt kommt.

**Härte:** hart

```regex
(?:^|[.!?]\s)(?:Kein|Keine|Nicht)\b[^.!?]{0,40}[.!?]\s*(?:Kein|Keine|Nicht)\b[^.!?]{0,40}[.!?]
```

**Floskel:** Kein Fehler. Kein Versehen. Ein Systemproblem.

**Klartext:** Der Fehler trat in allen 40 Vorgängen auf. Er steckt im Ablauf.

**Zulässig:** In Zitaten und in Textsorten, die von Rhythmus leben, etwa einer Rede.

---

## Wortwahl

### magische-adverbien

**Erkennung:** Ein Adverb behauptet Gewicht, ohne eine Information hinzuzufügen.

**Härte:** weich

```wortliste
tiefgreifend*
bemerkenswert*
zweifellos
subtil*
grundlegend*
maßgeblich*
nachhaltig*
```

**Floskel:** eine tiefgreifende Transformation der gesamten Branche

**Klartext:** Von 120 Stellen im Vertrieb bleiben 80.

**Zulässig:** Wenn das Adverb einen messbaren Unterschied benennt, den der Satz auch belegt.

### stille-revolution

**Erkennung:** Etwas geschieht angeblich unbemerkt im Hintergrund und wird dadurch bedeutend.

**Härte:** hart

```wortliste
stille Revolution
still* Wandel
im Hintergrund still
leise Revolution
unbemerkt verändert
```

**Floskel:** eine stille Revolution, die unsere Arbeitswelt verändert

**Klartext:** Drei von vier Sachbearbeitern nutzen das Werkzeug täglich, ohne dass es je angekündigt wurde.

### analyse-ankuendigung

**Erkennung:** Die Analyse wird angekündigt, statt zu beginnen.

**Härte:** hart

```wortliste
Tauchen wir
tiefer eintauchen
tiefer einsteigen
näher beleuchten
genauer beleuchten
unter die Lupe
einen genaueren Blick
werfen wir einen Blick
Im Folgenden betrachten
```

**Floskel:** Tauchen wir tiefer in das Thema ein.

**Klartext:** Der Vertrag deckt drei der fünf Fälle ab. Die beiden übrigen stehen unten.

**Zulässig:** In Lehrtexten, wenn der Leser eine Wegmarke braucht, dann höchstens einmal je Kapitel.

### landschaft-oekosystem

**Erkennung:** Ein Fachgebiet wird zur Landschaft, eine Gruppe von Beteiligten zum Ökosystem.

**Härte:** weich

```wortliste
Landschaft
Ökosystem
Paradigm*
Synergi*
Spannungsfeld
Geflecht
Zusammenspiel
Rahmenwerk
```

**Floskel:** die sich ständig wandelnde KI-Landschaft

**Klartext:** die vier Anbieter, die im deutschen Markt Modelle anbieten

**Zulässig:** Wo der Begriff fachlich feststeht, etwa das Ökosystem eines Sees oder die Landschaft in einem Gutachten zur Bauleitplanung.

### dient-als

**Erkennung:** Ein einfaches Verb wird durch eine feierliche Konstruktion ersetzt.

**Härte:** hart

```wortliste
dient als
dienen als
fungiert als
fungieren als
steht sinnbildlich
verkörpert
stellt einen Meilenstein
markiert einen Wendepunkt
markiert einen Meilenstein
```

**Floskel:** Das Urteil dient als wichtiger Weckruf für Unternehmen.

**Klartext:** Nach dem Urteil haftet der Betreiber für fremde Inhalte ab Kenntnis.

**Zulässig:** Wenn eine Sache tatsächlich zweckentfremdet wird: Die Kiste dient als Tisch.

### behauptete-wichtigkeit

**Erkennung:** Ein Wort behauptet Bedeutung an der Stelle, an der die Begründung stehen müsste.

**Härte:** weich

```wortliste
zentral*
entscheidend*
wesentlich*
essenziell*
von großer Bedeutung
von entscheidender Bedeutung
elementar*
unerlässlich
```

**Floskel:** Ein zentraler Aspekt ist die Transparenz.

**Klartext:** Ohne Einsicht in die Rohdaten lässt sich die Quote nicht nachrechnen.

**Zulässig:** Wenn der Satz die Bedeutung anschließend belegt.

### business-adjektive

**Erkennung:** Ein positives Adjektiv benennt keine überprüfbare Eigenschaft.

**Härte:** weich

```wortliste
innovativ*
robust*
nahtlos*
ganzheitlich*
leistungsstark*
zukunftssicher*
maßgeschneidert*
hochmodern*
wegweisend*
state of the art
```

**Floskel:** eine robuste und skalierbare Lösung mit echtem Mehrwert

**Klartext:** Der Dienst hält 2000 Anfragen je Sekunde aus und lief im letzten Quartal 99,9 Prozent der Zeit.

**Zulässig:** Wenn die Eigenschaft im selben Absatz mit einer Zahl oder einem Beleg unterlegt wird.

### sauber

**Erkennung:** `sauber` als Allzweck-Gütesiegel vor einem Partizip.

**Härte:** hart

```regex
(?i)\bsauber\s+(?:zusammengestellt|strukturiert|getrennt|aufgebaut|gelöst|dokumentiert|abgegrenzt|recherchiert|umgesetzt|implementiert|gekapselt|formatiert)
```

**Floskel:** Das Modul ist sauber getrennt und sauber dokumentiert.

**Klartext:** Das Modul kennt nur die Schnittstelle, nicht die Datenbank. Jede öffentliche Funktion hat einen Kommentar mit Beispiel.

**Zulässig:** Wörtlich: eine sauber gewischte Fläche.

### nutzenwoerter

**Erkennung:** Ein Nutzen wird behauptet, ohne die Verbesserung zu benennen.

**Härte:** hart

```wortliste
Mehrwert
echten Mehrwert
Potenziale heben
ungenutzte Potenziale
neue Chancen eröffn*
Impulse setz*
Effizienzgewinn*
nächste Level
nächsten Level
nachhaltige Wirkung
```

**Floskel:** Die Plattform schafft echten Mehrwert und hebt ungenutzte Potenziale.

**Klartext:** Die Plattform ersetzt die wöchentliche Excel-Liste. Zwei Stunden Handarbeit je Woche entfallen.

### uebersetztes-englisch

**Erkennung:** Eine englische Wendung wurde Wort für Wort übernommen.

**Härte:** hart

```wortliste
das Narrativ verändern
durch diese Linse
resonier*
Ownership übernehmen
eine Reise beginn*
den Raum schaffen
den Raum dafür
Gamechanger
Game Changer
am Ende des Tages
Level heben
```

**Floskel:** Der Beitrag soll mit dem Publikum resonieren und das Narrativ verändern.

**Klartext:** Der Beitrag soll Leser überzeugen, die bisher gegen das Vorhaben sind.

**Zulässig:** In Fachtexten, in denen der englische Begriff der eingeführte ist, etwa Ownership im Sinne von Rust.

### synonymvariation

**Erkennung:** Derselbe Gegenstand bekommt in einem Absatz mehrere Namen, weil das Modell die Wiederholung meidet. Der Leser fragt sich, ob mehrere Dinge gemeint sind.

**Härte:** weich

**Floskel:** Die Regelung greift ab Juli. Die Vorschrift betrifft alle Anbieter. Das Regelwerk sieht Übergangsfristen vor.

**Klartext:** Die Regelung greift ab Juli. Sie betrifft alle Anbieter und sieht Übergangsfristen vor.

**Zulässig:** Wenn die Begriffe verschiedene Dinge bezeichnen. In Fachtexten bleibt ein Begriff durchgehend gleich benannt, auch um den Preis der Wiederholung.

### uebergangsdichte

**Erkennung:** Fast jeder Absatz beginnt mit einem Übergangswort, obwohl der Zusammenhang aus dem Inhalt hervorgeht.

**Härte:** weich

**Metrik:** uebergangsdichte

**Floskel:** Zudem ... Darüber hinaus ... Gleichzeitig ... Vor diesem Hintergrund ...

**Klartext:** Absätze, die mit ihrem Gegenstand beginnen. Ein Übergangswort steht dort, wo der Sprung sonst nicht zu verstehen wäre.

**Zulässig:** Einzeln sind diese Wörter unverdächtig und in guten Texten nötig. Es geht um die Dichte.

### leere-uebergaenge

**Erkennung:** Ein neuer Punkt wird angekündigt, ohne ihn mit dem vorherigen zu verbinden.

**Härte:** hart

```wortliste
Es ist erwähnenswert
erwähnenswert ist
Bemerkenswert ist
Interessanterweise
Hervorzuheben ist
Nicht zu unterschätzen ist
Wichtig ist in diesem Zusammenhang
Es sei angemerkt
```

**Floskel:** Es ist erwähnenswert, dass dieser Ansatz auch Grenzen hat.

**Klartext:** Der Ansatz versagt, sobald mehr als zwei Mandanten dieselbe Datenbank teilen.

### lieblingsverben

**Erkennung:** Ein Verb erzeugt den Eindruck von Wirkung, ohne die Handlung zu benennen.

**Härte:** weich

```wortliste
ermöglicht
ermöglichen
optimiert
optimieren
fördert
fördern
stärkt
stärken
unterstreicht
unterstreichen
verdeutlicht
verdeutlichen
adressiert
adressieren
vorantreibt
vorantreiben
treibt voran
begleitet
begleiten
abbildet
abbilden
```

**Floskel:** Die Lösung ermöglicht eine effizientere Zusammenarbeit.

**Klartext:** Zwei Personen können dieselbe Datei gleichzeitig bearbeiten.

**Zulässig:** Wenn Gegenstand und Wirkung im Satz stehen: Der Schlüssel ermöglicht den Zugang zum Serverraum. Die Liste nennt nur Verbformen, weil die Wortstämme sonst auch Substantive wie Abbildung, Optimierung oder Förderung treffen, die nichts behaupten.

---

## Satzbau

### rhetorische-frage-sofortantwort

**Erkennung:** Eine Frage, die niemand gestellt hat, wird sofort selbst beantwortet.

**Härte:** hart

```regex
[A-ZÄÖÜ][^.!?\n]{3,50}\?\s+[A-ZÄÖÜ][\wäöüß]+(?:\s+[\wäöüß]+){0,2}\.
```

**Floskel:** Das Ergebnis? Ernüchternd.

**Klartext:** Von zwölf Testläufen bestanden drei.

**Zulässig:** Im Interview und in der wörtlichen Rede.

### doppelpunkt-enthuellung

**Erkennung:** Kurze Nominalphrase, Doppelpunkt, kleingeschriebene Auflösung. Der Doppelpunkt ersetzt den Satzbau und kündigt eine Pointe an, die der Inhalt nicht einlöst.

**Härte:** weich

```regex
(?:^|(?<=[.!?]\s))(?:Der|Die|Das|Ein|Eine)\s+[\wäöüß]+(?:\s+[\wäöüß]+){0,2}:\s+[a-zäöüß][^.!?\n]{2,40}[.!?]
```

**Floskel:** Das Beste daran: es lernt mit jedem Durchlauf dazu.

**Klartext:** Mit jedem Durchlauf sinkt die Fehlerquote.

**Zulässig:** Vor einer Aufzählung, vor einem Zitat und dort, wo der Doppelpunkt eine Bezeichnung einführt.

### anapher-mechanisch

**Erkennung:** Mehrere Sätze in Folge beginnen gleich, sodass der Text wie eine Rede klingt.

**Härte:** weich

**Metrik:** anapher

**Floskel:** Wir brauchen klare Regeln. Wir brauchen mutige Unternehmen. Wir brauchen Debatten.

**Klartext:** Es fehlt an Regeln für den Umgang mit Trainingsdaten. Die vorhandenen stammen von 2019.

**Zulässig:** In einer Rede und dort, wo der Rhythmus die Aussage trägt, einmal im Text und nicht in jedem Abschnitt.

### dreiergruppen

**Erkennung:** Inhalte ordnen sich auffällig oft zu dritt, ohne dass die Zahl aus der Sache folgt.

**Härte:** weich

**Metrik:** dreiergruppen

**Floskel:** schnell, sicher und effizient

**Klartext:** Der Import dauert acht Sekunden. Bei Fehlern bricht er ab, statt halbe Datensätze zu schreiben.

**Zulässig:** Wenn es tatsächlich drei Dinge sind.

### analysenachtrag

**Erkennung:** An einen Tatsachensatz hängt sich ein Nachsatz, der Bedeutung behauptet und nichts erklärt.

**Härte:** hart

```regex
(?i),?\s+(?:und\s+)?(?:unterstreicht\s+(?:damit|so)|verdeutlicht\s+damit|zeigt\s+damit|trägt\s+(?:damit|so)\s+(?:zu|dazu)|spiegelt\s+(?:damit|so)\s+wider|was\s+die\s+(?:zentrale|wachsende|große)\s+\w+)
```

**Floskel:** Die Zahl der Anträge stieg um 30 Prozent und unterstreicht damit die wachsende Bedeutung von Transparenz.

**Klartext:** Die Zahl der Anträge stieg um 30 Prozent. Die Behörde bearbeitet sie mit unverändert vier Stellen.

### falsche-spannweite

**Erkennung:** `von X bis Y` suggeriert eine Skala, obwohl nur Verschiedenes aufgezählt wird.

**Härte:** weich

```regex
(?i)\bvon\s+[\wäöüß]{3,25}\s+(?:über\s+[\wäöüß]{3,25}\s+)?bis\s+(?:hin\s+)?zu[rm]?\s+[\wäöüß]{3,25}
```

**Floskel:** von Strategie über Technologie bis hin zu Vertrauen

**Klartext:** Strategie, Technik und die Frage, wer haftet

**Zulässig:** Bei echten Skalen: von 5 bis 50 Grad, von Montag bis Freitag.

### kuenstliche-kausalitaet

**Erkennung:** Eine kleine Maßnahme wird mit einer großen Folge verbunden, ohne den Zusammenhang zu belegen.

**Härte:** weich

```regex
(?i)\b(?:und\s+(?:schafft|stärkt|sichert)\s+(?:so|damit)|so\s+entsteht|trägt\s+dazu\s+bei|wodurch\s+[\wäöüß]+\s+entsteh)
```

**Floskel:** Das Unternehmen veröffentlicht einen Leitfaden und stärkt damit das Vertrauen.

**Klartext:** Das Unternehmen hat einen Leitfaden veröffentlicht. Ob ihn jemand liest, ist offen.

**Zulässig:** Wenn die Wirkung belegt ist und der Beleg danebensteht.

### absicherungskaskade

**Erkennung:** Mehrere Abtönungen in einem Satz. Der Leser erfährt nicht, wie sicher die Aussage ist.

**Härte:** hart

```regex
(?i)\b(?:könnte|dürfte|mag|scheint|lässt sich|kann)\b[^.!?]{0,40}\b(?:möglicherweise|unter Umständen|potenziell|gegebenenfalls|womöglich|in vielen Fällen|nach aktuellem Stand|bis zu einem gewissen Grad|nicht vollständig)\b
```

**Floskel:** Der Ansatz könnte möglicherweise dazu beitragen, die Quote zu verbessern.

**Klartext:** Ob der Ansatz die Quote verbessert, ist ungetestet.

**Zulässig:** Eine Abtönung je Aussage, wenn die Unsicherheit echt ist. Zwei sind eine zu viel.

### demonstrativkette

**Erkennung:** Mehrere Sätze in Folge beginnen mit Dies, Dabei, Dadurch, Damit. Der Bezug verschwimmt.

**Härte:** weich

**Metrik:** demonstrativkette

**Floskel:** Dies verbessert die Effizienz. Dadurch reagieren Unternehmen schneller. Damit entsteht die Grundlage für Wachstum.

**Klartext:** Der Import läuft jetzt nachts. Die Sachbearbeiter finden die Zahlen morgens fertig vor.

### kurzsatz-dramaturgie

**Erkennung:** Sehr kurze Sätze stehen als eigene Absätze, um gewöhnlichen Aussagen Gewicht zu geben.

**Härte:** weich

**Metrik:** kurzabsatz_anteil

**Floskel:** Das war öffentlich. Für alle sichtbar. Und niemand reagierte.

**Klartext:** Der Bericht stand vier Monate lang auf der Website. Angesehen haben ihn 30 Personen.

**Zulässig:** Ein kurzer Absatz an einer Stelle, an der er wirklich schneidet.

### aphoristisches-gegensatzpaar

**Erkennung:** Zwei kurze Sätze am Absatzanfang, die wie eine zitierfähige Lebensweisheit klingen.

**Härte:** weich

**Floskel:** Charisma fällt auf. Verlässlichkeit zeigt sich erst mit der Zeit.

**Klartext:** In der Beurteilung stand nichts über Pünktlichkeit. Befördert wurde der Kollege, der die Präsentation hielt.

### ungefragter-einwand

**Erkennung:** Ein Einwand wird eingeführt, den im Text niemand erhoben hat.

**Härte:** hart

```regex
(?i)\b(?:Das\s+bedeutet\s+nicht,?\s+dass|Damit\s+ist\s+nicht\s+gesagt|Das\s+heißt\s+(?:keineswegs|nicht,?\s+dass)|Missverstehen\s+Sie\s+mich\s+nicht)\b
```

**Floskel:** Das bedeutet nicht, dass Unternehmen auf KI verzichten müssen.

**Klartext:** Für Rechnungsprüfung taugt das Modell. Für Kündigungen nicht.

**Zulässig:** Wenn der Einwand vorher im Text steht oder aus der Diskussion bekannt ist.

### wenn-dann-absicherung

**Erkennung:** Mehrere Konditionalsätze fangen in einer kurzen Nachricht jede Abweichung im Voraus ab.

**Härte:** weich

**Metrik:** konditional_haeufung

**Floskel:** Sollte sich die Lieferung verzögern, schicke ich eine vorläufige Fassung. Falls der Termin nicht passt, richte ich mich nach einer Alternative. Sollten Rückfragen bestehen, stehe ich zur Verfügung.

**Klartext:** Die Zahlen kommen Freitag. Wenn nicht, sage ich Donnerstag Bescheid.

**Zulässig:** Einzeln sind das eingeführte Höflichkeitsformeln. Auffällig wird erst die Häufung.

---

## Absatzstruktur

### liste-im-trenchcoat

**Erkennung:** Eine nummerierte Liste ist als Fließtext verkleidet.

**Härte:** hart

```regex
(?i)\b(?:Der|Die|Das)\s+(?:erste|zweite|dritte|vierte|fünfte)\s+[\wäöüß]{3,20}\s+(?:ist|lautet|betrifft|liegt|besteht)
```

**Floskel:** Das erste Problem ist die fehlende Schnittstelle. Das zweite Problem ist der fehlende Zugriff.

**Klartext:** Es fehlt eine Schnittstelle, und ohne sie kommt niemand an die Daten.

**Zulässig:** Als echte Liste mit Aufzählungszeichen.

### uebersaubere-checkliste

**Erkennung:** Ein praktischer Abschnitt endet mit genau drei Fragen gleicher Grammatik, die überall passen würden.

**Härte:** weich

**Floskel:** Was ist das Ziel? Wer ist verantwortlich? Wie messen wir den Erfolg?

**Klartext:** Offen ist, wer die Freigabe erteilt. Ohne sie startet der Import nicht.

**Zulässig:** Wenn die Punkte aus dem konkreten Vorgang folgen und nicht auf jeden anderen passen.

### uniforme-textsammlung

**Erkennung:** Bei Sammelaufträgen haben alle Texte dieselbe Länge, denselben Rhythmus und dieselbe Schlusslehre. Essay, Post, Witz und Büromail klingen gleich.

**Härte:** weich

**Floskel:** Jeder der fünf Vorschläge hat Einleitung, Mitte und Schluss und ist etwa gleich lang.

**Klartext:** Der Witz ist zwei Zeilen lang und hat keine Moral. Der Essay hat 900 Wörter und endet mitten im Gedanken.

---

## Ton

### spannungsankuendigung

**Erkennung:** Eine Offenbarung wird angekündigt, obwohl ein gewöhnlicher Punkt folgt.

**Härte:** hart

```wortliste
Jetzt wird es spannend
Hier liegt der entscheidende Punkt
Und genau hier beginnt
Und genau hier liegt
Jetzt kommt der Punkt
Und hier wird es interessant
```

**Floskel:** Jetzt wird es spannend.

**Klartext:** Die Frist läuft am 30. Juni ab.

### analogie-reflex

**Erkennung:** Eine Analogie erklärt Fachleuten einen einfachen Zusammenhang und ist ungenauer als der Gegenstand selbst.

**Härte:** hart

```regex
(?i)\b(?:Stellen\s+Sie\s+sich\s+(?:das|es)\s+(?:wie|vor)|Denken\s+Sie\s+an\s+ein|Es\s+ist,?\s+als\s+(?:würde|ob)|Man\s+kann\s+es\s+sich\s+wie)\b
```

**Floskel:** Stellen Sie sich das wie eine Autobahn für Daten vor.

**Klartext:** Die Leitung überträgt 10 Gigabit je Sekunde. Ausgelastet ist sie zu einem Fünftel.

**Zulässig:** Wenn der Leser den Gegenstand nachweislich nicht kennt und die Analogie genauer ist als die Beschreibung.

### welt-szenario

**Erkennung:** Ein Zukunftsszenario beginnt mit einer Einladung zum Vorstellen, dann folgt eine Liste reibungsloser Entwicklungen.

**Härte:** hart

```regex
(?i)\b(?:Stellen\s+Sie\s+sich\s+(?:eine\s+Welt\s+)?vor|Stell\s+dir\s+vor|In\s+einer\s+Welt,\s+in\s+der)\b
```

**Floskel:** Stellen Sie sich eine Welt vor, in der jedes Werkzeug eine stille Intelligenz besitzt.

**Klartext:** Ab Version 4 schlägt das Programm die Kontierung vor. Bestätigen muss sie weiterhin ein Mensch.

### performative-ehrlichkeit

**Erkennung:** Offenheit wird simuliert, ohne ein Risiko einzugehen.

**Härte:** hart

```wortliste
Seien wir ehrlich
Ganz transparent
Ich gebe offen zu
Um ehrlich zu sein
Mal ehrlich
Hand aufs Herz
```

**Floskel:** Seien wir ehrlich: Das Thema ist komplex.

**Klartext:** Die Berechnung habe ich zweimal falsch aufgesetzt, bevor sie stimmte.

### wahrheit-ist-einfach

**Erkennung:** Eine Sache wird für eindeutig erklärt, statt sie zu belegen.

**Härte:** hart

```regex
(?i)\b(?:Die\s+Wahrheit\s+ist|Die\s+Realität\s+(?:ist|sieht)|Die\s+Sache\s+ist\s+(?:einfach|klar)|In\s+Wahrheit\s+geht\s+es)\b
```

**Floskel:** Die Wahrheit ist einfach: Niemand liest die Berichte.

**Klartext:** Der Bericht wurde im letzten Quartal viermal geöffnet, dreimal davon von der Autorin.

### tragweiten-ueberhoehung

**Erkennung:** Ein Produktupdate oder eine Entscheidung wird zum historischen Einschnitt erklärt.

**Härte:** hart

```wortliste
verändert alles
definiert die Zukunft
prägt die nächste Ära
revolutionier*
neues Zeitalter
historischer Wendepunkt
historischen Wendepunkt
schreibt die Regeln neu
stellt die Weichen für eine neue
für immer verändern
```

**Floskel:** Das Update revolutioniert die Art, wie wir arbeiten.

**Klartext:** Das Update ersetzt das alte Freigabeverfahren. Wer bisher zwei Klicks brauchte, braucht jetzt einen.

**Zulässig:** In der Rückschau auf Vorgänge, die die Bezeichnung tragen.

### lehrerrolle

**Erkennung:** Der Leser wird durch jeden Schritt geführt, als könne er nicht folgen.

**Härte:** hart

```regex
(?i)\b(?:Lassen\s+Sie\s+uns|Lass\s+uns|Schauen\s+wir\s+uns|Betrachten\s+wir\s+gemeinsam|Gehen\s+wir\s+das\s+(?:einmal\s+)?durch|Schritt\s+für\s+Schritt\s+aufschlüsseln)\b
```

**Floskel:** Lassen Sie uns das Schritt für Schritt aufschlüsseln.

**Klartext:** Der Ablauf hat vier Stationen. Die dritte ist die, an der es klemmt.

**Zulässig:** In einer Anleitung, in der der Leser wirklich mitarbeitet.

### vage-zuschreibung

**Erkennung:** Der Text beruft sich auf nicht benannte Autoritäten.

**Härte:** hart

```regex
(?i)\b(?:Experten\s+(?:sind\s+sich\s+einig|gehen\s+davon\s+aus|empfehlen)|Studien\s+(?:zeigen|belegen)|Untersuchungen\s+(?:zeigen|belegen)|Branchenberichte|Fachleute\s+sind\s+sich)\b
```

**Floskel:** Studien zeigen, dass hybride Modelle besser funktionieren.

**Klartext:** In der Erhebung des Ifo-Instituts von Januar 2026 gaben 61 Prozent der Befragten an, zwei Tage im Büro zu arbeiten.

**Zulässig:** Nie ohne Quelle. Mit Quelle braucht es die Wendung nicht mehr.

### erfundene-konzeptetiketten

**Erkennung:** Ein zusammengesetzter Begriff klingt analytisch, ist aber weder etabliert noch definiert. Der Name ersetzt die Begründung.

**Härte:** weich

```regex
\b(?:das|des|dem|die|der)\s+[A-ZÄÖÜ][\wäöüß]{4,20}(?:paradox|dilemma|illusion|falle|vakuum|lücke|inversion)\b
```

**Floskel:** Hier zeigt sich das Transparenzparadox.

**Klartext:** Je mehr die Behörde veröffentlicht, desto seltener fragt jemand nach. Die Zahl der Anfragen fiel von 400 auf 90.

**Zulässig:** Wenn der Begriff in der Fachliteratur eingeführt ist und die Quelle danebensteht.

### vernuenftige-mitte

**Erkennung:** Ein klares Urteil weicht der Ausgewogenheit aus, ohne die Argumente zu gewichten.

**Härte:** hart

```wortliste
verantwortungsvoller Umgang
verantwortungsvollen Umgang
ausgewogene Betrachtung
ausgewogenen Betrachtung
Chancen nutzen und Risiken
Chancen und Risiken im Blick
bewusster Umgang
richtige Weg liegt zwischen
```

**Floskel:** Es kommt auf einen verantwortungsvollen Umgang an.

**Klartext:** Für die Rechnungsprüfung ist das Verfahren freigegeben. Für Personalentscheidungen nicht.

### allgemeinplatz

**Erkennung:** Eine Aussage, der jeder zustimmt, wird als Einsicht ausgegeben.

**Härte:** hart

```wortliste
Kommunikation ist der Schlüssel
Schlüssel zum Erfolg
entsteht nicht über Nacht
Chancen und Risiken mit sich
Jede Medaille hat zwei Seiten
Der Weg ist das Ziel
```

**Floskel:** Vertrauen entsteht nicht über Nacht.

**Klartext:** Die Abteilung hat zwei Jahre gebraucht, bis sie Zahlen ohne Rückfrage weitergibt.

---

## Formatierung

### geviertstrich

**Erkennung:** Der lange Geviertstrich ist englische Typografie und kommt im Deutschen nicht vor. Der deutsche Gedankenstrich ist der Halbgeviertstrich mit Leerzeichen.

**Härte:** hart

```regex
—
```

**Floskel:** Das Problem — und darüber spricht niemand — liegt im System.

**Klartext:** Das Problem liegt im System, und niemand spricht darüber.

**Zulässig:** In englischen Zitaten und in Code.

### gedankenstrich-dichte

**Erkennung:** Der Halbgeviertstrich ist korrektes Deutsch. Auffällig ist die Menge: Ein Modell setzt ihn in fast jedem Absatz, weil die meisten Menschen die Tastenkombination nicht kennen.

**Härte:** weich

**Metrik:** gedankenstrich_dichte

**Floskel:** Der Tüftlergeist ist nicht verschwunden – er wurde aufgekauft.

**Klartext:** Der Tüftlergeist ist nicht verschwunden. Er wurde aufgekauft.

**Zulässig:** Ein Komma, ein Punkt oder eine Klammer trägt denselben Satz meist besser. Vereinzelt ist der Strich richtig.

### gerade-anfuehrungszeichen

**Erkennung:** Gerade Anführungszeichen in deutschem Text sind durchgereichte englische Konvention. Deutsch ist „so“ oder »so«.

**Härte:** hart

```regex
"[^"\n]{2,80}"
```

**Floskel:** Der Kollege nannte das Vorgehen "alternativlos".

**Klartext:** Der Kollege nannte das Vorgehen „alternativlos“.

**Zulässig:** In Code, in Dateipfaden und in englischen Zitaten.

### fette-listenetiketten

**Erkennung:** Jeder Listenpunkt beginnt mit einem fett gesetzten Etikett.

**Härte:** hart

```regex
^\s*[-*+]\s+\*\*[^*\n]{2,60}\*\*
```

```floskel
- **Sicherheit:** Konfiguration über Umgebungsvariablen
```

```klartext
- Zugangsdaten stehen in Umgebungsvariablen, nicht im Repository.
```

**Zulässig:** In einem Glossar, in dem das Etikett der Begriff ist.

### unicode-dekoration

**Erkennung:** Pfeile und typografischer Schmuck, die sich nicht aus dem Inhalt ergeben.

**Härte:** hart

```regex
[→➜⇒▶✔✓★☑✦❯]
```

**Floskel:** Input → Verarbeitung → Output

**Klartext:** Die Daten kommen aus dem Import, werden geprüft und landen in der Tabelle.

**Zulässig:** In Diagrammen, in Code und dort, wo der Pfeil eine Richtung bezeichnet, die im Fließtext umständlich wäre.

### emoji-gliederung

**Erkennung:** Emojis ersetzen Struktur, Ton oder eine echte Überschrift.

**Härte:** hart

```regex
^\s*(?:[-*+]\s*)?[\U0001F300-\U0001FAFF✨⭐⚡✅❌❗]
```

```floskel
💡 Tipp: Vorlagen sparen Zeit.
```

```klartext
Wer die Vorlage nutzt, spart das Formatieren.
```

**Zulässig:** Wo Emojis Teil der Textsorte sind, etwa in einer Chatnachricht unter Kollegen.

### doppelpunkt-titel

**Erkennung:** Schlagwort, Doppelpunkt, erklärender Nachsatz, im Journalismus üblich, hier reflexhaft auf jede Textsorte angewendet.

**Härte:** weich

```regex
^#{1,6}\s+[^:\n]{3,40}:\s+\S
```

```floskel
## Vertrauen: Der unterschätzte Erfolgsfaktor
```

```klartext
## Warum die Abteilung keine Zahlen weitergibt
```

**Zulässig:** In Fachaufsätzen und in der Presse, wo die Form eingeführt ist.

### zahlen-ueberschrift

**Erkennung:** Die Überschrift kündigt eine feste Anzahl von Punkten an, die sich nicht aus der Sache ergibt.

**Härte:** hart

```regex
(?i)^#{0,6}\s*(?:Die\s+)?\d{1,2}\s+(?:wichtigsten\s+|häufigsten\s+|größten\s+|besten\s+)?(?:Gründe|Tipps|Wege|Fehler|Punkte|Schritte|Regeln|Trends|Strategien|Dinge|Merkmale)\b
```

```floskel
## 5 Gründe, warum Ihr Projekt scheitert
```

```klartext
## Woran die letzten drei Projekte gescheitert sind
```

**Zulässig:** Wenn die Zahl feststeht, etwa bei den vier Fristen einer Verordnung.

### fettdruck-im-fliesstext

**Erkennung:** Einzelne Wörter mitten im Absatz werden fett gesetzt, ohne erkennbares System.

**Härte:** weich

**Metrik:** fettdruck_dichte

**Floskel:** Der Zugriff ist **streng limitiert** und die Freigabe erfolgt **ausschließlich** durch die Fachabteilung.

**Klartext:** Zugriff haben vier Personen. Die Freigabe erteilt die Fachabteilung.

**Zulässig:** In Dokumentation, in der die Hervorhebung einer festen Regel folgt.

### ueberschriften-schablone

**Erkennung:** Alle Überschriften folgen derselben Grammatik, der Text wirkt wie erzeugte Dokumentation.

**Härte:** weich

```regex
^#{1,6}\s+(?:Warum|Wie|Was)\s+[^\n]{3,40}(?:wichtig\s+ist|funktioniert|bedeutet|bringt)\s*$
```

```floskel
## Warum Transparenz wichtig ist
```

```klartext
## Wer die Zahlen sehen darf
```

### meta-ueberschrift

**Erkennung:** Die Überschrift benennt ihre Position im Text, nicht den Gegenstand.

**Härte:** weich

```regex
^#{1,6}\s*(?:Einleitung|Hintergrund|Analyse|Wichtige\s+Aspekte|Chancen\s+und\s+Herausforderungen|Fazit|Ausblick|Zusammenfassung)\s*$
```

```floskel
## Fazit
```

```klartext
## Was die Umstellung kostet
```

**Zulässig:** In Gutachten, Aufsätzen, Studien und Schriftsätzen sind diese Gliederungspunkte vorgeschrieben. Das Problem entsteht erst, wenn hinter der Überschrift ein leerer Abschnitt steht: ein Fazit, das nur wiederholt, oder ein Ausblick, der nichts Offenes benennt.

---

## Komposition

### fraktale-zusammenfassung

**Erkennung:** Ankündigen, erklären, zusammenfassen, auf Textebene und zusätzlich in jedem Abschnitt.

**Härte:** hart

```regex
(?i)\b(?:In\s+diesem\s+(?:Abschnitt|Kapitel|Beitrag)|Im\s+Folgenden\s+(?:werden|findest|finden|betrachten|zeigen)|Dieser\s+Abschnitt\s+(?:behandelt|zeigt|erläutert))\b
```

**Floskel:** Im Folgenden werden drei zentrale Aspekte erläutert.

**Klartext:** Die Umstellung betrifft die Freigabe, den Import und die Archivierung.

**Zulässig:** In Handbüchern mit Nachschlagecharakter, wo der Leser mitten im Text einsteigt.

### totgerittene-metapher

**Erkennung:** Eine Bildwelt zieht sich durch den ganzen Text: Reise, Etappe, Kompass, oder Fundament, Baustein, Säule.

**Härte:** weich

**Metrik:** metapherndichte

**Floskel:** Die Reise beginnt mit dem ersten Baustein und braucht einen Kompass für die nächste Etappe.

**Klartext:** Zuerst wird die Schnittstelle gebaut. Ohne sie läuft der Rest nicht.

### historische-vergleichskaskade

**Erkennung:** Bekannte Unternehmen oder Epochen werden aneinandergereiht, um einer These Autorität zu geben.

**Härte:** weich

**Floskel:** Apple baute nicht Uber. Facebook baute nicht Spotify. Stripe baute nicht Shopify.

**Klartext:** Der Marktführer hat das Format zweimal angekündigt und beide Male eingestellt.

### verduennung

**Erkennung:** Ein einfacher Punkt wird über viele Absätze, Beispiele und Metaphern wiederholt. Der Text wirkt umfangreich und enthält wenig.

**Härte:** weich

**Floskel:** Dieselbe These achtmal in anderen Worten, jeder Abschnitt mit einer neuen Metapher.

**Klartext:** Die These einmal, dann die Einwände, dann der Fall, in dem sie nicht gilt.

### gleichbleibende-flughoehe

**Erkennung:** Jeder Absatz bleibt auf demselben Abstraktionsgrad. Kein Einzelfall, keine Ausnahme, kein Absatz deutlich länger als die anderen. Ein menschlicher Text hat Höhenunterschiede: Er beißt sich an einem Begriff fest und geht über anderes hinweg.

**Härte:** weich

**Metrik:** flughoehe

**Floskel:** Sechs Absätze, jeder vier Sätze lang, jeder gleich allgemein.

**Klartext:** Ein Absatz mit einer Zahl und einem Namen, daneben zwei Zeilen, die den Rest abräumen.

### schluss-appell

**Erkennung:** Der Text endet mit einer Handlungsaufforderung, obwohl niemand um Rat gebeten hat.

**Härte:** hart

```regex
(?i)\b(?:Beginnen\s+Sie\s+(?:noch\s+)?heute|Starten\s+Sie\s+jetzt|Prüfen\s+Sie\s+(?:jetzt|noch\s+heute)|Der\s+erste\s+Schritt\s+liegt\s+bei\s+Ihnen|Worauf\s+warten\s+Sie)\b
```

**Floskel:** Beginnen Sie noch heute damit, Ihre Prozesse zu prüfen.

**Klartext:** Wer die Frist am 30. Juni reißt, zahlt das Bußgeld nach Absatz 3.

**Zulässig:** In Werbung, die als solche erkennbar ist, und in Anleitungen.

### hohler-schluss

**Erkennung:** Der letzte Satz klingt zitierfähig und fügt nichts hinzu.

**Härte:** hart

```wortliste
Am Ende kommt es auf
Am Ende zählt
Die Zukunft beginnt
Am Ende steht der Mensch
Der Mensch im Mittelpunkt
Technologie muss den Menschen
Technologie sollte den Menschen
Der Mensch bleibt der entscheidende
```

**Floskel:** Am Ende kommt es auf den Menschen an.

**Klartext:** Die Entscheidung fällt im Fachbereich, nicht in der IT.

### angekuendigte-schlussfolgerung

**Erkennung:** Der Text weist ausdrücklich darauf hin, dass jetzt der Schluss folgt.

**Härte:** hart

```regex
(?i)\b(?:Abschließend\s+(?:lässt\s+sich|bleibt|kann)|Zusammenfassend\s+(?:lässt\s+sich|kann)|Insgesamt\s+zeigt\s+sich|Alles\s+in\s+allem)\b
```

**Floskel:** Zusammenfassend lässt sich festhalten, dass die Umstellung Vorteile bringt.

**Klartext:** Die Umstellung spart zwei Stellen und kostet einmalig 40.000 Euro.

**Zulässig:** In langen Fachtexten, in denen der Leser den Anfang nicht mehr präsent hat.

### erzwungene-ausgewogenheit

**Erkennung:** Erst Positives, dann Herausforderungen, am Ende eine optimistische Mitte, ohne Gewichtung.

**Härte:** hart

```regex
(?i)\b(?:Trotz\s+dieser\s+Herausforderungen|Einerseits\b[^.!?]{5,80}\bandererseits|birgt\s+jedoch\s+auch\s+Risiken|Chancen\s+und\s+Risiken\s+gleichermaßen)\b
```

**Floskel:** Trotz dieser Herausforderungen bietet die Technologie erhebliche Chancen.

**Klartext:** Der Test lief in zwei von drei Abteilungen. In der dritten fehlt bis heute die Freigabe.

### inhaltliche-doppelung

**Erkennung:** Absätze wiederholen sich fast wörtlich, besonders in langen Ausgaben.

**Härte:** hart

**Metrik:** doppelung

**Floskel:** Absatz 3 und Absatz 17 sagen dasselbe in leicht anderen Worten.

**Klartext:** Jede Aussage steht einmal.

---

## Assistenten-Muster

### meta-einleitung

**Erkennung:** Der Assistent kündigt an, dass jetzt eine Sammlung oder eine strukturierte Antwort folgt. Der Nutzer sieht das bereits.

**Härte:** hart

```regex
(?i)\b(?:Hier\s+(?:ist|sind|kommt)\s+(?:eine|ein|einige|die)|Gerne,?\s+hier|Klar,?\s+hier|Im\s+Folgenden\s+(?:findest|finden)\s+(?:du|Sie)|Sehr\s+gerne)\b
```

**Floskel:** Gerne, hier sind einige abwechslungsreiche Vorschläge.

**Klartext:** Der Text beginnt mit dem ersten Vorschlag.

### service-schluss

**Erkennung:** Der Text ist fertig, danach folgt ein Angebot oder eine Gebrauchsanweisung.

**Härte:** hart

```regex
(?i)\b(?:Gerne\s+(?:passe|kann)\s+ich|Auf\s+Wunsch\s+(?:kann|erstelle)\s+ich|Ich\s+kann\s+(?:dir|Ihnen)\s+(?:außerdem|gerne|auch)|Sag\s+(?:einfach\s+)?Bescheid,?\s+wenn|Melde\s+dich,?\s+wenn\s+du)\b
```

**Floskel:** Gerne passe ich den Text weiter an.

**Klartext:** Nichts. Der Text hört auf, wenn er fertig ist.

**Zulässig:** Wenn tatsächlich eine Entscheidung aussteht, die der Nutzer treffen muss.

### makellose-bueromail

**Erkennung:** Die Mail enthält alle sechs Teile (Anlass, Begründung, Zusicherung, Nutzen, nächster Schritt, freundlicher Abschluss), auch wenn zwei Sätze gereicht hätten. Menschen lassen unter Zeitdruck Teile weg oder hängen den Anlass hinten an.

**Härte:** weich

**Floskel:** Eine Frage, verpackt in Begründung, Zusicherung, Nutzen und Ausblick.

**Klartext:** Kommst du Donnerstag um zehn? Es geht um die Freigabe für den Import.

### zeitgeistphrase

**Erkennung:** Eine Zeitdiagnose simuliert Dringlichkeit, ohne etwas zu belegen.

**Härte:** hart

```wortliste
Gerade in Zeiten
In Zeiten des Wandels
wichtiger denn je
In einer Welt, in der
in der heutigen schnelllebigen
in der heutigen digitalen
Immer mehr Menschen fragen sich
zunehmend digitalen Welt
```

**Floskel:** Gerade in Zeiten des Wandels ist Vertrauen wichtiger denn je.

**Klartext:** Seit der Umstellung im März fragen drei Abteilungen dieselben Zahlen doppelt ab.

### im-kern-geht-es-um

**Erkennung:** Eine Zuspitzung wird angekündigt, die keine ist.

**Härte:** hart

```regex
(?i)\b(?:Im\s+Kern\s+geht\s+es\s+um|Letztlich\s+geht\s+es\s+um|Am\s+Ende\s+geht\s+es\s+um|Im\s+Grunde\s+geht\s+es\s+um)\b
```

**Floskel:** Im Kern geht es um Vertrauen.

**Klartext:** Die Abteilung gibt die Zahlen nicht heraus, solange sie für Fehler darin haftet.

**Zulässig:** Einmal im Text, wenn danach wirklich zugespitzt wird.

### es-zeigt-sich

**Erkennung:** Klingt analytisch, wiederholt aber die vorherige Behauptung.

**Härte:** hart

```regex
(?i)\b(?:Es\s+zeigt\s+sich,?\s+dass|Dabei\s+zeigt\s+sich|Daran\s+zeigt\s+sich|Hier\s+zeigt\s+sich,?\s+(?:dass|wie))\b
```

**Floskel:** Es zeigt sich, dass Unternehmen handeln müssen.

**Klartext:** Vier der sechs Anbieter haben die Frist bereits verstreichen lassen.

### wichtiger-erster-schritt

**Erkennung:** Eine Maßnahme wird gelobt, ohne ihre Wirkung zu bewerten.

**Härte:** hart

```wortliste
wichtiger erster Schritt
wichtigen ersten Schritt
setzt ein wichtiges Signal
setzt ein starkes Signal
schafft eine gute Grundlage
ist ein guter Anfang
Schritt in die richtige Richtung
```

**Floskel:** Die Leitlinie ist ein wichtiger erster Schritt.

**Klartext:** Die Leitlinie nennt keine Fristen und keine Zuständigkeit.

### es-bleibt-abzuwarten

**Erkennung:** Ein leeres Ende ohne konkrete offene Frage.

**Härte:** weich

```regex
(?i)\b(?:bleibt\s+abzuwarten|Es\s+bleibt\s+spannend|Die\s+weitere\s+Entwicklung\s+bleibt)\b
```

**Floskel:** Es bleibt abzuwarten, wie sich die Praxis entwickelt.

**Klartext:** Ob die Aufsicht die Auslegung teilt, entscheidet sich mit dem Verfahren im Herbst.

**Zulässig:** In juristischen und journalistischen Texten, wenn die offene Frage danebensteht.

### komplexe-herausforderungen

**Erkennung:** Aus einem Problem wird eine komplexe Herausforderung in einem dynamischen Umfeld.

**Härte:** hart

```wortliste
komplex* Herausforderung*
vielfältig* Anforderung*
zunehmend* Dynamik
wachsend* Komplexität
anspruchsvoll* Umfeld
dynamisch* Umfeld
zahlreich* Stakeholder
vielschichtig* Fragestellung*
komplex* Rahmenbedingung*
```

**Floskel:** Unternehmen stehen vor komplexen Herausforderungen in einem dynamischen Umfeld.

**Klartext:** Drei Verordnungen mit unterschiedlichen Fristen gelten gleichzeitig, und zwei widersprechen sich beim Löschanspruch.

---

## Herkunft

Die Musterlisten stammen aus „KI-Sprachmuster im Deutschen vermeiden“ von Tobias Voßberg, [www.iplaw.lol/ki-floskeln](https://www.iplaw.lol/ki-floskeln/). Die Klartext-Fassungen, die Ausnahmen und die Prüfregeln sind hier hinzugekommen.
