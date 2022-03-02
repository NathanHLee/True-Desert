import arcade
import random

# ---- Globals ----
# Screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "True Oasis"




# ---- ----
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

        # Create player info
        self.cursor_sprite = None
        self.score = 0

        # Make the cursor invisible
        self.window.set_mouse_visible(False)

        # Create the background
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """ Set Up Value To Variables """
        # Sprite lists
        self.cursor_list = arcade.SpriteList()
        self.oasis_list = arcade.SpriteList()

        # Score
        count = 0

        # Set up the cursor
        self.cursor_sprite = Cursor("Cursor.png", .5)
        self.cursor_sprite.center_x = 1
        self.cursor_sprite.center_y = 1
        self.cursor_list.append(self.cursor_sprite)

    def on_draw(self):
        """ Render The Screen """
        self.clear()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 / 3 + 50, 0, arcade.color.DESERT)

        self.cursor_list.draw()

        # Put the score on the screen
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=14)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = TrueOasis()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()