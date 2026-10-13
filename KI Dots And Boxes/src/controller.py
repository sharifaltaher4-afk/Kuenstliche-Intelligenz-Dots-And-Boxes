from model import Graph, Point, Edge
from view import GameView
from game_model import Player, HumanPlayer, RandomNPC, MinimaxNPC
from minimax_agent import MinimaxAgent
from game_model import Player, RandomNPC,MinimaxNPC_withalpha_beta
from UCSController import UCSDrawAgent
import random

class GraphController:
    """
   Spezifische Logik für ein Spiel, das ein 5x5-Grid verwendet.
    Nutzt intern einen allgemeinen Graphen (GameGraph).
    Angenommen, bei einem 5x5-Raster (UI-Raster mit Knoten und Kanten) ergeben sich 9 Knoten, die folgendermaßen
    angeordnet sind (zeilenweise):
    0   1   2
    3   4   5
    6   7   8

    Attribute:
        -graph (Graph): Repräsentiert das Spielfeld als Graph aus Knoten und Verbindungen.
        -grid_size (int): Größe des Gitters (z.B. 5 für ein 5x5-Grid).
        -boxes (list): Liste aller bereits geschlossenen Boxen inklusive deren Position, Besitzer.
        -last_selected_edge (Edge oder None): Speichert die zuletzt ausgewählte Verbindung.


    Funktionen:
        is_game_over() return bool:
            Prüft, ob das Spiel beendet ist (alle Boxen wurden geschlossen).
        setup_grid() return None:
            Erstellt das Spielfeld, indem Punkte im Spielfeld erzeugt werden.
        add_edges() return None:
            Verbindet die Knoten mit gültigen Kanten entsprechend der Spiellogik.
        __select_edge(a: Point, b: Point, color: str) return bool:
            Interne Methode zum Auswählen einer Verbindung zwischen zwei Punkten. Verhindert doppelte Auswahl und markiert die Kante als belegt.
        select_edge_point_number(a: int, b: int, color: str) return bool:
            Öffentliche Schnittstelle zur Kantenauswahl über Punkt-Indizes. Prüft Eingaben und übergibt an __select_edge.
        check_box(current_player: Player) return int:
            Überprüft, ob durch den letzten Zug neue Boxen entstanden sind. Gibt die Anzahl der neu geschlossenen Boxen zurück.
        get_all_available_edges() return list:
            Liefert alle noch verfügbaren Verbindungen als Indexpaare.
        copy() return GraphController:
            Erstellt eine Kopie des aktuellen Spielzustands (Graph und Boxen).

   """


    def is_game_over(self):
        """
        funktion zum beenden des Spieles
        """
        ##print(self.boxes)

        return len(self.boxes) == 4


    def __init__(self, grid_size: int = 5) -> None:
        self.graph = Graph()
        self.grid_size = grid_size
        self.boxes = []
        self.last_seleced_edge = None
        self.setup_grid()

    #"Geburt" des Spielfelds.
    def setup_grid(self) -> None:
        """die Methode geht wie ein Scanner duch ein 5X5 Gitter.
         i -> Zeilen (von oben nach unten)
         j -> Spalten
         durch das Gerade Zahlen Filter können wir die Knoten nur auf gerade die Koordinaten(0,2,4) erstellen
         dies schafft platz für Lücken für die Linien und Boxen auf ungeraden Positionen(1,3)
         """
        box_to_player = {}

        point_index = 0
        # Knoten an den "geraden" Positionen hinzufügen.
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                #Erstelle einen Punkt nur, wenn Zeile und Spalte gerade sind
                if i % 2 == 0 and j % 2 == 0:
                    node = Point((i, j), f"P{point_index}")
                    self.graph.add_node(node) # füge einen Punkt zum Graphen hinzu
                    point_index += 1 #im Letzten durchlauf wird zu 9
        self.add_edges() # Nach dem alle Punkte stehen, werden die erlaubte Verbindungen(Kanten) definiert

    def add_edges(self) -> None:
        """Diese Funktion baut das Skellet des Spiels zusammen.
            Hier wenden die Punkte(Knoten) mit den möglichen Linien(Edges) verbunden.
            Ohne diese Funktion, gäbe nur Punkte im Raum aber keine einzige Linie gezogen

            Warum nur eine Richtung ? das liegt daran dass die Funktion add_edge im Model schlau ist, und die
            Verbindungen für beide Richtungen im Dictionary speichert -> ungerichten Graph
            """
        points = self.graph.nodes
        #Nur fortfahren, wenn das 3x3 Gitter komplett ist
        if len(points) == 9:# Schutz gegen IndexError Was ist wenn man das Spielfeld später Skallieren möchte ? (Hardcodiert)
            #Manuelle und gezielte Def. der Kanten.
            #12 Kanten
            edges = [
                Edge(points[0], points[1]), Edge(points[0], points[3]),
                Edge(points[1], points[2]), Edge(points[1], points[4]),
                Edge(points[2], points[5]), Edge(points[3], points[4]),
                Edge(points[3], points[6]), Edge(points[4], points[5]),
                Edge(points[4], points[7]), Edge(points[5], points[8]),
                Edge(points[6], points[7]), Edge(points[7], points[8])
            ]
            # Jede definierte Kante im Graph-Model (Adjazenzliste) registrieren
            for edge in edges:
                self.graph.add_edge(edge.point_one, edge.point_two)

    def __select_edge(self, a: Point, b: Point, color: str) -> bool:
        """
        Sucht die Kante im Graphen und aktiviert sie in beide Richtungen.
        Verhindert, dass eine Linie (z.B 1-4) doppelt gezogen wird
        nur weil die Punkte vertauscht wurden (4-1).
        """
        edges = self.graph.get_edges()
        target_edge = None

        # 1. Schritt: Prüfen, ob die Kante in irgendeiner Richtung bereits gewählt wurde
        for e in edges:
            # Prüft A-B oder B-A
            if (e.point_one == a and e.point_two == b) or (e.point_one == b and e.point_two == a):
                if e.selected:
                    print("Diese Verbindung wurde bereits gewählt")
                    return False
                target_edge = e  # Wir merken uns eine Instanz für die Rückgabe

        # 2. Schritt: Wenn wir hier sind, ist die Kante frei. Jetzt beide Richtungen markieren
        if target_edge:
            for e in edges:
                if (e.point_one == a and e.point_two == b) or (e.point_one == b and e.point_two == a):
                    e.select(color)

            # Wichtig für die Box-Prüfung, Die zuletzt gewählte Kante speichern
            self.last_seleced_edge = target_edge
            return True

        print("Keine gültige Verbindung zwischen diesen Punkten.")
        return False

    def select_edge_point_number(self, a: int, b: int, color: str):
        """Diese Funktion ist der Übersetzer, sie nimmt die zahlen a und b
        von User Eingabe und schlägt in der Hauptlist nodes nach , welche Point-Objecte
        dazu gehören. Dies geschiht später duch das einreichen an __select_edge"""

        if a < 0 or b < 0 or a > 8 or b >8:
            print("Ungültige Eingabe")
            return False
        if a == b:
            print("Zweimal gleicher Punkt")
            return False
        return self.__select_edge(self.graph.nodes[a],self.graph.nodes[b],color)

    def check_box(self, current_player: Player) -> int:
        """
        Prüft auf neu geschlossene Boxen und verknüpft sie direkt mit dem Spieler-Objekt.
        """
        temp = [e for e in self.graph.get_edges() if e.selected]

        possible_boxes = [
            ([0, 1, 3, 4], "oben links"),
            ([1, 2, 4, 5], "oben rechts"),
            ([3, 4, 6, 7], "unten links"),
            ([4, 5, 7, 8], "unten rechts")
        ]

        in_diesem_zug_gebildete_boxen = 0

        def has_edge(a, b):
            for e in temp:
                if ((e.point_one == self.graph.nodes[a] and e.point_two == self.graph.nodes[b]) or
                        (e.point_one == self.graph.nodes[b] and e.point_two == self.graph.nodes[a])):
                    return True
            return False

        for box_points, richtung_der_geschlossenen_box in possible_boxes:
            if has_edge(box_points[0], box_points[1]) and \
                    has_edge(box_points[2], box_points[3]) and \
                    has_edge(box_points[0], box_points[2]) and \
                    has_edge(box_points[1], box_points[3]):

                # Prüfen, ob Box bereits existiert
                if box_points not in [b["points"] for b in self.boxes]:
                    # Wir nehmen den ersten Buchstaben des Namens vom Spieler-Objekt
                    char = current_player.name[-1].upper()

                    # Berechne die visuelle Mitte (ungerade Koordinaten im 5x5 Grid)
                    row = self.graph.nodes[box_points[0]].position[0] + 1 # Position
                    col = self.graph.nodes[box_points[0]].position[1] + 1

                    self.boxes.append({
                        "points": box_points,# Eckpunkte der Box
                        "center": (row, col),# Mitte der Box
                        "char": char, # Spieler Tag
                        "color": current_player.color  # Farbe direkt vom Spieler
                    })

                    #print(f"Box geschlossen: {richtung_der_geschlossenen_box}")
                    in_diesem_zug_gebildete_boxen += 1

        return in_diesem_zug_gebildete_boxen

    def get_all_available_edges(self):
        """Gibt eine Liste von Indizes (a, b) für alle noch nicht gewählten Kanten zurück"""
        available = []
        seen_connections = set()  # Um Duplikate wie (1,4) und (4,1) zu vermeiden
        edges = self.graph.get_edges()

        # Wir müssen die Indizes finden. Wir suchen die Nodes.
        for edge in edges:
            if not edge.selected:
                # Wir suchen die Indizes der Punkte in der self.graph.nodes Liste
                idx1 = self.graph.nodes.index(edge.point_one)
                idx2 = self.graph.nodes.index(edge.point_two)
                connection = tuple(sorted((idx1, idx2)))
                # Nur hinzufügen, wenn wir diese Verbindung in dieser Runde noch nicht gesehen haben
                # und wenn sie im Graphen noch nicht als 'selected' markiert ist
                if connection not in seen_connections and not edge.selected:
                    available.append((idx1, idx2))
                    seen_connections.add(connection)
        return available


    def copy(self):
        """
        Diese Methode erschafft quasi eine Simulationsebene für den Agenten, um nicht im echten Spielfeld zu spielen.
        Der Agent nutzt die copy-Methode des Controllers, um tausende unabhängige Simulationsebenen bzw. „Parallelwelten“
        des Spielfelds zu erschaffen, in denen der Agent Züge gefahrlos ausprobieren kann.
        Jede Kopie übernimmt den exakten Stand der vorherigen Simulationsebene (gesetzte Linien und bereits gewonnene Boxen),
        damit der Agent Schritt für Schritt vorausplanen kann.
        Durch diese Trennung bleibt unser echtes Spiel auf völlig unberührt, während der Agent im Hintergrund
        verschiedene Szenarien bis zum Ende durchspielt.
        1. Die Methode erstellt ein Objekt vom Typ GraphController. new_ctrl mit derselben Gitter Größe wie im  echten.
        2. Dann kopiert den graph vom echten Graph(Graph-Klasse) mit Hilfe der Methode copy()
        3. Anschließend erstellt eine einfach (flach) Kopie von den boxen(wer welche Box gewonnen hat) auch.
           Der Agent muss wissen: "Wenn ich diese Linie ziehe, bekomme ich dann einen Punkt?"
        4. Am Ende wird das neu erstellten(zusammengebastelten) Objekt 'new_ctrl' zurückgegeben
        """
        # Manuelle Kopie statt deepcopy JEDES MAL(bei jedem Zug)
        # Damit jeder Ast im Entscheidungsbaum(Graph) seine eigene, ungestörte Welt hat.
        new_ctrl = GraphController(self.grid_size)
        new_ctrl.graph = self.graph.copy()
        # Der Doppelpunkt bedeutet hier „Gehe von Anfang bis Ende durch die Liste self.boxes und kopiere jedes Element einzeln in eine neue, eigene Liste.“
        new_ctrl.boxes = self.boxes[:]  # Flache Kopie der Liste reicht bei Dicts oft
        return new_ctrl
    def __repr__(self) -> str:
        """Ich selbst bin nur der Verwalter. Wenn du wissen willst,
           wie ich aussehe, schau dir die Daten in meinem Graphen an!

           Erstellt eine textuelle Repräsentation des Objekts für Debugging-Zwecke.
           Delegiert die Darstellung direkt an das Graph-Modell weiter.
           """
        return repr(self.graph)


