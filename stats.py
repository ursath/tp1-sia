from a_star import run_a_10_times
from greedy import run_g_10_times
from uninformative_searchs import run_uninformative_search
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic, ManhattanDistanceWithDeadlockDetection, CombinedHeuristicWithDeadlockDetection
import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

filename = 'data/stats.csv'

graphs_folder = 'data/graphs/'

if not os.path.exists(filename):
    with open(filename, 'w') as file:
        file.write('map,algorithm,heuristic,execution_time,explored,frontier,path_length\n')
file = open(filename, 'a')

def exp_nodes_by_heuristic(map_name, algorithm):
    df = pd.read_csv(filename)
    df['explored'] = pd.to_numeric(df['explored'])
    df['heuristic'] = df['heuristic'].astype(str)

    df = df[(df['map'] == map_name) & (df['algorithm'] == algorithm)]

    df_manhattan = df[df['heuristic'] == 'ManhattanDistance']
    df_manhattan_improved = df[df['heuristic'] == 'ManhattanImproved']
    df_player_distance = df[df['heuristic'] == 'PlayerDistance']
    df_combined = df[df['heuristic'] == 'CombinedHeuristic']
    df_manhattan_dl = df[df['heuristic'] == 'ManhattanDistanceWithDeadlockDetection']
    df_combined_dl = df[df['heuristic'] == 'CombinedHeuristicWithDeadlockDetection']

    man_avg = df_manhattan['explored'].mean()
    man_std = df_manhattan['explored'].std()

    man_imp_avg = df_manhattan_improved['explored'].mean()
    man_imp_std = df_manhattan_improved['explored'].std()

    player_avg = df_player_distance['explored'].mean()
    player_std = df_player_distance['explored'].std()

    combined_avg = df_combined['explored'].mean()
    combined_std = df_combined['explored'].std()

    man_dl_avg = df_manhattan_dl['explored'].mean()
    man_dl_std = df_manhattan_dl['explored'].std()

    combined_dl_avg = df_combined_dl['explored'].mean()
    combined_dl_std = df_combined_dl['explored'].std()

    plt.bar(['Distancia Manhattan', 'Manhattan Mejorada', 'Distancia del Jugador', 'Heuristica Combinada', 'Manhattan (Deadlock)', 'Combinada (Deadlock)'], [man_avg, man_imp_avg, player_avg, combined_avg, man_dl_avg, combined_dl_avg], color=['blue', 'orange', 'green', 'red'])
    plt.ylabel('Nodos Expandidos')
    plt.xticks(rotation=45)
    plt.title(f'Nodos Expandidos para el Mapa {map_name[:-4]} con el algoritmo {algorithm}')
    #plt.savefig(f'{graphs_folder}exp_nodes_{map_name[:-4]}_{algorithm}.png')
    plt.show()

## camino optimo segun heurisitca para greedy
def optimal_path_by_heuristic(map_name, method):
    df = pd.read_csv(filename)
    df = df[(df['map'] == map_name) & (df['algorithm'] == method)]


    df_manhattan = df[df['heuristic'] == 'ManhattanDistance']
    df_manhattan_improved = df[df['heuristic'] == 'ManhattanImproved']
    df_player_distance = df[df['heuristic'] == 'PlayerDistance']
    df_combined = df[df['heuristic'] == 'CombinedHeuristic']
    df_manhattan_dl = df[df['heuristic'] == 'ManhattanDistanceWithDeadlockDetection']
    df_combined_dl = df[df['heuristic'] == 'CombinedHeuristicWithDeadlockDetection']

    path_manhattan = df_manhattan['path_length'].mean()
    path_manhattan_avg = df_manhattan['path_length'].std()

    path_manhattan_improved = df_manhattan_improved['path_length'].mean()
    path_manhattan_improved_avg = df_manhattan_improved['path_length'].std()

    path_player_distance = df_player_distance['path_length'].mean()
    path_player_distance_avg = df_player_distance['path_length'].std()

    path_combined = df_combined['path_length'].mean()
    path_combined_avg = df_combined['path_length'].std()

    man_dl_path = df_manhattan_dl['path_length'].mean()
    man_dl_path_std = df_manhattan_dl['path_length'].std()

    combined_dl_path = df_combined_dl['path_length'].mean()
    combined_dl_path_std = df_combined_dl['path_length'].std()


    plt.bar(['Distancia Manhattan', 'Manhattan Mejorada', 'Distancia del Jugador', 'Heuristica Combinada', 'Manhattan (Deadlock)', 'Combinada (Deadlock)'], [path_manhattan, path_manhattan_improved, path_player_distance, path_combined, man_dl_path, combined_dl_path], color=['blue', 'orange', 'green', 'red'])
    plt.xticks(rotation=45)
    plt.ylabel('Longitud del camino')
    plt.title(f'Longitud del camino optimo para el Mapa {map_name[:-4]} con el algoritmo {method}')
    #plt.savefig(f'{graphs_folder}optimal_path_{map_name[:-4]}.png')
    plt.show()


