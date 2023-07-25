import tkinter as tk
import numpy as np
import functions
import random
import settings
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


class ModelXMeans:
    def __init__(self, data, nr_cluster_init, renderer):
        self.data = data
        self.initial_number_of_clusters = nr_cluster_init
        self.initial_centers = None
        self.renderer = renderer
        self.clusters = None

    def initialize_centers(self):
        self.initial_centers = kmeans_plusplus_initializer(self.data, self.initial_number_of_clusters).initialize()

    def perform_algorithm(self):
        pass

    def get_clusters(self):
        pass
        l = []
        for c in self.clusters:
            l.append([])
            for i in c:
                l[-1].append(self.data[i])
        return l

    def draw_clusters(self):
        pass


class ModelDBSCAN:
    def __init__(self, data, epsilon):
        self.data = data
        self.epsilon = epsilon

    def get_clusters(self):
        pass


class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clustering Game")
        self.root.geometry(f"{settings.window_width}x{settings.window_height}")
        self.canvas = tk.Canvas(self.root, width=settings.window_width,
                                height=settings.window_height, bg="white")
        self.canvas.pack()

    def get_canvas(self):
        return self.canvas

    def create_menu(self, game):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create algorithm menu
        algorithm_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Algorithm", menu=algorithm_menu)

        # Options in algorith menu
        algorithm_menu.add_radiobutton(label="X-Means")
        algorithm_menu.add_radiobutton(label="DBSCAN")

        # Create game options
        game_options = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=game_options)

        # Options in option menu
        game_options.add_command(label="Reset Game", command=game.reset_game)

        return menu_bar


class Renderer:

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_coordinate_system(self):
        functions.draw_coordinate_system(self.canvas, settings.origin_x, settings.origin_y,
                                         settings.window_width, settings.window_height, settings.scale)

    def draw_point(self, x, y, color):
        functions.draw_point(self.canvas, x, y, color=color)

    def clear(self):
        self.canvas.delete("all")


class Game:
    def __init__(self, renderer):
        self.points = np.empty(shape=(1, 2))
        self.renderer = renderer
        self.nr_of_turns = 0
        self.clustering_algorithm = "xmeans"
        self.end_game = False

    def start_game(self):
        self.renderer.draw_coordinate_system()

    def player_turn(self, x, y):
        self.add_point(x, y)
        self.renderer.draw_point(x, y, color="black")
        randomX, randomY = random.randint(
            0, settings.window_width), random.randint(0, settings.window_height)
        self.add_point(randomX, randomY)
        self.renderer.draw_point(randomX, randomY, color="red")
        self.nr_of_turns += 1

    def add_point(self, x, y):
        scaled_x = (x - settings.origin_x) / settings.scale
        scaled_y = -(y - settings.origin_y) / settings.scale
        self.points = np.vstack((self.points, np.array([scaled_x, scaled_y])))

    def reset_game(self):
        self.points = np.empty(shape=(1, 2))
        self.renderer.clear()
        self.renderer.draw_coordinate_system()

    def change_model(self, model):
        self.clustering_algorithm = model

    def update_state(self):
        if self.nr_of_turns == 20:
            self.end_game = True
        return self.end_game


def main():
    window = GameWindow()

    canvas = window.get_canvas()

    renderer = Renderer(canvas)
    game = Game(renderer)

    # Bind the click event to the canvas
    def on_click(event):
        x, y = event.x, event.y
        game.player_turn(x, y)

    canvas.bind("<Button-1>", on_click)

    window.create_menu(game)

    game.start_game()

    # Start the Tkinter main loop
    window.root.mainloop()


if __name__ == "__main__":
    main()
