import tkinter as tk
from tkinter import *
import os

# str = "interpolation.py"
# os.system(str)


def printInfo():
    # entry_output.delete(0, END)
    # R = int(entry_input.get())
    # S = 3.1415926 * R * R
    # entry_output.insert(10, S)
    # entry_input.delete(0, END)
    return []


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Client")

    # set position of the panel
    #width = 380
    #height = 300
    #screen_width = window.winfo_screenwidth()
    #screen_height = window.winfo_screenheight()
    #alignstr = '%dx%d+%d+%d' % (width, height, (screen_width-width), (screen_height-height))
    #window.geometry(alignstr)
    window.resizable(width=False, height=False)
    title = tk.Label(window, text='this is Tkinter', font=('Arial', 12), width=30, height=2)\
        .grid(row=0, column=1, padx=5, pady=5)
    label_input = tk.Label(window, text="input").grid(row=1, column=0)
    label_output = tk.Label(window, text="output").grid(row=2, column=0)
    entry_input = tk.Entry(window).grid(row=1, column=1)
    entry_output = tk.Entry(window).grid(row=2, column=1)
    submit_button = tk.Button(window, text="submit", relief="raised", command=printInfo(), state="normal")\
        .grid(row=3, column=0, sticky="W", padx=5, pady=5)
    quit_button = tk.Button(window, text="quit", relief="raised", state="normal").\
        grid(row=3, column=1, sticky="W", padx=5, pady=5)
    window.mainloop()
