# modified from the SO answer here: https://stackoverflow.com/a/58130065

import tkinter as tk
from PIL import ImageGrab, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.bbox = None
        self.screenshot = None

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both",expand=True)

        image = ImageGrab.grab()
        image = image.resize((image.size[0]//2, image.size[1]//2))
        self.image = ImageTk.PhotoImage(image)
        self.photo = self.canvas.create_image(0,0,image=self.image,anchor="nw")

        self.update()
        self.state("zoomed")
        w = self.winfo_width() + self.winfo_rootx()
        h = self.winfo_height() + self.winfo_rooty()
        self.overrideredirect(True)
        self.state('normal')
        self.geometry(f'{w}x{h}+0+0')

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,"<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.photo,"<B1-Motion>", self.on_move_press)
        self.canvas.tag_bind(self.photo,"<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.bbox = self.canvas.bbox(self.rect)
        self.withdraw()
        self.after(100, self.take_screenshot)

    def take_screenshot(self):
        self.screenshot = ImageGrab.grab(self.bbox)
        self.destroy()

def promptScreenshot():
    root = GUI()
    root.mainloop()
    if root.screenshot is None:
        raise Exception("Screenshot prompt failed")
    return root.screenshot, root.bbox
