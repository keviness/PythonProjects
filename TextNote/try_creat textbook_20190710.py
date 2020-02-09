#try_great a text book_20190710

from tkinter import*
from tkinter import filedialog, messagebox
from wordcloud import WordCloud
import jieba
from PIL import Image, ImageTk

win = Tk()
win.title("Textbook DIY")
frame_left = Frame(win, relief ="raised",borderwidth=2, bg="white", width=600, height=900)
frame_left.pack(side="left", fill="both",  expand=1)
frame_right= Frame(win, relief="raised", borderwidth=2, bg="blue", width=300, height=300)
frame_right.pack(side="right",fill="both", expand=1 )

scrollbar1 = Scrollbar(frame_left, orient="horizontal")
scrollbar1.pack(side="bottom", fill="x")
scrollbar2 = Scrollbar(frame_left)
scrollbar2.pack(side="right", fill="y")

textbook = Text(frame_left, width=80, undo=True, xscrollcommand=scrollbar1.set(0, 0.3), yscrollbar=scrollbar2.set(0, 0.3))
textbook.pack(side="left", fill="both")

scrollbar1.config(command=textbook.xview)
scrollbar2.config(command=textbook.yview)

listbox = Listbox(frame_right, width=50, height=40)
listbox.pack(side="bottom",  fill="both")


def openfile():
    textbook.delete(1.0, "end")
    global txt
    filename = filedialog.askopenfilename()
    if filename != None:
        f = open(filename, "r")
        txt = f.read()
        f.close()
        textbook.insert("insert", txt)
    else:
        messagebox.showinfo("提示", "文件名错误")
def saveasfile():
    save()
    filename_save = filedialog.asksaveasfilename()
    if filename_save != None:
        with open(filename_save, "w") as f_save:
            f_save.write(textbook.get(1.0, "end"))
        f_save.close()
    else:
        messagebox.showinfo("提示", "文件名错误")

def window_quit():
    global txt
    if textbook.get(1.0, "end") != txt:
        handleprotocol()
    else:
        win.destroy()
def handleprotocol():
    if messagebox.askokcancel("提示", "需要保存修改吗？") == True:
        save()
        win.destroy()
    else:
        win.destroy()
def wordsnumber():
    dct = {}
    txt_count = textbook.get(1.0, "end")
    word_count = jieba.lcut(txt_count)
    for word in word_count:
        if len(word) == 1:
            continue
        dct[word] = dct.get(word, 0) + 1
    items = list(dct.items())
    items.sort(key=lambda x:x[1], reverse=True)
    for w in range(15):
        listbox.insert("end", "{0:<6}:{1:>6}".format(items[w][0], items[w][1]))
        
def generate_wordcloud():
    txt_cloud = textbook.get(1.0, "end")
    words = jieba.lcut(txt_cloud)
    newtext = "".join(words)
    wordcloud = WordCloud(background_color="red",max_font_size=20, font_path="msyh.ttc").generate(newtext)
    wordcloud.to_file("词云.png")
    
def showpopmenu(event):
    popmenu.post(event.x_root, event.y_root)
    
def showpicture():
    global imge
    imgfilename = filedialog.askopenfilename()
    print(imgfilename)
    img = Image.open(imgfilename)
    imge = ImageTk.PhotoImage(img)
    textbook.image_create("insert", image=imge)

def cut():
    global content
    content = textbook.get(SEL_FIRST, SEL_LAST)
    if content == None:
        return
    else:
        textbook.delete(SEL_FIRST, SEL_LAST)
        return content
def copy():
    global content
    content = textbook.get(SEL_FIRST, SEL_LAST)
    return content
def paste():
    global content
    textbook.insert("insert", content)
def save():
    textbook.tag_add(textbook.get(1.0, "end"), 1.0, "end")

def redo():
    textbook.edit_redo()
def undo():
    textbook.edit_undo()
def select_all():
    textbook.tag_add("sel", 1.0, "end")

def about():
    if messagebox.showinfo("about", "copyright by keviness") == True:
        pass
    

topmenu = Menu(win)
filemenu = Menu(topmenu, tearoff=False)
filemenu.add_command(label="打开", command=openfile)
filemenu.add_command(label="另存为", command=saveasfile)
filemenu.add_separator()
filemenu.add_command(label="生成词云", command=generate_wordcloud)
filemenu.add_command(label="展示图片", command=showpicture)
filemenu.add_command(label="统计词频", command=wordsnumber)
topmenu.add_cascade(label="文件",menu=filemenu)

editmenu = Menu(topmenu, tearoff=False)
editmenu.add_command(label="剪切", command=cut)
editmenu.add_command(label="复制",  command = copy)
editmenu.add_command(label="粘贴", command = paste)
editmenu.add_command(label="保存", command=save)
topmenu.add_cascade(label="编辑", menu=editmenu)

functionmenu = Menu(topmenu, tearoff=False)
functionmenu.add_command(label="撤销", command=undo)
functionmenu.add_command(label="恢复", command=redo)
functionmenu.add_command(label="全选", command=select_all)
topmenu.add_cascade(label="功能", menu=functionmenu)

aboutusmenu = Menu(topmenu, tearoff=False)
aboutusmenu.add_command(label="关于", command=about)
topmenu.add_cascade(label="关于", menu=aboutusmenu)
win.config(menu=topmenu)

popmenu = Menu(win, tearoff=False)
popmenu.add_command(label="打开", command=openfile)
popmenu.add_command(label="生成词云", command=generate_wordcloud)
popmenu.add_command(label="展示图片", command=showpicture)
popmenu.add_command(label="统计词频", command=wordsnumber)
popmenu.add_separator()
popmenu.add_command(label="剪切", command=cut)
popmenu.add_command(label="复制", command=copy)
popmenu.add_command(label="粘贴", command=paste)
popmenu.add_command(label="保存", command=save)
popmenu.add_separator()
popmenu.add_command(label="撤销", command=undo)
popmenu.add_command(label="恢复", command=redo)
popmenu.add_command(label="全选", command=select_all)
textbook.bind("<Button-3>", showpopmenu)

win.protocol("WM_DELETE_WINDOW", window_quit)
win.mainloop()

