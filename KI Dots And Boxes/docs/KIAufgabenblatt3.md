# Aufgabenblatt 3

<sup>
Prof. Dr. Jürgen te Vrugt, Peter Weßeler M.Sc.
</sup>

Praktikum zum Modul Künstliche Intelligenz

## Ziele

In diesem Abschnitt schließen wir den Abschnitt „Problemlösen“ ab.

- Wir beschleunigen den Minimax-Algorithmus durch den Einsatz von Alpha-Beta-Pruning.
- Im A*-Algorithmus beobachten wir die Effizienzsteigerung durch den Einsatz geeigneter Kosten-Funktionen.
- Das Thema „Aussagenlogik“ wird als Grundlage logischer Agenten eingeführt.

---

## 🎓 Aufgabe P10 – Alpha-Beta-Pruning

Erweitern Sie Ihren Minimax-Algorithmus aus dem vorherigen Praktikum um das **Alpha-Beta-Pruning**. Erstellen Sie einen zusätzlichen Spieler, sodass der Minimax-Algorithmus auch gegen eine Version mit Alpha-Beta-Pruning antreten kann.

Vergleichen Sie das Verhalten der beiden Algorithmen und analysieren Sie dabei insbesondere:

- Ändert sich das Ergebnis der Suche?
- Ist der Effekt des Prunings messbar? Implementieren Sie geeignete Tests, um diese Aspekte zu demonstrieren.

---

## 🎓 Aufgabe P11 – A\* Suche
<center> 
  
  ![Beschreibung](res/Labyrinth.jpg)

*(Figure 1: Labyrinth als Bild)*
</center>

### Zielsetzung

Entwickeln Sie einen A\*-Algorithmus, der einen optimalen Pfad von einem Startpunkt (grün) zu einem Endpunkt (rot) in einem ASCII-Text-Labyrinth findet (vgl. Figure 1). Berücksichtigen Sie dabei unterschiedliche Kosten für das Betreten verschiedener Felder (Weiß, Hellgrau, Dunkelgrau, Weiß).

### 🎓 Aufgabe

#### Modellierung des Labyrinths

- Verwenden Sie die vorgegebene Textdatei (`maze_with_legend.txt`), die das Labyrinth in ASCII-Darstellung enthält.
- Wandeln Sie das vorgegebene Labyrinth in einen bidirektionalen Graphen um. Dieser soll zur A\*-Suche verwendet werden.

#### Kostendefinition für die Zelltypen

- Weißes Feld (`.`): Kosten = 1
- Hellgraues Feld (`H`): Kosten = 4
- Dunkelgraues Feld (`D`): Kosten = 10
- Hindernisse (`#`): **unpassierbar**
- Start (`S`) und Endpunkt (`E`) werden als freie Felder betrachtet, ohne zusätzliche Kosten.

#### Implementierung des A\*-Algorithmus

- Entwickeln Sie den A\*-Suchalgorithmus basierend auf den Vorlesungsunterlagen.
- Berechnen Sie die Gesamtkosten von Start (`S`) zu allen anderen passierbaren Feldern, um den kürzesten Pfad zum Ziel (`E`) zu bestimmen.
- Nutzen Sie eine geeignete Heuristik, um die Distanz zum Ziel effizient abzuschätzen.

#### Modellierung von Hindernissen

Stellen Sie sicher, dass die schwarzen bzw. `#`-Felder, die als unpassierbar gelten, korrekt modelliert werden, sodass der Algorithmus diese Felder nicht betritt.  
**Frage:** Wie gehen Sie dabei vor?

#### Ausgabe des Ergebnisses

- Präsentieren Sie den gefundenen Pfad als **Liste von Koordinaten**.
- *Optional:* Geben Sie die Gesamtkosten des Pfades an und visualisieren Sie den Pfad im ASCII-Labyrinth durch Ersetzung der Passierpfade beispielsweise durch `*`.

#### Dokumentation und Abgabe

- Dokumentieren Sie Ihr Vorgehen und die Modellierung des Graphen in einer `Log.md`-Datei, die die Struktur und die entscheidenden Schritte Ihrer Lösung beschreibt.
- *Optional:* Stellen Sie sicher, dass Sie auch andere Labyrinthe in ASCII-Darstellung einlesen können. Hierzu bekommen Sie hier alle 5 Minuten ein neues zufällig generiertes [Labyrinth](https://labyrinth-generator-047e43.fh-muenster.io/).

---

## 🎓 Aufgabe P12 – Aussagenlogik

Erstellen Sie die **Wahrheitstafel** zum folgenden Satz:

$$
(B \Rightarrow C) \land (A \Rightarrow B)
\;\Leftrightarrow\;
\neg (A \Rightarrow B) \lor \neg (B \Rightarrow C)
$$

- Handelt es sich um eine **Tautologie**? Begründen Sie ihre Feststellung.
- Laden Sie die vollständige Wahrheitstafel und ihre Antworten vorab in Ihrem Git-Repository hoch.
