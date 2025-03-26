import time
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

def uninformed_search_algorithm(game, initial_state, is_goal, get_children, sorting_criteria=None, method="bfs"):
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
        if is_goal(current_node.state, game):
            end_time = time.time()
            write_output(method, "Éxito", current_node, iteration, len(frontier), (end_time - start_time) * 1000)
            write_output_for_visualization(method, current_node)
            return current_node.get_moves()

        # 14: n → Exp
        explored.append(current_node.state)

        # 11-13: Expandir el nodo n, sucesores → Fr, Tr
        for move, child_state, cost, boxed_moved, depth in get_children(current_node, game):

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
    write_output(method, "Fracaso", current_node, iteration, len(frontier), (end_time - start_time) * 1000)
    return None

def get_children(current_node, game):
    # starts where the player is located in the current state
    starting_point = current_node.state.player
    last_state = current_node.state
    result = []
    directions= [[- 1, 0], [0, 1], [1, 0], [0, -1]]

    for direction in directions:
        current_position = [starting_point[0] + direction[0], starting_point[1] + direction[1]]
        if check_limits([starting_point[0] + direction[0], starting_point[1] + direction[1]], game, last_state, direction):
            new_boxes = last_state.boxes.copy()
            boxed_moved = False
            if current_position in last_state.boxes:
                box = ([current_position[0] + direction[0], current_position[1] + direction[1]])
                if not check_limits(box, game, last_state, direction):
                    continue
                boxed_moved = True
                new_boxes.remove(current_position)
                new_boxes.append(box)
                new_state = Uninformed_State(new_boxes, current_position)
            else:
                new_state = Uninformed_State(new_boxes, current_position)

            result.append([direction, new_state, 1, boxed_moved, current_node.depth + 1])

    return result

def is_goal(state, game):
    for box_position in state.boxes:
        if box_position not in game.goals:
            return False

    return True

# making sure that the next position is not occupied by a wall or a stucked box
def check_limits(coordinates, game, last_state, direction):
    if coordinates in game.walls:
        return False
    if coordinates in last_state.boxes:
        if is_blocked_box_for_direction(coordinates, last_state, direction):
            return False
    return True


# direction can be only be an array with [dx, dy]
def is_blocked_box_for_direction(coordinates, last_state, direction):
    if coordinates not in last_state.boxes:
        return False
    if [coordinates[0] + direction[0], coordinates[1] + direction[1]] in last_state.boxes:
        return True
    return False

def write_output(method, result, current_node, iteration, frontier_len, time):
    with open(f'{method}_results.txt', 'w') as file:
        file.write(f"Resultado: {result}\n")
        file.write(f"Costo: {current_node.cost}\n")
        file.write(f"Cantidad de Nodos Expandidos: {iteration}\n")
        file.write(f"Cantidad de Nodos Frontera: {iteration + frontier_len}\n")
        file.write(f"Solución:\n")
        for node in current_node.get_path():
            file.write(f"Paso {node.depth}:\n")
            file.write("Estado:\n")
            file.write(f"*  Posición del jugador: ({node.state.player[0]}, {node.state.player[1]})\n")
            file.write(f"*  Posición de las cajas: [")
            last_index = len(node.state.boxes)-1
            for index in range(last_index):
                file.write(f"({node.state.boxes[index][0]}, {node.state.boxes[index][1]}),")
            file.write(f"({node.state.boxes[last_index][0]}, {node.state.boxes[last_index][1]})]\n")
            push_status = "Si" if node.boxed_moved else "No"
            file.write(f"*  Empuje: {push_status}\n")
            if node.parent:
                file.write(f"Movimiento previo: {node.action}\n\n")
            else:
                file.write(f"\n")
        file.write(f"Tiempo de procesamiento: {time} ms\n")

def write_output_for_visualization(method, current_node):
    with open(f'{method}_visualization.txt', 'w') as file:
        file.write(str(current_node.get_moves()))

# For deadlocks -> move to heuristics
def load_all_playable_positions_for_boxes(goals, walls):
    valid_box_positions = []
    
    # Iterate through each goal square
    for goal in goals:
        # Create a set to track explored positions during pulling
        explored = []
        frontier = [goal]
        explored.append(goal)
        
        # Directions for pulling (opposite of pushing)
        directions = [
            [1, 0],   # Down to Up
            [-1, 0],  # Up to Down
            [0, 1],   # Right to Left
            [0, -1]   # Left to Right
        ]
        
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
                if (box_position not in walls and 
                    player_position not in walls and 
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