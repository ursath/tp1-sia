from a_star import run_a_10_times
from greedy import run_g_10_times
from heuristics import ManhattanDistance, ManhattanImproved, PlayerDistance, CombinedHeuristic
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

# Tiempo promedio en n iteraciones de x algoritmo
def average_time(map_name):
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy = df[df['algorithm'] == 'Greedy'].groupby('map')
    df_a_star = df[df['algorithm'] == 'A*'].groupby('map')

    mean_greedy = df_greedy.get_group(map_name)['execution_time_ms'].mean()
    std_greedy = df_greedy.get_group(map_name)['execution_time_ms'].std()
    mean_a_star = df_a_star.get_group(map_name)['execution_time_ms'].mean()
    std_a_star = df_a_star.get_group(map_name)['execution_time_ms'].std()

    plt.bar(['Greedy', 'A*'], [mean_greedy, mean_a_star], color=['blue', 'orange'])
    plt.errorbar(['Greedy', 'A*'], [mean_greedy, mean_a_star], yerr=[std_greedy, std_a_star], fmt='o', color='black')
    plt.ylabel('Tiempo de Ejecucion (ms)')
    plt.title(f'Tiempo de Ejecucion para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_time_{map_name[:-4]}.png')
    plt.show()
    
# Cantidad de nodos frontera promedio en n iteraciones de x algoritmo
def average_frontier_nodes(map_name):
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
    plt.ylabel('Nodos Frontera')
    plt.title(f'Cantidad Promedio de Nodos Frontera para el Mapa {map_name[:-4]}')
    #plt.savefig(f'{graphs_folder}average_frontier_nodes_{map_name[:-4]}.png')
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

    bars_greedy = ax.bar(x - width/2, greedy_times, width, label='Greedy', color='blue')
    bars_a_star = ax.bar(x + width/2, a_star_times, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_times, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_times, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Frontera')
    ax.set_title('Cantidad Promedio de Nodos Frontera para Cada Mapa')
    ax.legend()
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}frontier_nodes_all_maps.png')
    plt.show()

# Greedy vs A* en un mapa (nodos expandidos vs tamaño del mapa)
def greedy_vs_a_star_exp_nodes(map_name):
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

    bars_greedy = ax.bar(x - width/2, greedy_times, width, label='Greedy', color='blue')
    bars_a_star = ax.bar(x + width/2, a_star_times, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_times, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_times, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Nodos Explorados')
    ax.set_title('Nodos Explorados para cada Mapas')
    ax.legend()
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}explored_nodes_maps_all.png')
    plt.show()

# Greedy vs A* comparando distintos mapas 
def greedy_vs_a_star_time():
    df = pd.read_csv(filename)
    df['execution_time'] = pd.to_numeric(df['execution_time'])
    df['execution_time_ms'] = df['execution_time'] 

    df_greedy_mean = df[df['algorithm'] == 'Greedy'].groupby('map')['execution_time_ms'].mean()
    df_greedy_std = df[df['algorithm'] == 'Greedy'].groupby('map')['execution_time_ms'].std()
    df_a_star_mean = df[df['algorithm'] == 'A*'].groupby('map')['execution_time_ms'].mean()
    df_a_star_std = df[df['algorithm'] == 'A*'].groupby('map')['execution_time_ms'].std()

    maps = df['map'].unique()

    greedy_times = [df_greedy_mean.get(map_name, 0) for map_name in maps]
    greedy_std_dev = [df_greedy_std.get(map_name, 0) for map_name in maps]
    a_star_times = [df_a_star_mean.get(map_name, 0) for map_name in maps]
    a_star_std_dev = [df_a_star_std.get(map_name, 0) for map_name in maps]

    x = np.arange(len(maps)) 
    width = 0.4  # Bar width

    fig, ax = plt.subplots(figsize=(10, 6))

    bars_greedy = ax.bar(x - width/2, greedy_times, width, label='Greedy', color='blue')
    bars_a_star = ax.bar(x + width/2, a_star_times, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_times, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_times, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Tiempo de Ejecucion (ms)')
    ax.set_title('Tiempo de Ejecucion Promedio para cada Mapa')
    ax.legend()
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}execution_time_maps.png')
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

    bars_greedy = ax.bar(x - width/2, greedy_path, width, label='Greedy', color='blue')
    bars_a_star = ax.bar(x + width/2, a_star_path, width, label='A*', color='orange')

    # Center the error bar
    ax.errorbar(x - width/2, greedy_path, yerr=greedy_std_dev, fmt='o', color='black', capsize=5)
    ax.errorbar(x + width/2, a_star_path, yerr=a_star_std_dev, fmt='o', color='black', capsize=5)

    ax.set_xticks(x)
    ax.set_xticklabels(maps, rotation=45)
    ax.set_ylabel('Path Length')
    ax.set_title('Path Length for Each Map')
    ax.legend()
    plt.tight_layout()
    #plt.savefig(f'{graphs_folder}path_len_maps.png')
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
    run_a_10_times()
    run_g_10_times()

    # average_time('1.txt')
    # average_frontier_nodes('1.txt')
    # greedy_vs_a_star_exp_nodes('1.txt')
    # greedy_vs_a_star_frontier_nodes_all()
    # greedy_vs_a_star_time()
    # path_len_greed_vs_a_star()
    # avg_running_time()

if __name__ == "__main__":
    main()