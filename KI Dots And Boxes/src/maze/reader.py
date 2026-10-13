from termcolor import colored
from maze.controller import Controller
from model import Maze
from view import View

class Reader:
    def __init__(self, dateiname = "maze_with_legend.txt"):
        self.dateiname = dateiname
        self.Maze = Maze()

    def read(self) -> None:
        with open(self.dateiname, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            self.Maze.set_maze(lines)

if __name__ == '__main__':
    import sys
    datei = sys.argv[1] if len(sys.argv) > 1 else "maze_with_legend.txt"
    reader = Reader(datei)
    reader.read()
    view = View(reader.Maze)
    view.ausgabe()
    controller = Controller(reader.Maze)
    pfad, kosten = controller.a_star()

    if pfad:
        print("\nGefundener Pfad (Koordinaten von Start nach Ziel):")
        print(pfad)
        print("Gesamtkosten:", kosten)

        # Labyrinth-Kopie erstellen
        labyrinthsicht = [list(zeile) for zeile in reader.Maze.get_maze()]
        # Pfad mit * markieren (außer S/E)
        for (x, y) in pfad:
            if labyrinthsicht[y][x] not in ('S', 'E'):
                labyrinthsicht[y][x] = '*'

        print("\nLabyrinth mit Pfad (*) in grün:")
        for zeile in labyrinthsicht:
            gefärbte_zeichen = []
            for zeichen in zeile:
                if zeichen == '*':
                    gefärbte_zeichen.append(colored('*', 'green'))
                else:
                    gefärbte_zeichen.append(zeichen)
            print(' '.join(gefärbte_zeichen))
    else:
        print("Keine Route gefunden.")