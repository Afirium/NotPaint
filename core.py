from tkinter import *


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
        c.create_rectangle(self.x1, self.y1,
                           self.x2, self.y2,
                           fill='white')


class Oval(Shape):
    def shape_create(self, event):
        c.delete(self.id)
        self.id = c.create_oval(self.x1, self.y1,
                                event.x, event.y,
                                fill='white')
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
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
        c.create_line(self.x1, self.y1,
                      self.x2, self.y2)


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


# Parameters for TKinter

main = Tk()
main.geometry('1500x750')
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')
canvas_width = 1130
canvas_height = 750
canvas_color = 'white'
c = Canvas(main, bg=canvas_color)
c.pack(expand=1, fill=BOTH)
