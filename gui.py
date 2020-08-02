from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview

from core import Core
from custom_notebook import CustomNotebook

# Parameters for TKinter


main = Tk()
mcolor = '#FFFFFF'
main.geometry('1500x850')
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')
main.configure(bg=mcolor)

nb = CustomNotebook(main)
nb.pack(side=LEFT, expand=1, fill=BOTH)

# Notebook


# left_frame = Frame(nb, bg="white")
# nb.add(left_frame, text="Canvas 1")

# canvas_width = 1130
# canvas_height = 750
# canvas_color = '#F6F5F6'
# c = Canvas(left_frame, bg=canvas_color, borderwidth=0,
#            highlightthickness=0, width=400, height=400)
# c.pack(side=LEFT, anchor='nw')
# left_frame.winfo_children()[0]['bg'] = 'red'
remove_icon = PhotoImage(file='./icons/remove.png')
up_icon = PhotoImage(file='./icons/up_layer.png')
down_icon = PhotoImage(file='./icons/bottom_layer.png')
menu_context = Menu(tearoff=0)

# Information frame
f_top = Frame(main, bg=mcolor)
f_top.pack(side=TOP)
#
#   BUG КОГДА ДОБАВЛЯЮ В ГРУПППУ ЕЛЕМЕНТ А У НЕГО УЖЕ ЕСТЬ ГРУППА
#

# Combobox for names
lb_name = Label(f_top, text='Shape', bg=mcolor, font='Helvetica 10 bold')
lb_name.pack(expand=1, fill=X)
combo_name = Combobox(f_top, font='Helvetica 10')
combo_name.pack(expand=1, fill=X, pady=5)

# Tools
lb_width = Label(f_top, text='Border', bg=mcolor, font='Helvetica 10 bold')
lb_width.pack(expand=1, fill=X)
txt_width = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_width.pack(expand=1, fill=X, pady=5)

lb_opacity = Label(f_top, text='Opacity', bg=mcolor,
                   font='Helvetica 10 bold')
lb_opacity.pack(expand=1, fill=X)
txt_opacity = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_opacity.pack(expand=1, fill=X, pady=5)

lb_color = Label(f_top, text='Color', bg=mcolor, font='Helvetica 10 bold')
lb_color.pack(expand=1, fill=X)
txt_color = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_color.pack(expand=1, fill=X, pady=5)

lb_shape_width = Label(f_top, text='Width', bg=mcolor,
                       font='Helvetica 10 bold')
lb_shape_width.pack(expand=1, fill=X)
txt_shape_width = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_shape_width.pack(expand=1, fill=X, pady=5)

lb_shape_height = Label(f_top, text='Heigth', bg=mcolor,
                        font='Helvetica 10 bold')
lb_shape_height.pack(expand=1, fill=X)
txt_shape_height = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_shape_height.pack(expand=1, fill=X, pady=5)

# Tree View for groups
lb_group = Label(f_top, text='New group', bg=mcolor,
                 font='Helvetica 10 bold')
lb_group.pack(expand=1, fill=X)

txt_group = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_group.pack(expand=1, fill=X)
treeview = Treeview(f_top)
treeview.pack(expand=1, fill=X)

core = Core(
    treeview,
    menu_context,
    txt_color,
    txt_width,
    txt_opacity,
    txt_shape_width,
    txt_shape_height,
    txt_group,
    main,
    combo_name,
    nb)

nb.bind('<<NotebookTabChanged>>', core.select_current_canvas)

menu_context.add_command(label="Upper layer", image=up_icon,
                         compound='left', command=core.upper_layer)
menu_context.add_command(label="Remove", image=remove_icon, compound='left',
                         command=core.remove_item)
menu_context.add_command(label="Bottom layer", image=down_icon, compound='left',
                         command=core.bottom_layer)

# Frame
f_bottom = Frame(main)
f_bottom.pack(side=BOTTOM)
f_bottom_2 = Frame(main)
f_bottom_2.pack(side=BOTTOM)
f_bottom_3 = Frame(main)
f_bottom_3.pack(side=BOTTOM)

# Tools buttons
rect_icon = PhotoImage(file='./icons/ractangle.png')
rect_btn = Button(f_bottom, bg='white', height=50, width=50, fg='black',
                  image=rect_icon, compound=TOP, relief='flat')
rect_btn.pack(expand=NO, fill=NONE, side=LEFT)
rect_btn.bind('<Button-1>', core.draw_rectangle)

oval_icon = PhotoImage(file='./icons/circle.png')
oval_btn = Button(f_bottom, bg='white', height=50,
                  width=50, fg='black', image=oval_icon, compound=TOP,
                  relief='flat')