# Tiempo promedio en n iteraciones de x algoritmo
def bfs_vs_dfs_average_time(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_dfs = df[df['algorithm'] == 'dfs'].groupby('map')
    df_bfs = df[df['algorithm'] == 'bfs'].groupby('map')

    mean_dfs = df_dfs.get_group(map_name)['execution_time_ms'].mean()
    mean_bfs = df_bfs.get_group(map_name)['execution_time_ms'].mean()

    plt.bar(['bfs', 'dfs'], [mean_bfs, mean_dfs], color=['blue', 'orange'])
    plt.ylim(bottom=0)
    plt.ylabel('Tiempo de Ejecucion (ms)')
    plt.title(f'Tiempo de Ejecucion para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_time_{map_name[:-4]}.png')
    plt.show()


def greedy_vs_astar_average_time(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy = df[df['algorithm'] == 'Greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['execution_time_ms'].mean()
    std_greedy = df_greedy.get_group(map_name)['execution_time_ms'].std()
    mean_a_star = df_a_star.get_group(map_name)['execution_time_ms'].mean()
    std_a_star = df_a_star.get_group(map_name)['execution_time_ms'].std()
   
    print(f"Greedy: {mean_greedy} std: {std_greedy}")

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.errorbar(['Greedy', 'A*'], [mean_greedy, mean_a_star], yerr=[std_greedy, std_a_star], fmt='o', color='black')
    plt.ylim(bottom=0)
    plt.ylabel('Tiempo de Ejecucion (ms)')
    plt.title(f'Tiempo de Ejecucion para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_time_{map_name[:-4]}.png')
    plt.show()
    

def greedy_vs_astar_average_frontier_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy = df[df['algorithm'] == 'Greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['frontier'].mean()
    std_greedy = df_greedy.get_group(map_name)['frontier'].std()
    mean_a_star = df_a_star.get_group(map_name)['frontier'].mean()
    std_a_star = df_a_star.get_group(map_name)['frontier'].std()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.errorbar(['Greedy', 'A*'], [mean_greedy, mean_a_star], yerr=[std_greedy, std_a_star], fmt='o', color='black')
    plt.ylim(bottom=0)
    plt.ylabel('Nodos Frontera')
    plt.title(f'Cantidad Promedio de Nodos Frontera para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()


def bfs_vs_dfs_average_frontier_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_dfs = df[df['algorithm'] == 'dfs'].groupby('map')
    df_bfs = df[df['algorithm'] == 'bfs'].groupby('map')

    mean_dfs = df_dfs.get_group(map_name)['frontier'].mean()
    mean_bfs = df_bfs.get_group(map_name)['frontier'].mean()

    plt.bar(['bfs', 'dfs'], [mean_bfs, mean_dfs], color=['blue', 'orange'])
    plt.ylim(bottom=0)
    plt.ylabel('Nodos Frontera')
    plt.title(f'Cantidad Promedio de Nodos Frontera para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()


def bfs_vs_dfs_average_explored_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_dfs = df[df['algorithm'] == 'dfs'].groupby('map')
    df_bfs = df[df['algorithm'] == 'bfs'].groupby('map')

    mean_dfs = df_dfs.get_group(map_name)['frontier'].mean()
    mean_bfs = df_bfs.get_group(map_name)['frontier'].mean()

    plt.bar(['bfs', 'dfs'], [mean_bfs, mean_dfs], color=['blue', 'orange'])
    plt.ylim(bottom=0)
    plt.ylabel('Nodos Explorados')
    plt.title(f'Cantidad Promedio de Nodos Explorados para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()


def greedy_vs_astar_average_explored_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy = df[df['algorithm'] == 'Greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['explored'].mean()
    std_greedy = df_greedy.get_group(map_name)['explored'].std()
    mean_a_star = df_a_star.get_group(map_name)['explored'].mean()
    std_a_star = df_a_star.get_group(map_name)['explored'].std()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.errorbar(['Greedy', 'A*'], [mean_greedy, mean_a_star], yerr=[std_greedy, std_a_star], fmt='o', color='black')
    plt.ylim(bottom=0)
    plt.ylabel('Nodos Explorados')
    plt.title(f'Cantidad Promedio de Nodos Explorados para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
    plt.show()


def bfs_vs_dfs_frontier_nodes_all():
    df = pd.read_csv(filename)
    df['frontier'] = pd.to_numeric(df['frontier'])

    df_dfs_mean = df[df['algorithm'] == 'dfs'].groupby('map')['frontier'].mean()
    df_bfs_mean = df[df['algorithm'] == 'bfs'].groupby('map')['frontier'].mean()

    maps = df['map'].unique()

    dfs_times = [df_dfs_mean.get(map_name, 0) for map_name in maps]
    bfs_times = [df_bfs_mean.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps)) 
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, bfs_times, width, label='BFS', color='blue')
    ax.bar(x + width/2, dfs_times, width, label='DFS', color='orange')

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Frontera')
    ax.set_title('Cantidad Promedio de Nodos Frontera para Cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}frontier_nodes_all_maps.png')
    plt.show()


def bfs_vs_dfs_exp_nodes_all():
    df = pd.read_csv(filename)
    df['explored'] = pd.to_numeric(df['explored'])

    df_dfs_mean = df[df['algorithm'] == 'dfs'].groupby('map')['explored'].mean()
    df_bfs_mean = df[df['algorithm'] == 'bfs'].groupby('map')['explored'].mean()

    maps = df['map'].unique()

    dfs_times = [df_dfs_mean.get(map_name, 0) for map_name in maps]
    bfs_times = [df_bfs_mean.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps)) 
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, bfs_times, width, label='BFS', color='blue')
    ax.bar(x + width/2, dfs_times, width, label='DFS', color='orange')

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Explorados')
    ax.set_title('Cantidad Promedio de Nodos Explorados para Cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}frontier_nodes_all_maps.png')
    plt.show()


def greedy_vs_a_star_frontier_nodes_all():
    df = pd.read_csv(filename)
    df['frontier'] = pd.to_numeric(df['frontier'])

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['frontier'].mean()
    df_greedy_std = df[df['algorithm'] == 'Greedy'].groupby('map')['frontier'].std()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['frontier'].mean()
    df_a_star_std = df[df['algorithm'] == 'A*'].groupby('map')['frontier'].std()

    maps = df['map'].unique()

    greedy_times = [df_greedy_mean.get(map_name, 0) for map_name in maps]
    greedy_std_dev = [df_greedy_std.get(map_name, 0) for map_name in maps]
    a_star_times = [df_a_star_mean.get(map_name, 0) for map_name in maps]
    a_star_std_dev = [df_a_star_std.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps)) 
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, greedy_times, width, label='Greedy', color='blue')
    ax.bar(x + width/2, a_star_times, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_times, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_times, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Frontera')
    ax.set_title('Cantidad Promedio de Nodos Frontera para Cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}frontier_nodes_all_maps.png')
    plt.show()

# Greedy vs A* en un mapa (nodos expandidos vs tamaño del mapa)
def greedy_vs_a_star_exp_nodes_all():
    df = pd.read_csv(filename)
    df['explored'] = pd.to_numeric(df['explored'])

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['explored'].mean()
    df_greedy_std = df[df['algorithm'] == 'Greedy'].groupby('map')['explored'].std()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['explored'].mean()
    df_a_star_std = df[df['algorithm'] == 'A*'].groupby('map')['explored'].std()

    maps = df['map'].unique()

    greedy_times = [df_greedy_mean.get(map_name, 0) for map_name in maps]
    greedy_std_dev = [df_greedy_std.get(map_name, 0) for map_name in maps]
    a_star_times = [df_a_star_mean.get(map_name, 0) for map_name in maps]
    a_star_std_dev = [df_a_star_std.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps)) 
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, greedy_times, width, label='Greedy', color='blue')
    ax.bar(x + width/2, a_star_times, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_times, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_times, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Explorados')
    ax.set_title('Cantidad Promedio de Nodos Explorados para Cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}frontier_nodes_all_maps.png')
    plt.show()


def path_len_bfs_vs_a_dfs():
    df = pd.read_csv(filename)

    df_bfs_mean = df[df['algorithm'] == 'bfs'].groupby('map')['path_length'].mean()
    df_dfs_mean = df[df['algorithm'] == 'dfs'].groupby('map')['path_length'].mean()

    maps = df['map'].unique()

    dfs_path = [df_dfs_mean.get(map_name, 0) for map_name in maps]
    bfs_path = [df_bfs_mean.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps))
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, bfs_path, width, label='BFS', color='blue')
    ax.bar(x + width/2, dfs_path, width, label='DFS', color='orange')

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Longitud del camino')
    ax.set_title('Longitud del Camino para cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}path_len_maps.png')
    plt.show()


def path_len_greed_vs_a_star():
    df = pd.read_csv(filename)

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['path_length'].mean()
    df_greedy_std = df[df['algorithm'] == 'Greedy'].groupby('map')['path_length'].std()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['path_length'].mean()
    df_a_star_std = df[df['algorithm'] == 'A*'].groupby('map')['path_length'].std()

    maps = df['map'].unique()

    greedy_path = [df_greedy_mean.get(map_name, 0) for map_name in maps]
    greedy_std_dev = [df_greedy_std.get(map_name, 0) for map_name in maps]
    a_star_path = [df_a_star_mean.get(map_name, 0) for map_name in maps]
    a_star_std_dev = [df_a_star_std.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps))
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - width/2, greedy_path, width, label='Greedy', color='blue')
    ax.bar(x + width/2, a_star_path, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_path, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_path, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Longitud del camino')
    ax.set_title('Longitud del Camino para cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}path_len_maps.png')
    plt.show()


def path_len_all(map):
    df = pd.read_csv(filename)

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['path_length'].mean()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['path_length'].mean()
    df_bfs_mean = df[df['algorithm'] == 'bfs'].groupby('map')['path_length'].mean()
    df_dfs_mean = df[df['algorithm'] == 'dfs'].groupby('map')['path_length'].mean()

    maps = df['map'].unique()

    greedy_path = [df_greedy_mean.get(map_name, 0) for map_name in maps]
    a_star_path = [df_a_star_mean.get(map_name, 0) for map_name in maps]
    bfs_path = [df_bfs_mean.get(map_name, 0) for map_name in maps]
    dfs_path = [df_dfs_mean.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps))
    width = 0.2  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(x - 1.5 * width, greedy_path, width, label='Greedy', color='blue')
    ax.bar(x - 0.5 * width, a_star_path, width, label='A*', color='orange')
    ax.bar(x + 0.5 * width, bfs_path, width, label='BFS', color='green')
    ax.bar(x + 1.5 * width, dfs_path, width, label='DFS', color='red')

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Longitud del camino')
    ax.set_title('Longitud del Camino para cada Mapa')
    ax.legend()
    plt.ylim(bottom=0)
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}path_len_maps.png')
    plt.show()

