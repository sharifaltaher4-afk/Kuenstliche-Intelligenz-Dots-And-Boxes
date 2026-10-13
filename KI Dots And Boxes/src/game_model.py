from dataclasses import dataclass
from symtable import Class
import random

from alphabeta_agent import AlphaBetaAgent
from minimax_agent import MinimaxAgent


@dataclass
class Player():
    """
    Repräsentiert den Spieler
    """
    name: str
    color: str
    points:int =0

    def get_move(self, available_edges = None) -> tuple[int, int]:
        """Diese Methode wird von den Unterklassen überschrieben"""
        pass


class HumanPlayer (Player):
    """Der menschliche Spieler nutzt die Konsole"""
    #def get_move(self, available_edges=None) -> tuple[int, int]:
    def get_move(self, controller=None) -> tuple[int, int]:
        while True:
            print(f"{self.name}, dein Zug (z.B. 0 1): ")
            try:
                p1 = int(input("Punkt 1: "))
                p2 = int(input("Punkt 2: "))
                return (p1, p2)
            except ValueError:
                print("Bitte Zahlen eingeben!")



class RandomNPC(Player):
    """Der NPC wählt zufällig einen erlaubten Zug  """
    #def get_move(self, available_edges) -> tuple[int, int]:
    def get_move(self, controller) -> tuple[int, int]:
        available_edges = controller.get_all_available_edges()
        while True:
            if not available_edges:
                return (0, 0)   # Sollte im Spielverlauf nicht passieren
            zug = random.choice(available_edges)
            print(f"NPC {self.name} hat {zug[0]} - {zug[1]} gewählt")
            return zug

class MinimaxNPC(Player):
    """
    Ein NPC, der den Minimax Algorithmus nutzt um den optimalen Zug zu finden.
    """
    def __init__(self, name, color):
        super().__init__(name, color)
        self.agent = MinimaxAgent(color)

    def get_move(self, controller) -> tuple[int, int]:
        # Der Controller wird hier als 'state' an den Minimax übergeben
        print(f"KI {self.name} berechnet den nächsten Zug...")
        return self.agent.get_action(controller)

class MinimaxNPC_withalpha_beta(Player):
    """
    Ein NPC, der den Minimax Algorithmus nutzt um den optimalen Zug zu finden.
    """
    def __init__(self, name, color):
        super().__init__(name, color)
        self.agent = AlphaBetaAgent(color)

    def get_move(self, controller) -> tuple[int, int]:
        # Der Controller wird hier als 'state' an den Minimax übergeben
        print(f"KI {self.name} berechnet den nächsten Zug...")
        return self.agent.get_action(controller)