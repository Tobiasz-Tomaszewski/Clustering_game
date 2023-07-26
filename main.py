import tkinter as tk
import numpy as np
import functions
import random
import settings
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.xmeans import xmeans
import tkinter.messagebox


class ModelInterface:
    def perform_clustering(self, data):
        raise NotImplementedError()

    @property
    def nr_of_clusters(self):
        raise NotImplementedError()


class XMeansModel(ModelInterface):
    def __init__(self):
        self.clusters = None

    def perform_clustering(self, data):
        initial_number_of_clusters = 1
        initial_centers = kmeans_plusplus_initializer(data, initial_number_of_clusters).initialize()
        xmeans_instance = xmeans(data, initial_centers, 40)
        xmeans_instance.process()
        self.clusters = xmeans_instance.get_clusters()

    @property
    def nr_of_clusters(self):
        return len(self.clusters)


class PointCounter:
    def __init__(self, model, goal_nr):
        self.model = model
        self.goal_nr = goal_nr

    def count_score(self, data):
        """The game can only end with two results. We either win or loose and
        there is no natural way of counting the score of the player. This method check weather the number of clusters
        that model has calculated is the same as the goal. If the player wins the game this method will return True,
        and False if the player looses."""
        self.model.perform_clustering(data)
        nr_of_clusters = self.model.nr_of_clusters
        if nr_of_clusters == self.goal_nr:
            return True
        return False


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
        self.ended = False
        self.goal_nr = 2
        self.score = None

    def start_game(self):
        self.renderer.draw_coordinate_system()

    def player_turn(self, x, y):
        if self.ended:
            return

        self.add_point(x, y)
        self.renderer.draw_point(x, y, color="black")
        randomX, randomY = random.randint(
            0, settings.window_width), random.randint(0, settings.window_height)
        self.add_point(randomX, randomY)
        self.renderer.draw_point(randomX, randomY, color="red")

        self.nr_of_turns += 1
        if self.nr_of_turns > 20:
            self.end_game()

    def end_game(self):
        self.ended = True
        model = XMeansModel()
        point_counter = PointCounter(model, self.goal_nr)
        self.score = point_counter.count_score(self.points)
        if self.score:
            tkinter.messagebox.showinfo('Score', 'You have won')
        else:
            tkinter.messagebox.showinfo('Score', 'You have lost')

    def add_point(self, x, y):
        scaled_x = (x - settings.origin_x) / settings.scale
        scaled_y = -(y - settings.origin_y) / settings.scale
        self.points = np.vstack((self.points, np.array([scaled_x, scaled_y])))

    def reset_game(self):
        self.points = np.empty(shape=(1, 2))
        self.renderer.clear()
        self.renderer.draw_coordinate_system()
        self.ended = False
        self.score = None
        self.nr_of_turns = 0

    def change_model(self, model):
        self.clustering_algorithm = model


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
