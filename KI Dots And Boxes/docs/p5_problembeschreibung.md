# Dokumentation P5 – Formale Problembeschreibung

Basierend auf der Vorlesung KI3 (Folie 61 und 62) und Literatur Russel/Norvig, wird das Spiel „Dots and Boxes“ für den Unentschieden-Agenten wie folgt definiert:

## Problemkomponenten
* **Ausgangszustand (Initial State):** Wo der Agent beginnt. Also: Ein leeres 3x3 Punkteraster (keine Kanten gesetzt). Punktestand 0:0.
* **Aktionen (Actions):** Aktionen, die dem Agenten zur Verfügung stehen. Für einen geg. Zustand $s$ gibt die Funktion $ACTIONS(s)$ die Menge der Aktionen zurück, die sich in $s$ ausführen lassen bzw. in $s$ anwendbar sind. Alos: Das Setzen einer bisher unbesetzten Kante (insgesamt 12 Kanten möglich).
* **Überführungsmodell (Transition Model):** Eine Beschreibung was jede Aktion bewirkt, durch eine Funktion $RESULT(s, a)$ spezifiziert, die den Zustand zurückgibt, der von der Ausführung der Aktion $a$ im Zustand $s$ resultiert. Also: Diese Funktion liefert den Folgezustand, in dem die gewählte Kante besetzt ist. Wird eine Box geschlossen, erhält der Spieler einen Punkt und darf erneut ziehen.
* **Zieltest (Goal Test):** Alle 12 Kanten sind gesetzt UND der Punktestand beträgt exakt 2:2 (Unentschieden).
* **Pfadkosten (Path Cost):** Ist die Funktion, die jedem Pfad einen nummerischen Wert zuweist. Alos Jede Aktion (Kante setzen) hat die Kosten 1. Ein vollständiger Pfad zum Ziel hat Gesamtkosten von 12.

### Konkreter Beispielpfad im Suchraum (Tiefe 12)

Der folgende Pfad beschreibt eine erfolgreiche Sequenz von 12 Aktionen, die zu einem Unentschieden (2:2) führt. Die Knotenpunkte sind von 0 bis 8 durchnummeriert.

| Zug | Akteur | Kante (Punkte) | Status / Effekt | Stand (A:B) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Bot A | 2 - 5 | Vertikal (rechts-oben) | 0:0 |
| 2 | Bot B | 3 - 6 | Vertikal (links-unten) | 0:0 |
| 3 | Bot A | 4 - 7 | Vertikal (mitte-unten) | 0:0 |
| 4 | Bot B | 1 - 4 | Vertikal (mitte-oben) | 0:0 |
| 5 | Bot A | 4 - 5 | Horizontal (mitte-rechts) | 0:0 |
| 6 | Bot B | 3 - 4 | Horizontal (mitte-links) | 0:0 |
| 7 | Bot A | 5 - 8 | Vertikal (rechts-unten) | 0:0 |
| 8 | Bot B | 7 - 8 | Horizontal (unten-rechts) -> **Box unten rechts** | 0:1 |
| 9* | Bot B | 6 - 7 | Horizontal (unten-links) -> **Box unten links** | 0:2 |
| 10 | Bot B | 0 - 3 | Vertikal (links-oben) | 0:2 |
| 11 | Bot A | 1 - 2 | Horizontal (oben-rechts) -> **Box oben rechts** | 1:2 |
| 12* | Bot A | 0 - 1 | Horizontal (oben-links) -> **Box oben links** | 2:2 |

*\*Zusatzzug nach Schließen einer Box.*

**Analyse des Pfades:**
Der Pfad hat eine Länge von 12 Kantenplatzierungen (Pfadkosten = 12). Er demonstriert die kooperative Natur des Unentschieden-Agenten, da Bot B in Zug 10 eine Kante wählt, die es Bot A ermöglicht, in den verbleibenden Zügen 11 und 12 ebenfalls zwei Boxen zu schließen.