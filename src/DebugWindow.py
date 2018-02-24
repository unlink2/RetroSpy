# This tk winodw is used to log the state of pins

import tkinter as tk
import SerialMonitor
import time

class DebugWindow:
    def __init__(self, comport, ui=8, ports_to_read=9):
        self.serial = SerialMonitor.SerialMonitor(serial_port=comport)
        time.sleep(3)  # sleep to ensure connection has been made
        # by default this runs a bit less than 16 times a second
        self.update_interval = ui
        self.ports_to_read = ports_to_read
        self.labels = []
        self.ports_to_read = ports_to_read

        self.root = tk.Tk()
        self.root.minsize(width=400, height=40)
        self.root.maxsize(width=400, height=40)

        self.logfile = open('./debug_log.txt', 'a')

        w = tk.Label(self.root, text='Listening to port: ' + comport)
        w.pack()

        for i in range(0, ports_to_read + 1):
            self.serial.set_pin_mode(i, 'I')
            self.serial.digital_write(i, 0)

        v = tk.StringVar()
        w = tk.Label(self.root, textvariable=v)
        w.pack()
        self.labels.append({'label': w, 'string': v})

        self.root.after(self.update_interval, self.update)
        self.root.mainloop()

    def update(self):
        outstr = 'P'

        status = self.serial.digital_read(0xff)
        self.labels[0]['string'].set('PINS: ' + str(status))
        outstr = outstr + str(status)

        self.logfile.write(outstr + '\n')
        self.root.after(self.update_interval, self.update)
