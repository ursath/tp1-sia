import heapq
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic
import time


class State:
    def __init__(self, boxes, player, targets):
        self.boxes = frozenset(boxes) 
        self.player = player
        self.targets = frozenset(targets)

    def __hash__(self):
        return hash((self.boxes, self.player))  

    def __eq__(self, other):
        return self.boxes == other.boxes and self.player == other.player
    
    def __lt__(self, other):
        return (self.player, self.boxes) < (other.player, other.boxes)

    def __str__(self):
        return f"Player: {self.player}, Boxes: {self.boxes}"

    def move(self, direction, map):
        new_player_pos = (self.player[0] + direction[0], self.player[1] + direction[1])

        # Check wall
        if new_player_pos in map.walls:
            return None
        
        # If the movement moves a box, check it's a valid move
        new_boxes = set(self.boxes)
        if new_player_pos in self.boxes:
            new_box_pos = (new_player_pos[0] + direction[0], new_player_pos[1] + direction[1])
            if new_box_pos in map.walls or new_box_pos in self.boxes:
                # Avoids moving boxes into walls or into other boxes
                return None
            new_boxes.remove(new_player_pos)
            new_boxes.add(new_box_pos)
        return State(frozenset(new_boxes), new_player_pos, self.targets)

    def is_goal(self):
        return self.boxes == self.targets

class A_star:
    def __init__(self, initial_state, heuristics, map):
        self.initial_state = initial_state
        self.heuristics = heuristics
        self.explored = set()
        self.priority_queue = []
        self.g_cost_accum = {initial_state: 0}
        self.parent = {}
        self.map = map

    def search(self):

        answer = {}

        answer['frontier'] = 0
        answer['execution_time'] = time.time() # To substract from the end time

        heapq.heappush(self.priority_queue, (0, 0, self.initial_state))  # (f(n), g(n), state)

        while self.priority_queue:
            answer['frontier'] += len(self.priority_queue)
            f_n, g_n, current_state = heapq.heappop(self.priority_queue)

            if current_state.is_goal():
                answer['explored'] = len(self.explored)
                answer['execution_time'] = time.time() - answer['execution_time']
                answer['path'] = self.get_path(current_state)[0]
                answer['directions'] = self.get_path(current_state)[1]
                answer['g_n'] = g_n 
                return answer

            self.explored.add(current_state)

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_state = current_state.move(direction, self.map)
                if new_state is None or new_state in self.explored:
                    continue

                new_g_n = g_n + 1
                if new_state not in self.g_cost_accum or new_g_n < self.g_cost_accum[new_state]:
                    self.g_cost_accum[new_state] = new_g_n

                    if isinstance(self.heuristics, (ManhattanDistance, ManhattanImproved)):
                        # ManhattanDistance and ManhattanImproved only take boxes
                        f_n = new_g_n + self.heuristics.get(new_state.boxes)
                    else:
                        # PlayerDistance or CombinedHeuristic take boxes and player
                        f_n = new_g_n + self.heuristics.get(new_state.boxes, new_state.player)
                    heapq.heappush(self.priority_queue, (f_n, new_g_n, new_state))
                    self.parent[new_state] = (current_state, direction)

        print("No path found.")
        return None, 0  # No path found
    
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

class MapInfo:
    def __init__(self, map):
        self.map = map
        self.targets = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "."}
        self.boxes = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "$"}
        self.player = next((x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "@")
        self.walls = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "#"}

def load_map(map_file):
    with open(map_file, "r") as f:
        return [list(line.strip()) for line in f.readlines()]
    
def execute(a_star):
    answer = a_star.search()

    print(f"Execution time: {answer['execution_time']}")
    print(f"Nodes explored: {answer['explored']}")
    print(f"Frontier: {answer['frontier']}")
    print(f"Path length: {len(answer['path'])}")
    print(f"g_n: {answer['g_n']}")
    print(f"Directions: {answer['directions']}")
    print("-------")

def main():
    map = MapInfo(load_map("maps/2.txt"))

    manhattan_distance = ManhattanDistance(map.targets)
    manhattan_improved = ManhattanImproved(map.targets)
    player_distance = PlayerDistance(map.targets)
    combined_heuristic = CombinedHeuristic(map.targets)

    initial_state = State(map.boxes, map.player, map.targets)

    a_star_manhattan = A_star(initial_state, manhattan_distance, map)
    execute(a_star_manhattan)

    a_star_manhattan_improved = A_star(initial_state, manhattan_improved, map)
    execute(a_star_manhattan_improved)
   
    a_star_player_distance = A_star(initial_state, player_distance, map)
    execute(a_star_player_distance)

    a_star_combined = A_star(initial_state, combined_heuristic, map)
    execute(a_star_combined)


if __name__ == "__main__":
    main()
