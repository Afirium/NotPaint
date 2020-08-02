import pickle
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageGrab

from shapes import Rectanle, Oval, Line, Polygon, CustomShape


class Move:
    def __init__(self, tree, canvas):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.treeview = tree
        self.c = canvas

    def first_click(self, event):
        if self.c.find_withtag(CURRENT) and \
                self.c.gettags(self.c.find_withtag(CURRENT))[0] \
                in ['group_' + i for i in self.treeview.get_children()]:
            self.x2 = event.x
            self.y2 = event.y
        else:
            self.x1 = event.x
            self.y1 = event.y

    def move_motion(self, event):
        if self.c.find_withtag(CURRENT) and \
                self.c.gettags(self.c.find_withtag(CURRENT))[0] \
                in ['group_' + i for i in self.treeview.get_children()]:
            self.c.move(self.c.gettags(self.c.find_withtag(CURRENT))[0],
                        event.x - self.x2,
                        event.y - self.y2)
            self.x2 = event.x
            self.y2 = event.y
        elif self.c.find_withtag(CURRENT) and 'custom_shape=' in \
                self.c.gettags(CURRENT)[0]:
            self.c.move(self.c.gettags(CURRENT)[0], event.x - self.x1,
                        event.y - self.y1)
            self.x1 = event.x
            self.y1 = event.y
        else:
            self.c.move('current', event.x - self.x1, event.y - self.y1)
            self.x1 = event.x
            self.y1 = event.y


