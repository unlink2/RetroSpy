import tkinter as tk


class PopupListbox(tk.Listbox):
    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.popupmenu = tk.Menu(parent, tearoff=0)
        self.popupmenu.add_command(label='Test')


        self.bind('<Button-3>', self.popup)

    def popup(self, event):
        try:
            self.popupmenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popupmenu.grab_release()

