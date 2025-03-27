import time
from functools import partial
from map import MapInfo
import os
from generate_outputs import write_output, write_output_for_visualization

class Uninformed_State:
    def __init__(self, boxes, player, move = None):
        self.boxes = boxes
        self.player = player
    def __eq__(self, other):
        return self.boxes == other.boxes and self.player == other.player
    def __hash__(self):
        return hash((tuple(tuple(box) for box in self.boxes), 
                     tuple(self.player)))

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, boxed_moved=False, depth = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.boxed_moved = boxed_moved
        self.depth = depth
        
    def __lt__(self, other):
        return self.cost < other.cost
        
    def get_path(self):
        path = []
        current_node = self
        while current_node:
            path.append(current_node)
            current_node= current_node.parent
        return list(reversed(path))  

    def get_moves(self):
        path = []
        current_node = self
        while current_node:
            if current_node.action:
                path.append(current_node.action)
            current_node= current_node.parent
        return list(reversed(path))          

def get_children_array(current_node, walls):
    # starts where the player is located in the current state
    starting_point = current_node.state.player
    last_state = current_node.state
    result = []
    directions= [[- 1, 0], [0, 1], [1, 0], [0, -1]]

    for direction in directions:
        current_position = [starting_point[0] + direction[0], starting_point[1] + direction[1]]
        if check_limits_array([starting_point[0] + direction[0], starting_point[1] + direction[1]], walls, last_state, direction):
            new_boxes = last_state.boxes.copy()
            boxed_moved = False
            if current_position in last_state.boxes:
                box = ([current_position[0] + direction[0], current_position[1] + direction[1]])
                if not check_limits_array(box, walls, last_state, direction):
                    continue
                boxed_moved = True
                new_boxes.remove(current_position)
                new_boxes.append(box)
                new_state = Uninformed_State(new_boxes, current_position)
            else:
                new_state = Uninformed_State(new_boxes, current_position)

            result.append([direction, new_state, 1, boxed_moved, current_node.depth + 1])

    return result

def is_goal_array(state, goals):
    for box_position in state.boxes:
        if box_position not in goals:
            return False

    return True

# making sure that the next position is not occupied by a wall or a stucked box
def check_limits_array(coordinates, walls, last_state, direction):
    if coordinates in walls:
        return False
    if coordinates in last_state.boxes:
        if is_blocked_box_for_direction_array(coordinates, last_state, direction):
            return False
    return True


# direction can be only be an array with [dx, dy]
def is_blocked_box_for_direction_array(coordinates, last_state, direction):
    if coordinates not in last_state.boxes:
        return False
    if [coordinates[0] + direction[0], coordinates[1] + direction[1]] in last_state.boxes:
        return True
    return False


def uninformed_search_algorithm(map_name, goals, walls, initial_state, is_goal, get_children, sorting_criteria=None, method="bfs"):
    start_time = time.time()
    # 4: Crear Tr, Fr, Exp vacíos
    # Tr se representa implícitamente mediante los enlaces padre en los nodos
    frontier = []  # Fr
    explored = []  # Exp
    
    # 5: Insertar nodo inicial n0 → Tr, Fr
    initial_node = Node(initial_state)
    frontier.append(initial_node)
    
    # metadata
    iteration = 0
    depth = 0

    # 6: while Fr ≠ ∅ do
    while frontier:
        # 7: Extraer primer nodo de Fr → n
        # bfs -> pop(0) -> saco como una cola
        # dfs -> pop() -> saco como una pila
        if (method == "bfs"):
            current_node = frontier.pop(0)
        else:
            current_node = frontier.pop()

        iteration = iteration + 1
        # 8-10: if n Goal then return solución
        if is_goal(current_node.state, goals):
            end_time = time.time()
            write_output(method, "Éxito", current_node.get_path(), len(explored), len(frontier)+len(explored), (end_time - start_time) * 1000, current_node.cost, True)
            write_output_for_visualization(map_name,method, (end_time - start_time) * 1000, len(explored), len(explored) + len(frontier), current_node.cost)
            return current_node.get_moves()

        # 14: n → Exp
        explored.append(current_node.state)

        # 11-13: Expandir el nodo n, sucesores → Fr, Tr
        for move, child_state, cost, boxed_moved, depth in get_children(current_node, walls):

            # Verificar si el estado ya fue explorado
            if child_state in explored:
                continue

            # Verificar si el estado ya está en la frontera
            if any(n.state == child_state for n in frontier):
                continue

            # Crear nuevo nodo y añadirlo a la frontera
            child_node = Node(
                state = child_state,
                parent = current_node,
                action = move,
                cost = current_node.cost + cost,
                boxed_moved= boxed_moved,
                depth = depth
            )
            frontier.append(child_node)

        # 15: Reordenar Fr según criterio
        if sorting_criteria:
            frontier.sort(key=sorting_criteria)
    
    # 17-19: if Solución vacía then No existe solución
    end_time = time.time()
    write_output(method, "Fracaso", current_node.get_path(), len(explored), len(frontier)+len(explored), (end_time - start_time) * 1000, current_node.cost, True)
    return None

