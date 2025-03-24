from scipy.optimize import linear_sum_assignment


class HeuristicBase:
    def __init__(self, goals):
        self.goals = goals

class ManhattanDistance(HeuristicBase):
    def get(self, boxes):
        manhattan_distance = 0
        for box in boxes:
            min_distance = float('inf')
            for goal in self.goals:
                min_distance = min(min_distance, abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
            manhattan_distance += min_distance
        return manhattan_distance
    
# Mejora de la heurística de Manhattan: no permite que dos bloques tengan un mismo objetivo
class ManhattanImproved(HeuristicBase):
    def get(self, boxes):
        matrix = []
        for box in boxes:
            row = []
            for goal in self.goals:
                row.append(abs(box[0] - goal[0]) + abs(box[1] - goal[1]))
            matrix.append(row)
        
        # Uso el algoritmo de asignación de Kuhn-Munkres para encontrar la asignación que minimiza la suma de las distancias
        # sin que dos bloques tengan el mismo objetivo
        row_ind, col_ind = linear_sum_assignment(matrix)
        total_cost = 0
        for i in range(len(row_ind)):
            total_cost += matrix[row_ind[i]][col_ind[i]]
        return total_cost



if __name__ == "__main__":
    goals = [[1, 4], [6, 2]]
    HeuristicBase(goals)
    boxes = [[1, 1], [4, 4]]
    heuristic = ManhattanDistance(goals)
    print(heuristic.get(boxes))
    heuristic = ManhattanImproved(goals)
    print(heuristic.get(boxes))
        