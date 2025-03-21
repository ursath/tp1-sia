import os
import arcade

SCREEN_TITLE = "Sokoban Game"
PNG_SIZE = 64

ELEMENTS = {
    "#": "./textures/wall.png",   # Pared
    " ": "./textures/free.png",   # Espacio libre (null)
    ".": "./textures/goal.png",   # Objetivo
    "@": "./textures/player.png", # Jugador
    "$": "./textures/box.png",    # Caja
    "*": "./textures/box_goal.png" # Caja sobre objetivo
}

class SokobanGame(arcade.Window):
    def __init__(self, map_file):
        with open(map_file, "r") as f:
            self.map_data = [list(line.strip()) for line in f.readlines()]

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

    def on_draw(self):

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = col * PNG_SIZE + PNG_SIZE // 2
                y = (self.num_rows - row - 1) * PNG_SIZE + PNG_SIZE // 2  

                tile = self.map_data[row][col]
                if tile in self.textures and self.textures[tile]:
                    rect = arcade.Rect(x-PNG_SIZE//2, x+PNG_SIZE//2, y-PNG_SIZE//2, y+PNG_SIZE//2, PNG_SIZE, PNG_SIZE, x, y)

                    arcade.draw_texture_rect(self.textures[tile], rect)



if __name__ == "__main__":
    game = SokobanGame("./maps/1.txt")
    arcade.run()