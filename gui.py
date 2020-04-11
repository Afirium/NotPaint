from tkinter import *
from core import main, rectangle_select

rect_icon = PhotoImage(file='./icons/ractangle.png')
rect_btn = Button(main, bg='white', height=75,
                  width=75, fg='black', image=rect_icon, compound=TOP)
rect_btn.pack(expand=NO, fill=NONE, side=LEFT)
rect_btn.bind('<Button-1>', rectangle_select)
rect_btn.place(relx=0, x=2, y=100, anchor=NW)

mainloop()
