import tkinter as tk
import numpy as np
import menu
import coordinate_system
import random

points = np.empty(shape=(1, 2))

def on_click(event):
    x, y = event.x, event.y
    scaled_x = (x - origin_x) / scale
    scaled_y = -(y - origin_y) / scale
    global points
    points = np.vstack((points, np.array([scaled_x, scaled_y])))
    random_x, random_y = random.randint(0, window_width), random.randint(0, window_height)
    canvas.create_oval(x, y, x, y, width=5, fill='black')
    canvas.create_oval(random_x, random_y, random_x, random_y, width=5, outline="red")
    scaled_random_x, scaled_random_y = (random_x - origin_x) / scale, -(random_y - origin_y) / scale
    points = np.vstack((points, np.array([scaled_random_x, scaled_random_y])))
    print(points)

def right_click(event):
    canvas.delete("all")
    coordinate_system.draw_coordinate_sys(canvas, origin_x, origin_y, window_width, window_height, scale)

# Create the main window
root = tk.Tk()
root.title("Clustering game")

# Set the size of the window
window_width, window_height = 400, 400
root.geometry(f"{window_width}x{window_height}")

#Create the Menu
menu.create_menu(root)

# Set up the coordinate system parameters
origin_x, origin_y = window_width // 2, window_height // 2  # Center of the window
scale = 40  # 1 unit = scale pixels

# Create a canvas widget to draw on
canvas = tk.Canvas(root, width=window_width, height=window_height, bg="white")
canvas.pack()

coordinate_system.draw_coordinate_sys(canvas, origin_x, origin_y, window_width, window_height, scale)

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_click)
canvas.bind("<Button-3>", right_click)

# Start the Tkinter main loop
root.mainloop()
