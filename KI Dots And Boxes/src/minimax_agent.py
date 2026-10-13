import math


class MinimaxAgent:
    def __init__(self, player_color):
        """
        Initialisiert den Minimax-Agenten.
        :param player_color: Die Farbe, die dieser Agent vertritt (z.B. "blue").
        """
        self.player_color = player_color
        self.opponent_color = "yellow" if player_color == "blue" else "blue"
        self.nodes_expanded = 0

    def get_action(self, controller):
        """
        Schnittstelle für das Spiel: Gibt den besten nächsten Zug zurück.
        """
        self.nodes_expanded = 0
        return self.minimax_decision(controller)

    def minimax_decision(self, state):
        """
        Implementiert minimax_decision laut Vorlesung.
        Sucht den Zug, der den Rückgabewert von MIN-VALUE maximiert.
        """
        best_val = -math.inf
        best_move = None
        chosen_path = []

        available_moves = state.get_all_available_edges()

        for move in available_moves:
            # RESULT(_state, _a): Simulation des Zuges in einer Kopie
            sim_ctrl = state.copy()
            sim_ctrl.select_edge_point_number(move[0], move[1], self.player_color)

            # Sonderregel Dots and Boxes: Hat MAX eine Box geschlossen?
            # Wir nutzen einen Dummy-Spieler für die Prüfung
            class Dummy:
                color = self.player_color
                name = "Computer"

            if sim_ctrl.check_box(Dummy()) > 0:
                # MAX darf nochmal ziehen
                val, path = self.max_value(sim_ctrl)
            else:
                # Wechsel zu MIN
                val, path = self.min_value(sim_ctrl)

            if val > best_val:
                best_val = val
                best_move = move
                chosen_path = [move] + path

        # P8 Anforderung: Ausgabe des gewählten Pfades
        print(f"\n--- Minimax Entscheidung ---")
        print(f"Bester Zug: {best_move}")
        print(f"Vorhergesehener Pfad (Züge): {chosen_path}")
        print(f"Erwartete Punktedifferenz: {best_val}")
        print(f"Untersuchte Knoten:{self.nodes_expanded}")
        return best_move

    def max_value(self, state):
        """
        MAX-VALUE Funktion: Versucht den UtilityWert zu maximieren.
        """
        # TERMINAL-TEST
        self.nodes_expanded += 1
        if state.is_game_over():
            return self.utility(state), []

        v = -math.inf
        best_path = []

        for action in state.get_all_available_edges():
            sim_ctrl = state.copy()
            sim_ctrl.select_edge_point_number(action[0], action[1], self.player_color)

            class Dummy:
                color = self.player_color
                name = "Computer"

            if sim_ctrl.check_box(Dummy()) > 0:
                res, path = self.max_value(sim_ctrl)  # Zusatzzug für MAX
            else:
                res, path = self.min_value(sim_ctrl)  # Wechsel zu MIN

            if res > v:
                v = res
                best_path = [action] + path

        return v, best_path

    def min_value(self, state):
        """
        MIN-VALUE Funktion: Versucht den Utility wert zu minimieren (Gegner Sicht).
        """
        self.nodes_expanded += 1
        # TERMINAL-TEST
        if state.is_game_over():
            return self.utility(state), []

        v = math.inf
        best_path = []

        for action in state.get_all_available_edges():
            sim_ctrl = state.copy()
            sim_ctrl.select_edge_point_number(action[0], action[1], self.opponent_color)

            class Dummy:
                color = self.opponent_color
                name = "Gegner"

            if sim_ctrl.check_box(Dummy()) > 0:
                res, path = self.min_value(sim_ctrl)  # Zusatzzug für MIN
            else:
                res, path = self.max_value(sim_ctrl)  # Wechsel zu MAX

            if res < v:
                v = res
                best_path = [action] + path

        return v, best_path

    def utility(self, state):
        """
        UTILITY Funktion: Bewertet den Endzustand.
        Gibt die Differenz der Boxen zurück (Eigene - Gegner).
        """
        points_me = sum(1 for b in state.boxes if b["color"] == self.player_color)
        points_opp = sum(1 for b in state.boxes if b["color"] == self.opponent_color)
        return points_me - points_opp