from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview, Combobox
from PIL import ImageGrab


# Primitives

class Shape:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.id = 0

    # work without him
    def shape_create(self, event):
        c.bind("<ButtonRelease-1>", self.shape_create_end)

    def shape_create_start(self, event):
        self.x1 = event.x
        self.y1 = event.y

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y


class Rectanle(Shape):
    def shape_create(self, event):
        c.delete(self.id)
        self.id = c.create_rectangle(self.x1, self.y1,
                                     event.x, event.y,
                                     fill='green')
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id)
        c.create_rectangle(self.x1, self.y1,
                           self.x2, self.y2,
                           fill='green')


class Oval(Shape):
    def shape_create(self, event):
        c.delete(self.id)
        self.id = c.create_oval(self.x1, self.y1,
                                event.x, event.y,
                                fill='white')
        c.update_idletasks()
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id)
        c.create_oval(self.x1, self.y1,
                      self.x2, self.y2,
                      fill='white')


class Line(Shape):
    def shape_create(self, event):
        c.delete(self.id)
        self.id = c.create_line(self.x1, self.y1,
                                event.x, event.y)
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id)
        c.create_line(self.x1, self.y1,
                      self.x2, self.y2)


b = [1]
k = [0, 0]


class Move:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def first_click(self, event):
        # if current_group[0] in c.gettags(c.find_withtag(CURRENT)):
        if c.gettags(c.find_withtag(CURRENT))[0] in treeview.get_children():
            self.x2 = event.x
            self.y2 = event.y
        else:
            self.x1 = event.x
            self.y1 = event.y

    def move_motion(self, event):
        # if current_group[0] in c.gettags(c.find_withtag(CURRENT)):
        print(c.gettags(c.find_withtag(CURRENT)))
        if c.gettags(c.find_withtag(CURRENT))[0] in treeview.get_children():
            c.move(c.gettags(c.find_withtag(CURRENT))[0], event.x - self.x2,
                   event.y - self.y2)
            self.x2 = event.x
            self.y2 = event.y
        else:
            c.move('current', event.x - self.x1, event.y - self.y1)
            self.x1 = event.x
            self.y1 = event.y


def draw_rectangle(event):
    r = Rectanle()
    c.bind('<Button-1>', r.shape_create_start)
    c.bind('<B1-Motion>', r.shape_create)


def draw_oval(event):
    o = Oval()
    c.bind('<Button-1>', o.shape_create_start)
    c.bind('<B1-Motion>', o.shape_create)


def draw_line(event):
    l = Line()
    c.bind('<Button-1>', l.shape_create_start)
    c.bind('<B1-Motion>', l.shape_create)


def unbind_all_custom():
    c.unbind('<Button-1>')
    c.unbind('<ButtonRelease-1>')
    c.unbind('<B1-Motion>')


def select_move(event):
    unbind_all_custom()
    m = Move()
    c.bind('<Button-1>', m.first_click)
    c.bind('<B1-Motion>', m.move_motion)


def context_menu(event):
    if c.find_withtag(CURRENT):
        menu_context.post(event.x_root, event.y_root)


def bottom_layer(event):
    obj = c.find_withtag(CURRENT)
    c.tag_lower(obj)


def select_bottom_layer(event):
    unbind_all_custom()
    c.bind('<Button-1>', bottom_layer)


def upper_layer(event):
    obj = c.find_withtag(CURRENT)
    c.tag_raise(obj)


def select_upper_layer(event):
    unbind_all_custom()
    c.bind('<Button-1>', upper_layer)


def remove_item(event):
    c.update_idletasks()
    obj = c.find_withtag(CURRENT)
    if item_by_pointer[0] == obj:
        item_by_pointer[0] = None
    for t_item in treeview.get_children():
        for shape in treeview.get_children(t_item):
            if c.find_withtag(shape) == obj:
                c.dtag(shape, treeview.parent(t_item))
                treeview.delete(shape)
    c.delete(obj)


def select_remove_item(event):
    unbind_all_custom()
    c.bind('<Button-1>', remove_item)


