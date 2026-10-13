# Aufgabenblatt 2  - SoSe26

<sup>
Prof. Dr. Jürgen te Vrugt, Peter Weßeler M.Sc.
</sup>

Praktikum zum Modul Künstliche Intelligenz


## Ziele

- In diesem Praktikum werden Suchalgorithmen praktisch eingesetzt. Diese bilden die Grundlage für eine Vielzahl klassischer KI-Anwendungen.
- Sie betrachten sowohl einen einzelnen Agenten als auch ein Multi-Agenten-System.

> :information_source: **Hinweis:**  
> Die Aufgaben der Aufgabenblätter 1 und 2 bauen aufeinander auf. Beide enthalten Hinweise und Vorgehensweisen, die die erfolgreiche Bearbeitung unterstützen sollen.  
> *Lesen Sie die Aufgabenstellung sorgfältig durch und berücksichtigen Sie die Inhalte der Vorlesung!*

---

## :mortar_board: Aufgabe P5 – Problembeschreibung

Modellieren Sie das Spiel **„Dots and Boxes“** als ein Problembeschreibung (vgl. Vorlesung) und entwerfen Sie einen Agenten, der die Züge sowohl für den Spieler in **Grün** als auch in **Rot** ausführt.

Beachten Sie dabei folgende Vorgaben:

- In dieser Aufgabe konzentrieren Sie sich auf Zustände, Aktionen usw., **ohne** den kompetitiven Charakter des Spiels zu berücksichtigen.
- Beschreiben Sie die Zustände und ihre Aktionen detailliert und geben Sie die Anzahl der möglichen Aktionen abhängig vom Zustand an.
- Das Ziel ist, einen Spielzustand **„unentschieden“** zu erreichen, wobei abwechselnd die Kanten *Grün* und *Rot* auf dem Spielfeld platziert werden.  
  Erläutern Sie anhand eines Beispielpfades im Suchraum, wie der Zustand „unentschieden“ erreicht werden kann.
- Ersetzen Sie die zwei Spieler durch **einen „Unentschieden-Agenten“**, der die Spielzüge beider Spieler übernimmt.

### Dokumentation

Erstellen Sie hierzu eine Dokumentation, die sich an der Beschreibung eines Problems gemäß der Vorlesung orientiert.
Laden Sie Ihre Dokumentation vorab in Ihrem Git-Repository unter `docs/` hoch.   

---

## :mortar_board: Aufgabe P6 – Baum- vs. Graph-Suche[^1]

Wählen Sie eine geeignete Struktur des Suchraums für das Problem aus der vorangegangenen Aufgabe:

- Entscheiden Sie sich entweder für eine **Baum-** oder **Graph-Suche**.
- Analysieren Sie, welche Struktur der Suchraum im Spiel „Dots and Boxes“ aufweist, und begründen Sie Ihre Wahl der Suchmethode.

### Dokumentation

*Dokumentieren Sie diese Überlegungen ebenfalls und laden Sie Ihre Notizen vorab ins Git-Repository hoch.*

---

> :information_source: **Hinweise:**
> - In den nun folgenden Aufgaben des Aufgabenblattes ist **keine** Dokumentation im Git bereitzustellen.  
  Wir weisen in den Aufgabenstellungen explizit darauf hin, wenn eine Dokumentation im Git bereitzustellen ist.
> - Achten Sie weiterhin auf die Dokumentation Ihres Codes und die Erstellung eines Changelogs.
> - Ihre Dokumentation sollte unter anderem die Diskussion Ihrer Lösung unterstützen.  
  Sie können die Dokumentation beispielsweise nutzen, um den grundlegenden Ablauf und die Struktur eines Algorithmus darzustellen.

---

## :mortar_board: Aufgabe P7 – Uninformierte Suche

Realisieren Sie den **Uniform-Cost-Search**-Algorithmus:

- Achten Sie auf ein objektorientiertes Design unter Beachtung der gegebenen Interfaces, um die Suche in Ihrem „Dots and Boxes“-Spiel des vorherigen Aufgabenblatts einsetzen zu können.  
  Erstellen Sie hierfür einen geeigneten neuen Controller, der sowohl **grüne** als auch **rote** Kanten setzen kann.
