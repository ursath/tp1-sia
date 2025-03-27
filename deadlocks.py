from game_solver import Uninformed_State
from game_solver import Node
from game_solver import uninformed_search_algorithm
from game_solver import is_goal
from game_solver import get_children

#from game_solver import *
from functools import partial

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

    
    corral_solution = uninformed_search_algorithm("",goals,walls, deleted_boxes_state, new_is_goal, get_children, None, "bfs")

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
        uninformed_search_algorithm("",goals,walls, state, is_goal, get_children, None, "dfs")

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