def group_items(event):
    item = c.find_withtag(CURRENT)
    if item and current_group[0] is not None:
        print(c.type(item), item)
        c.addtag_withtag(current_group[0], CURRENT)
        treeview.insert(current_group[0], END, item,
                        text=(c.type(item), str(item[0])))
    else:
        messagebox.showinfo('Error', 'Choose or add a group')


def select_group(event):
    unbind_all_custom()
    c.bind('<Button-1>', group_items)


item_by_pointer = [0, 0, 0]


def clear_txtbox():
    txt_color.delete(0, END)
    txt_width.delete(0, END)
    txt_opacity.delete(0, END)
    txt_shape_width.delete(0, END)
    txt_shape_height.delete(0, END)


def pointer_set_item(event):
    if c.find_withtag(CURRENT):
        item_by_pointer[0] = c.find_withtag(CURRENT)

        print(c.type(item_by_pointer[0]))

        clear_txtbox()
        txt_width.insert(0, c.itemcget(item_by_pointer[0], 'width'))
        txt_color.insert(0, c.itemcget(item_by_pointer[0], 'fill'))
        txt_opacity.insert(0, 1)

        crd = c.coords(item_by_pointer[0])
        txt_shape_width.insert(0, crd[2] - crd[0])
        txt_shape_height.insert(0, crd[3] - crd[1])
        item_by_pointer[1] = crd[2] - crd[0]
        item_by_pointer[2] = crd[3] - crd[1]

        return item_by_pointer
    else:
        clear_txtbox()


def select_pointer(event):
    unbind_all_custom()
    c.bind('<Button-1>', pointer_set_item)


current_group = [None]


def select_set_all(event):
    # print(c.itemconfig(c.find_all()[0]))
    if current_name[0] != combo_name.get():
        if c.find_withtag(current_name[0]) != () and \
                isinstance(c.find_withtag(current_name[0])[0], int):
            item = c.find_withtag(current_name[0])
            c.addtag_withtag('name_' + combo_name.get(), item)
            current_name[0] = combo_name.get()
        else:
            item = c.find_withtag('name_' + current_name[0])
            c.dtag(item, 'name_' + current_name[0])
            c.addtag_withtag('name_' + combo_name.get(), item)
            current_name[0] = combo_name.get()

    if (txt_group.get() != '' and txt_group.get() not in treeview.get_children()
            and not txt_group.get().isnumeric()):
        current_group[0] = txt_group.get()
        treeview.insert('', END, current_group, text=current_group)
        txt_group.delete(0, END)

    if txt_shape_width.get() != '' and txt_shape_height.get() != '' and float(
            txt_shape_width.get()) >= 0 and float(txt_shape_height.get()) >= 0:
        crd = c.coords(item_by_pointer[0])

        width_coord = float(txt_shape_width.get()) - item_by_pointer[1]
        height_coord = float(txt_shape_height.get()) - item_by_pointer[2]
        item_by_pointer[1] = float(txt_shape_width.get())
        item_by_pointer[2] = float(txt_shape_height.get())

        c.coords(item_by_pointer[0], crd[0], crd[1],
                 crd[2] + width_coord, crd[3] + height_coord)
    c.itemconfigure(item_by_pointer[0], width=txt_width.get(),
                    fill=txt_color.get())
    if txt_opacity.get() == '0':
        c.itemconfig(item_by_pointer[0], fill='')


def save_as_image():
    x = main.winfo_rootx() + c.winfo_x()
    y = main.winfo_rooty() + c.winfo_y()
    xx = x + c.winfo_width()
    yy = y + c.winfo_height()
    ImageGrab.grab(bbox=(x, y, xx, yy)).save("test.png")


def select_group_from_tree(event):
    t_item = treeview.identify('item', event.x, event.y)
    if treeview.parent(t_item) == '':
        current_group[0] = str(t_item)


def delete_group_from_tree(event):
    t_item = treeview.identify('item', event.x, event.y)

    current_group[0] = None
    if t_item and treeview.parent(t_item) == '':
        for i in treeview.get_children(t_item):
            treeview.delete(i)
        treeview.delete(t_item)
    elif t_item and treeview.parent(t_item) != '':
        shape = c.find_withtag(treeview.item(t_item, "text").split(' ')[1])
        c.dtag(shape, treeview.parent(t_item))
        treeview.delete(treeview.item(t_item, "text").split(' ')[1])


