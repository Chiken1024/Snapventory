import tkinter as tk
from tkinter.filedialog import askopenfilename#, asksaveasfile

from interface.input_display import InputDisplay
from tesseract.scan import scan

class GUI:
  def __init__(self, cap) -> None:
    self.cap = cap
    
    self.root: tk.Tk = tk.Tk("Snapventory")
    self.root.geometry("660x540")
    self.root.wm_minsize(660, 540)
    self.root.wm_maxsize(660, 540)
    self.root.configure(background="#252526")

    self.input_display_label: InputDisplay = InputDisplay(
      self.root, "#2d2d30", (91, 32)
    )
    self.input_display_label.place(x=8, y=45)

    self.open_camera_button: tk.Button = tk.Button(
      self.root, text="Open Camera", command=self.update,
      foreground="#ffffff", background="#3e3e42"
    )
    self.open_camera_button.place(x=8, y=10)

    self.load_image_button: tk.Button = tk.Button(
      self.root, text="Load image", command=self.load_image,
      background="#3e3e42", foreground="#ffffff"
    )
    self.load_image_button.place(x=100, y=10)
    
    self.root.bind("<Key>", self.key_handler)
    self.root.mainloop()

  def update(self) -> None:
    if self.input_display_label.show_webcam(self.cap):
      self.input_display_label.after(5, self.update)
  
  def load_image(self):
    path: str = askopenfilename(title="Open image file")
    
    self.input_display_label.show_image(path)
  
  def key_handler(self, event) -> None:
    if self.input_display_label.mode == "webcam" and event.keysym == "space":
      print(scan(self.input_display_label.get_webcam_frame(self.cap)))