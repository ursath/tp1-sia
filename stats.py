from a_star import A_star, MapInfo, State
from greedy import Greedy
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic
import os
from matplotlib import pyplot as plt
import pandas as pd

filename = 'data/stats.csv'

graphs_folder = 'data/graphs/'

if not os.path.exists(filename):
    with open(filename, 'w') as file:
        file.write('map,algorithm,execution_time,explored,frontier,path_length\n')
file = open(filename, 'a')

def load_maps():
    maps = []
    for map_dir in os.listdir('maps'):
        with open(f"maps/{map_dir}", "r") as f:
            maps.append([list(line.strip()) for line in f.readlines()])
    return maps

def a_star_n_times(n):
    maps = load_maps()
    for map in maps:
        map_name = str(maps.index(map)) + ".txt"
        map_info = MapInfo(map)

        manhattan_distance = ManhattanDistance(map_info.targets)
        manhattan_improved = ManhattanImproved(map_info.targets)
        player_distance = PlayerDistance(map_info.targets)
        combined_heuristic = CombinedHeuristic(map_info.targets)

        heuristics = [manhattan_distance, manhattan_improved, player_distance, combined_heuristic]

        for i in range(n):
            initial_state = State(map_info.boxes, map_info.player, map_info.targets)
            for heuristic in heuristics:
                a_star = A_star(initial_state, heuristic, map_info)
                answer = a_star.search()
                file.write(f"{map_name},A*,{answer['execution_time']},{answer['explored']},{answer['frontier']},{len(answer['path'])}\n")

def greedy_n_times(n):
    maps = load_maps()
    for map in maps:
        map_name = str(maps.index(map)+1) + ".txt"
        map_info = MapInfo(map)

        manhattan_distance = ManhattanDistance(map_info.targets)
        manhattan_improved = ManhattanImproved(map_info.targets)
        player_distance = PlayerDistance(map_info.targets)
        combined_heuristic = CombinedHeuristic(map_info.targets)

        heuristics = [manhattan_distance, manhattan_improved, player_distance, combined_heuristic]

        for i in range(n):
            initial_state = State(map_info.boxes, map_info.player, map_info.targets)
            for heuristic in heuristics:
                greedy = Greedy(initial_state, heuristic, map_info)
                answer = greedy.search()
                file.write(f"{map_name},greedy,{answer['execution_time']},{answer['explored']},{answer['frontier']},{len(answer['path'])}\n")

# Tiempo promedio en n iteraciones de x algoritmo
def average_time(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] * 1000

    df_greedy = df[df['algorithm'] == 'greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['execution_time_ms'].mean()
    mean_a_star = df_a_star.get_group(map_name)['execution_time_ms'].mean()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.ylabel('Execution Time (ms)')
    plt.title(f'Average Execution Time for Map {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_time_{map_name[:-4]}.png')
    plt.show()

    
# Cantidad de nodos frontera promedio en n iteraciones de x algoritmo
def average_frontier_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] * 1000

    df_greedy = df[df['algorithm'] == 'greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['frontier'].mean()
    mean_a_star = df_a_star.get_group(map_name)['frontier'].mean()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.ylabel('Frontier Nodes')
    plt.title(f'Average Frontier Nodes for Map {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()

# Greedy vs A* en un mapa (nodos expandidos vs tamaño del mapa)
def greedy_vs_a_star_exp_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] * 1000

    df_greedy = df[df['algorithm'] == 'greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['explored'].mean()
    mean_a_star = df_a_star.get_group(map_name)['explored'].mean()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.ylabel('Explored Nodes')
    plt.title(f'Average Explored Nodes for Map {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()

# Greedy vs A* aumentando el tamaño del mapa (tiempo vs tamaño del mapa)
def greedy_vs_a_star_time():
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] * 1000

    df_greedy = df[df['algorithm'] == 'greedy'].groupby('map')['execution_time_ms'].mean()
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')['execution_time_ms'].mean()

    maps = df['map'].unique()
    greedy_times = [df_greedy.get(map_name, 0) for map_name in maps]
    a_star_times = [df_a_star.get(map_name, 0) for map_name in maps]

    x = range(len(maps))
    plt.bar(x, greedy_times, width=0.4, label='Greedy', color='blue', align='center')
    plt.bar(x, a_star_times, width=0.4, label='A*', color='orange', align='edge')

    plt.xticks(x, maps, rotation=45)
    plt.ylabel('Execution Time (ms)')
    plt.title('Execution Time for Each Map')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    # a_star_n_times(10)
    # greedy_n_times(10)
    file.close()

    #average_time('1.txt')
    #average_frontier_nodes('1.txt')
    # greedy_vs_a_star_exp_nodes('1.txt')
    # greedy_vs_a_star_time()

if __name__ == "__main__":
    main()



