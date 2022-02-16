from math import comb
from pickle import TRUE
import random
import arcade

# --- Constants ---
SPRITE_SCALING = 1
OASIS_COUNT = 3

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
DEFAULT_FONT_SIZE = 10
SCREEN_TITLE = "True Oasis"

TRUE_STATEMENTS = ['1a.png', '1b.png', '1c.png']
FALSE_STATEMENTS = ['0a.png', '0b.png', '0c.png', '0d.png', '0e.png', '0f.png', '0g.png', '0h.png', '0i.png']



class Button(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.button_image = arcade.load_texture("Button.png")

    def on_draw(self):
        



class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.cursor_list = arcade.SpriteList()
        self.oasis_list = arcade.SpriteList()

        # Set up the player info
        self.player_sprite = arcade.Sprite("Cursor.png", SPRITE_SCALING / 2)
        self.cursor_list.append(self.player_sprite)
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Background for the sky
        arcade.set_background_color(arcade.color.SKY_BLUE)


    def setup(self):
        """ Set up the game and initialize the variables. """
        # Score
        count = 0
        exception = False
        pass

    def on_draw(self):
        """ Draw everything """
        self.clear()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 / 3 + 50, 0, arcade.color.DESERT)
        self.cursor_list.draw()
        pass


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.player_sprite.center_x = x + 20
        self.player_sprite.center_y = y - 20
        pass


    def on_update(self, delta_time):
        """ Movement and game logic """
        pass
    

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass
        


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()