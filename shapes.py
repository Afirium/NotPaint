import uuid


class Shape:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.id = 0

    def shape_create_start(self, event):
        self.x1 = event.x
        self.y1 = event.y

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y


class Rectanle(Shape):
    def __init__(self, c):
        super().__init__()
        self.c = c

    def shape_create(self, event):
        self.c.delete(self.id)
        self.id = self.c.create_rectangle(self.x1, self.y1,
                                          event.x, event.y,
                                          fill='green')
        self.c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.c.delete(self.id)
        self.c.create_rectangle(self.x1, self.y1,
                                self.x2, self.y2,
                                fill='green')


class Oval(Shape):
    def __init__(self, c):
        super().__init__()
        self.c = c

    def shape_create(self, event):
        self.c.delete(self.id)
        self.id = self.c.create_oval(self.x1, self.y1,
                                     event.x, event.y,
                                     fill='white')
        self.c.update_idletasks()
        self.c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.c.delete(self.id)
        self.c.create_oval(self.x1, self.y1,
                           self.x2, self.y2,
                           fill='white')


class Line(Shape):
    def __init__(self, c):
        super().__init__()
        self.c = c

    def shape_create(self, event):
        self.c.delete(self.id)
        self.id = self.c.create_line(self.x1, self.y1,
                                     event.x, event.y)
        self.c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.c.delete(self.id)
        self.c.create_line(self.x1, self.y1,
                           self.x2, self.y2)


class Polygon(Shape):
    def __init__(self, c):
        super().__init__()
        self.c = c

    def shape_create(self, event):
        self.c.delete(self.id)
        self.id = self.c.create_polygon([self.x1, self.y1,
                                         event.x, event.y,
                                         self.x1 - (event.x - self.x1),
                                         event.y],
                                        fill='red', width=1, outline='black')
        self.c.bind('<ButtonRelease-1>', self.shape_create_end)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.c.delete(self.id)
        self.c.create_polygon([self.x1, self.y1,
                               self.x2, self.y2,
                               self.x1 - (self.x2 - self.x1), self.y2],
                              fill='red', width=1, outline='black')


class CustomShape(Shape):
    def __init__(self, c):
        super().__init__()
        self.c = c
        self.id2 = None
        self.id3 = None
        self.unique_id = None

    def shape_create(self, event):
        self.c.delete(self.id)
        self.c.delete(self.id2)
        self.c.delete(self.id3)

        self.unique_id = str(uuid.uuid4())

        self.c.bind('<ButtonRelease-1>', self.shape_create_end)
        self.id = self.c.create_oval(self.x1, self.y1,
                                     event.x, event.y,
                                     fill='white',
                                     tag='custom_shape=' + self.unique_id)

        self.id3 = self.c.create_arc([self.x1, self.y1, event.x, event.y],
                                     style="chord",
                                     start=220, extent=140,
                                     tag='custom_shape=' + self.unique_id)
        self.id2 = self.c.create_arc([self.x1, self.y1, event.x, event.y],
                                     style="chord",
                                     start=40, extent=140,
                                     tag='custom_shape=' + self.unique_id)

    def shape_create_end(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.c.delete(self.id)
        self.c.delete(self.id2)
        self.c.delete(self.id3)
        self.c.create_oval(self.x1, self.y1,
                           event.x, event.y,
                           fill='white',
                           tag='custom_shape=' + self.unique_id)

        self.c.create_arc([self.x1, self.y1, event.x, event.y],
                          style="chord",
                          start=220, extent=140,
                          tag='custom_shape=' + self.unique_id)
        self.c.create_arc([self.x1, self.y1, event.x, event.y],
                          style="chord",
                          start=40, extent=140,
                          tag='custom_shape=' + self.unique_id)
