# Log – A*-Suche im Labyrinth

## Vorgehen

1. **Einlesen des Labyrinths**  
   Die Datei `maze_with_legend.txt` wird zeilenweise gelesen.  
   Die ersten Zeilen bis zur Zeile "Legend" enthalten das Gitter.  
   Die Dimensionen werden aus der Zeile "Dimensions: 10 x 10" ausgelesen.

   2. **Modellierung des Graphen**  
      - Jede begehbare Zelle (`.` , `H` , `D` , `S` , `E`) ist ein **Knoten**.  
      - Hindernisse (`#`) sind **nicht begehbar**.  
      - **Kanten** entstehen durch 4‑Nachbarschaft (oben, unten, links, rechts).  
      - Der Graph ist **bidirektional**: Von A nach B und B nach A möglich.  
      - Die **Kosten** sind zelltypspezifisch:  
        Kostendefinition (laut Aufgabenstellung)

        - `.` (freier Pfad) – Kosten 1

        - `H` (hellgraue Spezialzelle) – Kosten 4

        - `D` (dunkelgraue Spezialzelle) – Kosten 10

        - `#` (Hindernis) – nicht passierbar

        - `S` (Start) und `E` (Ziel) – keine Kosten (0)
     
        Implementiert in Controller.get_cost(). 
        Diese Kosten werden im A*-Algorithmus als Schrittkosten verwendet (g(n)).
        Die Heuristik (Manhattan-Distanz) ist zulässig, weil die minimalen Schrittkosten 1 betragen.

3. **A*-Algorithmus**  
   - **Heuristik:** Manhattan‑Distanz (zulässig, da minimaler Schrittkosten 1).  
   - **Prioritätswarteschlange:** `heapq` nach `f = g + h`.  
   - **Geschlossene Menge** (`explorierte_menge`) verhindert Zyklen.  
   - **Pfadrekonstruktion** über `vorheriger_knoten`‑Dictionary.

4. **Hindernisbehandlung**  
   In `get_neighbors()` werden Nachbarn, die `#` enthalten, ignoriert.  
   Der Algorithmus betritt diese Felder nie.

5. **Ausgabe**  
   - Koordinatenliste des Pfades.  
   - Gesamtkosten.  
   - Optional: Visualisierung des Pfades im Labyrinth mit `*`.

## Entscheidende Schritte

- `create_field()` extrahiert das Gitter aus der Datei.  
- `get_cost()` liefert die Schrittkosten.  
- `heuristic()` = Manhattan‑Distanz.  
- `a_star()` implementiert die A*-Graphsuche.

## Anmerkungen

- Der Algorithmus findet immer den **optimalen** Pfad, da die Heuristik zulässig ist.  
- Das Labyrinth kann ausgetauscht werden, indem der Pfad in `reader.read()` geändert wird (zB. als Kommandozeilenargument).
- So kann man das Programm mit python reader.py maze_andere.txt aufrufen und jedes beliebige ASCII‑Labyrinth im gleichen Format einlesen.