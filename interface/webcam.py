import tkinter as tk
from opencv.process_image import to_imagetk

class Webcam(tk.Label):
  def __init__(self, master = None, background = None) -> None:
    super().__init__(master, background=background)

  def get_frame(self, cap):
    return cap.read()[1]

  def show(self, cap) -> bool:
    ret, frame = cap.read()
  
    imagetk = to_imagetk(frame)
    self.configure(image=imagetk)
    self.image = imagetk
    self.update()

    return ret