class PlayerController:
    """
    Verwaltet die Spieler sowie den Ablauf der Spielrunden.

    Die Klasse hält fest, welcher Spieler aktuell am Zug ist und wechselt zwischen den zwei Spielern.

    Attribute:
        -player1 (Player): Erster Spieler.
        -player2 (Player): Zweiter Spieler.
        -current_player (Player): Der Spieler der aktuell am Zug ist.
        -other_player (Player): Der nicht aktive Spieler.

    Funktionen:
        get_player_edge() return edge:
            Fordert den aktuellen Spieler auf, einen Zug auszuführen und gibt die gewählte Verbindung zurück.
        switch_player() return None:
            Wechselt den aktuellen Spieler.
        get_color() return str:
            Gibt die Farbe des aktuellen Spielers zurück.
    """

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.other_player = player2

    """
    Holt den Zug vom aktuellen Spieler
    """
    def get_player_edge(self):
        """ Diese Funktion fordert den aktuellen Spieler auf, seinen Zug zu mchen
            und gibt die gewählte kante zurück
         """
        edge = self.current_player.get_move()
        return edge

    def switch_player(self):
        """
        Tauscht den aktuellen Spieler gegen den anderen Spieler
        """
        tmp = self.current_player
        self.current_player = self.other_player
        self.other_player = tmp

    def get_color(self):
        """
        gibt die Farbe des aktuellen Spielers
        """
        return self.current_player.color


