#learn Tkinter_2_20190615
from tkinter import*
import tkinter.messagebox
def handelleftbuttonevent(event):
    label["text"] = "sum is:" + str(1+2)
def handleProtocol():
    if tkinter.messagebox.askokcancel("Tips","do you sure to close it?"):
        win.destroy()
win = Tk()
frame = Frame(win, relief=RAISED, borderwidth=2, width=200, height=200)
button1= Button(frame, text = "1")
button2 = Button(frame, text = "2")
button3 = Button(frame, text="sum")
label = Label(frame, text="")
label.place(x=16, y=49)
button3.bind("<Button-1>", handelleftbuttonevent)
button1.place(x=16, y=20); button2.place(x=46, y=20);button3.place(x=76, y=20)
frame.pack(side=TOP)
win.protocol("WM_DELETE_WINDOW", handleProtocol)
win.mainloop()
