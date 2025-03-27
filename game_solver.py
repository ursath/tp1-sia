import time
from functools import partial
from a_star import MapInfo
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
            write_output(method, "Éxito", current_node.get_path(), iteration, len(frontier)+iteration, (end_time - start_time) * 1000, current_node.cost, True)
            write_output_for_visualization(map_name,method, (end_time - start_time) * 1000, explored, frontier, iteration)
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
    write_output(method, "Fracaso", current_node.get_path(), iteration, len(frontier)+iteration, (end_time - start_time) * 1000, current_node.cost, True)
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
    if coordinates in walls:
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
        maps = []

    for m in os.listdir('maps'):
        maps.append(MapInfo(load_map(f"maps/{m}"), m))
        map = MapInfo(load_map(f"maps/{m}"), m)
        initial_state = Uninformed_State(map.boxes, map.player)
        uninformed_search_algorithm(map.targets, map.walls, initial_state, is_goal, get_children, None, method)

# For deadlocks -> move to heuristics
def load_all_playable_positions_for_boxes(goals, walls):
    valid_box_positions = []
    
    # Iterate through each goal square
    for goal in goals:
        # Create a set to track explored positions during pulling
        explored = []
        frontier = [[goal[0], goal[1]]]
        explored.append([goal[0], goal[1]])
        
        # Directions for pulling (opposite of pushing)
        directions = [
            [1, 0],   # Down to Up
            [-1, 0],  # Up to Down
            [0, 1],   # Right to Left
            [0, -1]   # Left to Right
        ]

        wall_list = []
        for wall in walls:
            wall_list.append([wall[0],wall[1]])
        
        # Breadth-first search to pull the box
        while frontier:
            current_position = frontier.pop(0)
            
            # Try pulling from each direction
            for direction in directions:
                # Calculate the box position before pulling
                box_position = [
                    current_position[0] - direction[0], 
                    current_position[1] - direction[1]
                ]
                
                # Calculate the player position that would allow this pull
                player_position = [
                    box_position[0] - direction[0], 
                    box_position[1] - direction[1]
                ]
                
                # Check if the pull is valid:
                # 1. Box position is not a wall
                # 2. Player position is not a wall
                # 3. Box position hasn't been explored before
                if (box_position not in wall_list and
                    player_position not in wall_list and 
                    box_position not in explored):
                    
                    # Mark this position as explored and add to frontier
                    explored.append(box_position)
                    frontier.append(box_position)
        
        # Add all explored positions to valid box positions
        for pos in explored:
            if pos not in valid_box_positions:
                valid_box_positions.append(pos)
    
    return valid_box_positions

def check_simple_deadlock_for_boxes(boxes, valid_box_positions):
    for box in boxes:
        for valid_box in valid_box_positions:
            if box[0] == valid_box[0] and box[1] == valid_box[1]:
                return False     
    return True

def check_freeze_deadlock(state, game):
    for box in state.boxes:
        is_freezed = check_box_freezed(box, state, game)
        if (is_freezed):
            return True
    return False


def check_box_freezed(box, state, game):
    # Check if the box is already on a goal - if so, it can't be frozen
    if box in game.goals:
        return False

    # Check horizontal freezing
    is_freezed_horizontally = False
    left_position = [box[0], box[1]-1]
    right_position = [box[0], box[1]+1]

    # Wall blocking horizontally
    if left_position in game.walls and right_position in game.walls:
        is_freezed_horizontally = True
    
    # Deadlock squares blocking horizontally
    if (not is_freezed_horizontally and 
        check_simple_deadlock_for_boxes([left_position], game) and 
        check_simple_deadlock_for_boxes([right_position], game)):
        is_freezed_horizontally = True
    
    # Recursive check for boxes blocking horizontally
    if not is_freezed_horizontally:
        # Check if boxes on left or right are blocking
        if (left_position in state.boxes and 
            check_box_freezed(left_position, state, game)) or \
           (right_position in state.boxes and 
            check_box_freezed(right_position, state, game)):
            is_freezed_horizontally = True

    # If horizontally blocked, check vertical freezing
    if is_freezed_horizontally:
        is_freezed_vertically = False
        up_position = [box[0]-1, box[1]]
        down_position = [box[0]+1, box[1]]

        # Wall blocking vertically
        if up_position in game.walls and down_position in game.walls:
            is_freezed_vertically = True
        
        # Deadlock squares blocking vertically
        if (not is_freezed_vertically and 
            check_simple_deadlock_for_boxes([up_position], game) and 
            check_simple_deadlock_for_boxes([down_position], game)):
            is_freezed_vertically = True
        
        # Recursive check for boxes blocking vertically
        if not is_freezed_vertically:
            # Check if boxes above or below are blocking
            if (up_position in state.boxes and 
                check_box_freezed(up_position, state, game)) or \
               (down_position in state.boxes and 
                check_box_freezed(down_position, state, game)):
                is_freezed_vertically = True

        # Box is frozen only if blocked both horizontally and vertically
        return is_freezed_vertically
    
    return False

