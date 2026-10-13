import math


class AlphaBetaAgent:
    def __init__(self, player_color):
        """
        Initialisiert den Alpha-Beta-Agenten.
        :param player_color: Die Farbe, die dieser Agent vertritt (z.B. "blue").
        """
        self.player_color = player_color
        self.opponent_color = "yellow" if player_color == "blue" else "blue"
        self.nodes_expanded = 0

    def get_action(self, controller):
        """
        Schnittstelle für das Spiel: Gibt den besten nächsten Zug zurück.
        """
        self.nodes_expanded =0
        return self.alpha_beta_search(controller)



    def alpha_beta_search(self, state):
        """
        Implementiert ALPHA-BETA-SEARCH laut Vorlesung (Folie 100, Zeile 1-4).
        """
        value, move = self.max_value(state, -math.inf, math.inf)

        # Ausgabe für Debugging
        print(f"\n--- Alpha-Beta Entscheidung ---")
        print(f"Bester Zug: {move}")
        print(f"Erwartete Utility: {value}")
        print(f"Untersuchte Knoten: {self.nodes_expanded}")

        return move


    def max_value(self, state,alpha,beta):
        """
        Implementiert MAX-VALUE laut Vorlesung (Folie 100, Zeile 1-12).
        Returns a (utility, move) pair.
        """
        # Zeile 2-3: Terminal-Test
        # TERMINAL-TEST
        #self.nodes_expanded += 1
        if state.is_game_over():
            return self.utility(state), None

        # Zeile 4
        v = -math.inf
        move = None

        # Zeile 5: for each action in ACTIONS(state)
        for action in state.get_all_available_edges():
            # Zeile 6: v2, a2 <== MIN-VALUE(RESULT(state, action), alpha, beta)
            sim_ctrl = state.copy()
            sim_ctrl.select_edge_point_number(action[0], action[1], self.player_color)

            # Sonderregel: Hat MAX eine Box geschlossen?
            class Dummy:
                color = self.player_color
                name = "Computer"

            if sim_ctrl.check_box(Dummy()) > 0:
                # MAX darf nochmal ziehen
                v2, a2 = self.max_value(sim_ctrl, alpha, beta)
            else:
                # Wechsel zu MIN
                v2, a2 = self.min_value(sim_ctrl, alpha, beta)
            # Zeile 7-8: if v2 > v then v, move <== v2, action
            if v2 > v:
                v = v2
                #best_path = [action] + path
                move = action
            # Zeile 9: alpha <== max(alpha, v)
            alpha = max(alpha, v)

            # Zeile 10-11: if v >= beta then return v, move
            if v >= beta:
                return v, move
        # Zeile 12: return v, move
        return v, move

    def min_value(self, state,alpha,beta):
        """
        Implementiert MIN-VALUE laut Vorlesung (Folie 101, Zeile 1-12).
        Returns a (utility, move) pair.
        """
        self.nodes_expanded += 1

        # Zeile 2-3: Terminal-Test
        if state.is_game_over():
            return self.utility(state), None

        # Zeile 4: v <== +infi
        v = math.inf
        move = None

        # Zeile 5: for each action in ACTIONS(state)
        for action in state.get_all_available_edges():
            # Zeile 6: v2, a2 <== MAX-VALUE(RESULT(state, action), alpha, beta)
            sim_ctrl = state.copy()
            sim_ctrl.select_edge_point_number(action[0], action[1], self.opponent_color)

            # Sonderregel Dots and Boxes: Hat MIN eine Box geschlossen?
            class Dummy:
                color = self.opponent_color
                name = "Gegner"

            if sim_ctrl.check_box(Dummy()) > 0:
                # MIN darf nochmal ziehen
                v2, a2 = self.min_value(sim_ctrl, alpha, beta)
            else:
                # Wechsel zu MAX
                v2, a2 = self.max_value(sim_ctrl, alpha, beta)

            # Zeile 7-8: if v2 < v then v, move <== v2, action
            if v2 < v:
                v = v2
                move = action

            # Zeile 9: beta <== min(beta, v)
            beta = min(beta, v)

            # Zeile 10-11: if v <= alpha then return v, move
            if v <= alpha:
                return v, move

        # Zeile 12: return v, move
        return v, move

    def utility(self, state):
        """
        UTILITY Funktion: Bewertet den Endzustand.
        Gibt die Differenz der Boxen zurück (Eigene - Gegner).
        """
        points_me = sum(1 for b in state.boxes if b["color"] == self.player_color)
        points_opp = sum(1 for b in state.boxes if b["color"] == self.opponent_color)
        return points_me - points_opp