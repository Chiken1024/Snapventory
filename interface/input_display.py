import tkinter as tk

from opencv.process_image import mat_to_photoimage, path_to_photoimage

class InputDisplay(tk.Label):
  def __init__(self, cap, master = None, background = None) -> None:
    super().__init__(master, background=background, width=91, height=32)
    self.cap = cap
    self.mode: str = "none"
    self.path: str = ""

  def get_webcam_frame(self):
    return self.cap.read()[1]

  def show(self, path: str | None = None):
    match self.mode:
      case "none":
        self.path = ""
        self.configure(image="", width=91, height=32)
      case "webcam":
        self.path = ""
        
        ret, frame = self.cap.read()
        
        photoimage = mat_to_photoimage(frame)
        self.configure(image=photoimage, width=640, height=480)
        self.image = photoimage
        self.update()

        return ret
      case "file":
        self.path = path
        photoimage = path_to_photoimage(path)
        self.configure(image=photoimage, width=640, height=480)
        self.image = photoimage
        self.update()
  
  def cancel(self) -> None:
    self.mode = "none"
    self.show()