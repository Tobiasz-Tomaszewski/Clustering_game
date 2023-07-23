import tkinter as tk
import numpy as np
import menu
import functions
import random
import settings as s

points = np.empty(shape=(1, 2))


class Game:
    def __init__(self, points, canvas):
        self.canvas = canvas
        self.points = points


def on_click(event):
    x, y = event.x, event.y
    scaled_x = (x - s.origin_x) / s.scale
    scaled_y = -(y - s.origin_y) / s.scale
    global points
    points = np.vstack((points, np.array([scaled_x, scaled_y])))
    random_x, random_y = random.randint(0, s.window_width), random.randint(0, s.window_height)
    g.canvas.create_oval(x, y, x, y, width=5, fill='black')
    g.canvas.create_oval(random_x, random_y, random_x, random_y, width=5, outline="red")
    scaled_random_x, scaled_random_y = (random_x - s.origin_x) / s.scale, -(random_y - s.origin_y) / s.scale
    points = np.vstack((points, np.array([scaled_random_x, scaled_random_y])))
    print(points)


def reset_game(g):
    g.canvas.delete("all")
    g.points = np.empty(shape=(1, 2))
    functions.draw_coordinate_system(g.canvas, s.origin_x, s.origin_y, s.window_width, s.window_height, s.scale)


# Create the main window
root = tk.Tk()
root.title("Clustering game")

# Set the size of the window
root.geometry(f"{s.window_width}x{s.window_height}")

# Create the Menu
menu.create_menu(root)

# Create a canvas widget to draw on
g = Game(points, tk.Canvas(root, width=s.window_width, height=s.window_height, bg="white"))
g.canvas.pack()
root.config(menu=functions.draw_coordinate_system(g.canvas, s.origin_x, s.origin_y, s.window_width, s.window_height, s.scale))


# Bind the click event to the canvas
g.canvas.bind("<Button-1>", on_click)

# Start the Tkinter main loop
root.mainloop()
