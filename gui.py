from tkinter import *
from core import main, draw_rectangle, draw_oval, draw_line, select_move, \
    select_bottom_layer, select_remove_item, select_upper_layer

# Frame
f_bottom = Frame(main)
f_bottom.pack(side=BOTTOM)
f_bottom_2 = Frame(main)
f_bottom_2.pack(side=BOTTOM)
f_bottom_3 = Frame(main)
f_bottom_3.pack(side=BOTTOM)
f_top = Frame(main)
f_top.pack(side=TOP)

# Tools buttons
rect_icon = PhotoImage(file='./icons/ractangle.png')
rect_btn = Button(f_bottom, bg='white', height=50, width=50, fg='black',
                  image=rect_icon, compound=TOP)
rect_btn.pack(expand=NO, fill=NONE, side=LEFT)
rect_btn.bind('<Button-1>', draw_rectangle)

oval_icon = PhotoImage(file='./icons/circle.png')
oval_btn = Button(f_bottom, bg='white', height=50,
                  width=50, fg='black', image=oval_icon, compound=TOP)
oval_btn.pack(expand=NO, fill=NONE, side=LEFT)
oval_btn.bind('<Button-1>', draw_oval)

polygon_icon = PhotoImage(file='./icons/polygon.png')
polygon_btn = Button(f_bottom, bg='white', height=50,
                     width=50, fg='black', image=polygon_icon, compound=TOP)
polygon_btn.pack(expand=NO, fill=NONE, side=LEFT)
polygon_btn.bind('<Button-1>', draw_line)

line_icon = PhotoImage(file='./icons/line.png')
line_btn = Button(f_bottom, bg='white', height=50,
                  width=50, fg='black', image=line_icon, compound=TOP)
line_btn.pack(expand=NO, fill=NONE, side=LEFT)
line_btn.bind('<Button-1>', draw_line)

move_icon = PhotoImage(file='./icons/move.png')
move_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                  image=move_icon, compound=TOP)
move_btn.pack(expand=NO, fill=NONE, side=LEFT)
move_btn.bind('<Button-1>', select_move)

bot_icon = PhotoImage(file='./icons/down.png')
bot_layer_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                       image=bot_icon, compound=TOP)
bot_layer_btn.pack(expand=NO, fill=NONE, side=LEFT)
bot_layer_btn.bind('<Button-1>', select_bottom_layer)

up_icon = PhotoImage(file='./icons/up.png')
up_layer_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                      image=up_icon, compound=TOP)
up_layer_btn.pack(expand=NO, fill=NONE, side=LEFT)
up_layer_btn.bind('<Button-1>', select_upper_layer)

remove_icon = PhotoImage(file='./icons/delete.png')
remove_item_btn = Button(f_bottom_2, bg='white', height=50, width=50,
                         fg='black',
                         image=remove_icon, compound=TOP)
remove_item_btn.pack(expand=NO, fill=NONE, side=LEFT)
remove_item_btn.bind('<Button-1>', select_remove_item)

pointer_icon = PhotoImage(file='./icons/pointer.png')
pointer_btn = Button(f_bottom_3, bg='white', height=50, width=50,
                     fg='black',
                     image=pointer_icon, compound=TOP)
pointer_btn.pack(expand=NO, fill=NONE, side=LEFT)
pointer_btn.bind('<Button-1>', select_remove_item)

rotate_icon = PhotoImage(file='./icons/rotate.png')
rotate_btn = Button(f_bottom_3, bg='white', height=50, width=50,
                    fg='black',
                    image=rotate_icon, compound=TOP)
rotate_btn.pack(expand=NO, fill=NONE, side=LEFT)
rotate_btn.bind('<Button-1>', select_remove_item)

# Menu bar
menubar = Menu(main)
toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Show tools", command=NONE)
toolsmenu.add_command(label="Show property menu", command=NONE)
menubar.add_cascade(label="Tools", menu=toolsmenu)

main.config(menu=menubar)

mainloop()
