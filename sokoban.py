import os
import arcade
from uninformative_searchs import *
from deadlocks import load_all_playable_positions_for_boxes
from greedy import get_greedy
from a_star import get_astar

SCREEN_TITLE = "Sokoban Game"
PNG_SIZE = 64

ELEMENTS = {
    "#": "./textures/wall.png",   # Pared
    " ": "./textures/free.png",   # Espacio libre (null)
    ".": "./textures/goal.png",   # Objetivo
    "@": "./textures/player.png", # Posicion inicial del jugador
    "$": "./textures/box.png",    # Caja
    "*": "./textures/box_goal.png" # Caja sobre objetivo
}

class SokobanGame(arcade.Window):
    def __init__(self, map_file, moves):
        with open(map_file, "r") as f:
            self.map_data = [list(line.strip()) for line in f.readlines()]

        self.walls = [] 
        self.goals = []
        boxes = []

        self.moves = moves  
        self.current_move_index = 0  

        self.player_position = [0, 0]
        for row in range(0, len(self.map_data)):
            for col in range(0, len(self.map_data[0])):
                current_element = self.map_data[row][col]
                match current_element:
                    case '#': 
                        self.walls.append([row, col])
                    case '$':
                        boxes.append([row, col])
                    case '@':
                        self.player_position = [row,col]
                        self.clean_cell(row, col)
                    case '.':
                        self.goals.append([row, col])
                    #case '*':
                        #self.goals.add((row,  col))
                        #boxes.append([row , col])
        self.current_state = Uninformed_State(boxes, self.player_position)

        self.num_rows = len(self.map_data)
        self.num_cols = len(self.map_data[0])
        width = self.num_cols * PNG_SIZE
        height = self.num_rows * PNG_SIZE

        super().__init__(width, height, SCREEN_TITLE)   
        arcade.set_background_color(arcade.color.BLACK)

        self.textures = {
            key: arcade.load_texture(img) if img else None
            for key, img in ELEMENTS.items()
        }

        arcade.schedule(self.update_game, 0.5)

    def on_draw(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = col * PNG_SIZE + PNG_SIZE // 2
                y = (self.num_rows - row - 1) * PNG_SIZE + PNG_SIZE // 2  

                tile = self.map_data[row][col]
                if tile in self.textures and self.textures[tile]:
                    rect = arcade.Rect(x-PNG_SIZE//2, x+PNG_SIZE//2, y-PNG_SIZE//2, y+PNG_SIZE//2, PNG_SIZE, PNG_SIZE, x, y)
                    arcade.draw_texture_rect(self.textures[tile], rect)

        px = self.player_position[1] * PNG_SIZE + PNG_SIZE // 2
        py = (self.num_rows - self.player_position[0] - 1) * PNG_SIZE + PNG_SIZE // 2  
        rect = arcade.Rect(px-PNG_SIZE//2, px+PNG_SIZE//2, py-PNG_SIZE//2, py+PNG_SIZE//2, PNG_SIZE, PNG_SIZE, px, py)
        arcade.draw_texture_rect(self.textures["@"], rect)

        for goal in self.goals:
            if(self.map_data[goal[0]][goal[1]] == " "):
                gx = goal[1] * PNG_SIZE + PNG_SIZE // 2
                gy = (self.num_rows - goal[0] - 1) * PNG_SIZE + PNG_SIZE // 2
                rect = arcade.Rect(gx-PNG_SIZE//2, gx+PNG_SIZE//2, gy-PNG_SIZE//2, gy+PNG_SIZE//2, PNG_SIZE, PNG_SIZE, gx, gy)
                arcade.draw_texture_rect(self.textures["."], rect)


    def update_game(self, delta_time):
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index]
            new_x = self.player_position[0] + move[0]
            new_y = self.player_position[1] + move[1]

            if(self.map_data[new_x][new_y] == "$" or self.map_data[new_x][new_y] == "*"):
                new_box_x = new_x + move[0]
                new_box_y = new_y + move[1]
                if [new_box_x, new_box_y] in self.goals:
                    self.map_data[new_box_x][new_box_y] = "*"
                else:
                    self.map_data[new_box_x][new_box_y] = "$"

            self.clean_cell(self.player_position[0], self.player_position[1])
            self.player_position = [new_x, new_y]
            self.current_move_index += 1

    def clean_cell(self, row, col):
        if(self.map_data[row][col] != "."):
            self.map_data[row][col] = " "


if __name__ == "__main__":
    data_map = "./maps/Facil.txt"
    map_name = os.path.splitext(os.path.basename(data_map))[0]
    game = SokobanGame(data_map, [])
    valid_box_positions = load_all_playable_positions_for_boxes(game.goals, game.walls)
    moves = uninformed_search_algorithm(map_name,game.goals,game.walls, game.current_state, is_goal_array, get_children_array, None, "dfs")
    game.moves = moves
    #moves = get_greedy(data_map, "combined", game)
    #moves = get_astar(data_map, "manhattan_with_corral_deadlock_detection", valid_box_positions)
    #game.moves = moves['directions']
    arcade.run()


    
