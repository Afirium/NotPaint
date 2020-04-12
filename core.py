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
                                     fill='white')
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id)
        c.create_rectangle(self.x1, self.y1,
                           self.x2, self.y2,
                           fill='white')


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


def select_move(event):
    c.unbind('<Button-1>')
    c.unbind('<ButtonRelease-1>')
    c.unbind('<B1-Motion>')
    m = Move()
    c.bind('<Button-1>', m.move1)
    c.bind('<B1-Motion>', m.move2)


def context_menu(event):
    if c.find_withtag(CURRENT):
        menu_context.post(event.x_root, event.y_root)


def upper_layer():
    obj = c.find_withtag(CURRENT)
    c.tag_raise(obj)


def bottom_layer():
    obj = c.find_withtag(CURRENT)
    c.tag_lower(obj)


def remove_item():
    obj = c.find_withtag(CURRENT)
    c.delete(obj)


# Parameters for TKinter

main = Tk()
main.geometry('1500x750')
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')
canvas_width = 1130
canvas_height = 750
canvas_color = '#b8bfc2'
c = PatchedCanvas(main, bg=canvas_color, borderwidth=0, highlightthickness=0)
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
