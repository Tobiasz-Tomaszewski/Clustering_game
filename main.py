import tkinter as tk
import numpy as np
import menu
import functions
import random
import settings


class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = np.empty(shape=(1, 2))
        self.canvas.pack()

    def start_game(self):
        functions.draw_coordinate_system(self.canvas, settings.origin_x, settings.origin_y,
                                         settings.window_width, settings.window_height, settings.scale)

    def player_turn(self, x, y):
        # check whether exists already or not.
        self.add_point(x, y)
        functions.draw_point(self.canvas, x, y, color="black")
        randomX, randomY = random.randint(
            0, settings.window_width), random.randint(0, settings.window_height)
        self.add_point(randomX, randomY)
        functions.draw_point(self.canvas, randomX, randomY, color="red")

    def add_point(self, x, y):
        scaled_x = (x - settings.origin_x) / settings.scale
        scaled_y = -(y - settings.origin_y) / settings.scale
        self.points = np.vstack((self.points, np.array([scaled_x, scaled_y])))

    def reset_game(self):
        self.canvas.delete("all")
        self.points = np.empty(shape=(1, 2))
        functions.draw_coordinate_system(self.canvas, settings.origin_x, settings.origin_y,
                                         settings.window_width, settings.window_height, settings.scale)


def on_click(event):
    x, y = event.x, event.y
    g.player_turn(x, y)


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Clustering game")

    # Set the size of the window
    root.geometry(f"{settings.window_width}x{settings.window_height}")

    # Create a canvas widget to draw on
    canvas = tk.Canvas(root, width=settings.window_width,
                       height=settings.window_height, bg="white")

    # Bind the click event to the canvas
    canvas.bind("<Button-1>", on_click)

    g = Game(canvas)

    # Create the Menu
    menu_bar = menu.create_menu(root, g)
    root.config(menu=menu_bar)

    g.start_game()

    # Start the Tkinter main loop
    root.mainloop()
