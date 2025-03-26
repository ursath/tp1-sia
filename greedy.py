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
        self.best_heuristic = {}
        self.frontier = set()

    def search(self):

        answer = {}
        answer['execution_time'] = time.time()  # To substract from the end time
        answer['frontier'] = 0

        if isinstance(self.heuristics, (ManhattanDistance, ManhattanImproved)):
            # ManhattanDistance and ManhattanImproved only take boxes
            h_n = self.heuristics.get(self.initial_state.boxes)
        else:
            # PlayerDistance or CombinedHeuristic take boxes and player
            h_n = self.heuristics.get(self.initial_state.boxes, self.initial_state.player)

        heapq.heappush(self.priority_queue, (h_n, self.initial_state))  # (h(n), state)
        self.best_heuristic[self.initial_state] = h_n

        while self.priority_queue:
            current_h_n, current_state = heapq.heappop(self.priority_queue)

            if current_state.is_goal():
                answer['execution_time'] = time.time() - answer['execution_time']
                answer['path'] = self.get_path(current_state)[0]
                answer['directions'] = self.get_path(current_state)[1]
                answer['explored'] = len(self.explored) 
                answer['frontier'] = len(self.explored) + len(self.priority_queue)
                return answer

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

                if new_state not in self.best_heuristic or h_n < self.best_heuristic[new_state]:
                    self.best_heuristic[new_state] = h_n
                    heapq.heappush(self.priority_queue, (h_n, new_state))
                    self.parent[new_state] = (current_state, direction)

        print("No path found.")
        return [] 

    def get_path(self, state):
        path = []
        directions = []
    
        while state in self.parent:
            parent_state, direction = self.parent[state]
            path.append(state)
            directions.append(direction)
            state = parent_state
    
        path.append(self.initial_state)
        path.reverse()
        directions.reverse()
        return path, directions
    

def load_map(map_file):
    with open(map_file, "r") as f:
        return [list(line.strip()) for line in f.readlines()]
    
def execute(greedy):
    answer = greedy.search()

    print(f"Execution time: {answer['execution_time']}")
    print(f"Nodes explored: {answer['explored']}")
    print(f"Frontier: {answer['frontier']}")
    print(f"Path length: {len(answer['path'])}")
    print(f"Directions: {answer['directions']}")
    print("-----")

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
