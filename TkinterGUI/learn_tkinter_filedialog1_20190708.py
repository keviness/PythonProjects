from tkinter  import*
from tkinter import filedialog

win = Tk()
win.title(string = "Textbook")
text = Text(win, font = 30, undo = True)
def creatopenfile():
    filename = filedialog.askopenfilename()
    if filename != None:
        f = open(filename, "r")
        txt = f.read()
        f.close()
        text.insert("insert", txt)

Button(win, text="open", command=creatopenfile).pack(side=LEFT)

text.pack(side=RIGHT)


win.mainloop()