class Game:
    """
   Spielsteuerung

    Verbindung zwischen controler, Spieler und der View also mvc

    Attribute:
        graph_controller (GraphController): Verwaltet das Spielfeld und die Spielregeln.
        player_controller (PlayerController): Verwaltet die Spieler und deren Reihenfolge.
        view (GameView): Zuständig für die Darstellung des Spielfelds.

    Funktionen:
        start() return None:
            Startet das Spiel, verarbeitet Züge, prüft auf Boxen und beendet das Spiel.
    """
    def __init__(self, graph_controller: GraphController,
                 player_controller: PlayerController,
                 view: GameView):

        self.graph_controller = graph_controller
        self.player_controller = player_controller
        self.view = view

    def start(self):
        """
       Startet das Spiel, verarbeitet Züge, prüft auf Boxen und beendet das Spiel.
        """
        # Das Spiel läuft solange bis man es händlich abbricht(oder Später mit Bedingung, wenn alle Boxen voll sind)
        #Warte auf den User Eingabe -> speichere diese in edge
        while True:
            #1. Spieler macht einen Zug
            #edge = self.player_controller.get_player_edge()
            #2. Versuch, die Kante zu setzen
            # select_edge_point_number -> gib es noch die Kante(edge) ? ist sie noch frei?
            available = self.graph_controller.get_all_available_edges()
            #edge = self.player_controller.current_player.get_move(available)
            #Übergebe den gesamten graph_controller für die KI-Simulation
            edge = self.player_controller.current_player.get_move(self.graph_controller)
            if self.graph_controller.select_edge_point_number(
                    int(edge[0]), int(edge[1]),
                    self.player_controller.get_color()):
                # self.view.update_print_array()
                #3. Box prüfen und punkte vergeben
                # Wir übergeben das Spieler-Objekt direkt an die Prüfung
                anzahl_der_geschlossenen_boxen = self.graph_controller.check_box(self.player_controller.current_player)
                if anzahl_der_geschlossenen_boxen > 0:
                    #Addiere die tatsächliche Anzahl der Boxen zu den Punkten des Spielers
                    self.player_controller.current_player.points += anzahl_der_geschlossenen_boxen
                    print(f"Spieler {self.player_controller.current_player.name} hat {anzahl_der_geschlossenen_boxen} neue Box(en) geschlossen")
                    print(f"Gesamtpunkte {self.player_controller.current_player.points}")
                    # Bei einem Punktgewinn wird switch_player NICHT aufgerufen,
                    #damit der Spieler nochmal ziehen darf
                else:
                    #Nur wenn keine Box geschloßen wurde, ist der andere Spieler dran
                    self.player_controller.switch_player()

                # 4. Anzeige aktualisieren
                self.view.display(self.graph_controller.grid_size,self.graph_controller.graph.adjacency,self.graph_controller.boxes)

                #5. Sofot prüfen ob Spiel beenden soll
                if self.graph_controller.is_game_over():
                    print("Spiel ist vorbei\n")
                    # Zeige die Punkte von BEIDEN Spielern an
                    p1 = self.player_controller.player1
                    p2 = self.player_controller.player2
                    print(f"{p1.name} hat {p1.points} Punkte.")
                    print(f"{p2.name} hat {p2.points} Punkte.")
                    # Gewinner ermitteln
                    if self.player_controller.player1.points > self.player_controller.player2.points:
                        print(f"Gewinner: {self.player_controller.player1.name}!")
                    elif self.player_controller.player2.points > self.player_controller.player1.points:
                        print(f"Gewinner: {self.player_controller.player2.name}!")
                    else:
                        print("Unentschieden")
                    break




