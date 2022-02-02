from pickle import TRUE
import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_OASIS = .35
SPRITE_SCALING_STATEMENT = .4
OASIS_COUNT = 3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
DEFAULT_FONT_SIZE = 10
DEFAULT_LINE_HEIGHT = 50
SCREEN_TITLE = "Sprite Collect Coins Example"

TRUE_STATEMENTS = ['1a.png', '1b.png', '1c.png']
FALSE_STATEMENTS = ['0a.png', '0b.png', '0c.png', '0d.png', '0e.png', '0f.png', '0g.png', '0h.png', '0i.png']



# class Oasis(arcade.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.oasis_sprite = None
#         self.true_statement = None
#         self.false_statement = None
    

#     def construct_sprite(self):
#         self.oasis_sprite = arcade.Sprite("Oasis.png", SPRITE_SCALING_OASIS)
#         # start_x = 0
#         # start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
#         # arcade.draw_text("Text Drawing Examples",
#         #                  start_x,
#         #                  start_y,
#         #                  arcade.color.BLACK,
#         #                  DEFAULT_FONT_SIZE * 2,
#         #                  width=SCREEN_WIDTH,
#         #                  align="center")
    
#     def delete():
#         pass


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.cursor_list = None
        self.oasis_list = None
        self.true_false_statements = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.SKY_BLUE)


    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.cursor_list = arcade.SpriteList()
        self.oasis_list = arcade.SpriteList()
        self.true_false_statements = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the cursor
        self.player_sprite = arcade.Sprite("Cursor.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 1
        self.player_sprite.center_y = 1
        self.cursor_list.append(self.player_sprite)
        

        # Create the oasis
        for i in range(OASIS_COUNT):

            # Create the oasis instance
            oasis = arcade.Sprite("Oasis.png", SPRITE_SCALING_OASIS)

            # Position the oasis
            oasis.center_x = SCREEN_WIDTH * i / 3 + 150
            if i == 1:
                oasis.center_y = SCREEN_HEIGHT / 2 + 100
            else:
                oasis.center_y = SCREEN_HEIGHT / 2 + 50

            # Add the coin to the lists
            self.oasis_list.append(oasis)
            
        

    def on_draw(self):
        """ Draw everything """
        self.clear()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 / 3 + 50, 0, arcade.color.DESERT)
        self.oasis_list.draw()
        self.cursor_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=14)


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


    def on_update(self, delta_time):
        """ Movement and game logic """
        pass
    

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            oasis_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.oasis_list)
            for oasis in oasis_hit_list:
                oasis.remove_from_sprite_lists()
                self.score += 1


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()