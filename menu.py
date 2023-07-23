import tkinter as tk


def create_menu(root):
    menuBar = tk.Menu(root)
    submenu = tk.Menu(root)
    menuBar.add_cascade(label="Algorithm", menu=submenu)
    submenu.add_radiobutton(label="X-Means")
    submenu.add_radiobutton(label="DBSCAN")
    root.config(menu=menuBar)

