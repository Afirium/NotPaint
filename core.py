from tkinter import *


# Primitives

class Shape:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.id1 = 0
        self.id2 = 0

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
        x = event.x
        y = event.y
        c.delete(self.id1)
        self.id2 = c.create_rectangle(self.x1, self.y1,
                                      x, y,
                                      fill='white')
        self.id1 = self.id2
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id2)
        c.create_rectangle(self.x1, self.y1,
                           self.x2, self.y2,
                           fill='white')


class Oval(Shape):
    def shape_create(self, event):
        x = event.x
        y = event.y
        c.delete(self.id1)
        self.id2 = c.create_oval(self.x1, self.y1,
                                 x, y,
                                 fill='white')
        self.id1 = self.id2
        c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        c.delete(self.id2)
        c.create_oval(self.x1, self.y1,
                      self.x2, self.y2,
                      fill='white')


def rectangle_select(event):
    if flag == 0:
        r = Rectanle()
        c.bind('<Button-1>', r.shape_create_start)
        c.bind('<B1-Motion>', r.shape_create)


# Parameters for TKinter

main = Tk()
main.geometry('1500x750')
flag = 0
main.title('NotPaint')
main.iconbitmap('./icons/window_ico.ico')
canvas_width = 1130
canvas_height = 750
canvas_color = 'white'
c = Canvas(main, width=canvas_width, height=canvas_height, bg=canvas_color)
c.pack(expand=NO, fill=NONE)
