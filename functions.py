from tkinter.commondialog import Dialog


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


def _show(title=None, message=None, _icon=None, _type=None, **options):
    if _icon and "icon" not in options:    options["icon"] = _icon
    if _type and "type" not in options:    options["type"] = _type
    if title:   options["title"] = title
    if message: options["message"] = message
    res = ModalMessage(**options).show()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        if res:
            return 'yes'
        return 'no'
    # In others we get a Tcl_Obj.
    return str(res)


class ModalMessage(Dialog):
    "A message box"

    command  = "tk_messageBox"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grab_set()


def showerror(title=None, message=None, **options):
    "Show an error message"
    return _show(title, message, 'error', 'ok', **options)