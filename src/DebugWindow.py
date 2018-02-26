# This tk winodw is used to log the state of pins

import tkinter as tk
from PIL import Image, ImageTk
import SerialMonitor
import time
from util import readBit

# This is the experimental mega drive input view window.
# This will move to the normal view window once it is implemented.


class DebugSerialCallback:
    def __init__(self, window):
        self.window = window

    def onSuccess(self, data):
        if(len(data) < 2):
            return # bad data

        pinstr0 = ''

        # up
        if readBit(data[0], 2) == 0:
            self.window.cv.itemconfigure(self.window.dpad_pressed_up_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.dpad_pressed_up_mob, state=tk.HIDDEN)

        # down
        if readBit(data[0], 3) == 0:
            self.window.cv.itemconfigure(self.window.dpad_pressed_down_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.dpad_pressed_down_mob, state=tk.HIDDEN)

        # left
        if readBit(data[0], 4) == 0:
            self.window.cv.itemconfigure(self.window.dpad_pressed_left_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.dpad_pressed_left_mob, state=tk.HIDDEN)

        # right
        if readBit(data[0], 5) == 0:
            self.window.cv.itemconfigure(self.window.dpad_pressed_right_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.dpad_pressed_right_mob, state=tk.HIDDEN)

        # A
        if readBit(data[1], 6) == 0:
            self.window.cv.itemconfigure(self.window.a_pressed_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.a_pressed_mob, state=tk.HIDDEN)

        # B
        if readBit(data[0], 6) == 0:
            self.window.cv.itemconfigure(self.window.b_pressed_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.b_pressed_mob, state=tk.HIDDEN)

        # C
        if readBit(data[0], 7) == 0:
            self.window.cv.itemconfigure(self.window.c_pressed_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.c_pressed_mob, state=tk.HIDDEN)

        # start
        if readBit(data[1], 7) == 0:
            self.window.cv.itemconfigure(self.window.start_pressed_mob, state=tk.NORMAL)
        else:
            self.window.cv.itemconfigure(self.window.start_pressed_mob, state=tk.HIDDEN)

    def onError(self, data):
        pass


class DebugWindow:
    def __init__(self, comport, ui=1, ports_to_read=9):
        self.serial = SerialMonitor.SerialMonitor(serial_port=comport,
                      callback=DebugSerialCallback(self), baud_rate=115200)

        time.sleep(2)  # sleep to ensure connection has been made
        # by default this runs a bit less than 16 times a second
        self.update_interval = ui
        self.ports_to_read = ports_to_read
        self.labels = []
        self.ports_to_read = ports_to_read

        self.root = tk.Tk()
        self.root.minsize(width=800, height=600)
        self.root.maxsize(width=800, height=600)
        self.root.title('MegaDrive Input Display Debug Window')

        w = tk.Label(self.root, text='Listening to port: ' + comport)
        w.pack()

        # display images on this
        self.cv = tk.Canvas(self.root, width=800, height=500)
        self.cv.pack()

        tmp = Image.open('./skins/MegaDrive-test/images/Controller-def.png')
        self.bg_image = ImageTk.PhotoImage(image=tmp)
        self.bg_mob = self.cv.create_image(0, 0, anchor='nw', image=self.bg_image)

        self.trigger_pressed_img = Image.open('./skins/MegaDrive-test/images/Trigger_pressed.png')
        self.trigger_pressed_image = ImageTk.PhotoImage(image=self.trigger_pressed_img)
        self.a_pressed_mob = self.cv.create_image(490, 240, anchor='nw', image=self.trigger_pressed_image)
        self.cv.itemconfigure(self.a_pressed_mob, state=tk.HIDDEN)

        self.b_pressed_mob = self.cv.create_image(570, 203, anchor='nw', image=self.trigger_pressed_image)
        self.cv.itemconfigure(self.b_pressed_mob, state=tk.HIDDEN)

        self.c_pressed_mob = self.cv.create_image(650, 170, anchor='nw', image=self.trigger_pressed_image)
        self.cv.itemconfigure(self.c_pressed_mob, state=tk.HIDDEN)

        self.start_pressed_img = Image.open('./skins/MegaDrive-test/images/start_pressed.png')
        self.start_pressed_image = ImageTk.PhotoImage(image=self.start_pressed_img)
        self.start_pressed_mob = self.cv.create_image(515, 100, anchor='nw', image=self.start_pressed_image)
        self.cv.itemconfigure(self.start_pressed_mob, state=tk.HIDDEN)


        self.dpad_pressed_up_down_img = Image.open('./skins/MegaDrive-test/images/dpad_pressed_up_down.png')
        self.dpad_pressed_up_down_image = ImageTk.PhotoImage(image=self.dpad_pressed_up_down_img)
        self.dpad_pressed_up_mob = self.cv.create_image(167, 175, anchor='nw', image=self.dpad_pressed_up_down_image)
        self.cv.itemconfigure(self.dpad_pressed_up_mob, state=tk.HIDDEN)

        self.dpad_pressed_down_mob = self.cv.create_image(167, 250, anchor='nw', image=self.dpad_pressed_up_down_image)
        self.cv.itemconfigure(self.dpad_pressed_down_mob, state=tk.HIDDEN)


        self.dpad_pressed_left_right_img = Image.open('./skins/MegaDrive-test/images/dpad_pressed_left_right.png')
        self.dpad_pressed_left_right_image = ImageTk.PhotoImage(image=self.dpad_pressed_left_right_img)
        self.dpad_pressed_left_mob = self.cv.create_image(120, 218, anchor='nw', image=self.dpad_pressed_left_right_image)
        self.cv.itemconfigure(self.dpad_pressed_left_mob, state=tk.HIDDEN)


        self.dpad_pressed_right_mob = self.cv.create_image(205, 218, anchor='nw', image=self.dpad_pressed_left_right_image)
        self.cv.itemconfigure(self.dpad_pressed_right_mob, state=tk.HIDDEN)

        self.root.after(self.update_interval, self.update)
        self.root.mainloop()

    def update(self):
        self.serial.serial_read()
        self.root.after(self.update_interval, self.update)
