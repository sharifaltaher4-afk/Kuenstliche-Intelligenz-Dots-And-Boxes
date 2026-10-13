# Changelog

## 19.05.2026
### Hinzugefügt
- **Alpha-Beta-Pruning (Aufgabe P10):**
  - Implementierung der Klasse `AlphaBetaAgent` in `alphabeta_agent.py` zur Beschleunigung des Minimax-Suchraums.
  - Integration von Alpha-Beta-Grenzberechnungen (`alpha`, `beta`) in die rekursiven Funktionen `max_value` und `min_value` gemäß der Vorlesungsfolien.
  - Implementierung eines neuen NPCs (`MinimaxNPC_withalpha_beta`) in `game_model.py`.
  - Hinzufügen der interaktiven CLI-Demo-Option `4. minimax-WithAlphaBeta` in `controller.py` zum direkten Leistungsvergleich.
- **Knoten-Zähler für Performance-Analysen:**
  - Tracking der expandierten Zustände (`self.nodes_expanded`), um den Optimierungseffekt des Prunings quantitativ messbar zu machen.

### Geändert
- **Refactoring des Suchalgorithmus:**
  - Anpassung der Alpha-Beta-Struktur an den exakten Pseudocode der Vorlesung.

## 29.04.2026 
## P8 – Informierte Suche & Spiele (Minimax-Algorithmus)

### 1. Implementierung des Minimax-Agenten
Für die strategische Spielsteuerung wurde ein **Minimax-Agent** implementiert, der in der Lage ist, das Spielende durch eine vollständige Exploration des Zustandsraums vorauszuberechnen.

#### Algorithmus-Details:
* **Entscheidungsmodell:** Implementierung von `MINIMAX-DECISION`, `MAX-VALUE` und `MIN-VALUE` gemäß der Vorlesung (Russell & Norvig).
* **Zusatzzüge:** Die Logik wurde so erweitert, dass der Agent bei einem Punktgewinn (Box geschlossen) innerhalb der Rekursion einen weiteren Zug auf derselben Hierarchieebene (`MAX` bleibt `MAX`) ausführt.
* **Utility-Funktion:** Bewertung der Endzustände durch die Punktedifferenz (`Eigene Punkte - Gegnerische Punkte`).

### 2. Integration & Simulation
* **Zustandssimulation:** Der Agent nutzt die `copy()`-Methode des `GraphController`, um "Parallelwelten" zu erschaffen. Züge werden dort virtuell ausgeführt, um deren Konsequenzen zu bewerten, ohne das echte Spiel zu beeinflussen.
* **Dummy-Player:** Einsatz einer leichten Hilfsklasse innerhalb der Simulation, um die `check_box`-Logik des Controllers ohne Overhead zu bedienen.
* **Pfad-Vorhersage:** Der Agent gibt nicht nur den besten nächsten Zug zurück, sondern den gesamten optimalen Pfad bis zum Spielende.

### 3. Komplexitätsanalyse & Performance-Tests
Im Rahmen der Implementierung wurde die exponentielle Zunahme der Rechenzeit (Fakultät der verbleibenden Züge) analysiert und dokumentiert:

* **Szenario A (10 freie Kanten):** Rechenzeit ca. **120 Sekunden** ($10! \approx 3,6$ Mio. Pfade).
* **Szenario B (9 freie Kanten):** Rechenzeit ca. **14 Sekunden** ($9! \approx 362.880$ Pfade).
* **Szenario C (8 freie Kanten):** Rechenzeit ca. **2 Sekunden** ($8! \approx 40.320$ Pfade).
* **Szenario D (6 freie Kanten):** Rechenzeit **< 0,1 Sekunden** ($6! = 720$ Pfade).


### Behoben / Verbessert
* **Farben-Kompatibilität:** Umstellung der Vorbelegungs-Farbe von `gray` auf `white`, um Abstürze in der `termcolor`-Bibliothek zu verhindern.



## 22.04.2026 
## P7 – Uninformierte Suche (Uniform Cost Search)

### 1. Implementierung des Algorithmus
Für die Suche nach dem Unentschieden-Zustand (2:2) wurde der **Uniform Cost Search (UCS)** Algorithmus nach der Vorlesungsvariante (Russell & Norvig) implementiert. 

#### Algorithmus-Details:
* **Struktur:** Graph-Suche unter Verwendung eines `explored`-Sets zur Vermeidung von Pfadredundanz.
* **Frontier:** Priority Queue (`heapq`), sortiert nach den aufsummierten Pfadkosten $g(n)$.
* **Zustandsrepräsentation:** Ein eindeutiger Hash-Wert, basierend auf dem sortierten Tupel der Koordinaten aller aktuell gesetzten Kanten.

### 2. Pfadkosten und Zielzustand
* **Pfadkosten $g(n)$:** Jede Aktion (das Setzen einer Kante) wird mit Kosten von **1** gewichtet. Die Gesamtkosten eines Knotens entsprechen somit der Anzahl der Spielzüge.
* **Zieltest (Goal Test):** Der Zustand ist ein Zielzustand, wenn das Spiel beendet ist (`len(boxes) == 4`) und beide Spieler (Bot A und Bot B) jeweils exakt **2 Punkte** erzielt haben.

### 3. Optimierungen und Performance
Um die kombinatorische Explosion und die Laufzeitbeschränkungen von Python zu bewältigen, wurden folgende Optimierungen vorgenommen:

