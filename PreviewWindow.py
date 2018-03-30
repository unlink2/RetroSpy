from ViewWindow import ViewWindow
import tkinter as tk
from serial.serialutil import SerialException


class PreviewWindow(ViewWindow):
    def __init__(self, root, skin, bgname):
        ViewWindow.__init__(self, root, skin, bgname, '', preview=True)

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title('Edit')

        keylabel = tk.Label(self.edit_window, text='Key name (like in xml)')
        keylabel.pack()

        self.keyentry = tk.StringVar('')

        self.add_key_list()
        # self.keyentry = tk.Entry(self.edit_window)
        # self.keyentry.pack()

        valuelabel = tk.Label(self.edit_window, text='Value (true/false or float number)')
        valuelabel.pack()

        self.valueentry = tk.Entry(self.edit_window)
        self.valueentry.pack()

        type_label = tk.Label(self.edit_window, text='Type of element')
        type_label.pack()
        self.elem_type = tk.StringVar('')

        self.elem_entry = tk.Entry(self.edit_window, textvariable=self.elem_type)
        self.elem_entry.pack()

        svb = tk.Button(self.edit_window, text='set value', command=self.set_value_pressed)
        svb.pack()

        rskb = tk.Button(self.edit_window, text='reload skin', command=self.reload_skin_pressed)
        rskb.pack()

        selb = tk.Button(self.edit_window, text='select', command=self.select_pressed)
        selb.pack()

        addb = tk.Button(self.edit_window, text='add', command=self.add_pressed)
        addb.pack()

        saveb = tk.Button(self.edit_window, text='save', command=self.save_pressed)
        saveb.pack()

        self.edit_window.protocol('WM_DELETE_WINDOW', self.on_close)

        self.current_select = None
        self.current_select_type = ''
        self.current_select_key = ''

        self.preview_data = {}
        self.preview_update()

    def on_close(self):
        ViewWindow.on_close(self)
        self.edit_window.destroy()

    def preview_update(self):
        if not self.is_open:
            return

        self.skin.type.controllerreader.update(self.preview_data)

        self.window.after(self.update_interval, self.preview_update)

        # update type tag
        for p in self.skin.backgrounds:
            if p.name == self.keyentry.get():
                self.elem_type.set('background')

        for p in self.skin.details:
            if p.name == self.keyentry.get():
                self.elem_type.set('detail')

        for p in self.skin.buttons:
            if p.name == self.keyentry.get():
                self.elem_type.set('button')

        for p in self.skin.rangebuttons:
            if p.name == self.keyentry.get():
                self.elem_type.set('rangebutton')

        for p in self.skin.analogsticks:
            if p.xname == self.keyentry.get() or p.yname == self.keyentry.get():
                self.elem_type.set('stick')

        for p in self.skin.analogtriggers:
            if p.name == self.keyentry.get():
                self.elem_type.set('analog')


    def select_pressed(self):
        key = self.keyentry.get()
        self.current_select_key = key
        self.current_select, self.current_select_type = self.skin.get_element(key)

    def add_pressed(self):
        pass

    def save_pressed(self):
        self.skin.write_to_xml()

    def on_canvas_click(self, event):
        if self.current_select is None:
            return

        # check which thing to move on screen
        to_move = None
        if self.current_select_type == 'button':
            to_move = self.buttons[self.current_select_key]
        elif self.current_select_type == 'detail':
            to_move = self.details[self.current_select_key]
        elif self.current_select_type == 'stick':
            to_move = self.analogsticks[self.current_select_key]
        elif self.current_select_type == 'trigger':
            to_move = self.analogtriggers[self.current_select_key]
        elif self.current_select_type == 'rangebutton':
            to_move = self.analogtriggers[self.current_select_key]

        if to_move is None:
            return

        # center image
        x = event.x - self.current_select.config.width / 2
        y = event.y - self.current_select.config.height / 2
        self.current_select.config.x = x
        self.current_select.config.y = y
        self.cv.coords(self.current_select_key, x, y)


    def reload_skin_pressed(self):
        self.skin.load()
        try:
            self.make_reader()
        except SerialException as e:
            tk.messagebox.showerror("Error", str(e))
        self.load()

    def set_value_pressed(self):
        key = self.keyentry.get()

        val = self.valueentry.get()

        typedesc = ''

        if val == 'true':
            val = True
            typedesc = 'button'
        elif val == 'false':
            val = False
            typedesc = 'button'
        else:
            # parse float
            try:
                val = float(val)
                typedesc = 'analog'
            except ValueError as e:
                return

        self.preview_data[key] = {'name': key, 'type': typedesc, 'val': val}

    def add_key_list(self):
        self.keymenu = tk.OptionMenu(self.edit_window, self.keyentry, [], '')
        self.key_list_updater()
        self.keymenu.pack()

    def key_list_updater(self):
        menu = self.keymenu.children['menu']
        menu.delete(0, 'end')

        for p in self.skin.backgrounds:
            menu.add_command(label=p.name, command=lambda v=p.name: self.keyentry.set(v))

        for p in self.skin.details:
            menu.add_command(label=p.name, command=lambda v=p.name: self.keyentry.set(v))

        for p in self.skin.buttons:
            self.keyentry.set(p.name)
            menu.add_command(label=p.name, command=lambda v=p.name: self.keyentry.set(v))

        for p in self.skin.rangebuttons:
            menu.add_command(label=p.name, command=lambda v=p.name: self.keyentry.set(v))

        for p in self.skin.analogsticks:
            menu.add_command(label=p.xname, command=lambda v=p.xname: self.keyentry.set(v))
            menu.add_command(label=p.yname, command=lambda v=p.yname: self.keyentry.set(v))

        for p in self.skin.analogtriggers:
            menu.add_command(label=p.name, command=lambda v=p.name: self.keyentry.set(v))

