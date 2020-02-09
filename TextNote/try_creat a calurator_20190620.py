#try_creat a calculator_20190620
from tkinter import*
win = Tk()
frame = Frame(win)
lst=["1", "2", "3"]
def print_number(lst):
    for w in range(len(lst)):
        expression.set(lst[w])
for i in range(len(lst)):
    button1= Button(frame, text=lst[i], command=print_number)
button1.pack(side=RIGHT)
expression = StringVar()
entry = Entry(frame, textvariable=expression)
entry.focus()
entry.pack()
frame.pack()
frame.mainloop()

        
    
