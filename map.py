class MapInfo:
    def __init__(self, map, name):
        self.map = map
        self.name = name
        self.targets = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "."}
        self.boxes = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "$"}
        self.player = next((x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "@")
        self.walls = {(x, y) for x, row in enumerate(map) for y, cell in enumerate(row) if cell == "#"}