import heapq
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic
from a_star import A_star, State, MapInfo
import time

class Greedy:

    def __init__(self, initial_state, heuristics, map):
        self.initial_state = initial_state
        self.heuristics = heuristics
        self.explored = set()
        self.priority_queue = []
        self.parent = {}
        self.map = map

    def search(self):
        heapq.heappush(self.priority_queue, (0, self.initial_state))  # (h(n), state)

        while self.priority_queue:
            h_n, current_state = heapq.heappop(self.priority_queue)

            if current_state.is_goal():
                return self.get_path(current_state)

            self.explored.add(current_state)

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_state = current_state.move(direction, self.map)
                if new_state is None or new_state in self.explored:
                    continue

                if isinstance(self.heuristics, (ManhattanDistance, ManhattanImproved)):
                    # ManhattanDistance and ManhattanImproved only take boxes
                    h_n = self.heuristics.get(new_state.boxes)
                else:
                    # PlayerDistance or CombinedHeuristic take boxes and player
                    h_n = self.heuristics.get(new_state.boxes, new_state.player)
                heapq.heappush(self.priority_queue, (h_n, new_state))
                self.parent[new_state] = current_state

        print("No path found.")
        return None, 0  # No path found

    def get_path(self, state):
        path = []
        while state in self.parent:
            path.append(state)
            state = self.parent[state]
        path.append(self.initial_state)
        path.reverse()

        return path
    

def load_map(map_file):
    with open(map_file, "r") as f:
        return [list(line.strip()) for line in f.readlines()]
    
def execute(greedy):
    start_time = time.time()
    path = greedy.search()
    end_time = time.time()

    print(f"Heuristic: {greedy.heuristics.__class__.__name__}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds")
    print(f"Path Length: {len(path)}")

def main():
    map = MapInfo(load_map("maps/2.txt"))

    manhattan_distance = ManhattanDistance(map.targets)
    manhattan_improved = ManhattanImproved(map.targets)
    player_distance = PlayerDistance(map.targets)
    combined_heuristic = CombinedHeuristic(map.targets)

    initial_state = State(map.boxes, map.player, map.targets)

    greedy_manhattan = Greedy(initial_state, manhattan_distance, map)
    execute(greedy_manhattan)

    greedy_manhattan_improved = Greedy(initial_state, manhattan_improved, map)
    execute(greedy_manhattan_improved)
   
    greedy_player_distance = Greedy(initial_state, player_distance, map)
    execute(greedy_player_distance)

    greedy_combined = Greedy(initial_state, combined_heuristic, map)
    execute(greedy_combined)


if __name__ == "__main__":
    main()
