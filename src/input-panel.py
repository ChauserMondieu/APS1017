import tkinter as tk

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Client")
    window.geometr("300*300")
    l = tk.Label(window, text='你好！this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
    l.pack()
    window.mainloop()
