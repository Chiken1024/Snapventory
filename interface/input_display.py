import tkinter as tk
from PIL import Image

from opencv.process_image import mat_to_imagetk, path_to_imagetk

class InputDisplay(tk.Label):
  def __init__(self, master = None, background = None, size: tuple[int, int] = (20, 20)) -> None:
    super().__init__(master, background=background, width=size[0], height=size[1])
    self.mode: str = "none"

  def get_webcam_frame(self, cap):
    return cap.read()[1]

  def show_webcam(self, cap) -> bool:
    self.mode = "webcam"
    
    ret, frame = cap.read()

    imagetk = mat_to_imagetk(frame)
    self.configure(image=imagetk, width=640, height=480)
    self.image = imagetk
    self.update()

    return ret
  
  def show_image(self, path: str) -> None:
    self.mode = "file"
    
    imagetk = path_to_imagetk(path)
    self.configure(image=imagetk, width=640, height=480)
    self.image = imagetk
    self.update()