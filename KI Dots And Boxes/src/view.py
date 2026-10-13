

from typing import List
from termcolor import colored
"""
    Darstellung des Spielfeldes im Terminal
    Darstellung der Verbindungen
"""

class GameView:
    """

Darstellung des Spielfeldes im Terminal.
Verantwortlich für die Ausgabe des Grids sowie der gesetzten Verbindungen und Boxen.

Attribute:
    - print_array (List[List[str]]): Matrix zur Darstellung des Spielfelds im Terminal.

Methoden:
    __create_print_array(grid_size: int) return List[List[str]]:
        Erstellt ein leeres Spielfeld als Matrix. Platziert '*' an Punkten und Leerzeichen für Verbindungen.
    __update_print_array(graph: dict, closed_boxes: list) return None:
        Aktualisiert die Darstellung mit aktuellen Spielinformationen. Zeichnet aktivierte Kanten sowie geschlossene Boxen ins Feld ein.
    display(grid_size: int, graph: dict, closed_boxes: list) return None:
        Hauptausgabefunktion der View. Baut das Spielfeld neu auf, aktualisiert es und gibt es im Terminal aus.
    """



    def __create_print_array(self, grid_size: int) -> List[List[str]]:
        """
        Erstellt ein leeres Array, dass das Spielfeld darstellt.
        Die Größe des Spielfelds wird über grid_size bestimmt.
        erzeugt eine 2D-Matrix(Liste von Listen) für die Ausgabe.
        Platziert * als Punkte auf allen geraden Koordinaten
        Leerzeichen freie Felder wo später die Verbindungen sind
        """
        array = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append("*" if (i % 2 == 0 and j % 2 == 0) else " ")
            array.append(row)
        return array

    def __update_print_array(self, graph: dict, closed_boxes: list) -> None:
        # 1. Kanten zeichnen
        for point, edges in graph.items():
            for edge in edges:
                if edge.selected:
                    pos = edge.position
                    i, j = int(pos[0]), int(pos[1])
                    if edge.point_one.position[0] == edge.point_two.position[0]:
                        self.print_array[i][j] = colored(u'\u2500', edge.color)
                    else:
                        self.print_array[i][j] = colored("|", edge.color)

        # 2. Box-Inhalte zeichnen (A/B oder was auch immer im Spieler-Objekt steht)
        for box in closed_boxes:
            r, c = box["center"]
            self.print_array[r][c] = colored(box["char"], box["color"])


    def display(self, grid_size: int, graph: dict,closed_boxes: list) -> None:
        """
        Die Haupt-Ausgabe-Fuktion der View.
        Baut das Gitter neu auf , aktualisiert die Linien und druckt es ins Terminal
        """
        self.print_array = self.__create_print_array(grid_size)
        self.__update_print_array(graph, closed_boxes)
        for row in self.print_array:
            print("".join(row))
