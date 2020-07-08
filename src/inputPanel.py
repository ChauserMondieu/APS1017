import tkinter as tk
import os

str = "interpolation.py"
os.system(str)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Client")

    # set position of the panel
    width = 380
    height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screen_width-width), (screen_height-height))
    window.geometry(alignstr)
    window.resizable(width=False,height=False)
    l = tk.Label(window, text='你好！this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
    l.pack()
    window.mainloop()
