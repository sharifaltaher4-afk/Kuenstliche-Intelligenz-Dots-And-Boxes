import heapq


class Controller:

    def __init__(self, maze):
        self.maze_model = maze
        self.maze = maze.get_maze()
        self.width = maze.get_width()
        self.height = maze.get_height()

    def get_cost(self, x, y):
        field = self.maze[y][x]
        costs = {
            ".": 1,
            "H": 4,
            "D": 10,
            "S": 0,
            "E": 0
        }
        return costs[field]

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        for d_x, d_y in directions:

            nx = x + d_x
            ny = y + d_y


            if nx < 0 or ny < 0:
                continue

            if nx >= self.width or ny >= self.height:
                continue


            if self.maze[ny][nx] == "#":
                continue

            neighbors.append((nx, ny))

        return neighbors

    def find_start_end(self):
        return self.maze_model.find_start_end()

    def heuristic(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self):
        """
           Führt die A*-Suche von Start (S) nach Ziel (E) durch.
           Rückgabe: (pfad_als_koordinaten_liste, gesamte_pfadkosten)
           Falls kein Pfad existiert: (None, float('inf'))
        """

        # 1. Start- und Zielkoordinaten aus dem Labyrinth ermitteln
        start, goal = self.find_start_end()
        if start is None or goal is None: return None, float("inf")

        # 2. Datenstrukturen für den Algo. initialisieren
        #    frontier = Pioritätswarteschlange mit (geschätzte_Gesamtkosten, (x,y))
        frontier = []
        heapq.heappush(frontier, (0, start))


        #   Vorheriger Knoten Speichert für jeden Knoten den Vorgänger auf dem Pfad
        vorheriger_knoten = {}

        #   Bisherig Kosten g(x,y) = tatsächlichliche Kosten vom Start zu (x.y)
        bisherige_kosten = {start:0}

        #   geschätzte Gesamtkosten  f(x,y) = g(x,y) + heuristik(x,y)
        geschätzte_gesamtkosten = {start: self.heuristic(start[0], start[1], goal[0], goal[1])}

        explorierte_menge = set()

        # 3. Hauptschleife des Algo.
        while frontier:
            # Hole den Knoten mit dem niedrigesten f-Wert aus der Warteschlange
            aktuelle_geschätzte_kosten, aktueller_knoten = heapq.heappop(frontier)

            # Ziel erreicht ? -> Pfad rekonstruieren und zurückgeben
            if aktueller_knoten == goal:
                # Pfad von start bis zum Ziel durch Rückverfolgung der Vorgänger erstellen
                pfad = []
                while aktueller_knoten in vorheriger_knoten:
                    pfad.append(aktueller_knoten)
                    aktueller_knoten = vorheriger_knoten[aktueller_knoten]
                pfad.append(start)
                pfad.reverse()
                gesamte_kosten = bisherige_kosten[goal]
                return  pfad, gesamte_kosten
            # Wenn der Knote schon expandiert wurde, überspringe
            if aktueller_knoten in explorierte_menge:
                continue

            # aktueller Knote als expandiert makieren
            explorierte_menge.add(aktueller_knoten)

            # alle Nachbarn des aktuellen Knotens untersuchen
            for nachbar_x, nachbar_y in self.get_neighbors(aktueller_knoten[0],aktueller_knoten[1]):
                nachbar = (nachbar_x, nachbar_y)

                #Nachbarn die bereits expandiert wurden, ignorieren
                if nachbar in explorierte_menge:
                    continue

                # berechne die Kosten, um vom Start über den aktuellen Kosten zum Nachbarn zu gelangen
                kosten_schritt = self.get_cost(nachbar_x, nachbar_y)
                neue_bisherige_kosten = bisherige_kosten[aktueller_knoten]+kosten_schritt

                # wenn der Nachbar noch nicht in der frontier ist oder ein besserer Pfad gefunden wurde
                if nachbar not in bisherige_kosten or neue_bisherige_kosten<bisherige_kosten[nachbar]:
                    # Vorgänger aktualisieren
                    vorheriger_knoten[nachbar] = aktueller_knoten
                    # Tatsächliche Kosten aktualiseren
                    bisherige_kosten[nachbar] = neue_bisherige_kosten
                    # Heuristik für den Nachbarn berehcnen
                    heuristik_wert = self.heuristic(nachbar_x, nachbar_y,goal[0], goal[1])

                    # Gesamte f-Wert = g+h
                    f_wert = neue_bisherige_kosten+heuristik_wert
                    geschätzte_gesamtkosten[nachbar] = f_wert

                    #Nachbarn in die Prioritätswarteschlange hinzufügen(oder mit besserm Wert aktualisieren
                    heapq.heappush(frontier, (f_wert, nachbar))

        # 4. Falls die frontier leer wird, gibt es keinen Pfad
        print("Kein Pfad vom Start nach Ziel gefunden")
        return None, float("inf")

























