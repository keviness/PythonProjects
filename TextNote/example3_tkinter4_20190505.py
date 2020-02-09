#example3_tkinter4_20190505
from tkinter import*
win = Tk()
frame1 = Frame(win, relief=RAISED, borderwidth=2)
frame1.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10, expand=0)
Button(frame1, text="button1").pack(side=LEFT, padx=10, pady=10)
Button(frame1, text="button2").pack(side=LEFT, padx=10, pady=20)
Button(frame1, text="button3").pack(side=LEFT, padx=10, pady=20)
Button(frame1, text="hello",command=quit).pack(side=RIGHT)
win.mainloop()
