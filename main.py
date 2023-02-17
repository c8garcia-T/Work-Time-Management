# imports
import tkinter as tk
from tkinter import scrolledtext, messagebox, font, ttk
from ttkthemes import ThemedTk
from csv import writer
from datetime import datetime

# Likert Scales
satisfaction_scale = [
    "VERY SATISFIED",
    "SATISFIED",
    "NEITHER SATISFIED NOR DISSATISFIED",
    "DISSATISFIED",
    "VERY DISSATISFIED",
]
energy_scale = ["VERY LOW", "LOW", "MODERATE", "HIGH", "VERY HIGH"]
session_task_split = ["Single Task", "Multi-Task"]
task_completion = ["Main Task Completed", "Multi-Task Contribution"]

# text box input user prompt
text_field_prompt = """
Please provide a brief explanation for your answers \n including any thoughts or observations you would \n like to share.
"""

# Condense:
label_ScaleWidgets = [
    "Satisfaction",
    "Energy Levels",
    "Focus",
    "Session Type",
    "Task Completion",
]
likert_widgets = [
    satisfaction_scale,
    energy_scale,
    energy_scale,
    session_task_split,
    task_completion,
]
assert len(label_ScaleWidgets) == len(likert_widgets)

# Functions to ease production of widgets
def label_widget(label, window):
    """
    Create and return a Tkinter Label widget with the specified text and font.

    Args:
        label (str): The text to display on the label.
        window (tk.Tk or tk.Frame): The window or frame where the label widget will be placed.

    Returns:
        tk.Label: The created label widget.
    """
    label_widget = ttk.Label(
        window, text=label, font=font.Font(family="Garamond", size=20)
    )
    return label_widget


def option_menu_widget(likert_scale: list, window: tk.Tk):
    """Create a Tkinter OptionMenu widget with default value 'Unanswered' and given likert scale options.

    Args:
        likert_scale (list): A list of strings representing the likert scale options.
        window (tk.Tk): The parent window for the OptionMenu widget.

    Returns:
        tk.OptionMenu: The created OptionMenu widget with default value 'Unanswered' and given likert scale options.
    """
    default_value = tk.StringVar(value="Unanswered")
    # default_value.set("Unanswered")
    option_menu = tk.OptionMenu(window, default_value, *likert_scale)
    # option_menu.config(font=font.Font(size=16))
    return option_menu, default_value


def likert_measures(scales, labels_for_widget, window):
    """
    This function generates a series of Likert scale measurement widgets based on the provided
    scales and labels. The widgets are placed in two columns, with two widgets side by side and
    repeated down the screen.

    Args:
        scales (list): A list of lists, where each inner list represents the options for a Likert
            scale. The first item in each inner list should be the default option.
        labels_for_widget (list): A list of strings representing the labels to be displayed for
            each widget.
        window (Tk): The tkinter window in which the widgets will be displayed.

    Returns:
        int: The y-coordinate of the last widget placed, for use in placing additional widgets
        below this set.
    """
    # fixed initials
    left_col_x = 0
    right_col_x = 350
    # variable y
    upper_pos = 0
    bottom_pos = 30
    alternator_pos = 0
    option_menu_values = []

    for row_indx in range(len(scales)):
        if alternator_pos == 0:
            lbl = label_widget(labels_for_widget[row_indx], window=window)
            lbl.place(x=left_col_x, y=upper_pos, relx=0.01)
            optsmenu, default_value = option_menu_widget(
                scales[row_indx], window=window
            )
            optsmenu.place(x=left_col_x, y=bottom_pos, relx=0.01)
            alternator_pos = 1
            option_menu_values.append((labels_for_widget[row_indx], default_value))

        else:
            lbl = label_widget(labels_for_widget[row_indx], window=window)
            lbl.place(x=right_col_x, y=upper_pos, relx=0.01)
            optsmenu, default_value = option_menu_widget(
                scales[row_indx], window=window
            )
            optsmenu.place(x=right_col_x, y=bottom_pos, relx=0.01)
            alternator_pos = 0
            upper_pos = bottom_pos + 30
            bottom_pos = upper_pos + 30
            option_menu_values.append((labels_for_widget[row_indx], default_value))
    if alternator_pos == 0:
        return bottom_pos + 30, option_menu_values
    else:
        return bottom_pos + 30, option_menu_values


# Helper functions
def show_message():
    tk.messagebox.showinfo(
        icon="info", message="Submission Recorded \n Automatically Closing Window"
    )
    root.destroy()


def save_data(data, file_path):
    with open(file_path, "a") as file:
        writer_obj = writer(file)
        writer_obj.writerow(data)


def on_submit():
    likert_metric = []
    likert_responses = []
    text_response = text_input.get("1.0", "end-1c")
    text_len = len(text_response)
    for widget in option_menu_values:
        likert_metric.append(widget[0])
        likert_responses.append(widget[1].get())
    if "Unanswered" in likert_responses or text_len < 1:
        tk.messagebox.showwarning(title="WARNING", message="Submission incomplete")
    else:
        likert_responses.append(text_response)
        likert_responses.append(datetime.now())
        save_data(likert_responses, "data.csv")
        show_message()


def on_close():
    if messagebox.askokcancel(
        "Quit", "Do you want to quit? \n Response will be discarded"
    ):
        root.destroy()


# GUI setup
root = ThemedTk(theme="adapta")
# Customize the label widget style
style = ttk.Style()
style.configure("TLabel", background="#F0F0F8", foreground="#1F2C56")
root.configure(background="#F0F0F8")
# Get the width and height of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Calculate the x and y coordinates for the Tkinter window to appear at the center of the screen
x_pos = 1100  # (screen_width // 2) - (600 // 2) for centered
y_pos = (screen_height // 2) - (600 // 2)
# Set the position of the window to the calculated x and y coordinates
window_width = 500
root.geometry(f"{window_width}x700+{x_pos}+{y_pos}")
# Body
root.title("Work Time Management")
continue_pos, option_menu_values = likert_measures(
    likert_widgets, label_ScaleWidgets, root
)
label_widget(text_field_prompt, root).place(relx=0.035, y=continue_pos)
text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=65, height=25)
continue_pos += 100
text_input.place(y=continue_pos, relx=0.01)
submit_button = ttk.Button(root, text="Submit", command=on_submit)
continue_pos += 350
submit_button.place(relx=0.4, y=continue_pos)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
