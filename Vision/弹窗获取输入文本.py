# -*- coding: cp936 -*-
from tkinter import *
from tkinter import messagebox


def on_click():
    global xls_text, root, x
    x = xls_text.get()
    if len(x) == 0:
        # 用户名必须输入!
        messagebox.showwarning(title='系统提示', message='请输入用户名!')
        return False
    root.quit()
    root.destroy()
    return x


def main_window():
    global xls_text, root, x
    root = Tk()
    root.title("Save Image")
    root.geometry('300x100') #是x 不是*

    l1 = Label(root, text="姓名：")
    l1.pack() #这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
    xls_text = StringVar()
    xls = Entry(root, textvariable = xls_text)
    xls_text.set("")
    xls.pack()

    Button(root, text="press", command=on_click).pack()
    root.mainloop()
    return x
