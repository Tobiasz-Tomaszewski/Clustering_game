import tkinter as tk
import numpy as np
import functions
import random
import settings_file
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.xmeans import xmeans
import tkinter.messagebox
from sklearn.cluster import DBSCAN
from pyclustering.cluster.gmeans import gmeans
from tkinter import IntVar
from marshmallow import validates_schema
from dataclasses import dataclass, field
import marshmallow_dataclass
import json
import warnings
np.warnings = warnings


class ModelInterface:
    def perform_clustering(self, data):
        raise NotImplementedError()

    @property
    def parameters_info(self):
        raise NotImplementedError()

    @property
    def nr_of_clusters(self):
        raise NotImplementedError()

    def change_parameters(self):
        raise NotImplementedError()

    def get_parameters(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()


class GMeansModel(ModelInterface):
    def __init__(self, GMeansSettings):
        self.clusters = None
        self.initial_number_of_clusters = GMeansSettings.initial_number_of_clusters

    def perform_clustering(self, data):
        gmeans_instance = gmeans(data, k_init=self.initial_number_of_clusters).process()
        self.clusters = gmeans_instance.get_clusters()
        self.clusters = functions.organize_clusters(data, self.clusters)

    @property
    def nr_of_clusters(self):
        return len(self.clusters)

    def change_parameters(self, GMeansSettings):
        self.initial_number_of_clusters = GMeansSettings.initial_number_of_clusters

    def get_parameters(self):
        return GMeansSettings(self.initial_number_of_clusters)

    @property
    def name(self):
        return 'gmeans'


@dataclass
class GMeansSettings:
    """Settings for the GMeans clustering model."""
    initial_number_of_clusters: int = field(metadata=dict(
        description="Initial number of clusters"))

    @validates_schema
    def validate(self, data, **_):
        if not (data['initial_number_of_clusters'] > 0) and (data['initial_number_of_clusters'] < 21):
            raise AssertionError('initial_number_of_clusters must be an integer, greater than 0 and lesser than 21.')


GMeansSettingsSchema = marshmallow_dataclass.class_schema(GMeansSettings)()


class DbscanModel(ModelInterface):
    def __init__(self, DbscanSettings):
        self.clusters = None
        self.epsilon = DbscanSettings.epsilon
        self.min_samples = DbscanSettings.min_samples

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

    def change_parameters(self, DbscanSettings):
        self.epsilon = DbscanSettings.epsilon
        self.min_samples = DbscanSettings.min_samples

    def get_parameters(self):
        return DbscanSettings(self.epsilon, self.min_samples)

    @property
    def name(self):
        return 'DBSCAN'


@dataclass
class DbscanSettings:
    """Settings for the Dbscan clustering model."""
    epsilon: float = field(metadata=dict(
        description="Epsilon"))
    min_samples: int = field(metadata=dict(
        description="The minimum number of points to be considered a cluster"))

    @validates_schema
    def validate(self, data, **_):
        if not (data['epsilon'] > 0):
            raise AssertionError('epsilon must be a number, greater than 0')
        if not ((data['min_samples'] > 0) and (type(data['min_samples']) == int)):
            raise AssertionError('min_samples must be an integer, greater than 0')


DbscanSettingsSchema = marshmallow_dataclass.class_schema(DbscanSettings)()


class XMeansModel(ModelInterface):
    def __init__(self, XMeansSettings):
        self.clusters = None
        self.initial_number_of_clusters = XMeansSettings.initial_number_of_clusters

    def perform_clustering(self, data):
        init = self.initial_number_of_clusters
        initial_centers = kmeans_plusplus_initializer(data, init).initialize()
        xmeans_instance = xmeans(data, initial_centers, 40)
        xmeans_instance.process()
        self.clusters = xmeans_instance.get_clusters()
        self.clusters = functions.organize_clusters(data, self.clusters)

    def update_parameters(self, XMeansSettings):
        self.initial_number_of_clusters = XMeansSettings.initial_number_of_clusters

    @property
    def nr_of_clusters(self):
        return len(self.clusters)

    def change_parameters(self, XMeansSettings):
        self.initial_number_of_clusters = XMeansSettings.initial_number_of_clusters

    def get_parameters(self):
        return XMeansSettings(self.initial_number_of_clusters)

    @property
    def name(self):
        return 'xmeans'


@dataclass
class XMeansSettings:
    """Settings for the XMeans clustering model."""
    initial_number_of_clusters: int = field(metadata=dict(
        description="Initial number of clusters"))

    @validates_schema
    def validate(self, data, **_):
        if not (data['initial_number_of_clusters'] > 0) and (data['initial_number_of_clusters'] < 21):
            raise AssertionError('initial_number_of_clusters must be an integer, greater than 0 and lesser than 21.')


XMeansSettingsSchema = marshmallow_dataclass.class_schema(XMeansSettings)()


class ModelSettingsHandler:
    def __init__(self, game):
        self.model = game.model
        self.settings = self.model.get_parameters()
        self.SettingsSchema = None

    def change_settings(self, game):
        global stop_player_turn
        stop_player_turn = True
        if game.model.name == 'xmeans':
            self.SettingsSchema = XMeansSettingsSchema
        if game.model.name == 'gmeans':
            self.SettingsSchema = GMeansSettingsSchema
        if game.model.name == 'DBSCAN':
            self.SettingsSchema = DbscanSettingsSchema
        import tempfile
        tmpFilePath = None
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmpFilePath = tmp.name
            serialized = self.SettingsSchema.dumps(game.get_settings, indent=2)
            tmp.write(serialized.encode('utf-8'))

        import os
        global settings_loaded_succesfully
        settings_loaded_succesfully = False

        def load_settings():
            global settings_loaded_succesfully
            while not settings_loaded_succesfully:
                global settings
                try:
                    os.system(f"notepad {tmpFilePath}")

                    with open(tmpFilePath) as tmp:
                        jsonObj = json.load(tmp)
                        settings = self.SettingsSchema.load(jsonObj)
                        settings_loaded_succesfully = True
                except Exception as ex:
                    print(ex)
                    load_settings()

        load_settings()

        os.remove(tmpFilePath)
        game.change_settings(settings)


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
        self.root.geometry(f"{settings_file.window_width}x{settings_file.window_height}")
        self.canvas = tk.Canvas(self.root, width=settings_file.window_width,
                                height=settings_file.window_height, bg="white")
        self.canvas.pack()
        self.rvar = IntVar(self.root)

    def get_canvas(self):
        return self.canvas

    @staticmethod
    def get_new_goal(new_goal, game, dialog):
        if new_goal.isdigit() and (int(new_goal) > 0) and (int(new_goal) < 21):
            game.change_goal(int(new_goal))
            dialog.withdraw()
        else:
            functions.show_modal_error("Error", "The goal should be a positive integer between 1 and 20.")

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

    def display_game_info(self, ingo_text):
        pass


    def create_menu(self, game, settings_handler):
        # Create menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create algorithm menu
        algorithm_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Algorithm", menu=algorithm_menu)

        # Options in algorith menu
        self.rvar.set(0)
        algorithm_menu.add_radiobutton(label="X-Means", var=self.rvar, value=0, command=lambda: game.change_model(
            XMeansModel(XMeansSettings(1))))
        algorithm_menu.add_radiobutton(label="G-Means", var=self.rvar, value=1, command=lambda: game.change_model(
            GMeansModel(GMeansSettings(1))))
        algorithm_menu.add_radiobutton(label="DBSCAN", var=self.rvar, value=2, command=lambda: game.change_model(
            DbscanModel(DbscanSettings(0.5, 5))))

        # Create game options
        game_options = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=game_options)

        # Options in option menu
        game_options.add_command(label="Reset Game", command=game.reset_game)
        game_options.add_command(label="Change goal", command=lambda: self.create_input_dialog_change_goal(game))

        # Create parameters menu
        game_options.add_command(label="Change parameters", command=lambda: settings_handler.change_settings(game))

        # Create info button
        menu_bar.add_command(label="Game info")

        return menu_bar


