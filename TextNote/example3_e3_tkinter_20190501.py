#example3_e1_tkinter_20190501
import tkinter
win = tkinter.Tk()
win.title(string = "Pythonworld")
b = tkinter.Label(win, text = "hello python world!")
b.pack()
Button(win, text = "Close", command = win.quit).pack(side="button")
win.mainloop()
