import tkinter as tk
from util import ABOUT_TEXT

class AboutWindow():
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('About')

        abouttext = tk.Text(self.window, height=20, width=81)
        scrollbar = tk.Scrollbar(self.window)
        abouttext.pack()
        scrollbar.config(command=abouttext.yview)
        abouttext.config(yscrollcommand=scrollbar.set)
        abouttext.insert(tk.END, ABOUT_TEXT)
        abouttext["state"] = tk.DISABLED
