import tkinter as tk
from tkinter import ttk


class CustomNotebook(ttk.Notebook):
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)

    def on_close_press(self, event):
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            for item in self.winfo_children():
                if str(item).split('k.')[1] == \
                        self.tab(index)['text'].split(' ')[1] \
                        and len(self.tabs()) > 1:
                    self.forget(item)
                    break
            self.event_generate("<<NotebookTabClosed>>")
            self._active = index

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAMAAADz0U65AAAABGdBTUEAALGPC/xh
                BQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA
                hFBMVEUjHyAjICAiHiAjHx8jHyAjHyAjISAjICAjHyAjHyAjHyAlHSIlIyIjHyAj
                HyAjHyAfHCEjHyAjHyAjHyAjHyAjHyAjHyAhHR0hHR8jHyAjHyAiHh0kIiEjHyAj
                HyAjHyAkHyElIiIkHSIhHRweGiIjHyAjHyAjHyAjHyAjHx4jHx////9N4xUEAAAA
                K3RSTlMAAAAA03kFBXXabQQDbNt2BGfecW/dagQDa+wDA27rcAQFBQMCaNx61QQE
                uzIdqwAAAAFiS0dEKyS55AgAAAAHdElNRQfkBgoOOgMXwkQ5AAAASklEQVQI1wXB
                hwKAEAAFwEe00aIo7aH+/wO7A+MxSMIZ0iwvSiEVqrppO2160ME6l48RyORnt6zA
                ZrUw2u/g0hzndT8I6o3op8IPh+0ExyYtVW0AAAAldEVYdGRhdGU6Y3JlYXRlADIw
                MjAtMDYtMTBUMTQ6NTc6NTIrMDA6MDAHpIU0AAAAJXRFWHRkYXRlOm1vZGlmeQAy
                MDIwLTA2LTEwVDE0OjU3OjUyKzAwOjAwdvk9iAAAAABJRU5ErkJggg==
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled",
                              "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"),
                             border=8, sticky='')
        style.layout("CustomNotebook",
                     [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label",
                                     {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close",
                                     {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