oval_btn.pack(expand=NO, fill=NONE, side=LEFT)
oval_btn.bind('<Button-1>', core.draw_oval)

polygon_icon = PhotoImage(file='./icons/triangle.png')
polygon_btn = Button(f_bottom, bg='white', height=50,
                     width=50, fg='black', image=polygon_icon, compound=TOP,
                     relief='flat')
polygon_btn.pack(expand=NO, fill=NONE, side=LEFT)
polygon_btn.bind('<Button-1>', core.draw_polygon)

line_icon = PhotoImage(file='./icons/line.png')
line_btn = Button(f_bottom, bg='white', height=50,
                  width=50, fg='black', image=line_icon, compound=TOP,
                  relief='flat')
line_btn.pack(expand=NO, fill=NONE, side=LEFT)
line_btn.bind('<Button-1>', core.draw_line)

move_icon = PhotoImage(file='./icons/move.png')
move_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                  image=move_icon, compound=TOP, relief='flat')
move_btn.pack(expand=NO, fill=NONE, side=LEFT)
move_btn.bind('<Button-1>', core.select_move)

bot_icon = PhotoImage(file='./icons/down.png')
bot_layer_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                       image=bot_icon, compound=TOP, relief='flat')
bot_layer_btn.pack(expand=NO, fill=NONE, side=LEFT)
bot_layer_btn.bind('<Button-1>', core.select_bottom_layer)

up_icon = PhotoImage(file='./icons/up.png')
up_layer_btn = Button(f_bottom_2, bg='white', height=50, width=50, fg='black',
                      image=up_icon, compound=TOP, relief='flat')
up_layer_btn.pack(expand=NO, fill=NONE, side=LEFT)
up_layer_btn.bind('<Button-1>', core.select_upper_layer)

remove_icon = PhotoImage(file='./icons/delete.png')
remove_item_btn = Button(f_bottom_2, bg='white', height=50, width=50,
                         fg='black',
                         image=remove_icon, compound=TOP, relief='flat')
remove_item_btn.pack(expand=NO, fill=NONE, side=LEFT)
remove_item_btn.bind('<Button-1>', core.select_remove_item)

pointer_icon = PhotoImage(file='./icons/pointer.png')
pointer_btn = Button(f_bottom_3, bg='white', height=50, width=50,
                     fg='black', borderwidth=6,
                     image=pointer_icon, compound=TOP, relief='flat',
                     highlightbackground="#37d3ff",
                     highlightthickness=3, bd=0
                     )
pointer_btn.pack(expand=NO, fill=NONE, side=LEFT)
pointer_btn.bind('<Button-1>', core.select_pointer)

group_icon = PhotoImage(file='./icons/group.png')
group_btn = Button(f_bottom_3, bg='white', height=50, width=50,
                   fg='black', relief='flat',
                   image=group_icon, compound=TOP,
                   highlightbackground="#37d3ff",
                   highlightthickness=3, bd=0
                   )
group_btn.pack(expand=NO, fill=NONE, side=LEFT)
group_btn.bind('<Button-1>', core.select_group)

cshape_icon = PhotoImage(file='./icons/polygon.png')
cshape_btn = Button(f_bottom_3, bg='white', height=50, width=50,
                    fg='black', borderwidth=6,
                    image=cshape_icon, compound=TOP, relief='flat',
                    highlightbackground="#37d3ff",
                    highlightthickness=3, bd=0)
cshape_btn.pack(expand=NO, fill=NONE, side=LEFT)
cshape_btn.bind('<Button-1>', core.draw_cshape)

btn_set_all = Button(f_top, bg='white', width=25, text='Apply', relief=SOLID,
                     bd=1,
                     font='Helvetica 10 bold')
btn_set_all.pack(expand=1, fill=X, pady=20)
btn_set_all.bind('<Button-1>', core.select_set_all)

# Menu bar
menubar = Menu(main)
toolsmenu = Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Save as image", command=core.save_as_image)
toolsmenu.add_command(label="Save as project", command=core.save_as_project)
toolsmenu.add_command(label="Open project", command=core.load_project)
menubar.add_cascade(label="File", menu=toolsmenu)
canvasmenu = Menu(menubar, tearoff=0)
canvasmenu.add_command(label="Clear canvas", command=core.clear_canvas)
canvasmenu.add_command(label="New canvas", command=core.create_new_canvas)
canvasmenu.bind('<Button-1>', core.unbind_all_custom)
menubar.add_cascade(label="Canvas", menu=canvasmenu)

main.config(menu=menubar)
mainloop()
