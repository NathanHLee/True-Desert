from math import comb
from pickle import TRUE
import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_OASIS = .35
SPRITE_SCALING_STATEMENT = .4
OASIS_COUNT = 3

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
DEFAULT_FONT_SIZE = 10
DEFAULT_LINE_HEIGHT = 50
SCREEN_TITLE = "True Oasis"

TRUE_STATEMENTS = ['1a.png', '1b.png', '1c.png']
FALSE_STATEMENTS = ['0a.png', '0b.png', '0c.png', '0d.png', '0e.png', '0f.png', '0g.png', '0h.png', '0i.png']




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
        self.true_false_tuple = None

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
        self.true_false_tuple = []
        self.combine_statements = []

        # Score
        count = 0
        exception = False

        # Set up the cursor
        self.player_sprite = arcade.Sprite("Cursor.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 1
        self.player_sprite.center_y = 1
        self.cursor_list.append(self.player_sprite)
        
        # Create the oasis
        for i in range(OASIS_COUNT):

            rand_num_t_or_f = random.randrange(2)
            if (rand_num_t_or_f == 0 or exception == True) and count != 2:
                image_num = random.randrange(len(FALSE_STATEMENTS))
                img = (FALSE_STATEMENTS[image_num], "FALSE")
                count += 1
            else:
                image_num = random.randrange(len(TRUE_STATEMENTS))
                img = (TRUE_STATEMENTS[image_num], "TRUE")
                exception = True

            # Create the oasis instance
            oasis = arcade.Sprite("Oasis.png", SPRITE_SCALING_OASIS)
            true_or_false = arcade.Sprite(img[0], SPRITE_SCALING_STATEMENT)

            # Position the oasis
            oasis.center_x = SCREEN_WIDTH * i / 3 + 150
            true_or_false.center_x = SCREEN_WIDTH * i / 3 + 150
            if i == 1:
                oasis.center_y = SCREEN_HEIGHT / 2 + 100
                true_or_false.center_y = SCREEN_HEIGHT / 2 - 150
            else:
                oasis.center_y = SCREEN_HEIGHT / 2 + 50
                true_or_false.center_y = SCREEN_HEIGHT / 2 - 150

            # Add the coin to the lists
            self.oasis_list.append(oasis)
            self.true_false_statements.append(true_or_false)
            self.true_false_tuple.append(img)
            
        # for i in range(OASIS_COUNT):
            self.combine_statements.append((self.true_false_statements[i], self.true_false_tuple[i][1]))

        

    def on_draw(self):
        """ Draw everything """
        self.clear()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 / 3 + 50, 0, arcade.color.DESERT)
        self.true_false_statements.draw()
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
        # if button == arcade.MOUSE_BUTTON_LEFT:
        print(self.combine_statements[0]) # Image with truthfulness
        print(self.true_false_tuple[0]) # Button with truthfulness
        statement_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.true_false_statements)
        for _ in statement_hit_list:
            
            if statement_hit_list == [self.combine_statements[0][0]]:
                if self.combine_statements[0][1] == "TRUE":
                    self.score += 300
                    start_x = 0
                    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
                    arcade.draw_text("Text Drawing Examples",
                                    start_x,
                                    start_y,
                                    arcade.color.BLACK,
                                    DEFAULT_FONT_SIZE * 2,
                                    width=SCREEN_WIDTH,
                                    align="center")
                else:
                    self.score -= 100
            elif statement_hit_list == [self.combine_statements[1][0]]:
                if self.combine_statements[1][1] == "TRUE":
                    self.score += 300
                    start_x = 0
                    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
                    arcade.draw_text("Text Drawing Examples",
                                    start_x,
                                    start_y,
                                    arcade.color.BLACK,
                                    DEFAULT_FONT_SIZE * 2,
                                    width=SCREEN_WIDTH,
                                    align="center")
                else:
                    self.score -= 100
            elif statement_hit_list == [self.combine_statements[2][0]]:
                if self.combine_statements[2][1] == "TRUE":
                    self.score += 300
                    start_x = 0
                    start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
                    arcade.draw_text("Text Drawing Examples",
                                    start_x,
                                    start_y,
                                    arcade.color.BLACK,
                                    DEFAULT_FONT_SIZE * 2,
                                    width=SCREEN_WIDTH,
                                    align="center")
                else:
                    self.score -= 100

            # When you click on an equation, remove the two FALSE oasis sprites
            if self.true_false_tuple[0][1] == 'TRUE':
                self.oasis_list[2].remove_from_sprite_lists()
                self.oasis_list[1].remove_from_sprite_lists()
            elif self.true_false_tuple[1][1] == 'TRUE':
                self.oasis_list[2].remove_from_sprite_lists()
                self.oasis_list[0].remove_from_sprite_lists()
            elif self.true_false_tuple[2][1] == 'TRUE':
                self.oasis_list[1].remove_from_sprite_lists()
                self.oasis_list[0].remove_from_sprite_lists()
        


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()