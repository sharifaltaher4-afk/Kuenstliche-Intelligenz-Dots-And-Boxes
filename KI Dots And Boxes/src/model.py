
from dataclasses import dataclass
from typing import Tuple, List, Dict


@dataclass(frozen=True, slots=True) # Punkte können während des Spieles nicht verändert werden(frozen). , die Klasse verbraucht min. Speicherplatz(slots)
class Point:
    """
    Ist der Punkt im Spielfeld
    mit den Eigenschaften Position, Name
    mit den Eigenschaften das sie nicht verändert werden können.

    Attribute:
        - position (Tuple[int, int]): Koordinaten des Punktes im Grid.
        - name (str): Eindeutiger Name des Punktes (z.B. "P0").

    Methoden:
        __repr__() return str:
            Debug-Darstellung des Punktes.

        __eq__(o: object) return bool:
            Vergleicht zwei Punkte anhand ihrer Position. Namen werden ignoriert.
    """
    position: Tuple[int, int]
    name: str

    def __repr__(self) -> str:
        """
        Debugging
        """
        return f"{self.name}({self.position})"

    def __eq__(self, o):
        """
        #Überschriebene Standard-Gleichheit-Funktion
        ist die Equal-Methode wenn zwei Punkte an der selben Position sind dann sind sie gleich.Namen sind egal
        """
        # Wenn zwei Punkte dieselbe Koordinate haben, dann sind sie gleich. ABGESEHEN von Name
        if self.position[0] == o.position[0] and self.position[1] == o.position[1]:
            return True
        return False


@dataclass
class Edge:
    """
    Sind die Verbindungen zwischen den Punkten
    mit den Eigenschaften wo sie sind, ob sie ausgewählt wurden und welche Farbe sie haben

    Attribute:
    - point_one (Point):
        Startpunkt der Verbindung.
    - point_two (Point):
        Endpunkt der Verbindung.
    - selected (bool):
        Gibt an, ob die Verbindung bereits gewählt wurde.
    - color (str):
        Farbe der Verbindung.

    Methoden:
        select(color: str) return None:
            Markiert die Verbindung als ausgewählt und setzt die Farbe.
        __eq__(o: object) return bool:
            Vergleicht zwei Verbindungen anhand ihrer verbundenen Punkte.
        position return Tuple[int, int]:
            Berechnet die Position der Verbindung im Grid für die Darstellung in der View.
         name return str:
            Gibt eine lesbare Darstellung der Verbindungen zurück.

    """
    point_one: Point
    point_two: Point
    selected: bool = False
    color: str = ""

    @property
    def position(self) -> Tuple[int, int]:
        """
            Berechnet dynamisch die Koordinate der Kanten-Mitte im Gitter.
            Wird von der View genutzt, um zu wissen, wo der Strich ('─' oder '|')
            gezeichnet werden muss.
            """
        p1 = self.point_one.position
        p2 = self.point_two.position
        # Berechne die mittlere Position zwischen den Punkten
        # Wenn der X-Abstand klein ist, liegen die Punkte nebeneinander (horizontal)
        if abs(p1[0] - p2[0]) <= 1: # ist der Abstand auf der x-Achse zwischen p1 und p2 kleiner gleich 1?
            # x - Achse
            # Die Zeile bleibt gleich, die Spalte ist genau zwischen p1 und p2
            return (p1[0], min(p1[1], p2[1]) + 1)
        else:
            # Y - Achse
            # Die Zeile ist genau zwischen p1 und p2, die Spalte bleibt gleich (vertikal)
            return (min(p1[0], p2[0]) + 1, p1[1])

    @property

    def name(self) -> str:
        """Name der Verbindung mit den Verbindungspunkten"""
        return f"{self.point_one.name} - {self.point_two.name}"

    def select(self, color: str) -> None:
        """
        setzt die Verbindung auf ausgewählt
        """
        self.selected = True
        self.color = color

    def __eq__(self, o):
        """Prüft, ob zwei Kanten identisch sind.
           Wichtig für die Suche im Graphen, wenn der User einen Zug macht.
            """
        # Debugging-Ausgabe zeigt den Vergleich im Console
        #print(o, self)
        # Standard-Vergleich (Richtung wird beachtet)
        if self.point_one == o.point_one and self.point_two == o.point_two:
            return True
        return False