def run_manual_game():
    """
    Die main hier wird der Spieler das Spielfeld und die view initialisiert 
    """
    print("\n--- MODUS WÄHLEN ---")
    print("1. Mensch gegen Mensch")
    print("2. Mensch gegen NPC")
    print("3. NPC gegen NPC")

    wahl = input("Wähle einen Modus (1- bis 3): ")

    if wahl == "1":
        print("--- MANUELLES Spiel ---\n Mensch gegen Mensch:")
        p1 = HumanPlayer("Player 1", "red")
        p2 = HumanPlayer("Player 2", "green")
    elif wahl == "2":
        print("--- MANUELLES Spiel ---\n Mensch gegen NPC:")
        p1 = HumanPlayer("Player 1", "red")
        p2 = RandomNPC("Bot A", "green")
    elif wahl == "3":
        print("--- MANUELLES Spiel ---\n NPC gegen NPC:")
        p1 = RandomNPC("Bot A", "blue")
        p2 = RandomNPC("Bot B", "yellow")
    else:
        print("Ungültige Wahl, starte Standard (Mensch vs. NPC)...")
        p1 = HumanPlayer("Player 1", "red")
        p2 = RandomNPC("Bot A", "green")

    game = Game(graph_controller=GraphController(grid_size=5),player_controller=PlayerController(p1,p2), view=GameView())
    game.start()

