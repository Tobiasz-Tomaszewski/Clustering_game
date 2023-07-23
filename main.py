import tkinter as tk
import numpy as np
import menu
import coordinate_system

points = np.empty(shape=(1, 2))
print(points)


def on_click(event):
    x, y = event.x, event.y
    scaled_x = (x - origin_x) / scale
    scaled_y = -(y - origin_y) / scale
    global points
    points = np.vstack((points, np.array([scaled_x, scaled_y])))
    canvas.create_oval(x, y, x, y, width=3, fill='black')


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

# Start the Tkinter main loop
root.mainloop()
