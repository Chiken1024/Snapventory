import sqlite3

class DatabaseConnection:
  def __init__(self, path: str) -> None:
    try:
      self.connection: sqlite3.Connection = sqlite3.connect(path)
      self.cursor: sqlite3.Cursor = self.connection.cursor()

    except sqlite3.Error as error:
      print(error)
      self.connection.rollback()
  
  def reset(self) -> None:
    open("data.db", "w").close()

    self.cursor.executescript(
"""
CREATE TABLE budget (balance FLOAT);
INSERT INTO budget VALUES (0.0);

CREATE TABLE inventory (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  UNIQUE(name)
);
"""
    )

    self.connection.commit()

  def update_budget(self, amount: float) -> None:
    try:
      self.cursor.execute("UPDATE budget SET balance = balance + ?", (amount,))
      
      self.connection.commit()
    except:
      print("Failed to update budget: incorrect format")

  def add(self, name: str, quantity: int) -> None:
    try:
      self.cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?) ON CONFLICT (name) DO UPDATE SET quantity = quantity + excluded.quantity", (name, quantity))
      self.connection.commit()

      self.cursor.execute("SELECT * FROM inventory")
      self.cursor.fetchall()
    except:
      print("Failed to pass item(s) into database: incorrect format, or id overlap")
  
  def remove(self, name: str, quantity: int) -> None:
    try:
      self.cursor.execute("UPDATE inventory SET quantity = MAX(quantity - ?, 0) WHERE name = ?", (quantity, name))
      self.cursor.execute("DELETE FROM inventory WHERE quantity = 0")
      self.connection.commit()

      self.cursor.execute("SELECT * FROM inventory")
      self.cursor.fetchall()
    except:
      print("Failed to remove item(s) from database: Incorrect format, item doesn't exist")

  def get(self) -> tuple[float, list]:
    self.cursor.execute("SELECT * FROM budget")
    budget = self.cursor.fetchall()[0]
    self.cursor.execute("SELECT * FROM inventory")
    return budget, self.cursor.fetchall()

  def close(self) -> None: self.connection.close()

#DatabaseConnection("data.db").reset()