class Graph:
    """
    Eine allgemeine Graph-Klasse, die Knoten und Kanten verwaltet.

    Attribute:
        - adjacency (Dict[Point, List[Edge]]): Adjazenzliste zur Speicherung aller Verbindungen pro Punkt.
        - nodes (List[Point]): Liste aller Punkte im Graphen.

    Methoden:
        __init__() return None:
            Initialisiert leeren Graphen.
        add_node(node: Point) return None:
            Fügt einen neuen Punkt in den Graphen ein.
        add_edge(a: Point, b: Point) return None:
            Erstellt eine Verbindung zwischen zwei Punkten in beide Richtungen.
        get_edges() return List[Edge]:
            Gibt alle Verbindungen im Graphen zurück.
        copy() return Graph:
            Erstellt eine Kopie des gesamten Graphen inkl. Verbindungen.
        __repr__() return str:
            Gibt eine lesbare Adjazenzliste zur Debug-Ausgabe zurück.
    """

    def __init__(self) -> None:
        # Verbinde einen Punkt dikret mit seinen Kanten. Gut, weil nachschlagen und nicht suchen! O(1)
        # Speichere was da ist (nur die gewollten Punte. Nicht die dazwischen "leere Punkte".
        self.adjacency: Dict[Point, List[Edge]] = {}
        # Hauptlist der Konten des Graphens (3X3 Gitter) zu der eindeutigen Indezierung im Spielfeld(3X3).
        # Speichert die Points dadurch ermöglicht die "Umwandelung" der User eingabe(0 bis 8) in Points(P0 bis P8)
        self.nodes: List[Point] = []


    def add_node(self, node: Point) -> None:
        """Diese Funktion sorgt dafür dass ein Punkt überhaupt im Sys. steht
            Erstellt einen Eintrag im Dect. für den Punkt falls noch nicht exis.
            Und initialisiert eine leere Liste für seine zukünftigen Nachbarn.
            Regestriert den Punkt in der nodes Liste für den Index-Zugriff
            """
        #Schaue nach, ob dieser Punkt schon einen Key im Dect. hat, wenn nicht erstelle einen und lege eine leere Liste hinein
        #Leere Liste, weil ein Punkt am Anfang noch keine Verbindungen hat
        self.adjacency.setdefault(node, [])
        self.nodes.append(node)# Füge den Punkt am ende der Hauptliste der Punkte


    def add_edge(self, a: Point, b: Point) -> None:
        """füge die kanten in beiden Richtungen a->b und b->a (Nachbar) zwischen zwei benachbarten Punkten zu der Adjazenz-Dictionary hinzu
           Also es wird an jedem Punkt P_i die Kanten(2) jeweils in beiden Richtungen (2) im Wörterbuch angehängt.
           ein Punkt in der Mitte (wie P4) hat aber 4 Kanten (oben, unten, links, rechts).
           Also Die Funktion add_edge wird also für P4 insgesamt viermal aufgerufen, bis sein "Ordner" im Dictionary vier Einträge hat.
           """
        edge_ab = Edge(a, b)
        edge_ba = Edge(b, a)
        #füge die Kante jeweils der Liste der Liste der Nachbarn des Startpunkts hinzuu
        self.adjacency[a].append(edge_ab)# in den Ordner des Punkts A wird die Verbindung zu B geheftet
        self.adjacency[b].append(edge_ba)# in den Ordner des Punkts B wird die Verbindung zu A geheftet

    def get_edges(self) -> List[Edge]:
        """
        gibt alles Verbindungen zurück
        """
        edge_list = []
        for ed_list in self.adjacency.values():
            for edge in ed_list:
                edge_list.append(edge)
        return edge_list

    """def copy(self):
        new_graph = Graph()
        # Kopiere die Knoten
        new_graph.nodes = [Point(n.position, n.name) for n in self.nodes]
        # Kopiere die Struktur und den Status der Kanten
        for node in self.nodes:
            new_node = new_graph.nodes[self.nodes.index(node)]
            new_graph.add_node(new_node)
            for edge in self.adjacency[node]:
                # Finde Partner-Knoten im neuen Graphen
                target_idx = self.nodes.index(edge.point_two)
                target_node = new_graph.nodes[target_idx]
                # Erstelle neue Kante mit gleichem Status
                new_edge = Edge(new_node, target_node, edge.selected, edge.color)
                new_graph.adjacency[new_node].append(new_edge)
        return new_graph"""

    def copy(self):
        new_graph = Graph()
        # Punkte sind frozen, wir können die Referenzen einfach übernehmen
        new_graph.nodes = self.nodes[:]

        for node in self.nodes:
            new_graph.adjacency[node] = []
            for edge in self.adjacency[node]:
                # Erstelle eine neue Kante, kopiere aber nur den Status
                new_edge = Edge(
                    edge.point_one,
                    edge.point_two,
                    edge.selected,
                    edge.color
                )
                new_graph.adjacency[node].append(new_edge)
        return new_graph


    def __repr__(self) -> str:
        """Das Programm geht duch jeden einzigen Punkt(Knote) im Dect.
           node ist der Punkt und edges ist die Liste aller Linien, die am Punkt hängen
           List Comprehension: edge_name = [...] : Da ein Edge ein komplexes Objekt ist, pikt sich die Funk. hier
           nur die Namen der Kanten herraus (z.B "P0-P1") damit derText nicht zu unüberichtlich wird
           Für jeden Punkt wird eine Zeile erstellt : P0:['P0-P1', 'P0-P3']
        """
        out = "Graph adjacency list:\n"

        for node, edges in self.adjacency.items():
            # Extrahiert nur die Namen der Kanten für eine kompakte Darstellung
            edge_names = [edge.name for edge in edges]
            out += f"{node.name}: {edge_names}\n"
        return out
