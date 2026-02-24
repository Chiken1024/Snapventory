import tkinter as tk

from opencv.camera import get_video_capture, get_camera_data, end_video_capture
from opencv.process_image import to_imagetk

root: tk.Tk = tk.Tk("Snapventory")
root.geometry("680x540")
root.configure(background="#1e1e1e")

cap = get_video_capture()

def show_camera() -> None:
  frame, key = get_camera_data(cap)
  
  imagetk = to_imagetk(frame)
  webcam_label.configure(image=imagetk)
  webcam_label.image = imagetk
  webcam_label.update()

  open_camera_button.after(10, show_camera)

open_camera_button: tk.Button = tk.Button(
  root, text="Open Camera", background="#3e3e42", command=show_camera
)
open_camera_button.pack(pady=5)

webcam_label: tk.Label = tk.Label(root)
webcam_label.pack()

root.mainloop()