def average_explored_vs_frontier_nodes(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy = df[df['algorithm'] == 'Greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')
    df_dfs = df[df['algorithm'] == 'dfs'].groupby('map')
    df_bfs = df[df['algorithm'] == 'bfs'].groupby('map')

    # Promedios de la frontera
    mean_greedy_frontier = df_greedy.get_group(map_name)['frontier'].mean()
    mean_a_star_frontier = df_a_star.get_group(map_name)['frontier'].mean()
    mean_dfs_frontier = df_dfs.get_group(map_name)['frontier'].mean()
    mean_bfs_frontier = df_bfs.get_group(map_name)['frontier'].mean()

    # Promedios de los nodos explorados
    mean_greedy_explored = df_greedy.get_group(map_name)['explored'].mean()
    mean_a_star_explored = df_a_star.get_group(map_name)['explored'].mean()
    mean_dfs_explored = df_dfs.get_group(map_name)['explored'].mean()
    mean_bfs_explored = df_bfs.get_group(map_name)['explored'].mean()

    # Cálculo de porcentajes
    perc_greedy = mean_greedy_explored / mean_greedy_frontier
    perc_a_star = mean_a_star_explored / mean_a_star_frontier
    perc_dfs = mean_dfs_explored / mean_dfs_frontier
    perc_bfs = mean_bfs_explored / mean_bfs_frontier

    # Gráfico
    plt.bar(['Greedy', 'A*', 'DFS', 'BFS'], [perc_greedy, perc_a_star, perc_dfs, perc_bfs], 
            color=['blue', 'orange', 'red', 'green'])
    plt.ylim(bottom=0)
    plt.ylabel('nodos explorados / frontera')
    plt.title(f'Proporción de nodos explorados de la Frontera para el Mapa {map_name[:-4]}')
    plt.show()

def avg_running_time():
    df = pd.read_csv(filename)

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['execution_time'].mean()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['execution_time'].mean()

    greedy_time = df_greedy_mean.mean()
    a_star_time = df_a_star_mean.mean()

    print(f'Tiempo de ejecucion promedio para Greedy: {greedy_time} error: {df_greedy_mean.std()}')
    print(f'Tiempo de ejecucion promedio para A*: {a_star_time} error: {df_a_star_mean.std()}')

def main():
    #run_a_10_times()
    #run_g_10_times()
    #run_uninformative_search("dfs")
    #run_uninformative_search("bfs")

    # Gráficos de comparación entre bfs y dfs
    #bfs_vs_dfs_average_time('Medio.txt')
    #bfs_vs_dfs_average_frontier_nodes('Medio.txt')
    #bfs_vs_dfs_average_explored_nodes('Medio.txt')

    #bfs_vs_dfs_exp_nodes_all()
    #bfs_vs_dfs_frontier_nodes_all()

    #path_len_bfs_vs_a_dfs()

    # Gráficos de comparación entre greedy y a*
    #greedy_vs_astar_average_time('Dificil.txt')
    #greedy_vs_astar_average_frontier_nodes('Dificil.txt')
    #greedy_vs_astar_average_explored_nodes('Dificil.txt')

    #greedy_vs_a_star_exp_nodes_all()
    #greedy_vs_a_star_frontier_nodes_all()

    #path_len_greed_vs_a_star()

    # Gráficos de comparación entre heurísticas
    #exp_nodes_by_heuristic('Medio.txt', 'Greedy')
    #exp_nodes_by_heuristic('Medio.txt', 'A*')

    #optimal_path_by_heuristic('Medio.txt', 'Greedy')
    #optimal_path_by_heuristic('Medio.txt', 'A*')

    # Gráficos de comparación entre los 4 métodos: bfs, dfs, greedy, a*
    # path_len_all('Medio.txt')
    average_explored_vs_frontier_nodes('Medio.txt')

    avg_running_time()

if __name__ == "__main__":
    main()