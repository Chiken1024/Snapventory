import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from interface.input_display import InputDisplay
from tesseract.scan import scan
from opencv.process_image import path_to_mat
from database.database import DatabaseConnection

class GUI:
  def __init__(self, cap, db: DatabaseConnection) -> None:
    self.db: DatabaseConnection = db
    
    self.root: tk.Tk = tk.Tk()
    self.root.title("Snapventory")
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
    self.output_text.insert(tk.END, "Price: \nItems:\n")

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
  
  def save_to_inventory(self) -> None:
    text: list[str] = self.output_text.get("1.0", tk.END).split("\n")
    while "" in text: text.remove("")

    price: float = float(text[0].split(" ")[-1])
    
    self.db.update_budget(-price)

    for item in text[2:]:
      name: str = " ".join(item.split(" ")[1:])
      quantity: int = item.split("x")[0]
      self.db.add(name, quantity)

  def edit_inventory(self) -> None:
    self.inventory: tk.Tk = tk.Tk()
    self.inventory.title("Edit Inventory")
    self.inventory.geometry("258x248")
    self.inventory.wm_minsize(258, 248)
    self.inventory.wm_maxsize(258, 248)
    self.inventory.configure(background="#252526")

    self.inventory.protocol("WM_DELETE_WINDOW", self.callback)

    self.create_inventory_interface()

  def callback(self) -> None:
    if self.saved == False: 
      if messagebox.askokcancel("Unsaved changes", "You have unsaved changes. Quit?"):
        self.inventory.destroy()
    else: self.inventory.destroy()

  def create_inventory_interface(self) -> None:
    self.saved: bool = True
    
    self.inventory_toolbar_frame: tk.Frame = tk.Frame(
      self.inventory, width=250, height=34,
      background="#3e3e42"
    )
    self.inventory_toolbar_frame.place(x=4, y=4)

    self.clear_inventory_button: tk.Button = tk.Button(
      self.inventory_toolbar_frame, text="Clear Inventory",
      command=self.clear_inventory, background="#3e3e42", foreground="#ffffff"
    )
    self.clear_inventory_button.place(x=4, y=4)

    self.budget_label: tk.Label = tk.Label(
      self.inventory_toolbar_frame, text=f"€{self.db.get()[0][0]:.2f}",
      width=8, relief="raised", background="#2d2d30", foreground="#ffffff"
    )
    self.budget_label.place(x=98, y=6)

    self.save_changes_button: tk.Button = tk.Button(
      self.inventory_toolbar_frame, text="Save Changes",
      command=self.save_changes, background="#4f4f54", foreground="#ffffff"
    )
    self.save_changes_button.place(x=163, y=4)
    
    self.inventory_frame: tk.Frame = tk.Frame(
      self.inventory, width=250, height=202, background="#3e3e42"
    )
    self.inventory_frame.place(x=4, y=42)
    
    self.inventory_listbox: tk.Listbox = tk.Listbox(
      self.inventory_frame, width=20, height=12, borderwidth=0,
      background="#2d2d30", foreground="#ffffff"
    )
    self.inventory_listbox.place(x=4, y=4)

    self.modify_amount_frame: tk.Frame = tk.Frame(
      self.inventory_frame, width=116, height=58, background="#4f4f54"
    )
    self.modify_amount_frame.place(x=131, y=4)

    self.modify_amount_button: tk.Button = tk.Button(
      self.modify_amount_frame, text="Modify Amount By:", width=14,
      command=self.modify_amount, background="#3e3e42", foreground="#ffffff"
    )
    self.modify_amount_button.place(x=4, y=4)

    self.modify_amount_spinbox: tk.Spinbox = tk.Spinbox(
      self.modify_amount_frame, from_=-256., to=256., buttonbackground="#4f4f54",
      width=15, background="#3e3e42", foreground="#ffffff"
    )
    self.modify_amount_spinbox.delete(0, tk.END)
    self.modify_amount_spinbox.insert(0, 0)
    self.modify_amount_spinbox.place(x=6, y=34)

    self.remove_item_button: tk.Button = tk.Button(
      self.inventory_frame, text="Remove Item", width=14,
      command=self.remove_item, background="#3e3e42", foreground="#ffffff"
    )
    self.remove_item_button.place(x=135, y=67)

    self.modify_budget_frame: tk.Frame = tk.Frame(
      self.inventory_frame, width=116, height=58, background="#4f4f54"
    )
    self.modify_budget_frame.place(x=131, y=103)

    tk.Label(
      self.modify_budget_frame, text="Edit Budget",
      background="#3e3e42", foreground="#ffffff"
    ).place(x=4, y=4)

    self.modify_budget_button: tk.Button = tk.Button(
      self.modify_budget_frame, text="Add", command=self.modify_budget,
      width=3, background="#3e3e42", foreground="#ffffff"
    )
    self.modify_budget_button.place(x=82, y=4)

    self.set_budget_button: tk.Button = tk.Button(
      self.modify_budget_frame, text="Set", command=self.set_budget,
      width=3, background="#3e3e42", foreground="#ffffff"
    )
    self.set_budget_button.place(x=82, y=29)

    self.modify_budget_entry: tk.Entry = tk.Entry(
      self.modify_budget_frame, width=7,
      background="#3e3e42", foreground="#ffffff"
    )
    self.modify_budget_entry.insert(0, "0.00")
    self.modify_budget_entry.place(x=4, y=29)

    self.undo_changes_button: tk.Button = tk.Button(
      self.inventory_frame, text="Undo Changes", width=14,
      command=self.undo_changes, background="#3e3e42", foreground="#ffffff"
    )
    self.undo_changes_button.place(x=135, y=172)

    for (_, name, quantity) in self.db.get()[1]:
      self.inventory_listbox.insert(tk.END, f"{quantity}x {name}")

  def clear_inventory(self) -> None:
    self.inventory_listbox.delete(0, tk.END)

    self.saved = False

  def save_changes(self) -> None:
    budget: float = self.db.get()[0][0]
    self.db.reset()
    self.db.update_budget(budget)
    
    for item in self.inventory_listbox.get(0, tk.END):
      name: str = " ".join(item.split(" ")[1:])
      quantity: int = item.split("x")[0]
      self.db.add(name, quantity)
    
    self.saved = True

  def modify_amount(self) -> None:
    selected_index: int = self.inventory_listbox.curselection()
    amount: int = int(self.modify_amount_spinbox.get())
    
    if selected_index != () and amount != 0:
      selected_index = selected_index[0]

      item: str = self.inventory_listbox.get(selected_index)
      original_amount: int = int(item.split("x")[0])
      
      self.inventory_listbox.delete(selected_index)
      if original_amount > -amount:
        modified_item: str = f"{original_amount + amount}x{"".join(item.split("x")[1:])}"
        self.inventory_listbox.insert(selected_index, modified_item)
    
      self.saved = False

  def remove_item(self) -> None:
    selected_index: int = self.inventory_listbox.curselection()
    if selected_index != ():
      self.inventory_listbox.delete(selected_index)
      
      self.saved = False

  def modify_budget(self) -> None:
    budget_orig: float = float(self.budget_label.cget("text")[1:])
    amount: float = float(self.modify_budget_entry.get())
    print(budget_orig, amount)
    self.budget_label.configure(text=f"€{(budget_orig + amount):.2f}")

    self.saved = False

  def set_budget(self) -> None:
    amount: float = float(self.modify_budget_entry.get())
    self.budget_label.configure(text=f"€{amount:.2f}")

    self.saved = False

  def undo_changes(self) -> None:
    self.inventory_listbox.delete(0, tk.END)
    db: tuple[float, list] = self.db.get()
    
    items: list[str] = db[1][::-1]
    for item in items: self.inventory_listbox.insert(0, f"{item[2]}x {item[1]}")

    self.budget_label.configure(text=db[0])

    self.saved = True

  def key_handler(self, event) -> None:
    if self.input_display_label.mode == "webcam" and event.keysym == "space":
      self.output_text.delete("1.0", tk.END)
      self.output_text.insert(
        tk.END, scan(self.input_display_label.get_webcam_frame())
      )