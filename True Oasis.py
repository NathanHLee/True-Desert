import arcade
import arcade.gui
import random


# ---- Globals ----
# Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "True Oasis"

# Difficulty for different statements
DIFFICULTY_MODIFIER = 1
DIFFICULTY_MAX = 4

# True and false statements
TRUE_STATEMENTS = ([],  ["10 > 4", "3 < 8", "22 > 11"],                       # Level 1
                        ["7 + 2 > 5", "8 - 8 < 9 + 8", "1 + 2 < 4"],          # Level 2
                        ["3 * 2 < 10", "4 / 2 < 2 * 2", "4 * 5 > 3 * 6"],     # Level 3
                        ["2x + 3 = 9; x = 3", "5 + x = 7; x = 2", "x + x = 6; x = 3"])  # Level 4

FALSE_STATEMENTS = ([], ["14 < 7", "8 < 6", "1 > 19"],                        # Level 1
                        ["10 + 4 > 23", "3 + 3 < 5", "14 - 4 < 14 - 5"],      # Level 2
                        ["2 * 3 < 2 + 3", "6 / 3 > 6 / 2", "2 * 8 > 3 * 6"],  # Level 3
                        ["x + 4 = 3; x = 1", "4x + 3 = 12; x = 2", "2x + 8 = 10; x = 0"]) # Level 4

# Keep a global score
SCORE = 0
LIVES = 3

# ---- ----
class InstructionsView(arcade.View):
    def __init__(self):
        """ Create empty variables """
        super().__init__()

        # Create the sprites
        self.cursor_list = None
        self.cursor_sprite = None
        self.arrow_list = None
        
        # Make the cursor invisible
        self.window.set_mouse_visible(False)

    def on_show(self):
        """ Set Up The Game Presets """
        # Background colour
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Create the cursor
        self.cursor_list = arcade.SpriteList()
        self.cursor_sprite = arcade.Sprite("Cursor.png", .5)
        self.cursor_list.append(self.cursor_sprite)

        # Create the arrows to change difficulty
        self.arrow_list = arcade.SpriteList()
        
        # Create the button instance
        for i in range(2):
            arrow_button = arcade.Sprite("Arrow.png", .1)
            arrow_button.angle = i * 180
            arrow_button.center_x = SCREEN_WIDTH * 2 / 3 + 200
            arrow_button.center_y = SCREEN_HEIGHT / 3 - (1 + (i * 150))

            self.arrow_list.append(arrow_button)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("True Oasis", 
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150,
                        font_size=50, anchor_x="center", color=arcade.color.DESERT)
        arcade.draw_text("Find the correct oasis to make it through the dry desert. The correct path is found by following the true equation", 
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                        font_size=30, anchor_x="center",
                        multiline=True, width=800, color=arcade.color.DESERT)
        arcade.draw_text("Press 'SPACE' to play", 
                        SCREEN_WIDTH / 2, 150,
                        font_size=30, anchor_x="center", color=arcade.color.DESERT)
        arcade.draw_text("Select grade level", 
                        SCREEN_WIDTH * 2 / 3 + 200, 275,
                        font_size=20, anchor_x="center", color=arcade.color.FOREST_GREEN)

        # Put the difficulty level on the screen
        difficulty = f"{DIFFICULTY_MODIFIER}"
        arcade.draw_text(difficulty, 
                         start_x=SCREEN_WIDTH * 2 / 3 + 200, start_y=SCREEN_HEIGHT / 4 - 30,
                         color=arcade.color.WHITE, font_size=30, anchor_x="center")
        
        self.arrow_list.draw()
        self.cursor_list.draw()
        
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.cursor_sprite.center_x = x
        self.cursor_sprite.center_y = y

    def on_key_press(self, key, modifiers):
        """ Press Space To Continue """
        game_view = TrueOasis()
        game_view.setup()
        self.window.show_view(game_view)
    
    def on_mouse_press(self, x, y, button, modifiers):
        global DIFFICULTY_MODIFIER
        statement_hit_list = arcade.check_for_collision_with_list(self.cursor_sprite, self.arrow_list)
        for _ in statement_hit_list:
            if statement_hit_list[0] == self.arrow_list[0] and DIFFICULTY_MODIFIER < DIFFICULTY_MAX:
                DIFFICULTY_MODIFIER += 1
                return
            elif statement_hit_list[0] == self.arrow_list[1] and DIFFICULTY_MODIFIER != 1:
                DIFFICULTY_MODIFIER -= 1
                return



