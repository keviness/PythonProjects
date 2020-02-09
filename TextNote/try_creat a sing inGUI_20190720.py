#try_creat a sing in GUI_20190720
from tkinter import *
from tkinter import filedialog
win = Tk()
expression1 = StringVar()
expression2 = StringVar()
frame = Frame(win, relief="raised", borderwidth=3, width=100, height=90)
frame.pack(side="top", fill="both", expand=1)
entry1 = Entry(frame, text="name",textvariable=expression1)
entry1.pack(side="top", fill="both")
entry2 = Entry(frame, text="password", textvariable=expression2)
entry2.pack(side="top", fill="both")

label2 = Label(frame)
label2.pack(side="bottom")
label = Label(win, width=80, height=280)
label.pack(side="bottom", fill="both")

def change_picture():
    image_name = filedialog.askopenfilename()
    images = PhotoImage(file=image_name)
    label(image=images)
def singup():
    global dic
    dic = {}
    dic[entry1.get()] = eval(entry2.get())
    label2.config(text="已注册")
    init()
def init():
    expression1.set("")
    expression2.set("")
def singin():
    global dic
    for keys in dic.keys():
        if keys== entry1.get() and dic[keys] == eval(entry2.get()):
            label2.config(text="successful!")
        else:
            label2.config(text="try again!~")
    
button1 = Button(frame, text="更换图片", command=change_picture)
button1.pack(side="bottom")
button2 = Button(frame, text="登录", command=singin)
button2.pack(side="bottom")
button3 = Button(frame, text="注册", command=singup)
button3.pack(side="bottom")
win.mainloop()

