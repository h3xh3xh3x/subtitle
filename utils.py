import os
import tkinter as tk
from tkinter import messagebox

def gui_prompt_overwrite(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    result = messagebox.askyesno("Overwrite?", message)
    root.destroy()
    return result

def check_file_exists(file_path):
    return os.path.isfile(file_path)
