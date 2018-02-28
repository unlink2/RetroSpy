from ViewWindow import ViewWindow
import tkinter as tk

class PreviewWindow(ViewWindow):
    def __init__(self, root, skin, bgname):
        ViewWindow.__init__(self, root, skin, bgname, '', preview=True)

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title('Edit')

        keylabel = tk.Label(self.edit_window, text='Key name (like in xml)')
        keylabel.pack()

        self.keyentry = tk.Entry(self.edit_window)
        self.keyentry.pack()

        valuelabel = tk.Label(self.edit_window, text='Value (true/false or float number)')
        valuelabel.pack()

        self.valueentry = tk.Entry(self.edit_window)
        self.valueentry.pack()

        svb = tk.Button(self.edit_window, text='set value', command=self.set_value_pressed)
        svb.pack()

        self.preview_data = {}
        self.preview_update()

    def preview_update(self):
        if not self.is_open:
            return

        self.skin.type.controllerreader.update(self.preview_data)

        self.window.after(1, self.preview_update)

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