def get_children(current_node, walls):
    # starts where the player is located in the current state
    starting_point = current_node.state.player
    last_state = current_node.state
    result = []
    directions= [[- 1, 0], [0, 1], [1, 0], [0, -1]]

    for direction in directions:
        current_position = [starting_point[0] + direction[0], starting_point[1] + direction[1]]
        if check_limits([starting_point[0] + direction[0], starting_point[1] + direction[1]], walls, last_state, direction):
            new_boxes = last_state.boxes.copy()
            boxed_moved = False
            current_position_tuple = tuple(current_position)
            if current_position_tuple in last_state.boxes:
                box = ([current_position[0] + direction[0], current_position[1] + direction[1]])
                if not check_limits(box, walls, last_state, direction):
                    continue
                boxed_moved = True
                new_boxes.remove(current_position_tuple)
                new_boxes.append(box)
                new_state = Uninformed_State(new_boxes, current_position)
            else:
                new_state = Uninformed_State(new_boxes, current_position)

            result.append([direction, new_state, 1, boxed_moved, current_node.depth + 1])

    return result

def is_goal(state, goals):
    for box_position in state.boxes:
        if box_position not in goals:
            return False

    return True

# making sure that the next position is not occupied by a wall or a stucked box
def check_limits(coordinates, walls, last_state, direction):
    if tuple(coordinates) in walls:
        return False
    if coordinates in last_state.boxes:
        if is_blocked_box_for_direction(coordinates, last_state, direction):
            return False
    return True


# direction can be only be an array with [dx, dy]
def is_blocked_box_for_direction(coordinates, last_state, direction):
    coordinates_tuple = tuple(coordinates)
    if coordinates_tuple not in last_state.boxes:
        return False
    if tuple([coordinates[0] + direction[0], coordinates[1] + direction[1]]) in last_state.boxes:
        return True
    return False

def load_map(map_file):
    with open(map_file, "r") as f:
        return [list(line.strip()) for line in f.readlines()]

def run_uninformative_search(method="bfs"):
    if 'stats.csv' not in os.listdir('data'):
        file = open('data/stats.csv', 'w')
        file.write('map,algorithm,heuristic,execution_time,explored,frontier,path_length\n')
        file.close()

    for m in os.listdir('maps'):
        if (m == "Dificil.txt"):
            continue
        map_data = load_map(f"maps/{m}")
        walls = [] 
        goals = []
        boxes = []

        player_position = [0, 0]
        for row in range(0, len(map_data)):
            for col in range(0, len(map_data[0])):
                current_element = map_data[row][col]
                match current_element:
                    case '#': 
                        walls.append([row, col])
                    case '$':
                        boxes.append([row, col])
                    case '@':
                        player_position = [row,col]
                    case '.':
                        goals.append([row, col])
        current_state = Uninformed_State(boxes, player_position)
        uninformed_search_algorithm(m,goals, walls, current_state, is_goal_array, get_children_array, None, method)
