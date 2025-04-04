import heapq
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic, ManhattanDistanceWithDeadlockDetection, CombinedHeuristicWithDeadlockDetection, ManhattanDistanceWithCorralDeadlockDetection
from deadlocks import load_all_playable_positions_for_boxes
import time
import os
from generate_outputs import write_output, write_output_for_visualization
from map import MapInfo

class State:
    def __init__(self, boxes, player, targets, box_moved=False):
        self.boxes = frozenset(boxes) 
        self.player = player
        self.targets = frozenset(targets)
        self.box_moved = box_moved

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
        box_moved = False
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
            box_moved = True
            new_boxes.remove(new_player_pos)
            new_boxes.add(new_box_pos)
        return State(frozenset(new_boxes), new_player_pos, self.targets, box_moved)

    def is_goal(self):
        return self.boxes == self.targets

class A_star:
    def __init__(self, initial_state, heuristics, map, valid_box_positions):
        self.initial_state = initial_state
        self.heuristics = heuristics
        self.explored = set()
        self.priority_queue = []
        self.g_cost_accum = {initial_state: 0}
        self.parent = {}
        self.frontier = set()
        self.map = map
        self.valid_box_positions = valid_box_positions

    def search(self):

        answer = {}

        answer['frontier'] = 0
        answer['execution_time'] = time.time() # To substract from the end time

        heapq.heappush(self.priority_queue, (0, 0, self.initial_state))  # (f(n), g(n), state)

        while self.priority_queue:
            f_n, g_n, current_state = heapq.heappop(self.priority_queue)

            if current_state.is_goal():
                f = open("data/stats.csv","a")
                line = f"{self.map.name},A*,{self.heuristics.__class__.__name__},{(time.time() - answer['execution_time']) * 1000},{len(self.explored)},{len(self.priority_queue) + len(self.explored)},{len(self.get_path(current_state)[0])}\n"
                f.write(line)
                f.close()

                answer['explored'] = len(self.explored)
                answer['execution_time'] = (time.time() - answer['execution_time']) * 1000
                answer['frontier'] = len(self.explored) + len(self.priority_queue)
                answer['path'] = self.get_path(current_state)[0]
                answer['directions'] = self.get_path(current_state)[1]
                answer['g_n'] = g_n 
                answer['result'] = "Exito"
                return answer

            self.explored.add(current_state)

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_state = current_state.move(direction, self.map)
                if new_state is None or new_state in self.explored:
                    continue

                new_g_n = g_n + 1
                if new_state not in self.g_cost_accum or new_g_n < self.g_cost_accum[new_state]:
                    self.g_cost_accum[new_state] = new_g_n

                    if isinstance(self.heuristics, (ManhattanDistanceWithDeadlockDetection)):
                        f_n = new_g_n + self.heuristics.get(new_state.boxes, self.valid_box_positions)
                    elif isinstance(self.heuristics, (CombinedHeuristicWithDeadlockDetection)):
                        f_n = new_g_n + self.heuristics.get(new_state.boxes, new_state.player, self.valid_box_positions)
                    elif isinstance(self.heuristics, (ManhattanDistanceWithCorralDeadlockDetection)):
                        f_n = new_g_n + self.heuristics.get(new_state.boxes, new_state.player, self.valid_box_positions, new_state.box_moved)
                    elif isinstance(self.heuristics, (ManhattanDistance, ManhattanImproved)):
                        # ManhattanDistance and ManhattanImproved only take boxes
                        f_n = new_g_n + self.heuristics.get(new_state.boxes)
                    else:
                        # PlayerDistance or CombinedHeuristic take boxes and player
                        f_n = new_g_n + self.heuristics.get(new_state.boxes, new_state.player)
                    heapq.heappush(self.priority_queue, (f_n, new_g_n, new_state))
                    self.parent[new_state] = (current_state, direction)

        print("No path found.")
        answer['execution_time'] = (time.time() - answer['execution_time']) * 1000
        answer['path'] = []
        answer['directions'] = []
        answer['explored'] = len(self.explored)
        answer['g_n'] = 0
        answer['result'] = "Fracaso"
        return answer  # No path found
    
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