1.  **Manuelle Objekt-Kopie:** Statt der langsamen `deepcopy()`-Funktion wurde eine spezifische `copy()`-Methode im Model implementiert, die nur die für die Suche relevanten Datenstrukturen dupliziert.
2.  **Transpositions-Management:** Durch die Graph-Suche konnte der Suchraum von theoretisch $12!$ (ca. 479 Mio. Pfade) auf die tatsächlich untersuchten **24.568 Knoten** reduziert werden.
3.  **Silent Execution:** Konsolenausgaben wurden während der Suche unterdrückt, um die Verzögerung durch Textausgaben zu verhindern.

### Testergebnis:
* **Geprüfte Knoten:** 24.568
* **Rechenzeit:** ca. 3,86 Sekunden
* **Ergebnis:** Der Agent findet zuverlässig einen Pfad von 12 Zügen, der zu einem 2:2 Unentschieden führt.

### 4. Abweichungen von der Vorlesung
Es wurde strikt die Graph-Such-Variante aus der Vorlesung verwendet. Eine Besonderheit ist die Nutzung eines `unique_id_counters` innerhalb der Priority Queue, um einen stabilen Vergleich der Knoten-Tupel in Python zu gewährleisten, falls zwei Pfade identische Kosten aufweisen.



## 2026-04-21 
### Hinzugefügt
- **P6:** Dokumentation der Suchraumanalyse abgeschlossen.



## 21.04.2026 - Synchronisation & Formale Modellierung (Blatt 2)
### Hinzugefügt
- **Aufgabe P5:** Formale Problembeschreibung für das "Dots and Boxes" Unentschieden-Problem erstellt (`docs/p5_problembeschreibung.md`).
- **Beispielpfad:** Konkrete Zugsequenz (Tiefe 12) aus dem Programm-Logs auf der Console dokumentiert, die zu einem 2:2 führt.
- **Konzept:** Definition des "Unentschieden-Agenten" als Single-Agent-Suchproblem dokumentiert.

### Technisches
- Branch `aufgabe_p5` erstellt und für das Abtestat vorbereitet.

## 14.04.2026
### Hinzugefügt
- **Non-Player-Character (NPC):** Integration eines computergesteuerten Gegners, der automatisiert valide Spielzüge ausführt.
- **Abstrakte Spieler-Struktur:** Umstellung auf eine objektorientierte Basisklasse für Spieler, die einen nahtlosen Wechsel zwischen menschlichen Spielern und NPCs ermöglicht.
- **Dynamische Kanten-Vorauswahl:** Neue Funktion zur Ermittlung aller aktuell verfügbaren Kanten, um sicherzustellen, dass der NPC nur gültige Züge wählt.

### Verbessert / Behoben
- **Ungerichtete Graphen-Logik:** Die Kanten-Aktivierung in `__select_edge` wurde korrigiert, sodass eine Verbindung nun in beide Richtungen (A-B und B-A) gleichzeitig als besetzt markiert wird.
- **NPC-Validierung:** Ein Fehler wurde behoben, durch den der NPC zuvor bereits gewählte Kanten in entgegengesetzter Richtung (z.B. erst 4-1, dann 1-4) wählen konnte.
- **Korrektur Doppelzug-Logik:** Sicherstellung, dass auch der NPC korrekt einen Bonus-Zug erhält, sobald er eine Box schließt.




## 13.04.2026
### Hinzugefügt
- **Doppel-Box-Erkennung:** Die Logik wurde so erweitert, dass ein einziger Spielzug zwei Boxen gleichzeitig schließen kann und der Spieler somit 2 Punkte erhält.
- **Unit-Test für Doppel-Boxen:** Ein neuer Testfall wurde hinzugefügt, um sicherzustellen, dass die gleichzeitige Vergabe von zwei Punkten bei einer gemeinsamen Mittellinie fehlerfrei funktioniert.
- **Detaillierte Spielend-Statistik:** Nach Abschluss aller Boxen werden nun die finalen Punktestände beider Spieler sowie der Gewinner (oder ein Unentschieden) explizit ausgegeben.
- **Umfassende Dokumentation:** Fachspezifische Docstrings und Inline-Kommentare im `GraphController` zur Erklärung der Grid-Logik und Kanten-Validierung hinzugefügt.

### Verbessert / Behoben
- **Optimierte Box-Logik:** Die `check_box`-Funktion wurde effizienter gestaltet, um die Rückgabe der exakten Anzahl neu geschlossener Boxen als Integer-Wert zu ermöglichen.
- **Stabilität der Spielschleife:** Die `is_game_over`-Prüfung erfolgt jetzt sofort nach jedem Punktgewinn, wodurch unnötige Eingabeaufforderungen nach dem letzten Zug eliminiert wurden.
- **Korrektur Box-Koordinaten:** Die Eckpunkt-Reihenfolge in der `possible_boxes`-Liste wurde korrigiert, sodass alle Felder im 3x3-Raster funktioniert



## 12.04.2026
### Hinzugefügt:
- Testdatei hinzugefügt
- Neue Testfunktionen hinzugefügt, um Kanten, Boxen und Spielende zu prüfen

### Behoben:
- Bug in spielerinput-Funktion behoben




## 11.04.2026
### Hinzugefügt:
- Erkennung von Boxen
- Speicherung der Boxen in controller.boxes, um zu prüfen, ob eine Box bereits erstellt wurde
- Punktesystem für Spieler
- Spiel beenden hinzugefügt
- Validierung der Eingaben hinzugefügt
- Debug-Ausgaben entfernt

### Behoben:
- Fehler in check_box-Funktion (hat immer True zurückgegeben)
