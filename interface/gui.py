import tkinter as tk

from interface.webcam import Webcam
from tesseract.scan import scan

class GUI:
  def __init__(self, cap) -> None:
    self.cap = cap
    
    self.root: tk.Tk = tk.Tk("Snapventory")
    self.root.geometry("660x535")
    self.root.configure(background="#1e1e1e")

    self.webcam_label: Webcam = Webcam(self.root, "#ffffff")
    self.webcam_label.pack(pady=10)

    self.open_camera_button: tk.Button = tk.Button(
      self.root, text="Open Camera", background="#3e3e42", command=self.update
    )
    self.open_camera_button.pack()
    
    def key_handler(event) -> None:
      if event.keysym == "space":
        print(scan(self.webcam_label.get_frame(self.cap)))

    self.root.bind("<Key>", key_handler)

    self.root.mainloop()

  def update(self) -> None:
    if self.webcam_label.show(self.cap):
      self.webcam_label.after(5, self.update)