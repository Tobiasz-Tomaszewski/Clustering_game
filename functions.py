import tkinter as tk
import numpy as np
import settings as s

def draw_coordinate_sys(canvas, origin_x, origin_y, window_width, window_height, scale):
    # Draw x and y axes
    canvas.create_line(0, origin_y, window_width, origin_y, fill="black")  # x-axis
    canvas.create_line(origin_x, 0, origin_x, window_height, fill="black")  # y-axis

    x_half = int(window_width / 2)
    y_half = int(window_height / 2)
    # Draw tick marks and labels on x-axis
    for i in range(-x_half + scale, x_half, scale):
        x = i + x_half
        canvas.create_line(x, y_half-2, x, y_half+2, fill="black")  # Tick mark
        if not x == origin_x:
            canvas.create_text(x, y_half+10, text=str(i//scale), fill="black")  # Label

    # Draw tick marks and labels on y-axis
    for i in range(-y_half + scale, y_half, scale):
        y = y_half - i
        canvas.create_line(x_half - 2, y, x_half+2, y, fill="black")  # Tick mark
        if not y == origin_y:
            canvas.create_text(y_half+10, y, text=str(i//scale), fill="black")  # Label


def reset_game():
    from main import canvas
    canvas.delete("all")
    global points
    points = np.empty(shape=(1, 2))
    draw_coordinate_sys(canvas, s.origin_x, s.origin_y, s.window_width, s.window_height, s.scale)
