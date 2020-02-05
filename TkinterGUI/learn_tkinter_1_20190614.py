#Learn_Tkinter_1_20190614

from tkinter import *
def handleEnterEvent(event):
    label1["text"] = "enter the frame!"
def handleLeaveEvent(event):
    label2["text"] = "leave the frame"
def handleLeftButtonPressEvent(event):
    label1["text"] = "you press the left button"
    label2["text"] = "({} : {})".format(event.x, event.y)

win = Tk()
frame = Frame(win, relief=RAISED, borderwidth=2, width=200, height=200)
frame.bind("<Enter>", handleEnterEvent)
frame.bind("<Leave>", handleLeaveEvent)
frame.bind("<Button-1>", handleLeftButtonPressEvent)

label1 = Label(frame, text="Nonthing")
label1.place(x=10, y=20)
label2 = Label(frame, text="x=")
label2.place(x=10, y=40)

frame.pack(side=TOP)
win.mainloop()
