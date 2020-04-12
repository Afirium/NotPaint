from tkinter import *
from core import main, draw_rectangle, draw_oval, draw_line, select_move

# Tools buttons
rect_icon = PhotoImage(file='./icons/ractangle.png')
rect_btn = Button(main, bg='white', height=50, width=50, fg='black',
                  image=rect_icon, compound=TOP)
rect_btn.pack(expand=NO, fill=NONE, side=LEFT)
rect_btn.bind('<Button-1>', draw_rectangle)

oval_icon = PhotoImage(file='./icons/circle.png')
oval_btn = Button(main, bg='white', height=50,
                  width=50, fg='black', image=oval_icon, compound=TOP)
oval_btn.pack(expand=NO, fill=NONE, side=LEFT)
oval_btn.bind('<Button-1>', draw_oval)

line_icon = PhotoImage(file='./icons/line.png')
line_btn = Button(main, bg='white', height=50,
                  width=50, fg='black', image=line_icon, compound=TOP)
line_btn.pack(expand=NO, fill=NONE, side=LEFT)
line_btn.bind('<Button-1>', draw_line)

move_icon = PhotoImage(file='./icons/move.png')
move_btn = Button(main, bg='white', height=50, width=50, fg='black',
                  image=move_icon, compound=TOP)
move_btn.pack(expand=NO, fill=NONE, side=LEFT)
move_btn.bind('<Button-1>', select_move)

# Menu bar
menubar = Menu(main)
toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Show tools", command=NONE)
toolsmenu.add_command(label="Show property menu", command=NONE)
menubar.add_cascade(label="Tools", menu=toolsmenu)

main.config(menu=menubar)

mainloop()
