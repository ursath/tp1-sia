class State:
    def __init__(self, boxes, player, move = None):
        self.boxes = boxes
        self.player = player

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, boxed_moved=False):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.boxed_moved = boxed_moved
        
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
    #with open('nodes_explored.txt', 'w') as file:

    # 6: while Fr ≠ ∅ do
    while frontier:

        # 7: Extraer primer nodo de Fr → n
        # bfs -> pop(0) -> saco como una cola
        # dfs -> pop() -> saco como una pila
        current_node = frontier.pop(0)

        # 8-10: if n Goal then return solución
        if is_goal(current_node.state, game):
            return current_node.get_path()
        
        # for debugging purposes
        # iteration = iteration + 1
        #move = current_node.action
        #opposite_move = {"[-1, 0]": "arriba", "[0, 1]": "derecha", "[1, 0]": "abajo" , "[0, -1]": "izquierda"}

        #line = (f"Paso {iteration}: posición_jugador: {current_node.state.player} - movimiento: {current_node.action} - Posiciones cajas: {current_node.state.boxes}\n")
        #file.write(line)

        # 14: n → Exp
        explored.add(current_node.state)

        # 11-13: Expandir el nodo n, sucesores → Fr, Tr
        for move, child_state, cost, boxed_moved in get_children(current_node, game):
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
                boxed_moved= boxed_moved
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
                new_boxes.remove(current_position)
                box = ([current_position[0] + direction[0], current_position[1] + direction[1]])
                new_boxes.append(box)
                new_state = State(new_boxes, current_position, direction)
                boxed_moved = True
            else:
                new_state = State(new_boxes, current_position, direction)

            result.append([direction, new_state, 0, boxed_moved])
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