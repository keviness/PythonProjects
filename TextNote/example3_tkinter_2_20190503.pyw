#example3_tkinter_2_20190503
from tkinter import *
win = Tk()
Button = (win, padx = 20, text = "close", command = quit).pack()
Label(win, background = bg, height = 10, width=10, text="Welcome to Python world!").pack()
win.mainloop()
