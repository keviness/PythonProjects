#try_creat_caculator2_20190621

from tkinter import *
win = Tk()
frame = Frame(win, relief=RAISED, borderwidth=2)

def cal():
    result = "="+str(eval(expression.get()))
    label1.config(text = result)
def clear():
    expression.set("")
    label1.config(text = "")
button0 = Button(frame, text="AC", command=clear)
label1 = Label(frame)
button2 = Button(frame, text="=", command=cal)
label2 = Label(frame, text="copyright by keviness",bg="SystemHighlight" )
button3 = Button(frame, text="Close", command=win.quit)
expression = StringVar()
entry = Entry(frame, textvariable=expression)
entry.pack()
entry.focus()
label1.pack(side=LEFT)
label2.pack(side=TOP)
frame.pack(side=TOP,  ipadx=40, ipady=50)
button0.pack(side=RIGHT)
button2.pack(side=RIGHT)
button3.pack(side=RIGHT)
frame.mainloop()
