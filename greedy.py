import heapq
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic, ManhattanDistanceWithDeadlockDetection, CombinedHeuristicWithDeadlockDetection
from a_star import A_star, State, MapInfo
import time
import os 

class Greedy:

    def __init__(self, initial_state, heuristics, map, game):
        self.initial_state = initial_state
        self.heuristics = heuristics
        self.explored = set()
        self.priority_queue = []
        self.parent = {}
        self.map = map
        self.best_heuristic = {}
        self.frontier = set()
        self.game = game

    def search(self):

        answer = {}
        answer['execution_time'] = time.time()  # To substract from the end time
        answer['frontier'] = 0

        if isinstance(self.heuristics, (ManhattanDistance, ManhattanImproved)):
            # ManhattanDistance and ManhattanImproved only take boxes
            h_n = self.heuristics.get(self.initial_state.boxes)
        elif isinstance(self.heuristics, (ManhattanDistanceWithDeadlockDetection)):
            h_n = self.heuristics.get(self.initial_state.boxes, self.game)
        elif isinstance(self.heuristics, (CombinedHeuristicWithDeadlockDetection)):
            h_n = self.heuristics.get(self.initial_state.boxes, self.initial_state.player, self.game)
        else:
            # PlayerDistance or CombinedHeuristic take boxes and player
            h_n = self.heuristics.get(self.initial_state.boxes, self.initial_state.player)

        heapq.heappush(self.priority_queue, (h_n, self.initial_state))  # (h(n), state)
        self.best_heuristic[self.initial_state] = h_n

        while self.priority_queue:
            current_h_n, current_state = heapq.heappop(self.priority_queue)

            if current_state.is_goal():
                f = open("data/stats.csv","a")
                line = f"{self.map.name},Greedy,{self.heuristics.__class__.__name__},{time.time() - answer['execution_time']},{len(self.explored)},{len(self.priority_queue)},{len(self.get_path(current_state)[0])}\n"
                f.write(line)
                f.close()
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
                elif isinstance(self.heuristics, (ManhattanDistanceWithDeadlockDetection)):
                    h_n = self.heuristics.get(new_state.boxes, self.game)
                elif isinstance(self.heuristics, (CombinedHeuristicWithDeadlockDetection)):
                    h_n = self.heuristics.get(new_state.boxes, new_state.player, self.game)
                else:
                    # PlayerDistance or CombinedHeuristic take boxes and player
                    h_n = self.heuristics.get(new_state.boxes, new_state.player)

                if new_state not in self.best_heuristic or h_n < self.best_heuristic[new_state]:
                    self.best_heuristic[new_state] = h_n
                    heapq.heappush(self.priority_queue, (h_n, new_state))
                    self.parent[new_state] = (current_state, direction)

        print("No path found.")
        answer['execution_time'] = time.time() - answer['execution_time']
        answer['path'] = []
        answer['directions'] = []
        answer['explored'] = len(self.explored)
        answer['g_n'] = 0
        return answer

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
    
def execute_g(greedy):
    answer = greedy.search()

    print(f"Execution time: {answer['execution_time']}")
    print(f"Nodes explored: {answer['explored']}")
    print(f"Frontier: {answer['frontier']}")
    print(f"Path length: {len(answer['path'])}")
    print(f"Directions: {answer['directions']}")
    print("-----")
    return answer

def get_greedy(data_map, heuristic, game):
    map = MapInfo(load_map(data_map))

    manhattan_distance = ManhattanDistance(map.targets)
    manhattan_improved = ManhattanImproved(map.targets)
    manhattan_with_deadlock_detection = ManhattanDistanceWithDeadlockDetection(map.targets)
    player_distance = PlayerDistance(map.targets)
    combined_heuristic = CombinedHeuristic(map.targets)
    combined_heuristic_with_deadlock_detection = CombinedHeuristicWithDeadlockDetection(map.targets)

    initial_state = State(map.boxes, map.player, map.targets)

    if heuristic == "manhattan_distance":
        print("Greedy - Manhattan Distance")
        greedy_manhattan = Greedy(initial_state, manhattan_distance, map)
        return execute_g(greedy_manhattan)

    if heuristic == "manhattan_improved":
        print("Greedy - Manhattan Improved")
        greedy_manhattan_improved = Greedy(initial_state, manhattan_improved, map, game)
        return execute_g(greedy_manhattan_improved)
   
    if heuristic == "manhattan_with_deadlock_detection":
        print("Greedy - Manhattan With Deadlock Detection")
        greedy_manhattan_deadlock= Greedy(initial_state, manhattan_with_deadlock_detection, map, game)
        return execute_g(greedy_manhattan_deadlock)

    if heuristic == "player_distance":
        print("Greedy - Player Distance")
        greedy_player_distance = Greedy(initial_state, player_distance, map, game)
        return execute_g(greedy_player_distance)
        greedy_player_distance = Greedy(initial_state, player_distance, map)
        return execute_g(greedy_player_distance)

    if heuristic == "combined":
        print("Greedy - Combined")
        greedy_combined = Greedy(initial_state, combined_heuristic, map, game)
        return execute_g(greedy_combined)

    if heuristic == "combined_with_deadlock_detection":
        print("Greedy - Combined With Deadlock Detection")
        greedy_combined_deadlock = Greedy(initial_state, combined_heuristic_with_deadlock_detection, map, game)
        return execute_g(greedy_combined_deadlock)

    # if csv not exist create and add header
    if 'stats.csv' not in os.listdir('data'):
        file = open('data/stats.csv', 'w')
        file.write('map,algorithm,heuristic,execution_time,explored,frontier,path_length\n')
        file.close()

def run_g_10_times():
    maps = []
    for m in os.listdir('maps'):
        maps.append(MapInfo(load_map(f"maps/{m}"), m))
        map = MapInfo(load_map(f"maps/{m}"), m)
    
        manhattan_distance = ManhattanDistance(map.targets)
        manhattan_improved = ManhattanImproved(map.targets)
        player_distance = PlayerDistance(map.targets)
        combined_heuristic = CombinedHeuristic(map.targets)
        initial_state = State(map.boxes, map.player, map.targets)
        
        print("AStar - Manhattan Distance")
        greedy_manhattan = Greedy(initial_state, manhattan_distance, map)
        execute_g(greedy_manhattan)

        print("AStar - Manhattan Improved")
        greedy_manhattan_improved = Greedy(initial_state, manhattan_improved, map)
        execute_g(greedy_manhattan_improved)
        
        print("AStar - Player Distance")
        greedy_player_distance = Greedy(initial_state, player_distance, map)
        execute_g(greedy_player_distance)
        
        print("AStar - Combined")
        greedy_combined = Greedy(initial_state, combined_heuristic, map)
        execute_g(greedy_combined)

def main():
    run_g_10_times()

if __name__ == "__main__":
    main()