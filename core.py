from tkinter import *


class PatchedCanvas(Canvas):
    def unbind(self, sequence, funcid=None):
        """Unbind for this widget for event SEQUENCE  the
            function identified with FUNCID."""
        if not funcid:
            self.tk.call('bind', self._w, sequence, '')
            return
        func_callbacks = self.tk.call('bind', self._w, sequence, None).split(
            '\n')
        new_callbacks = [l for l in func_callbacks if
                         l[6:6 + len(funcid)] != funcid]
        self.tk.call('bind', self._w, sequence, '\n'.join(new_callbacks))
        self.deletecommand(funcid)


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
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.select = 0

    def move1(self, event):
        self.x1 = event.x
        self.y1 = event.y
        self.select = c.find_withtag(CURRENT)

    def move2(self, event):
        if b[0] == 1:
            c.update_idletasks()
            b[0] = 3
            k[0] = event.x
            k[1] = event.y
            dx = event.x - self.x1
            dy = event.y - self.y1
            c.move(self.select, dx, dy)

        if b[0] == 3:
            c.update_idletasks()
            dx = event.x - k[0]
            dy = event.y - k[1]
            c.move(self.select, dx, dy)
            k[0] = event.x
            k[1] = event.y
        c.bind('<ButtonRelease-1>', self.move3)

    def move3(self, event):
        self.x2 = event.x
        self.y2 = event.y
        dx = self.x2 - k[0]
        dy = self.y2 - k[1]

        b[0] = 1
        k[0] = k[1] = 0


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
    c.bind('<Button-1>', m.move1)
    c.bind('<B1-Motion>', m.move2)


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
    c.delete(obj)


def select_remove_item(event):
    unbind_all_custom()
    c.bind('<Button-1>', remove_item)


item_by_pointer = [0, 0, 0]


def clear_txtbox():
    txt_color.delete(0, END)
    txt_width.delete(0, END)
    txt_opacity.delete(0, END)
    txt_rotate.delete(0, END)
    txt_shape_width.delete(0, END)
    txt_shape_height.delete(0, END)


def pointer_set_item(event):
    if c.find_withtag(CURRENT):
        item_by_pointer[0] = c.find_withtag(CURRENT)

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


def select_set_all(event):
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


# Parameters for TKinter
main = Tk()
main.geometry('1500x750')
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')

left_frame = Frame(main)
left_frame.pack(side=LEFT, expand=1, fill=BOTH)

canvas_width = 1130
canvas_height = 750
canvas_color = '#b8bfc2'
c = PatchedCanvas(left_frame, bg=canvas_color, borderwidth=0,
                  highlightthickness=0)
c.pack(expand=1, fill=BOTH)

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

f_top = Frame(main)
f_top.pack(side=TOP)

lb_width = Label(f_top, text='Border width')
lb_width.pack(expand=1, fill=X)
txt_width = Entry(f_top, justify=CENTER)
txt_width.pack(expand=1, fill=X)

lb_opacity = Label(f_top, text='Opacity')
lb_opacity.pack(expand=1, fill=X)
txt_opacity = Entry(f_top, justify=CENTER)
txt_opacity.pack(expand=1, fill=X)

lb_rotate = Label(f_top, text='Rotate angle')
lb_rotate.pack(expand=1, fill=X)
txt_rotate = Entry(f_top, justify=CENTER)
txt_rotate.pack(expand=1, fill=X)

lb_color = Label(f_top, text='Color')
lb_color.pack(expand=1, fill=X)
txt_color = Entry(f_top, justify=CENTER)
txt_color.pack(expand=1, fill=X)

lb_shape_width = Label(f_top, text='Width')
lb_shape_width.pack(expand=1, fill=X)
txt_shape_width = Entry(f_top, justify=CENTER)
txt_shape_width.pack(expand=1, fill=X)

lb_shape_height = Label(f_top, text='Heigth')
lb_shape_height.pack(expand=1, fill=X)
txt_shape_height = Entry(f_top, justify=CENTER)
txt_shape_height.pack(expand=1, fill=X)

btn_set_all = Button(f_top, bg='white', width=30, text='Apply')
btn_set_all.pack(expand=1, fill=X, pady=20)
btn_set_all.bind('<Button-1>', select_set_all)
