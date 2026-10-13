import heapq
import time

#from PIL.SpiderImagePlugin import iforms

from game_model import Player


class UCSDrawAgent:
    def __init__(self, initial_graph_controller):
        self.initial_gh_controller = initial_graph_controller
        self.best_score_found = (0, 0)  # Hilfsvariable zum Debuggen

    def goal_test(self, controller) -> bool:
        if controller.is_game_over():
            points_a = sum(1 for b in controller.boxes if b["char"] == "A")
            points_b = sum(1 for b in controller.boxes if b["char"] == "B")

            return points_a == 2 and points_b == 2
        return False

    def state(self,ctrl,player_idx):
        edges=tuple(sorted([e.position for e in ctrl.graph.get_edges() if e.selected]))
        points_a=sum(1 for b in ctrl.boxes if b["char"] == "A")
        points_b=sum(1 for b in ctrl.boxes if b["char"] == "B")
        return (edges,points_a,points_b,player_idx)



    def solve(self):
        print("--- UCS Suche gestartet ---")
        start_time = time.time()
        counter = 0
        # (Kosten, zustand, pfad, controller, player_idx)

        frontier = []
        explored = set()
        frontier_costs = {}

        start_ctrl = self.initial_gh_controller.copy()
        start_player = 0

        start_state=self.state(start_ctrl,start_player)

        heapq.heappush(frontier, (0, start_state,[],start_ctrl,start_player))#Speichern der besten bekannten Kosten pro zug anstat counter

        frontier_costs[start_state] = 0 #hinzufügen von startkosten

        node_count = 0



        while frontier:
            cost, state, path, current_ctrl, player_idx = heapq.heappop(frontier)

            #verhindert doppelte verarbeitung ohne das wir ein zustand öfters verarbeitet
            if state in explored:
                continue

            # State-Repräsentation für Explored-Set
            #current_state = tuple(sorted([e.position for e in current_ctrl.graph.get_edges() if e.selected]))

            if self.goal_test(current_ctrl):
                print(f"LÖSUNG GEFUNDEN! Knoten: {node_count} | Zeit: {time.time() - start_time:.2f}s")
                return path

            explored.add(state)

            frontier_costs.pop(state,None)  #entfernen aus frontier_cost da es aus frontier entfernt wurde
            node_count += 1

            if node_count % 1000 == 0:
                print(f"Knoten: {node_count} | Frontier: {len(frontier)}")

            for edge_coords in current_ctrl.get_all_available_edges():
                child_ctrl = current_ctrl.copy()
                # Dummy Player für Box-Logik
                p_name = "A" if player_idx == 0 else "B"
                p_color = "blue" if player_idx == 0 else "yellow"
                current_player = Player(p_name, p_color)

                if child_ctrl.select_edge_point_number(edge_coords[0], edge_coords[1], current_player.color):
                    new_boxes = child_ctrl.check_box(current_player)
                    next_player=player_idx if new_boxes > 0 else (1-player_idx)
                    child_state=self.state(child_ctrl,next_player)  #status des kindes
                    new_cost=cost+1
                    #bug fix da frontier nie überprüft wurde
                    if child_state not in explored and child_state not in frontier_costs:
                        heapq.heappush(frontier, (new_cost, child_state, path+[edge_coords],child_ctrl, next_player))
                        frontier_costs[child_state] = new_cost  #merken von kosten in frontier_cost

                    #ersetzten
                    elif child_state in frontier_costs and new_cost < frontier_costs[child_state]:
                        heapq.heappush(frontier,(new_cost, child_state, path+[edge_coords], child_ctrl, next_player))
                        frontier_costs[child_state] = new_cost

        return None