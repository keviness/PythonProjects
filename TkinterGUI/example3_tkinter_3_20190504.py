#example3_tkiner_3_20190504
from tkinter import *
win = Tk()
Button(win, padx=20, text="hello!", command=quit).pack()
Button(win, padx="2c", text="Cancel", command=quit).pack()
Button(win, padx="8m", text="Close", command=quit).pack()
Label(win, height=10, text="GoodNight!", font=("Times", 9, "bold"), background="SystemHighlight").pack()
Button(win, cursor = "crosshair", font=("Times", 19, "bold"), text="Life is short, we learn Python", command=quit).pack()
win.mainloop()
