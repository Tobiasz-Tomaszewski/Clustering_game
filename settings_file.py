window_width, window_height = 800, 800
# Set up the coordinate system parameters
origin_x, origin_y = window_width // 2, window_height // 2  # Center of the window
scale = 40  # 1 unit = scale pixels
supported_colors = [
    "red",
    "green",
    "blue",
    "cyan",
    "yellow",
    "magenta",
    "orange",
    "purple",
    "brown",
    "gray",
    "pink",
    "violet",
    "indigo",
    "turquoise",
    "gold",
    "salmon",
    "tomato",
    "sienna",
    "maroon",
    "navy",
    "skyblue",
    "steelblue",
    "lavender",
    "plum",
    "khaki",
    "orchid",
    "thistle",
    "darkgreen",
    "darkblue",
    "darkcyan",
    "darkred",
    "white",
    "black",
    "darkgray",
    "lightgray",
]

game_info = """Welcome to the clustering game. This game consists of 20 turns.
Each turn, the player places a point on the coordinate system, and the computer responds by placing one as well.
After 20 turns, the game ends, and one of the models performs clustering.

The goal of the game is to place the points on the coordinate system in such a way that the number of clusters found by
the algorithm is the same as the defined number. The player can change the goal number; the initial number is set to 2.

Additionally, the player can change the clustering algorithm. There are three models implemented:
-X-Means,
-G-Means,
-DBSCAN.

Furthermore, the player can modify the model parameters by pressing 'Options' -> 'Change Parameters'.
This action will create and open a temporary txt file. To update the settings,
the user must provide new valid parameters, save the file, and then close it.

WARNING: The file will keep reopening until the user provides valid parameters."""