class Renderer:

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_coordinate_system(self):
        functions.draw_coordinate_system(self.canvas, settings_file.origin_x, settings_file.origin_y,
                                         settings_file.window_width, settings_file.window_height, settings_file.scale)

    def draw_point(self, x, y, color):
        functions.draw_point(self.canvas, x, y, color=color)

    def draw_clusters(self, clusters, colors):
        self.clear()
        self.draw_coordinate_system()
        color_index = -1
        for c in clusters:
            color_index += 1
            for point in c:
                scaled_point_x = point[0] * settings_file.scale + settings_file.origin_x
                scaled_point_y = -(point[1] * settings_file.scale) + settings_file.origin_y
                self.draw_point(scaled_point_x, scaled_point_y, color=colors[color_index])

    def clear(self):
        self.canvas.delete("all")


class Game:
    def __init__(self, renderer):
        self.points = np.empty(shape=(1, 2))
        self.renderer = renderer
        self.nr_of_turns = 0
        self.model = XMeansModel(XMeansSettings(1))
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
            0, settings_file.window_width), random.randint(0, settings_file.window_height)
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
        self.renderer.draw_clusters(self.model.clusters, settings_file.supported_colors)
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
        scaled_x = (x - settings_file.origin_x) / settings_file.scale
        scaled_y = -(y - settings_file.origin_y) / settings_file.scale
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

    def change_settings(self, settings):
        self.model.change_parameters(settings)

    @property
    def get_settings(self):
        return self.model.get_parameters()


def main():
    global stop_player_turn
    stop_player_turn = False
    window = GameWindow()

    canvas = window.get_canvas()

    renderer = Renderer(canvas)
    game = Game(renderer)
    setting_handler = ModelSettingsHandler(game)
    # Bind the click event to the canvas
    def on_click(event):
        x, y = event.x, event.y
        if not stop_player_turn:
            game.player_turn(x, y)

    canvas.bind("<Button-1>", on_click)

    window.create_menu(game, setting_handler)

    game.start_game()

    # Start the Tkinter main loop
    window.root.mainloop()


if __name__ == "__main__":
    main()
