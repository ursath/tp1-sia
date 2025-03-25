class State:
    def __init__(self, boxes, player, move = None):
        self.boxes = boxes
        self.player = player
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
            if current_node.action:
                path.append(current_node.action)
            current_node= current_node.parent
        return list(reversed(path))  

def search_algorithm(game, initial_state, is_goal, get_children, sorting_criteria=None):
    # 4: Crear Tr, Fr, Exp vacíos
    # Tr se representa implícitamente mediante los enlaces padre en los nodos
    frontier = []  # Fr
    explored = set()  # Exp
    
    # 5: Insertar nodo inicial n0 → Tr, Fr
    initial_node = Node(initial_state)
    frontier.append(initial_node)
    
    # for debugging purposes we write to a file
    #iteration = 0
    depth = 0
    with open('nodes_explored.txt', 'w') as file:
        # 6: while Fr ≠ ∅ do
        while frontier:

            # 7: Extraer primer nodo de Fr → n
            # bfs -> pop(0) -> saco como una cola
            # dfs -> pop() -> saco como una pila
            current_node = frontier.pop(0)

            # 8-10: if n Goal then return solución
            if is_goal(current_node.state, game):
                return current_node.get_path()

            # for debugging purposes -> uncomment for debug mode :)
                #old debugging format: line = (f"paso {iteration}: posición_jugador: {current_node.state.player} - movimiento: {action_str[move]} - posiciones cajas: {current_node.state.boxes}\n")
                #now uses {depth (tree)} - {u,r,d,l,U,R,D,L} 

            #iteration = iteration + 1
            #action_str = {"[-1, 0]": "u", "[-1, 0]P": "U", "[0, 1]": "r", "[0, 1]P": "R", "[1, 0]": "d", "[1, 0]P": "D" , "[0, -1]": "l", "[0, -1]P": "L"}

            #   move = str(current_node.action)
            #   if (current_node.boxed_moved):
            #       move = move + 'P'

            #if (iteration > 1):
            #    line = (f"{current_node.depth}-{action_str[move]} ")
            #    file.write(line)

            # 14: n → Exp
            explored.add(current_node.state)

            # check deadlocks
            if check_deadlocks(current_node.state, game):
                print("hubo un deadlock pibe 0_0")
                continue

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
        return None

# starts where the player is located in the current state
def get_children(current_node, game):
    # I want to visit every position possible and continue exploring in depth
    # I check positions for up, right, down and left (in that order)
    # I need to check if it is a deadlock
    # I need to make sure that the next move doesn't undo the 
    # last move (I could be in a loop or make more steps) unless there is no other choice and i need to return the parent
    starting_point = current_node.state.player
    last_state = current_node.state
    result = []
    directions= [[- 1, 0], [0, 1], [1, 0], [0, -1]]

    if (current_node.action != None):
        last_move = str(current_node.action)
        opposite_move = {"[-1, 0]": [1, 0], "[0, 1]": [0, -1], "[1, 0]": [-1, 0] , "[0, -1]": [0, 1]}
        undo_last_move = opposite_move[last_move]
        directions.remove(undo_last_move)
     
    for direction in directions:
        current_position = [starting_point[0] + direction[0], starting_point[1] + direction[1]]
        if check_limits([starting_point[0] + direction[0], starting_point[1] + direction[1]], game, last_state, direction):
            # chequeo si existe una caja en la posición a la que nos movemos
            new_boxes = last_state.boxes.copy()
            boxed_moved = False
            if current_position in last_state.boxes:
                box = ([current_position[0] + direction[0], current_position[1] + direction[1]])
                if not check_limits(box, game, last_state, direction):
                    continue
                boxed_moved = True
                new_boxes.remove(current_position)
                new_boxes.append(box)
                new_state = State(new_boxes, current_position)
            else:
                new_state = State(new_boxes, current_position)

            result.append([direction, new_state, 0, boxed_moved, current_node.depth + 1])
            # for greedy -> result.append([direction, new_state, calculate_cost(last_state, game)])

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

def calculate_cost(state, game):
    return 0

#called before search_algorithm, the result is saved in game.valid_box_positions
def load_all_playable_positions_for_boxes(game):
    valid_box_positions = []
    for goal in game.goals:
        initial_node = Node(State([goal], goal, game.goals))
        directions= [[-1, 0], [0, 1], [1, 0], [0, -1]]
        frontier = []
        explored = []
        frontier.append(initial_node)
        explored.append(initial_node.state.boxes[0])
        
        while frontier:
            current_node = frontier.pop(0)
            starting_point = current_node.state.player
            valid_box_positions.append(current_node.state.boxes[0])

            for direction in directions:
                current_box_position = [starting_point[0] + direction[0], starting_point[1] + direction[1]]
                current_player_position = [current_box_position[0] + direction[0], current_box_position[1] + direction[1]]

                if current_box_position in explored:
                    continue
                explored.append(current_box_position)

                if current_player_position not in game.walls:
                    new_state = State([current_box_position], current_player_position, game.goals)

                    frontier.append(Node(new_state))

    game.valid_box_positions = valid_box_positions

def check_simple_deadlock_for_boxes(boxes, game):
    for box in boxes:
        if box not in game.valid_box_positions:
            print("hubo simple deadlock")
            return True
    return False

def check_freeze_deadlock(state, game):
    for box in state.boxes:
        is_freezed = check_box_freezed(box, state, game)
        if (is_freezed):
            return True
    return False

def check_box_freezed(box, state, game):
    is_freezed_horizontally = False
    left_position = [box[0], box[1]-1]
    right_position = [box[0], box[1]+1]
    # If there is a wall on the left or on the right side of the box then the box is blocked along this axis
    if (left_position in game.walls or right_position in game.walls):
        is_freezed_horizontally = True
    # If there is a simple deadlock square on both sides (left and right) of the box then the box is blocked along this axis
    if (not is_freezed_horizontally and check_simple_deadlock_for_boxes([left_position], game) and check_simple_deadlock_for_boxes([right_position], game)):
        is_freezed_horizontally = True
    # If there is a box on the left or right side then this box is blocked if the other box is blocked    
    if (not is_freezed_horizontally and (left_position in state.boxes and check_box_freezed(left_position, state, game)) or (right_position in game.walls and check_box_freezed(right_position, state, game))):
        is_freezed_horizontally = True

    if not is_freezed_horizontally:
        return False

    up_position = [box[0]-1, box[1]]
    down_position = [box[0]+1, box[1]]
    is_freezed_vertically = False

    # If there is a wall below or above the box then the box is blocked along this axis
    if (up_position in game.walls or down_position in game.walls):
        is_freezed_vertically = True
    # If there is a simple deadlock square on both sides (above and below) the box then the box is blocked along this axis
    if (not is_freezed_vertically and check_simple_deadlock_for_boxes([up_position], game) and check_simple_deadlock_for_boxes([down_position], game)):
        is_freezed_vertically = True
    # If there is a box below or above this box then the box is blocked if the other box is blocked    
    if (not is_freezed_vertically and (up_position in state.boxes and check_box_freezed(up_position, state, game)) or (down_position in game.walls and check_box_freezed(down_position, state, game))):
        is_freezed_vertically = True

    return is_freezed_horizontally and is_freezed_vertically

def check_deadlocks(state, game):
    return check_simple_deadlock_for_boxes(state.boxes, game) or check_freeze_deadlock(state, game)