def run_p7_unentschieden_demo():
    from UCSController import UCSDrawAgent

    # random_start=True;
    random_start = False;
    print("--- SUCHE NACH UNENTSCHIEDEN-PFAD ---")
    # Initialisiere das Model und die View
    gc = GraphController(grid_size=5)
    view = GameView()
    if random_start:
        available_edge = gc.get_all_available_edges()
        first_move = random.choice(available_edge);
        gc.select_edge_point_number(first_move[0], first_move[1], "yellow")
        print("startpunkte sind:", first_move[0], "und", first_move[1]);

    # Starte den UCS-Agenten
    agent = UCSDrawAgent(gc)
    solution_path = agent.solve()

    if solution_path:
        print(f"Erfolg: Pfad mit {len(solution_path)} Zügen gefunden.")

        # Den Pfad zur Demo abspielen
        p1 = Player("Bot A", "blue")
        p2 = Player("Bot B", "yellow")
        current_p = p1

        for move in solution_path:
            if random_start:
                view.display(gc.grid_size, gc.graph.adjacency, gc.boxes)
                print(f"Bot A: {p1.points} | Bot B: {p2.points}")
                print("-" * 27)
            # Setze die Kante im echten Graphen
            gc.select_edge_point_number(move[0], move[1], current_p.color)
            boxes = gc.check_box(current_p)
            if boxes > 0:
                current_p.points += boxes
                # Spieler darf nochmal (kein Wechsel)
            else:
                # Wechsel zum anderen Spieler
                current_p = p2 if current_p == p1 else p1

                # Spielfeld anzeigen
            view.display(gc.grid_size, gc.graph.adjacency, gc.boxes)
            print(f"Bot A: {p1.points} | Bot B: {p2.points}")
            print("-" * 27)

        print("Ziel erreicht: Unentschieden (2:2)")
    else:
        print("Fehler: Kein Unentschieden-Pfad gefunden.")