def run_a_10_times():

    # if csv not exist create and add header
    if 'stats.csv' not in os.listdir('data'):
        file = open('data/stats.csv', 'w')
        file.write('map,algorithm,heuristic,execution_time,explored,frontier,path_length\n')
        file.close()

    maps = []
    for m in os.listdir('maps'):
        maps.append(MapInfo(load_map(f"maps/{m}"), m))
        map = MapInfo(load_map(f"maps/{m}"), m)
        valid_box_positions = load_all_playable_positions_for_boxes(list(map.targets), list(map.walls)) 
    
        manhattan_distance = ManhattanDistance(map.targets)
        manhattan_improved = ManhattanImproved(map.targets)
        player_distance = PlayerDistance(map.targets)
        combined_heuristic = CombinedHeuristic(map.targets)
        manhattan_with_deadlock_detection = ManhattanDistanceWithDeadlockDetection(map.targets)
        combined_heuristic_with_deadlock_detection = CombinedHeuristicWithDeadlockDetection(map.targets)

        initial_state = State(map.boxes, map.player, map.targets)
        print("AStar - Manhattan Distance")
        a_star_manhattan = A_star(initial_state, manhattan_distance, map, valid_box_positions)
        answer = execute_a(a_star_manhattan)
        write_output("AStar_manhattan", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

        a_star_manhattan = A_star(initial_state, manhattan_distance, map, valid_box_positions)
        execute_a(a_star_manhattan)
        print("AStar - Manhattan Improved")
        a_star_manhattan_improved = A_star(initial_state, manhattan_improved, map, valid_box_positions)
        answer = execute_a(a_star_manhattan_improved)
        write_output("AStar_manhattan_improved", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

        print("AStar - Player Distance")
        a_star_player_distance = A_star(initial_state, player_distance, map, valid_box_positions)
        answer = execute_a(a_star_player_distance)
        write_output("AStar_player_distance", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

        print("AStar - Combined")
        a_star_combined = A_star(initial_state, combined_heuristic, map, valid_box_positions)
        answer = execute_a(a_star_combined)
        write_output("AStar_combined", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

        print("AStar - Manhattan With Deadlock Detection")
        a_star_manhattan_with_deadlock = A_star(initial_state, manhattan_with_deadlock_detection, map, valid_box_positions)
        answer = execute_a(a_star_manhattan_with_deadlock)
        write_output("AStar_manhattan_deadlock", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

        print("AStar - Combined With Deadlock Detection")
        a_star_combined_with_deadlock = A_star(initial_state, combined_heuristic_with_deadlock_detection, map, valid_box_positions)
        answer = execute_a(a_star_combined_with_deadlock)
        write_output("AStar_combined_deadlock", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)

def load_map(map_file):
    with open(map_file, "r") as f:
        return [list(line.strip()) for line in f.readlines()]
    
def execute_a(a_star):
    answer = a_star.search()

    print(f"Execution time: {answer['execution_time']}")
    print(f"Nodes explored: {answer['explored']}")
    print(f"Frontier: {answer['frontier']}")
    print(f"Path length: {len(answer['path'])}")
    print(f"g_n: {answer['g_n']}")
    print(f"Directions: {answer['directions']}")
    print("-------")
    return answer


def main():
    run_a_10_times()


if __name__ == "__main__":
    main()

def get_astar(data_map, heuristic, valid_box_positions):
    map = MapInfo(load_map(data_map), "")

    manhattan_distance = ManhattanDistance(map.targets)
    manhattan_improved = ManhattanImproved(map.targets)
    manhattan_with_deadlock_detection = ManhattanDistanceWithDeadlockDetection(map.targets)
    manhattam_with_corral_deadlock_detection = ManhattanDistanceWithCorralDeadlockDetection(map.targets,map.walls)
    player_distance = PlayerDistance(map.targets)
    combined_heuristic = CombinedHeuristic(map.targets)
    combined_heuristic_with_deadlock_detection = CombinedHeuristicWithDeadlockDetection(map.targets)

    initial_state = State(map.boxes, map.player, map.targets)

   
    if heuristic == "manhattan_distance":
        print("AStar - Manhattan Distance")
        a_star_manhattan = A_star(initial_state, manhattan_distance, map, valid_box_positions)
        answer = execute_a(a_star_manhattan)
        write_output("AStar_combined", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer

    if heuristic == "manhattan_improved":
        print("AStar - Manhattan Improved")
        a_star_manhattan_improved = A_star(initial_state, manhattan_improved, map, valid_box_positions)
        answer = execute_a(a_star_manhattan_improved)
        write_output("AStar_manhattan_improved", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer

    if heuristic == "manhattan_with_deadlock_detection":
        print("AStar - Manhattan With Deadlock Detection")
        a_star_manhattan_deadlock= A_star(initial_state, manhattan_with_deadlock_detection, map, valid_box_positions)
        answer = execute_a(a_star_manhattan_deadlock)
        write_output("AStar_manhattan_deadlock", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer
    
    if heuristic == "player_distance":
        print("AStar - Player Distance")
        a_star_player_distance = A_star(initial_state, player_distance, map, valid_box_positions)
        answer = execute_a(a_star_player_distance)
        write_output("AStar_player_distance", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer

    if heuristic == "combined":
        print("AStar - Combined")
        a_star_combined = A_star(initial_state, combined_heuristic, map, valid_box_positions)
        answer = execute_a(a_star_combined)
        write_output("AStar_combined", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer

    if heuristic == "combined_with_deadlock_detection":
        print("AStar - Combined With Deadlock Detection")
        a_star_combined_deadlock = A_star(initial_state, combined_heuristic_with_deadlock_detection , map, valid_box_positions)
        answer = execute_a(a_star_combined_deadlock)
        write_output("AStar_combined_deadlock", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer
        
    if heuristic == "manhattan_with_corral_deadlock_detection":
        print("AStar - Manhattan With Corral Deadlock Detection")
        a_star_manhattan_corral_deadlock = A_star(initial_state, manhattam_with_corral_deadlock_detection, map, valid_box_positions)
        answer = execute_a(a_star_manhattan_corral_deadlock)
        write_output("AStar_combined_deadlock", answer["result"], answer["path"], answer["explored"], answer["frontier"], answer["execution_time"], len(answer["path"]), False)
        return answer