# Parameters for TKinter

main = Tk()
main.geometry('1500x850')
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')
main.configure(bg='#ffd1dc')

left_frame = Frame(main, bg="white")
left_frame.pack(side=LEFT, expand=1, fill=BOTH)

canvas_width = 1130
canvas_height = 750
# canvas_color = '#b8bfc2'
canvas_color = '#b8bfc2'
c = Canvas(left_frame, bg=canvas_color, borderwidth=0,
           highlightthickness=0, width=400, height=400)
c.pack(side=LEFT, anchor='nw')
# c.pack(expand=1, fill=BOTH)

remove_icon = PhotoImage(file='./icons/remove.png')
up_icon = PhotoImage(file='./icons/up_layer.png')
down_icon = PhotoImage(file='./icons/bottom_layer.png')
menu_context = Menu(tearoff=0)

menu_context.add_command(label="Upper layer", image=up_icon,
                         compound='left', command=upper_layer)
menu_context.add_command(label="Remove", image=remove_icon, compound='left',
                         command=remove_item)
menu_context.add_command(label="Bottom layer", image=down_icon, compound='left',
                         command=bottom_layer)

c.bind("<Button-3>", context_menu)

# Information frame
f_top = Frame(main, bg='#ffd1dc')
f_top.pack(side=TOP)

#
#   BUG КОГДА ДОБАВЛЯЮ В ГРУПППУ ЕЛЕМЕНТ А У НЕГО УЖЕ ЕСТЬ ГРУППА
#

current_name = [0]


def combo_name_render(event):
    temp = []
    bln = True
    combo_name['values'] = []
    for i in c.find_all():
        for t in c.gettags(i):
            tag_name = t.split('_')
            if tag_name[0] == 'name':
                temp += [tag_name[1]]
                bln = False
        if bln:
            temp += [str(i)]
        bln = True
    combo_name['values'] = temp


def combo_name_get_current(event):
    current_name[0] = combo_name.get()


# Combobox for names
lb_name = Label(f_top, text='Shape', bg='#ffd1dc', font='Helvetica 10 bold')
lb_name.pack(expand=1, fill=X)
combo_name = Combobox(f_top, font='Helvetica 10')
combo_name.pack(expand=1, fill=X, pady=5)
combo_name.bind('<Button-1>', combo_name_render)
combo_name.bind('<<ComboboxSelected>>', combo_name_get_current)

# Tools
lb_width = Label(f_top, text='Border', bg='#ffd1dc', font='Helvetica 10 bold')
lb_width.pack(expand=1, fill=X)
txt_width = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_width.pack(expand=1, fill=X, pady=5)

lb_opacity = Label(f_top, text='Opacity', bg='#ffd1dc',
                   font='Helvetica 10 bold')
lb_opacity.pack(expand=1, fill=X)
txt_opacity = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_opacity.pack(expand=1, fill=X, pady=5)

lb_color = Label(f_top, text='Color', bg='#ffd1dc', font='Helvetica 10 bold')
lb_color.pack(expand=1, fill=X)
txt_color = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_color.pack(expand=1, fill=X, pady=5)

lb_shape_width = Label(f_top, text='Width', bg='#ffd1dc',
                       font='Helvetica 10 bold')
lb_shape_width.pack(expand=1, fill=X)
txt_shape_width = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_shape_width.pack(expand=1, fill=X, pady=5)

lb_shape_height = Label(f_top, text='Heigth', bg='#ffd1dc',
                        font='Helvetica 10 bold')
lb_shape_height.pack(expand=1, fill=X)
txt_shape_height = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_shape_height.pack(expand=1, fill=X, pady=5)

# Tree View for groups
lb_group = Label(f_top, text='New group', bg='#ffd1dc',
                 font='Helvetica 10 bold')
lb_group.pack(expand=1, fill=X)

txt_group = ttk.Entry(f_top, justify=CENTER, font='Helvetica 10')
txt_group.pack(expand=1, fill=X)
treeview = Treeview(f_top)
treeview.pack(expand=1, fill=X)

treeview.bind("<Button-1>", select_group_from_tree)
treeview.bind("<Button-2>", delete_group_from_tree)
