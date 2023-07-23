import tkinter as tk
import numpy as np
import menu

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

# Draw x and y axes
canvas.create_line(0, origin_y, window_width, origin_y, fill="black")  # x-axis
canvas.create_line(origin_x, 0, origin_x, window_height, fill="black")  # y-axis

x_half = int(window_width / 2)
y_half = int(window_height / 2)
for i in range(-x_half + scale, x_half, scale):
    x = i + x_half
    canvas.create_line(x, y_half-2, x, y_half+2, fill="black")  # Tick mark
    if not x == origin_x:
        canvas.create_text(x, y_half+10, text=str(i//scale), fill="black")  # Label

# Draw tick marks and labels on Y-axis

for i in range(-y_half + scale, y_half, scale):
    y = y_half - i
    canvas.create_line(x_half - 2, y, x_half+2, y, fill="black")  # Tick mark
    if not y == origin_y:
        canvas.create_text(y_half+10, y, text=str(i//scale), fill="black")  # Label

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_click)

# Start the Tkinter main loop
root.mainloop()
