import tkinter as tk
from PIL import Image, ImageTk
from InputSource import InputSource
from ControllerState import ControllerState
import Skin
import util
from serial.serialutil import SerialException
from threading import Thread
from time import sleep

class ViewWindow:
    def __init__(self, root, skin, bgname, comport, preview=False):
        self.skin = skin
        self.bgname = bgname
        self.comport = comport
        self.is_open = True
        self.preview = preview

        self.update_interval = 3

        try:
            self.make_reader()
        except SerialException as e:
            tk.messagebox.showerror("Error", str(e))
            return

        self.state = ControllerState({}, {})
        self.last_error = None

        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title('View')

        self.background = None
        self.buttons = {}
        self.details = {}
        self.rangebuttons = {}
        self.analogsticks = {}
        self.analogtriggers = {}

        # get current background
        self.current_bg = None
        for bg in self.skin.backgrounds:
            if bg.name == self.bgname:
                self.current_bg = bg

        self.makeCanvas(self.current_bg.width, self.current_bg.height)
        self.window.minsize(width=self.current_bg.width, height=self.current_bg.height)
        self.window.maxsize(width=self.current_bg.width, height=self.current_bg.height)

        self.load()

        self.root.withdraw()

        self.window.protocol('WM_DELETE_WINDOW', self.on_close)

        self.update()
        # self.start_update_t()

    def start_update_t(self):
        self.thread = Thread(target=self.state_update)
        self.thread.start()

    def make_reader(self):
        self.skin.type.makeControllerReader(comport=self.comport, preview=self.preview)
        self.skin.type.controllerreader.controllerstate += self.on_state
        self.skin.type.controllerreader.onerror += self.on_error

    def load(self):
        self.background = None
        self.buttons = {}
        self.details = {}
        self.rangebuttons = {}
        self.analogsticks = {}
        self.analogtriggers = {}

        self.cv.delete('all')

        self.addBackground()
        self.addButtons()
        self.addDetail()
        self.addAnalogSticks()
        self.addAnalogTriggers()
        self.addRangebuttons()

    # override this to get callback whenever the canvas was clicked
    # event.x event.y are click coordinates
    def on_canvas_click(self, event):
        pass

    def on_close(self):
        self.root.deiconify()
        self.window.destroy()
        self.skin.type.controllerreader.finish() # close controller reader
        self.is_open = False

    def makeCanvas(self, w, h):
        self.cv = tk.Canvas(self.window, width=w, height=h)
        # Button-1 is mouse1
        self.cv.bind('<Button-1>', self.on_canvas_click)
        self.cv.pack()

    def addBackground(self):
        self.cv.create_rectangle(0, 0, self.current_bg.width, self.current_bg.height,
                                 fill=self.current_bg.color)
        if self.current_bg.image is not None:
            self.bg_image = ImageTk.PhotoImage(image=self.current_bg.image)
            self.background = self.cv.create_image(0, 0, anchor='nw',
                               image=self.bg_image)

    def addButtons(self):
        for button in self.skin.buttons:
            # first we check if we do not render
            if not self.shouldEleRender(button.config):
                continue
            if button.config.image is None:
                continue

            # scale image
            button.config.image.resize((int(button.config.width), int(button.config.height)), Image.AFFINE)

            # now we add the image
            tmpimg = ImageTk.PhotoImage(image=button.config.image)

            tmpmob = self.cv.create_image(button.config.x, button.config.y,
                                          anchor='nw',
                                          image=tmpimg,
                                          tags=button.name)
            if not self.preview:
                self.cv.itemconfigure(tmpmob, state=tk.HIDDEN)

            # add button to list
            self.buttons[button.name] = {'mob': tmpmob, 'img': tmpimg, 'cfg': button}

    def addDetail(self):
        for detail in self.skin.details:
            # first we check if we do not render
            if not self.shouldEleRender(detail.config):
                continue
            if detail.config.image is None:
                continue

            # scale image
            detail.config.image.resize((int(detail.config.width), int(detail.config.height)), Image.AFFINE)

            # now we add the image
            tmpimg = ImageTk.PhotoImage(image=detail.config.image)

            tmpmob = self.cv.create_image(detail.config.x, detail.config.y,
                                          anchor='nw',
                                          image=tmpimg,
                                          tags=detail.name)
            if not self.preview:
                self.cv.itemconfigure(tmpmob, state=tk.HIDDEN)

            # add button to list
            self.details[detail.name] = {'mob': tmpmob, 'img': tmpimg, 'cfg': detail}

    def addAnalogSticks(self):
        for analog in self.skin.analogsticks:
            # first we check if we do not render
            if not self.shouldEleRender(analog.config):
                continue
            if analog.config.image is None:
                continue

            # scale image
            analog.config.image.resize((int(analog.config.width), int(analog.config.height)), Image.AFFINE)

            # now we add the image
            tmpimg = ImageTk.PhotoImage(image=analog.config.image)

            tmpmob = self.cv.create_image(analog.config.x, analog.config.y,
                                          anchor='nw',
                                          image=tmpimg,
                                          tags=[analog.xname, analog.yname])

            # add button to list
            self.analogsticks[analog.xname] = {'mob': tmpmob, 'img': tmpimg, 'cfg': analog}
            self.analogsticks[analog.yname] = {'mob': tmpmob, 'img': tmpimg, 'cfg': analog}

    def addRangebuttons(self):
        for rb in self.skin.rangebuttons:
            # first we check if we do not render
            if not self.shouldEleRender(rb.config):
                continue
            if rb.config.image is None:
                continue

            # scale image
            rb.config.image.resize((int(rb.config.width), int(rb.config.height)), Image.AFFINE)

            # now we add the image
            tmpimg = ImageTk.PhotoImage(image=rb.config.image)

            tmpmob = self.cv.create_image(rb.config.x, rb.config.y,
                                          anchor='nw',
                                          image=tmpimg,
                                          tags=rb.name)
            if not self.preview:
                self.cv.itemconfigure(tmpmob, state=tk.HIDDEN)

            # add button to list
            self.rangebuttons[rb.name] = {'mob': tmpmob, 'img': tmpimg, 'cfg': rb}

    def addAnalogTriggers(self):
        for rb in self.skin.analogtriggers:
            # first we check if we do not render
            if not self.shouldEleRender(rb.config):
                continue
            if rb.config.image is None:
                continue

            # scale image
            rb.config.image.resize((int(rb.config.width), int(rb.config.height)), Image.AFFINE)

            # now we add the image
            tmpimg = ImageTk.PhotoImage(image=rb.config.image)

            tmpmob = self.cv.create_image(rb.config.x, rb.config.y,
                                          anchor='nw',
                                          image=tmpimg,
                                          tags=rb.name)

            # add button to list
            self.analogtriggers[rb.name] = {'mob': tmpmob, 'img': tmpimg, 'cfg': rb}

    def shouldEleRender(self, elecfg):
        if (len(elecfg.target_backgrounds) == 0 or self.bgname in elecfg.target_backgrounds)\
                and self.bgname not in elecfg.ignore_backgrounds:
            return True

        return False

    def state_update(self):
        #while self.is_open:
        self.skin.type.controllerreader.update()


    def update(self):
        if not self.is_open:
            return

        if self.last_error is not None:
            tk.messagebox.showerror('Error', self.last_error)
            self.last_error = None

        self.state_update()

        # class plugins
        for p in util.plugins.plugins:
            p.update(self.state)

        self.window.after(self.update_interval, self.update)

        # go through states and check what to do
        for key in self.state.buttons:
            if key in self.buttons.keys():
                if self.state.buttons[key]:
                    self.cv.itemconfigure(self.buttons[key]['mob'], state=tk.NORMAL)

                    # check for onpress action
                    if self.buttons[key]['cfg'].config.on_keydown is not None:
                        util.sendKeyToOS(self.buttons[key]['cfg'].config.on_keydown)

                    # check if plugins need to be run
                    for p in util.plugins.plugins:
                        if self.buttons[key]['cfg'].config.action == p.name:
                            p.on_action(key, True)
                else:
                    for p in util.plugins.plugins:
                        if self.buttons[key]['cfg'].config.action == p.name:
                            p.on_action(key, False)
                    self.cv.itemconfigure(self.buttons[key]['mob'], state=tk.HIDDEN)

        for key in self.state.analogs:
            keyorg = key
            if self.state.analogs[key] < 0:
                key = key + '_'

            if key in self.rangebuttons.keys():
                cfg = self.rangebuttons[key]['cfg']
                if cfg.fromF <= self.state.analogs[keyorg] <= cfg.toF:
                    self.cv.itemconfigure(self.rangebuttons[key]['mob'], state=tk.NORMAL)

                    if self.rangebuttons[key]['cfg'].config.on_keydown is not None:
                        util.sendKeyToOS(self.rangebuttons[key]['cfg'].config.on_keydown)
                else:
                    if key+'_' in self.rangebuttons.keys():
                        self.cv.itemconfigure(self.rangebuttons[key+'_']['mob'], state=tk.HIDDEN)
                    if keyorg in self.rangebuttons.keys():
                        self.cv.itemconfigure(self.rangebuttons[keyorg]['mob'], state=tk.HIDDEN)

        for key in self.state.analogs:
            if key in self.analogsticks:
                if key == self.analogsticks[key]['cfg'].xname:
                    x, y = self.cv.coords(key)
                    reverse = 1
                    if self.analogsticks[key]['cfg'].xreverse:
                        reverse = -1
                    x = self.analogsticks[key]['cfg'].config.x + self.analogsticks[key]['cfg'].xrange * reverse * self.state.analogs[key]
                    self.cv.coords(key, x, y)
                elif key == self.analogsticks[key]['cfg'].yname:
                    x, y = self.cv.coords(key)
                    reverse = -1
                    if self.analogsticks[key]['cfg'].yreverse:
                        reverse = 1
                    y = self.analogsticks[key]['cfg'].config.y + self.analogsticks[key]['cfg'].yrange * reverse * self.state.analogs[key]
                    self.cv.coords(key, x, y)

            if key in self.analogtriggers:
                # decide how to crop
                direction = self.analogtriggers[key]['cfg'].direction
                w = int(self.analogtriggers[key]['cfg'].config.width)
                h = int(self.analogtriggers[key]['cfg'].config.height)

                # TODO this needs a lot of work!
                if not self.analogtriggers[key]['cfg'].is_reversed:
                    if direction == Skin.RIGHT:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w * self.state.analogs[key], h])
                    elif direction == Skin.LEFT:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [w - w * self.state.analogs[key], 0, w, h])
                        # adjust position
                        self.cv.coords(key, self.analogtriggers[key]['cfg'].config.x + w - w * self.state.analogs[key], self.analogtriggers[key]['cfg'].config.y)
                    elif direction == Skin.DOWN:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w, h * self.state.analogs[key]])
                    elif direction == Skin.UP:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, h - h * self.state.analogs[key], w, h])
                        self.cv.coords(key, self.analogtriggers[key]['cfg'].config.x, self.analogtriggers[key]['cfg'].config.y + h - h * self.state.analogs[key])
                else:
                    # TODO reverse only works LEFT and UP for now
                    if direction == Skin.RIGHT:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w - w * self.state.analogs[key], h])
                    elif direction == Skin.LEFT:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w - w * self.state.analogs[key], h])
                    elif direction == Skin.DOWN:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w, h - h * self.state.analogs[key]])
                    elif direction == Skin.UP:
                        self.analogtriggers[key]['cfg'].config.image_crop = self.analogtriggers[key]['cfg'].config.image.crop(
                            [0, 0, w, h - h * self.state.analogs[key]])

                tmpimg = ImageTk.PhotoImage(image=self.analogtriggers[key]['cfg'].config.image_crop)
                self.analogtriggers[key]['img'] = tmpimg
                self.cv.itemconfigure(self.analogtriggers[key]['mob'], image=tmpimg)

    def on_state(self, sender, state):
        self.state = state

    def on_error(self, sender, error):
        self.last_error = error
