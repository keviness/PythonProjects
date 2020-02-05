#learn_tkinter_Text1_20190708
from tkinter import*
win = Tk()
win.title("文本控件")
frame1=Frame(win, width=380, height=670)
text = Text(frame1, width=380, height=500)
file = open("笑傲江湖-网络版.txt", "r", encoding="utf-8")
txt = file.read()
text.insert(INSERT, txt)
text.insert(INSERT,"\n\n")
button = Button(win, text="Close", command=win.quit)
button.pack(side=BOTTOM)
text.pack(fill=BOTH)
frame1.pack(side=TOP, fill=BOTH, expand=1)
text.tag_config("button", justify="center")

win.mainloop()
