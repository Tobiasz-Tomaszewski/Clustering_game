import tkinter as tk
import numpy as np

points = np.empty(shape=(1, 2))
print(points)

def on_click(event):
    # Get the coordinates of the click event
    x, y = event.x, event.y
    # Convert the coordinates to the coordinate system scale (e.g., 100 pixels = 1 unit)
    scaled_x = (x - origin_x) / scale
    scaled_y = -(y - origin_y) / scale
    global points
    points = np.vstack((points, np.array([scaled_x, scaled_y])))
    print(points)


# Create the main window
root = tk.Tk()
root.title("Clickable Coordinate System")

# Set the size of the window
window_width, window_height = 400, 400
root.geometry(f"{window_width}x{window_height}")

# Set up the coordinate system parameters
origin_x, origin_y = window_width // 2, window_height // 2  # Center of the window
scale = 20  # 1 unit = 20 pixels

# Create a canvas widget to draw on
canvas = tk.Canvas(root, width=window_width, height=window_height, bg="white")
canvas.pack()

# Draw x and y axes
canvas.create_line(0, origin_y, window_width, origin_y, fill="black")  # x-axis
canvas.create_line(origin_x, 0, origin_x, window_height, fill="black")  # y-axis

for i in range(-180, 200, 20):
    x = i + 200
    canvas.create_line(x, 198, x, 202, fill="black")  # Tick mark
    canvas.create_text(x, 210, text=str(i), fill="black")  # Label

# Draw tick marks and labels on Y-axis
for i in range(-180, 200, 20):
    y = 200 - i
    canvas.create_line(198, y, 202, y, fill="black")  # Tick mark
    canvas.create_text(210, y, text=str(i), fill="black")  # Label

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_click)

# Start the Tkinter main loop
root.mainloop()
