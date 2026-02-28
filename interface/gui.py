import tkinter as tk
from tkinter.filedialog import askopenfilename

from interface.input_display import InputDisplay
from tesseract.scan import scan
from opencv.process_image import path_to_mat
from database.database import DatabaseConnection

class GUI:
  def __init__(self, cap, db: DatabaseConnection) -> None:
    self.db: DatabaseConnection = db
    
    self.root: tk.Tk = tk.Tk("Snapventory")
    self.root.geometry("651x644")
    self.root.wm_minsize(651, 644)
    self.root.wm_maxsize(651, 644)
    self.root.configure(background="#252526")

    self.create_interface(cap)
    
    self.root.bind("<Key>", self.key_handler)
    self.root.mainloop()

  def create_interface(self, cap) -> None:
    self.input_display_label: InputDisplay = InputDisplay(
      cap, self.root, "#2d2d30"
    )
    self.input_display_label.place(x=4, y=42)
    
    self.toolbar_frame: tk.Frame = tk.Frame(
      self.root, width=643, height=34, background="#3e3e42"
    )
    self.toolbar_frame.place(x=4, y=4)

    self.open_camera_button: tk.Button = tk.Button(
      self.toolbar_frame, text="Open Camera", command=self.start_webcam,
      foreground="#ffffff", background="#3e3e42"
    )
    self.open_camera_button.place(x=4, y=4)

    self.load_image_button: tk.Button = tk.Button(
      self.toolbar_frame, text="Load Image", command=self.load_image,
      background="#3e3e42", foreground="#ffffff"
    )
    self.load_image_button.place(x=92, y=4)

    self.scan_image_button: tk.Button = tk.Button(
      self.toolbar_frame, text="Scan Image", command=self.scan_image,
      background="#4f4f54", foreground="#ffffff"
    )

    self.cancel_button: tk.Button = tk.Button(
      self.toolbar_frame, text="Cancel",
      command=self.cancel,
      background="#3e3e42", foreground="#ffffff"
    )
    self.cancel_button.place(x=593, y=4)

    self.output_frame: tk.Frame = tk.Frame(
      self.root, width=643, height=108, background="#3e3e42"
    )
    self.output_frame.place(x=4, y=532)

    self.output_text: tk.Text = tk.Text(
      self.output_frame, relief="sunken", width=79, height=6,
      background="#2d2d30", foreground="#ffffff"
    )
    self.output_text.place(x=4, y=4)
    self.output_text.insert(tk.END, "[Press space to scan webcam]")

    self.save_button: tk.Button = tk.Button(
      self.output_frame, text="Save to Inventory", width=13,
      command=self.save_to_inventory,
      background="#4f4f54", foreground="#ffffff"
    )
    self.save_button.place(x=534, y=10)

    self.edit_inventory_button: tk.Button = tk.Button(
      self.output_frame, text="Edit Inventory", width=13,
      command=self.edit_inventory,
      background="#3e3e42", foreground="#ffffff"
    )
    self.edit_inventory_button.place(x=534, y=41)

  def start_webcam(self) -> None:
    self.input_display_label.mode = "webcam"
    self.load_image_button.configure(relief="raised")
    self.scan_image_button.place_forget()
    self.webcam_loop()

  def webcam_loop(self) -> None:
    if self.input_display_label.mode == "webcam" and self.input_display_label.show():
      self.input_display_label.after(5, self.webcam_loop)
  
  def load_image(self) -> None:
    self.input_display_label.mode = "file"
    
    path: str = askopenfilename(title="Open image file")
    
    if path != "":
      self.load_image_button.configure(relief="sunken")
      self.scan_image_button.place(x=164, y=4)
      self.input_display_label.show(path)
  
  def scan_image(self) -> None:
    self.output_text.delete("1.0", tk.END)
    self.output_text.insert(
      tk.END, scan(path_to_mat(self.input_display_label.path))
    )
  
  def cancel(self) -> None:
    self.output_text.delete("1.0", tk.END)
    self.load_image_button.configure(relief="raised")
    self.scan_image_button.place_forget()
    self.input_display_label.cancel()
  
  def save_to_inventory(self):
    text: str = self.output_text.get("1.0", tk.END).split("\n")
    text.pop()

    price: float = float(text[0].split(" ")[-1])
    
    self.db.update_budget(-price)

    for item in text[2:]:
      name: str = " ".join(item.split(" ")[1:])
      quantity: int = item.split("x")[0]
      self.db.add(name, quantity)

    self.db.display()

  def edit_inventory(self) -> None:
    print("Edit inventory")

  def key_handler(self, event) -> None:
    if self.input_display_label.mode == "webcam" and event.keysym == "space":
      self.output_text.delete("1.0", tk.END)
      self.output_text.insert(
        tk.END, scan(self.input_display_label.get_webcam_frame())
      )