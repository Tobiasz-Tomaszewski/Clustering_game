import settings
import numpy as np
import random


def draw_coordinate_system(canvas, origin_x, origin_y, window_width, window_height, scale):
    # Draw x and y axes
    canvas.create_line(0, origin_y, window_width,
                       origin_y, fill="black")  # x-axis
    canvas.create_line(origin_x, 0, origin_x, window_height,
                       fill="black")  # y-axis

    x_half = int(window_width / 2)
    y_half = int(window_height / 2)
    # Draw tick marks and labels on x-axis
    for i in range(-x_half + scale, x_half, scale):
        x = i + x_half
        canvas.create_line(x, y_half-2, x, y_half+2, fill="black")  # Tick mark
        if not x == origin_x:
            canvas.create_text(
                x, y_half+10, text=str(i//scale), fill="black")  # Label

    # Draw tick marks and labels on y-axis
    for i in range(-y_half + scale, y_half, scale):
        y = y_half - i
        canvas.create_line(x_half - 2, y, x_half+2, y,
                           fill="black")  # Tick mark
        if not y == origin_y:
            canvas.create_text(
                y_half+10, y, text=str(i//scale), fill="black")  # Label


def draw_point(canvas, x, y, color):
    canvas.create_oval(x-2, y-2, x+2, y+2, width=0, fill=color)


def organize_clusters(sample, clusters):
    l_ = []
    for c in clusters:
        l_.append([])
        for i in c:
            l_[-1].append(sample[i])
    return l_
