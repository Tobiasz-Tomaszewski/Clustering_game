import tkinter as tk


def p():
    print('does it print')


def create_menu(root):
    from main import reset_game
    # Create menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

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
    game_options.add_command(label="Reset Game", command=reset_game)

    return menu_bar