def check_deadlocks(state, game):
    simple = check_simple_deadlock_for_boxes(state.boxes, game) 
    freeze = check_freeze_deadlock(state, game)
    if simple:
        print(f"there was a simple deadlock in {state.boxes}")
    if freeze:
        print(f"there was a freeze deadlock in {state.boxes}")
    return simple or freeze

def check_corral_deadlock(walls,goals,player,boxes,box_moved,valid_boxes):

    state = Uninformed_State(boxes,player)

    reachable_positions = []
    reachable_positions = get_reachable_positions(walls,state)

    # With the reachable positions, we can get the area the player cannot reach (corral)
    corral = []
    corral = get_corral(reachable_positions, walls,state,valid_boxes)

    if not box_moved:
        return False

    if not corral:
        return False

    # Then delete the boxes that are not in the corral, so we can check if the corral is a deadlock 
    deleted_boxes_state, deleted_boxes = delete_boxes(corral,state,walls)

    if not valid_corral(deleted_boxes_state,corral,goals):
        return True

    # Try to get all the boxes in the corral to a goal
    new_is_goal = partial(is_corral_goal, corral=corral,deleted_boxes=deleted_boxes,walls=walls,goals=goals)

    
    corral_solution = uninformed_search_algorithm(walls,goals, deleted_boxes_state, new_is_goal, get_children, None, "bfs")

    # If there is no solution, then the corral is a deadlock
    # If any of the boxes in the corral is freezed, then the corral is a deadlock
    if corral_solution == None:
        return True
    
    # If there is a partial solution, then we need to place the boxes we deleted before
    # If any box exited the corral, then the corral was not a deadlock
    else:
        return False        
    


def valid_corral(state,corral,goals):

    goals_in_corral = 0
    for goal in goals:
        if inside_corral(corral, goal):
            goals_in_corral += 1

    if goals_in_corral == len(state.boxes):
        return True
    
    return False

    
def is_corral_goal(state, game,corral,deleted_boxes,walls,goals):

    if any_box_exit_corral(state, game,corral):
        return True
    
    boxes_placed = 0
    for box in state.boxes:
        if tuple(box) in game:
            boxes_placed += 1

    # If all the boxes inside the corral are placed in a goal, then we have to place the boxes deleted before
    if boxes_placed == len(state.boxes):
        for box in deleted_boxes:
            state.boxes.append(box)
        state = Uninformed_State(state.boxes, state.player)
        uninformed_search_algorithm(walls,goals, state, is_goal, get_children, None, "dfs")

    return False


def any_box_exit_corral(state, game,corral):

    for box in state.boxes:
        if not inside_corral(corral, box):
            return True

    return False

def delete_boxes(corral, state,game):

    new_state_boxes = []
    deleted_boxes = []

    for box in state.boxes:
        new_state_boxes.append(box)

    for box in state.boxes:
        #if not check_box_freezed(box,state,game):
            if not inside_corral(corral, box):
                new_state_boxes.remove(box)
                deleted_boxes.append(box)

    new_state = Uninformed_State(new_state_boxes, state.player)
    return new_state, deleted_boxes


def inside_corral(corral, box):
    for position in corral:
        if box[0] == position[0] and box[1] == position[1]:
            return True
    return False


def get_corral(reachable_positions, game, state,valid_boxes):
    corral = set()
    for position in valid_boxes:
        if tuple(position) not in reachable_positions and position not in state.boxes:
            corral.add(tuple(position))
    
    return get_adyacent(corral,game)


def get_adyacent(reachable_positions,walls):
    corral = set(reachable_positions)
    directions= [[- 1, 0], [0, 1], [1, 0], [0, -1]]

    for x,y in reachable_positions:
        for dx,dy in directions:
            if (x+dx,y+dy) not in reachable_positions and (x+dx,y+dy) in walls:
                corral.add((x+dx,y+dy))

    return corral


def get_reachable_positions(walls,state):

    frontier = []
    reachable_positions = []

    initial_node = Node (state)
    frontier.append(initial_node)

    while frontier:
        for frontier_node in frontier:
            for move, child_state, cost, boxed_moved, depth in get_children(frontier_node, walls):
            
                if boxed_moved:
                    continue

                child_node = Node(child_state, frontier_node, move, cost, boxed_moved, depth)
                
                if any(n.state.player == child_state.player for n in frontier):
                    continue

                if tuple(child_state.player) not in reachable_positions:
                    frontier.append(child_node)
    
            reachable_positions.append(tuple(frontier_node.state.player))
            frontier.remove(frontier_node)
            array = []
            for f in frontier:
                array.append(f.state.player)
    
    return reachable_positions


