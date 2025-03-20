import os

maps_folder = "maps"
map_number = input(f"Choose a map ({len(os.listdir(maps_folder))} Maps Available): ")

with open(f"{maps_folder}/{map_number}.txt") as f:
    map_data = f.read().splitlines()

map = []
for row in map_data:
    map.append(list(row))

print(map)
