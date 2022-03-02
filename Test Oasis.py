import arcade
import random

# ---- Globals ----
# Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "True Oasis"

# Difficulty for different statements
DIFFICULTY_MODIFIER = 2

# True and false statements
TRUE_STATEMENTS = ["10 > 4", "3 < 8", "22 > 11"], ["7 + 2 > 5", "8 - 8 < 9 + 8", "1 + 2 < 4"], ["3 * 2 < 10", "4 / 2 < 2 * 2", "4 * 5 > 3 * 6"]
FALSE_STATEMENTS = ["14 < 7", "8 < 6", "1 > 19"], ["10 + 4 > 23", "3 + 3 < 5", "14 - 4 < 14 - 5"], ["2 * 3 < 2 + 3", "6 / 3 > 6 / 2", "2 * 8 > 3 * 6"]


# ---- ----
class InstructionsView(arcade.View):
    def on_show(self):
        """ Set Background Colour """
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("True Oasis", 
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150,
                        font_size=50, anchor_x="center")
        arcade.draw_text("Find the correct oasis to survive through the dry desert. The correct path is found by following the true equation", 
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                        font_size=30, anchor_x="center",
                        multiline=True, width=800)
        arcade.draw_text("Left click to play", 
                        SCREEN_WIDTH / 2, 150,
                        font_size=30, anchor_x="center")
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Left click to continue """
        game_view = TrueOasis()
        game_view.setup()
        self.window.show_view(game_view)



class Cursor(arcade.Sprite):
    def __init__(self, sprite, scale):
        """ Collect Character Information """
        super().__init__()
        self.sprite = sprite
        self.scale = scale

    def update(self):
        """ Move the cursor """
        self.center_x = self.change_x
        self.center_y = self.change_y



class TrueOasis(arcade.View):
    def __init__(self):
        """ Create empty variables """
        super().__init__()

        # Create the sprites
        self.cursor_list = None
        self.oasis_list = None
        self.button_list = None

        # Create the tuples
        self.true_false_tuple = []
        self.true_false_button = []

        # Create player info
        self.cursor_sprite = None
        self.score = 1000000

        # After the player presses a button, don't allow them to continue pressing them
        self.has_pressed = False
        self.is_paused = False

        # Make the cursor invisible
        self.window.set_mouse_visible(False)

        # Create the background
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set Up Value To Variables """
        # Sprite lists
        self.cursor_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.oasis_list = arcade.SpriteList()

        # Set up tuple lists to find information between button, oasis, and equation
        self.true_false_tuple = []
        self.true_false_button = []

        # Score
        count = 0
        # 'exception' lets the 3rd oasis always be true, allowing
        #     one to always be a correct path
        exception = False

        # Set up the cursor
        self.cursor_sprite = arcade.Sprite("Cursor.png", .5)
        self.cursor_list.append(self.cursor_sprite)
        
        # Create the oasis
        for i in range(3):
            true_false_marker = random.randrange(2)
            # Create a false oasis if random is 0, a past oasis has been created,
            #    or 2 false oasises were already created
            if (true_false_marker == 0 or exception == True) and count != 2:
                index = random.randrange(len(FALSE_STATEMENTS))
                statement = (FALSE_STATEMENTS[DIFFICULTY_MODIFIER][index], "FALSE")
                count += 1
            else:
                index = random.randrange(len(TRUE_STATEMENTS))
                statement = (TRUE_STATEMENTS[DIFFICULTY_MODIFIER][index], "TRUE")
                exception = True
            
            # Create the oasis instance
            oasis = arcade.Sprite("Oasis.png", .3)
            # Position the oasis
            oasis.center_x = SCREEN_WIDTH * i / 3 + 150
            if i == 1:
                oasis.center_y = SCREEN_HEIGHT / 2 + 110
            else:
                oasis.center_y = SCREEN_HEIGHT / 2 + 60
            
            # Create the button instance
            oasis_button = arcade.Sprite("Button.png", .1)
            oasis_button.center_x = SCREEN_WIDTH * i / 3 + 150
            oasis_button.center_y = SCREEN_HEIGHT / 6

            self.oasis_list.append(oasis)
            self.button_list.append(oasis_button)
            self.true_false_tuple.append(statement) # Get relation between equation and truthfulness
            button_statement = (oasis_button, self.true_false_tuple[i][1])
            self.true_false_button.append(button_statement) # Get relation betwene button and truthfulness

    def on_draw(self):
        """ Render The Screen """
        self.clear()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 / 3 + 50, 0, arcade.color.DESERT)
        self.oasis_list.draw()
        self.button_list.draw()
        self.cursor_list.draw()

        for i in range(3):
            arcade.draw_text(self.true_false_tuple[i][0], 
                            SCREEN_WIDTH * i / 3 + 150, SCREEN_HEIGHT / 6 + 100,
                            font_size=20, anchor_x="center")

        # Put the score on the screen
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=30)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.cursor_sprite.center_x = x
        self.cursor_sprite.center_y = y
    
    def on_mouse_press(self, x, y, button, modifiers):
        statement_hit_list = arcade.check_for_collision_with_list(self.cursor_sprite, self.button_list)
        for _ in statement_hit_list:
            if statement_hit_list == [self.true_false_button[0][0]] and self.has_pressed == False:
                if self.true_false_button[0][1] == 'TRUE':
                    self.score += 300
                else:
                    self.score -= 100
            elif statement_hit_list == [self.true_false_button[1][0]] and self.has_pressed == False:
                if self.true_false_button[1][1] == 'TRUE':
                    self.score += 300
                else:
                    self.score -= 100
            elif statement_hit_list == [self.true_false_button[2][0]] and self.has_pressed == False:
                if self.true_false_button[2][1] == 'TRUE':
                    self.score += 300
                else:
                    self.score -= 100
            
            # Stop error message from appearing when there is nothing to delete
            if self.has_pressed == False:
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

            # After the player has pressed a button, stop all button functions
            self.has_pressed = True
            self.is_paused = True

    def on_update(self, delta_time):
        if self.is_paused == False:
            self.score -= 100000 * (delta_time * 2)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = InstructionsView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()