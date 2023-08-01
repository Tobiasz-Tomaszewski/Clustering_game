import tkinter as tk
import numpy as np
import functions
import random
import settings
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.xmeans import xmeans
import tkinter.messagebox
from sklearn.cluster import DBSCAN
from pyclustering.cluster.gmeans import gmeans
from tkinter import IntVar


class ModelInterface:
    def perform_clustering(self, data):
        raise NotImplementedError()

    @property
    def parameters_info(self):
        raise NotImplementedError()

    @property
    def nr_of_clusters(self):
        raise NotImplementedError()

    @property
    def model_info(self):
        raise NotImplementedError()

    def change_parameters(self):
        raise NotImplementedError()


class GMeansModel(ModelInterface):
    def __init__(self):
        self.clusters = None
        self.initial_number_of_clusters = 1

    def perform_clustering(self, data):
        gmeans_instance = gmeans(data, k_init=self.initial_number_of_clusters).process()
        self.clusters = gmeans_instance.get_clusters()
        self.clusters = functions.organize_clusters(data, self.clusters)

    def change_parameters(self, **parameters):
        self.initial_number_of_clusters = parameters['initial_number_of_clusters']

    @property
    def nr_of_clusters(self):
        return len(self.clusters)

    @property
    def model_info(self):
        info = [
            {'name': 'G-Means',
             'parameters': ['initial_number_of_clusters'],
             'parameters conditions': [lambda x: x == int(x) and x > 0]}
        ]
        return info


class DbscanModel(ModelInterface):
    def __init__(self):
        self.clusters = None
        self.epsilon = 0.5
        self.min_samples = 5

    def perform_clustering(self, data):
        clustering = DBSCAN(eps=self.epsilon, min_samples=self.min_samples).fit(data)
        labels = clustering.labels_
        self.clusters = []
        for i in set(labels) - {-1}:
            self.clusters.append(data[labels == i])

    def change_parameters(self, **parameters):
        self.epsilon = parameters['epsilon']
        self.min_samples = parameters['min_samples']

    @property
    def nr_of_clusters(self):
        return len(self.clusters)

    @property
    def model_info(self):
        info = [
            {'name': 'DBSCAN',
             'parameters': ['epsilon', 'min_samples'],
             'parameters conditions': [lambda x: x > 0, lambda x: x == int(x) and x > 0]}
        ]
        return info


class XMeansModel(ModelInterface):
    def __init__(self):
        self.clusters = None
        self.initial_number_of_clusters = 1

    def perform_clustering(self, data):
        initial_centers = kmeans_plusplus_initializer(data, self.initial_number_of_clusters).initialize()
        xmeans_instance = xmeans(data, initial_centers, 40)
        xmeans_instance.process()
        self.clusters = xmeans_instance.get_clusters()
        self.clusters = functions.organize_clusters(data, self.clusters)

    def change_parameters(self, **parameters):
        self.initial_number_of_clusters = parameters['initial_number_of_clusters']

    @property
    def nr_of_clusters(self):
        return len(self.clusters)

    @property
    def model_info(self):
        info = [
            {'name': 'X-Means',
             'parameters': ['initial_number_of_clusters'],
             'parameters conditions': [lambda x: x == int(x) and x > 0]}
        ]
        return info


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


class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clustering Game")
        self.root.geometry(f"{settings.window_width}x{settings.window_height}")
        self.canvas = tk.Canvas(self.root, width=settings.window_width,
                                height=settings.window_height, bg="white")
        self.canvas.pack()
        self.rvar = IntVar(self.root)

    def get_canvas(self):
        return self.canvas

    def create_diplay_setings(self):
        pass

    def create_game_parameters_settings(self):
        pass

    def get_new_goal(self, new_goal, game, dialog):
        if new_goal.isdigit() and (int(new_goal) > 0) and (int(new_goal) < 21):
            game.change_goal(int(new_goal))
            dialog.withdraw()
        else:
            tk.messagebox.showerror("Error", "The goal should be a positive integer between 1 and 20.")

    def create_input_dialog_change_goal(self, game):
        if not hasattr(self, "_input_dialog"):
            self._input_dialog = tk.Toplevel(self.root)
            self._input_dialog.title(f"Change goal. Current goal: {game.goal_nr}")

            label = tk.Label(self._input_dialog, text=f"Enter the new goal:")
            label.pack()
            input_entry = tk.Entry(self._input_dialog)
            input_entry.pack()

            input_entry.insert(0, str(game.goal_nr))

            ok_button = tk.Button(self._input_dialog, text="OK",
                                  command=lambda: self.get_new_goal(input_entry.get(), game, self._input_dialog))
            ok_button.pack()

            self._input_dialog.protocol("WM_DELETE_WINDOW", lambda: self._input_dialog.withdraw())

        self._input_dialog.deiconify()

    def create_menu(self, game):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create algorithm menu
        algorithm_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Algorithm", menu=algorithm_menu)

        # Options in algorith menu
        self.rvar.set(0)
        algorithm_menu.add_radiobutton(label="X-Means", var=self.rvar, value=0, command=lambda: game.change_model(XMeansModel()))
        algorithm_menu.add_radiobutton(label="G-Means", var=self.rvar, value=1, command=lambda: game.change_model(GMeansModel()))
        algorithm_menu.add_radiobutton(label="DBSCAN", var=self.rvar, value=2, command=lambda: game.change_model(DbscanModel()))

        # Create game options
        game_options = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=game_options)

        # Options in option menu
        game_options.add_command(label="Reset Game", command=game.reset_game)
        game_options.add_command(label="Change goal", command=lambda: self.create_input_dialog_change_goal(game))

        return menu_bar


class Renderer:

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_coordinate_system(self):
        functions.draw_coordinate_system(self.canvas, settings.origin_x, settings.origin_y,
                                         settings.window_width, settings.window_height, settings.scale)

    def draw_point(self, x, y, color):
        functions.draw_point(self.canvas, x, y, color=color)

    def draw_clusters(self, clusters, colors):
        self.clear()
        self.draw_coordinate_system()
        color_index = -1
        for c in clusters:
            color_index += 1
            for point in c:
                scaled_point_x = point[0] * settings.scale + settings.origin_x
                scaled_point_y = -(point[1] * settings.scale) + settings.origin_y
                self.draw_point(scaled_point_x, scaled_point_y, color=colors[color_index])

    def clear(self):
        self.canvas.delete("all")


class Game:
    def __init__(self, renderer):
        self.points = np.empty(shape=(1, 2))
        self.renderer = renderer
        self.nr_of_turns = 0
        self.model = XMeansModel()
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
        if self.nr_of_turns > 19:
            self.end_game()

    def end_game(self):
        self.ended = True
        point_counter = PointCounter(self.model, self.goal_nr)
        # points attribute was initialized with 'np.empty' which returns array with one random element.
        self.score = point_counter.count_score(self.points[1:])
        self.renderer.draw_clusters(self.model.clusters, settings.supported_colors)
        if self.score:
            tkinter.messagebox.showinfo('Score', 'You have won')
        else:
            if self.goal_nr == 1:
                proper_form_goal = 'cluster'
            else:
                proper_form_goal = 'clusters'

            if self.model.nr_of_clusters == 1:
                proper_form_result = 'custer'
            else:
                proper_form_result = 'clusters'
            tkinter.messagebox.showinfo('Score', f'You have lost. The goal was {self.goal_nr} {proper_form_goal}. End result is {self.model.nr_of_clusters} {proper_form_result}.')

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
        self.model = model

    def change_goal(self, new_goal):
        self.goal_nr = new_goal


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