class Core:
    def __init__(self, tree, mcontext, txtcolor, txtwidth, txtopacity,
                 txtshpwidth, txtshpheight, txtgroup, main, combo, notebook):
        self.c = Canvas()
        self.item_by_pointer = [0, 0, 0]
        self.current_group = [0]
        self.current_name = [None]
        self.treeview = tree
        self.menu_context = mcontext
        self.txt_color = txtcolor
        self.txt_width = txtwidth
        self.txt_opacity = txtopacity
        self.txt_shape_width = txtshpwidth
        self.txt_shape_height = txtshpheight
        self.txt_group = txtgroup
        self.main = main
        self.combo_name = combo
        self.nb = notebook
        self.frame_tab_list = []
        self.treeview_list = dict()
        self.current_tab = None
        self.create_new_canvas()
        self.get_current_tab()

        self.treeview.bind("<Button-1>", self.select_group_from_tree)
        self.treeview.bind("<Button-2>", self.delete_group_from_tree)
        self.combo_name.bind('<Button-1>', self.combo_name_render)
        self.combo_name.bind('<<ComboboxSelected>>',
                             self.combo_name_get_current)
        self.c.bind("<Button-3>", self.context_menu)

    def get_current_tab(self):
        self.current_tab = self.nb.tab(self.nb.select(), "text").split(' ')[1]

    def draw_rectangle(self, event):
        r = Rectanle(self.c)
        self.c.bind('<Button-1>', r.shape_create_start)
        self.c.bind('<B1-Motion>', r.shape_create)

    def draw_oval(self, event):
        o = Oval(self.c)
        self.c.bind('<Button-1>', o.shape_create_start)
        self.c.bind('<B1-Motion>', o.shape_create)

    def draw_line(self, event):
        l = Line(self.c)
        self.c.bind('<Button-1>', l.shape_create_start)
        self.c.bind('<B1-Motion>', l.shape_create)

    def draw_polygon(self, event):
        p = Polygon(self.c)
        self.c.bind('<Button-1>', p.shape_create_start)
        self.c.bind('<B1-Motion>', p.shape_create)

    def draw_cshape(self, event):
        cs = CustomShape(self.c)
        self.c.bind('<Button-1>', cs.shape_create_start)
        self.c.bind('<B1-Motion>', cs.shape_create)

    def unbind_all_custom(self):
        self.c.unbind('<Button-1>')
        self.c.unbind('<ButtonRelease-1>')
        self.c.unbind('<B1-Motion>')

    def select_move(self, event):
        self.unbind_all_custom()
        m = Move(self.treeview, self.c)
        self.c.bind('<Button-1>', m.first_click)
        self.c.bind('<B1-Motion>', m.move_motion)

    def context_menu(self, event):
        if self.c.find_withtag(CURRENT):
            self.menu_context.post(event.x_root, event.y_root)

    def bottom_layer(self, event):
        obj = self.c.find_withtag(CURRENT)
        self.c.tag_lower(obj)

    def select_bottom_layer(self, event):
        self.unbind_all_custom()
        self.c.bind('<Button-1>', self.bottom_layer)

    def upper_layer(self, event):
        obj = self.c.find_withtag(CURRENT)
        self.c.tag_raise(obj)

    def select_upper_layer(self, event):
        self.unbind_all_custom()
        self.c.bind('<Button-1>', self.upper_layer)

    def remove_item(self, event):
        self.c.update_idletasks()
        obj = self.c.find_withtag(CURRENT)
        if self.item_by_pointer[0] == obj:
            self.item_by_pointer[0] = None
        for t_item in self.treeview.get_children():
            for shape in self.treeview.get_children(t_item):
                if self.c.find_withtag(shape) == obj:
                    self.c.dtag(shape, self.treeview.parent(t_item))
                    self.treeview.delete(shape)
        if obj and 'custom_shape=' in self.c.gettags(CURRENT)[0]:
            tg = self.c.gettags(obj)[0]
            shapes = self.c.find_withtag(tg)
            for s in shapes:
                self.c.delete(s)
        self.c.delete(obj)

    def select_remove_item(self, event):
        self.unbind_all_custom()
        self.c.bind('<Button-1>', self.remove_item)

    def in_group(self, item):
        for tag in self.c.gettags(item):
            if tag.split('_')[0] == 'group':
                return True
        return False

    def group_items(self, event):
        item = self.c.find_withtag(CURRENT)
        print(self.current_group[0], "TEST")
        if item and self.current_group[0] is not None and not self.in_group(
                item):
            if 'custom_shape=' in self.c.gettags(CURRENT)[0]:
                tg = self.c.gettags(CURRENT)[0]
                shapes = self.c.find_withtag(tg)
                for s in shapes:
                    self.c.addtag_withtag(self.current_group[0], s)
            else:
                self.c.addtag_withtag(self.current_group[0], CURRENT)
                self.treeview.insert(self.current_group[0].split("_")[1], END,
                                     item,
                                     text=(self.c.type(item), str(item[0])))
        else:
            messagebox.showinfo('Error', 'Choose or add a group')

    def select_group(self, event):
        self.unbind_all_custom()
        self.c.bind('<Button-1>', self.group_items)

    def clear_txtbox(self):
        self.txt_color.delete(0, END)
        self.txt_width.delete(0, END)
        self.txt_opacity.delete(0, END)
        self.txt_shape_width.delete(0, END)
        self.txt_shape_height.delete(0, END)

    def pointer_set_item(self, event):
        if self.c.find_withtag(CURRENT):
            print(self.c.gettags(self.c.find_withtag(CURRENT)),
                  self.c.type(self.c.find_withtag(CURRENT)))
            self.item_by_pointer[0] = self.c.find_withtag(CURRENT)

            self.clear_txtbox()
            self.txt_width.insert(0,
                                  self.c.itemcget(self.item_by_pointer[0],
                                                  'width'))
            self.txt_color.insert(0,
                                  self.c.itemcget(self.item_by_pointer[0],
                                                  'fill'))
            self.txt_opacity.insert(0, 0 if self.c.itemcget(
                self.item_by_pointer[0],
                'fill') == '' else 1)

            crd = self.c.coords(self.item_by_pointer[0])
            if self.c.type(self.item_by_pointer[0]) != 'polygon':
                self.txt_shape_width.insert(0, crd[2] - crd[0])
                self.txt_shape_height.insert(0, crd[3] - crd[1])
                self.item_by_pointer[1] = crd[2] - crd[0]
                self.item_by_pointer[2] = crd[3] - crd[1]
            else:
                self.txt_shape_width.insert(0, crd[2] - crd[4])
                self.txt_shape_height.insert(0, crd[3] - crd[1])
                self.item_by_pointer[1] = crd[2] - crd[4]
                self.item_by_pointer[2] = crd[3] - crd[1]

            return self.item_by_pointer
        else:
            self.clear_txtbox()
            self.item_by_pointer[0] = 0
            self.txt_shape_height.insert(0, self.c['height'])
            self.txt_shape_width.insert(0, self.c['width'])
            self.txt_color.insert(0, self.c['bg'])

    def select_pointer(self, event):
        self.unbind_all_custom()
        self.c.bind('<Button-1>', self.pointer_set_item)

    def select_set_all(self, event):
        # Settings for canvas
        if self.item_by_pointer[0] == 0 and self.txt_shape_width.get() != '':
            self.c.config(bg=self.txt_color.get(),
                          width=self.txt_shape_width.get(),
                          height=self.txt_shape_height.get())

        if self.combo_name['values'] != '' and self.combo_name.get() != '' and \
                self.current_name[0] != self.combo_name.get():
            if self.c.find_withtag(self.current_name[0]) != () and \
                    isinstance(self.c.find_withtag(self.current_name[0])[0],
                               int):
                item = self.c.find_withtag(self.current_name[0])
                self.c.addtag_withtag('name_' + self.combo_name.get(), item)
                self.current_name[0] = 0
            else:
                item = self.c.find_withtag('name_' + self.current_name[0])
                self.c.dtag(item, 'name_' + self.current_name[0])
                self.c.addtag_withtag('name_' + self.combo_name.get(), item)
                self.current_name[0] = 0

        if (self.txt_group.get() != '' and self.txt_group.get()
                not in self.treeview.get_children()
                and not self.txt_group.get().isnumeric()):
            self.current_group[0] = self.txt_group.get()
            self.treeview.insert('', END, self.current_group,
                                 text=self.current_group)
            self.txt_group.delete(0, END)
        if self.item_by_pointer[0] != 0 and self.txt_shape_width.get() != '' \
                and self.txt_shape_height.get() != '' and float(
            self.txt_shape_width.get()) >= 0 and float(
            self.txt_shape_height.get()) >= 0:

            crd = self.c.coords(self.item_by_pointer[0])

            width_coord = float(self.txt_shape_width.get()) - \
                          self.item_by_pointer[1]
            height_coord = float(self.txt_shape_height.get()) - \
                           self.item_by_pointer[
                               2]
            self.item_by_pointer[1] = float(self.txt_shape_width.get())
            self.item_by_pointer[2] = float(self.txt_shape_height.get())
            if self.c.type(self.item_by_pointer[0]) != 'polygon':
                self.c.coords(self.item_by_pointer[0], crd[0], crd[1],
                              crd[2] + width_coord, crd[3] + height_coord)
            else:
                xy = self.c.coords(self.item_by_pointer[0])
                width_coord = float(self.txt_shape_width.get()) - (
                        xy[2] - xy[4])
                height_coord = float(self.txt_shape_height.get()) - (
                        xy[3] - xy[1])

                self.c.coords(self.item_by_pointer[0],
                              xy[0] + (width_coord / 2), xy[1] - height_coord,
                              xy[2] + width_coord, xy[3],
                              xy[4], xy[5])
            self.c.itemconfig(self.item_by_pointer[0],
                              width=self.txt_width.get(),
                              fill=self.txt_color.get())
        if self.txt_opacity.get() == '0':
            self.c.itemconfig(self.item_by_pointer[0], fill='')

    def save_as_image(self):
        x = self.main.winfo_rootx() + 1 + self.c.winfo_x()
        y = self.main.winfo_rooty() + 22 + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        filename = filedialog.asksaveasfilename(
            initialdir="C:/Users/desktop.ini",
            title="Select place",
            filetypes=(("PNG files", "*.png"),
                       ("All files", "*.*")),
            defaultextension=".png")
        ImageGrab.grab().crop((x, y, x1, y1)).save(filename, format="PNG")

    def save_as_project(self):
        c_info = []
        for i in self.c.find_all():
            c_info += [[self.c.type(i), self.c.coords(i), self.c.itemconfig(i),
                        self.c.gettags(i)]]
        self.main.update()
        c_info.append(
            [self.c.winfo_height(), self.c.winfo_width(), self.c["bg"]])

        file = filedialog.asksaveasfilename(
            initialdir="C:/Users/desktop.ini",
            title="Select place",
            filetypes=(
                ("PICKLE files", "*.pickle"),),
            defaultextension=".pickle")

        if not file:
            return

        with open(file, 'wb') as pickle_file:
            pickle.dump(c_info, pickle_file)

    def load_project(self):
        file = filedialog.askopenfilename(initialdir="C:/Users/desktop.ini",
                                          title="Select project",
                                          filetypes=(
                                              ("PICKLE files", "*.pickle"),),
                                          defaultextension=".pickle")

        if not file:
            return

        with open(file, 'rb') as pickle_file:
            data_new = pickle.load(pickle_file)
        self.c.delete('all')

        shape = None
        self.c.config(height=data_new[-1][0], width=data_new[-1][1],
                      bg=data_new[-1][2])
        print(data_new[:-1])
        for i in data_new[:-1]:
            if i[0] == 'rectangle':
                shape = self.c.create_rectangle(i[1])
            elif i[0] == 'oval':
                shape = self.c.create_oval(i[1])
            elif i[0] == 'line':
                shape = self.c.create_line(i[1])
            elif i[0] == 'arc':
                shape = self.c.create_arc(i[1])
                self.c.itemconfig(shape, width=i[2]['width'][4],
                                  fill=i[2]['fill'][4],style='chord',
                                  start=i[2]['start'][4], extent=i[2]['extent'][4],
                                  tags=i[2]['tags'][4])
            self.c.itemconfig(shape, width=i[2]['width'][4],
                              fill=i[2]['fill'][4])

    def select_group_from_tree(self, event):
        t_item = self.treeview.identify('item', event.x, event.y)
        if self.treeview.parent(t_item) == '':
            self.current_group[0] = 'group_' + str(t_item)

    def delete_group_from_tree(self, event):
        t_item = self.treeview.identify('item', event.x, event.y)

        if t_item and self.treeview.parent(t_item) == '':
            for i in self.treeview.get_children(t_item):
                self.treeview.delete(i)
            self.treeview.delete(t_item)
        elif t_item and self.treeview.parent(t_item) != '':
            shape = self.c.find_withtag(
                self.treeview.item(t_item, "text").split(' ')[1])
            self.c.dtag(shape, 'group_' + self.treeview.parent(t_item))
            self.treeview.delete(
                self.treeview.item(t_item, "text").split(' ')[1])

    def combo_name_render(self, event):
        temp = []
        bln = True
        self.combo_name['values'] = []
        for i in self.c.find_all():
            for t in self.c.gettags(i):
                tag_name = t.split('_')
                if tag_name[0] == 'name':
                    temp += [tag_name[1]]
                    bln = False
            if bln:
                temp += [str(i)]
            bln = True
        self.combo_name['values'] = temp

    def combo_name_get_current(self, event):
        self.current_name[0] = self.combo_name.get()
        self.item_by_pointer[0] = self.c.find_withtag(
            self.combo_name.get() if self.combo_name.get().isnumeric() else 'name_' + self.combo_name.get())
        self.clear_txtbox()
        self.txt_width.insert(0,
                              self.c.itemcget(self.item_by_pointer[0], 'width'))
        self.txt_color.insert(0,
                              self.c.itemcget(self.item_by_pointer[0], 'fill'))
        self.txt_opacity.insert(0, 1)

        crd = self.c.coords(self.item_by_pointer[0])
        self.txt_shape_width.insert(0, crd[2] - crd[0])
        self.txt_shape_height.insert(0, crd[3] - crd[1])
        self.item_by_pointer[1] = crd[2] - crd[0]
        self.item_by_pointer[2] = crd[3] - crd[1]

    def clear_canvas(self):
        self.clear_txtbox()
        self.treeview.delete(*self.treeview.get_children())
        self.c.delete('all')

    def create_new_canvas(self):
        self.unbind_all_custom()
        frame = Frame(self.nb, name=str(len(self.frame_tab_list) + 1),
                      bg='white')
        frame.pack_propagate(0)

        c = Canvas(frame, bg='#F6F5F6', borderwidth=0,
                   highlightthickness=0, width=400, height=400)
        c.pack(side=LEFT, anchor='nw')
        self.c = c
        self.frame_tab_list.append(frame)
        self.nb.add(frame, text=f'Canvas {len(self.frame_tab_list)}')

    def select_current_canvas(self, event):
        self.clear_txtbox()
        self.unbind_all_custom()

        tab_id = self.nb.tab(self.nb.select(), "text").split(' ')[1]

        dict_child = self.nb.children
        self.c = dict_child[tab_id].winfo_children()[0]
