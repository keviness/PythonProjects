#learn_tkinter_frame_20190709
from tkinter import*
win = Tk()
frame1 = Frame(win, relief = RAISED,width=200, height=300, borderwidth=2)
Button(frame1, text="button1").pack(side=LEFT, padx=10, pady=10)
Button(frame1, text="button2").pack(side=LEFT, padx=10, pady=10)
Button(frame1, text="button3").pack(side=LEFT,padx=10, pady=10)
frame1.pack(side=LEFT, fill=BOTH, expand=1,  ipadx=10, ipady=10)

frame2 = Frame(win, relief=RAISED, borderwidth=3)
frame2.pack(side=BOTTOM, fill=BOTH, expand=1)
for i in range(3):
    for x in range(3):
        Button(frame2, text=str(i)+","+str(x)).grid(row=i, column=x)
win.mainloop()