def run_p8_minimax_demo():
    print("--- START MINIMAX KI DEMO ---")
    # 1 Spieler definieren (Mensch gegen Minimax KI)
    p1 = HumanPlayer("Mensch", "blue")
    p2 = MinimaxNPC("minimax_Computer", "yellow")

    # 2 Controller und View initialisieren
    gc = GraphController(grid_size=5)
    pc = PlayerController(p1, p2)
    view = GameView()

    # 3Vorabbelegung
    # Wir setzen 6 Kanten vorab, damit nur noch 6 übrig sind (6! = 720 Zustände)
    #scenario_edges = [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (2, 5)]
    scenario_edges = [(0, 1), (1, 2), (3, 4), (4, 5)]
    #scenario_edges = [(0, 1), (0, 3), (7, 8) ]
    for a, b in scenario_edges:
        gc.select_edge_point_number(a, b, "white")

    # 4 Spiel starten
    game = Game(graph_controller=gc, player_controller=pc, view=view)

    # Anzeige einmal vorab ausgeben, damit man das Start Szenario sieht
    view.display(gc.grid_size, gc.graph.adjacency, gc.boxes)

    game.start()

def run_p10_minimax_withalphabeta_demo():
    print("--- START MINIMAX with alphabeta KI DEMO ---")
    # 1 Spieler definieren (Mensch gegen Minimax KI)
    p1 = HumanPlayer("Mensch", "blue")
    p2 = MinimaxNPC_withalpha_beta("minimax_with_alpha_beta_Computer", "yellow")

    # 2 Controller und View initialisieren
    gc = GraphController(grid_size=5)
    pc = PlayerController(p1, p2)
    view = GameView()

    # 3Vorabbelegung
    # Wir setzen 6 Kanten vorab, damit nur noch 6 übrig sind (6! = 720 Zustände)
    #scenario_edges = [(0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (2, 5)]
    #scenario_edges = [(0, 1), (1, 2), (3, 4), (4, 5)] # IST interesannt
    scenario_edges = [(0, 1), (0, 3), (7, 8) ]
    for a, b in scenario_edges:
        gc.select_edge_point_number(a, b, "white")

    # 4 Spiel starten
    game = Game(graph_controller=gc, player_controller=pc, view=view)

    # Anzeige einmal vorab ausgeben, damit man das Start Szenario sieht
    view.display(gc.grid_size, gc.graph.adjacency, gc.boxes)

    game.start()




if __name__ == "__main__":
    game = int(input("1. manuelle Spieler-Spieler-Spiel\n2. unentschieden-Demo\n3. minimax-Demo\n4. minimax-WithAlphaBeta\n "))
    if game == 1:
        run_manual_game()
    elif game == 2:
        run_p7_unentschieden_demo()
    elif game == 3:
        run_p8_minimax_demo()
    elif game == 4:
        run_p10_minimax_withalphabeta_demo()