- Implementieren Sie die Uniform-Cost-Search als **Baum-** bzw. **Graph-Suche**, entsprechend Ihrer Wahl in der vorherigen Aufgabe.  
  Achten Sie darauf, die Funktion der Pfadkosten geeignet zu formulieren und in Ihre Klasse zu integrieren.
- Integrieren Sie den Algorithmus in Ihr „Dots and Boxes“-Spiel.

> :information_source: **Hinweise**
> - Dieser Algorithmus ist für das Spiel „Dots and Boxes“ mit den üblichen Spielregeln nur eingeschränkt geeignet, da es **kein Multi-Player-Algorithmus** ist.
> - Orientieren Sie sich bei der Implementierung des Uniform-Cost-Search-Algorithmus an der Variante, die in der Vorlesung vorgestellt wurde.
> - Sollten Sie von der Vorlesungsvariante abweichen (z. B. Verwendung einer Variante aus einer Internet-Recherche), so zeigen Sie die Gemeinsamkeiten und Unterschiede der Variante auf.  
  Solche Abweichungen dokumentieren Sie **vorab im Code**.
> - Beachten Sie, dass in dieser Aufgabe der Agent sowohl die Züge des Spielers **„grün“** als auch des Spielers **„rot“** übernimmt und das Ziel des Spiels der Zustand **„unentschieden“** ist.

### Optionale Variante der Lösung

Führen Sie den ersten Spielzug **zufällig** aus, anstatt den Zug durch den Algorithmus auswählen zu lassen.  
*Was bewirkt diese Änderung?*

---

## :mortar_board: Aufgabe P8 – Minimax-Suche

Zuvor haben Sie einen Agenten betrachtet, der das Ziel „unentschieden“ verfolgt.  
In dieser Aufgabe orientieren wir uns an den traditionellen Spielregeln von „Dots and Boxes“, bei denen zwei kompetitive Spieler jeweils den Sieg anstreben.  
Eine **Multi-Agenten-Lösung** ist hier besonders geeignet.

- Implementieren Sie den **Minimax-Algorithmus** gemäß der Vorlesung und erweitern Sie Ihre Spieler um diesen Algorithmus, sodass der nächste Zug mithilfe von Minimax ermittelt wird.  
  Ihre Spieler können in beliebiger Kombination sein:
  - menschliche Mitspieler
  - Zufalls-NPCs
  - Minimax-NPCs
- Überlegen Sie, welcher Spieler in jedem Spielzug der **minimierende** bzw. **maximierende** Spieler ist, um den Minimax-Algorithmus effektiv anzuwenden.  
  Generieren Sie den Spielbaum oder -graphen rekursiv, indem Sie alle möglichen Züge für jeden Brettzustand analysieren.  
  Verwenden Sie bei Erreichen eines Endzustands passende Werte für:
  - „gewonnen“
  - „verloren“
  - „unentschieden“
- Die Berechnung eines Spielzugs durch den Minimax-Algorithmus basiert auf der Auswahl eines Pfades durch den Suchraum.  
  Geben Sie für **jeden Spielzug** die zugehörigen Zustände („Knoten“, siehe Aufgabe „Problembeschreibung“) des gewählten Pfades an.

> :information_source: **Hinweis:**  
> Es kann notwendig sein, das Spielfeld mit einigen Kanten vorzubelegen. – Überlegen Sie: *Warum?*

---

## :mortar_board: Aufgabe P9 – Übertragung

Welche Schritte sind notwendig, um den Minimax-Algorithmus auf das Spiel **„Vier gewinnt“** anzuwenden?

- Überlegen Sie sich vor dem Praktikum die notwendigen Änderungen.
- Eine **verbale Erläuterung** auf Grundlage geeigneter Notizen im Praktikum ist ausreichend – eine Implementierung ist **nicht erforderlich**.

---

[^1]: Mathematisch gesehen ist ein Baum ein spezieller Graph. Um hier die Sprechweise vereinfachen zu können, verwenden wir für „Baum“ und „Graph“ die Definitionen des Moduls *Diskrete Strukturen*, wobei wir bei Graphen explizit die Betrachtung von Graphen einschließen, die **keine** Bäume. 
