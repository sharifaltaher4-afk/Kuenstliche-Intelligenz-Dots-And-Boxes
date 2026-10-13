# Dokumentation P6 – Analyse des Suchraums (Baum- vs. Graph-Suche)

## 1. Auswahl der Suchstruktur
Für die Implementierung des Unentschieden-Agenten im Spiel „Dots and Boxes“ haben wir uns für eine **Graph-Suche** entschieden.

## 2. Analyse des Suchraums
Der Suchraum von „Dots and Boxes“ weist eine extrem hohe **Pfad-Redundanz** auf. In einem Spiel mit 12 Kanten ist das Endergebnis (der Zustand des Spielfelds) unabhängig von der zeitlichen Abfolge, in der die Kanten platziert wurden.

### Beispielanalyse am iPad (4 Kanten einer Box):
Bei der Untersuchung einer einzelnen Box mit 4 Kanten haben wir folgende Komplexitätsunterschiede festgestellt:

| Tiefe | Baum-Knoten (Permutation $n!$) | Graph-Zustände (Kombination $\binom{n}{k}$) | Ersparnis |
| :--- | :--- | :--- | :--- |
| 0 | 1 | 1 | 0 |
| 1 | 4 | 4 | 0 |
| 2 | 12 | 6 | 6 |
| 3 | 24 | 4 | 20 |
| 4 | 24 | 1 | 23 |

**Erläuterung der Parameter:**
* **n:** Die Anzahl der betrachteten Kanten (hier 4 für eine Box).
* **k:** Die aktuelle Suchtiefe (Anzahl gesetzter Kanten).
* **n! (Fakultät):** Berechnet die Pfade im Baum (Reihenfolge ist relevant).
* **n über k (Binomialkoeffizient):** Berechnet die tatsächlichen Spielfeldkonstellationen im Graph (Reihenfolge ist irrelevant).

## 3. Begründung der Wahl
Die Entscheidung für die Graph-Suche basiert auf folgenden Abwägungen:

1. **Vermeidung von Redundanz:** Wie die Tabelle zeigt, würde eine Baum-Suche denselben Spielfeldzustand (z. B. eine geschlossene Box) 24-mal redundant evaluieren. Bei 12 Kanten würde die Anzahl der Pfade auf $12!$ (ca. 479 Mio.) ansteigen, während die Anzahl der Graph-Zustände bei maximal $2^{12} = 4096$ liegt.
2. **Effizienz:** Die Graph-Suche nutzt ein **Explored Set**, um bereits besuchte Zustände zu speichern. Dadurch wird die Rechenzeit massiv reduziert, was bei der Suche nach einem Unentschieden (Tiefe 12) entscheidend ist.
3. **Vorlesungskontext:** Gemäß Vorlesungsfolien (66 - 69) ist die Graph-Suche das geeignete Mittel, um in Zustandsräumen mit vielen redundanten Pfaden eine kombinatorische Explosion zu verhindern.

## 4. Unsere Entscheidung
Die Graph-Suche ermöglicht es dem Unentschieden-Agenten, den Zielzustand (2:2) nahezu direkt zu finden, da sie sich auf die Einzigartigkeit der Spielfeldzustände konzentriert anstatt auf die redundanten Wege dorthin.
