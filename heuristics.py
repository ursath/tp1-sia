from scipy.optimize import linear_sum_assignment
from game_solver import check_simple_deadlock_for_boxes
from game_solver import check_corral_deadlock

class HeuristicBase:
    def __init__(self, goals,walls=None):
        self.goals = goals
        self.walls = walls

# La heurística de Manhattan consiste en la suma de las distancias de cada bloque a su objetivo más cercano
# No considera obstaculos
class ManhattanDistance(HeuristicBase):
    def get(self, boxes):
        manhattan_distance = 0
        for box in boxes:
            min_distance = float('inf')
            for goal in self.goals:
                min_distance = min(min_distance, abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
            manhattan_distance += min_distance
        return manhattan_distance
    
class ManhattanDistanceWithDeadlockDetection(ManhattanDistance):
    def get(self, boxes, valid_boxes):
        if check_simple_deadlock_for_boxes(boxes, valid_boxes) :
            return float('inf')
        return super.get(boxes)

# Mejora de la heurística de Manhattan: no permite que dos cajas tengan un mismo objetivo
# No considera obstaculos
class ManhattanImproved(HeuristicBase):
    def get(self, boxes):
        matrix = []
        for box in boxes:
            row = []
            for goal in self.goals:
                row.append(abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
            matrix.append(row)
        
        # Uso el algoritmo de Kuhn-Munkres para encontrar la asignación que minimiza la suma de las distancias sin que dos cajas tengan el mismo objetivo
        row_ind, col_ind = linear_sum_assignment(matrix)
        total_cost = 0
        for i in range(len(row_ind)):
            total_cost += matrix[row_ind[i]][col_ind[i]]
        return total_cost

# Calcula la distancia mínima del jugador a cada caja
class PlayerDistance(HeuristicBase):
    def get(self, boxes, player):
        min_distance = float('inf')
        for box in boxes:
            min_distance = min(min_distance, abs(player[0] - box[0]) + abs(player[1] - box[1]))
        return min_distance
    
# Combinación de las heurísticas de Manhattan y PlayerDistance
# Retorna la suma de ambas
class CombinedHeuristic(HeuristicBase):
    def get(self, boxes, player):
        return ManhattanDistance(self.goals).get(boxes) + PlayerDistance(self.goals).get(boxes, player)
    
class CombinedHeuristicWithDeadlockDetection(HeuristicBase):
    def get(self, boxes, player, valid_boxes):
        if check_simple_deadlock_for_boxes(boxes, valid_boxes):
            return float('inf')
        return CombinedHeuristic(self.goals).get(boxes, player)
    
class ManhattanDistanceWithCorralDeadlockDetection(HeuristicBase):
    def get(self, boxes,player, valid_boxes,box_moved):
        if check_corral_deadlock(self.walls,self.goals,player,list(boxes),box_moved,valid_boxes):
            return float('inf')
        return ManhattanDistance(self.goals).get(boxes)

        