# -*- coding: cp936 -*-
from tkinter import *
from tkinter import messagebox


def on_click():
    global xls_text, root, x
    x = xls_text.get()
    if len(x) == 0:
        # �û�����������!
        messagebox.showwarning(title='ϵͳ��ʾ', message='�������û���!')
        return False
    root.quit()
    root.destroy()
    return x


def main_window():
    global xls_text, root, x
    root = Tk()
    root.title("Save Image")
    root.geometry('300x100') #��x ����*

    l1 = Label(root, text="������")
    l1.pack() #�����side���Ը�ֵΪLEFT  RTGHT TOP  BOTTOM
    xls_text = StringVar()
    xls = Entry(root, textvariable = xls_text)
    xls_text.set("")
    xls.pack()

    Button(root, text="press", command=on_click).pack()
    root.mainloop()
    return x