class EndScreen(arcade.View):
    def __init__(self):
        """ Create empty variables """
        super().__init__()

        # Create the sprites
        self.cursor_list = None
        self.cursor_sprite = None
    
    def on_show(self):
        # Create the cursor
        self.cursor_list = arcade.SpriteList()
        self.cursor_sprite = arcade.Sprite("Cursor.png", .5)
        self.cursor_list.append(self.cursor_sprite)
    
    def on_draw(self):
        self.clear()
        if SCORE > 0:
            arcade.draw_text(f"Congragulations! You made {SCORE} points!", 
                            start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2,
                            color=arcade.color.WHITE, font_size=40, anchor_x="center")
        else:
            arcade.draw_text(f"Unfortunately, You lost {SCORE * -1} points!", 
                            start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2,
                            color=arcade.color.WHITE, font_size=40, anchor_x="center")
        self.cursor_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Reset the globals
        global SCORE
        global LIVES
        SCORE = 0
        LIVES = 3
        game_view = InstructionsView()
        self.window.show_view(game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # Move the center of the player sprite to match the mouse x, y
        self.cursor_sprite.center_x = x
        self.cursor_sprite.center_y = y


class TrueOasis(arcade.View):
    def __init__(self):
        """ Create empty variables """
        super().__init__()

        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(width=200)
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.add(start_button.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        start_button.on_click = self.on_click_start

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        # Create the sprites
        self.cursor_list = None
        self.oasis_list = None
        self.button_list = None

        # Create the tuples
        self.true_false_tuple = []
        self.true_false_button = []

        # Create player info
        self.cursor_sprite = None
        self.score = SCORE

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
                index = random.randrange(len(FALSE_STATEMENTS[DIFFICULTY_MODIFIER]))
                statement = (FALSE_STATEMENTS[DIFFICULTY_MODIFIER][index], "FALSE")
                count += 1
            else:
                index = random.randrange(len(TRUE_STATEMENTS[DIFFICULTY_MODIFIER]))
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
        
        # Put the lives on the screen
        output = f"Lives: {LIVES}"
        arcade.draw_text(text=output, start_x=10, start_y=SCREEN_HEIGHT - 40,
                         color=arcade.color.WHITE, font_size=30)
        
        if self.has_pressed == True:
            if LIVES != 0:
                self.manager.draw()
                arcade.draw_text("Continue!", 
                                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                font_size=20, anchor_x="center")
                self.cursor_list.draw()
            else:
                self.manager.draw()
                arcade.draw_text("Return!", 
                                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                font_size=20, anchor_x="center")
                self.cursor_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Movement """
        # Move the center of the player sprite to match the mouse x, y
        self.cursor_sprite.center_x = x
        self.cursor_sprite.center_y = y
    
    def on_mouse_press(self, x, y, button, modifiers):
        global LIVES
        statement_hit_list = arcade.check_for_collision_with_list(self.cursor_sprite, self.button_list)
        for _ in statement_hit_list:
            if statement_hit_list == [self.true_false_button[0][0]] and self.has_pressed == False:
                if self.true_false_button[0][1] == 'TRUE':
                    self.score += 300 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                else:
                    self.score -= 100 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                    LIVES -= 1
            elif statement_hit_list == [self.true_false_button[1][0]] and self.has_pressed == False:
                if self.true_false_button[1][1] == 'TRUE':
                    self.score += 300 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                else:
                    self.score -= 100 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                    LIVES -= 1
            elif statement_hit_list == [self.true_false_button[2][0]] and self.has_pressed == False:
                if self.true_false_button[2][1] == 'TRUE':
                    self.score += 300 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                else:
                    self.score -= 100 * (1 + (DIFFICULTY_MODIFIER * DIFFICULTY_MODIFIER))
                    LIVES -= 1
            
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

    def on_click_start(self, event):
        global SCORE
        if LIVES != 0:
            SCORE = self.score
            game_view = TrueOasis()
            game_view.setup()
            self.window.show_view(game_view)
        else:
            SCORE = self.score
            game_view = EndScreen()
            self.window.show_view(game_view)



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = InstructionsView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()