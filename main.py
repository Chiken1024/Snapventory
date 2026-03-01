from cv2 import VideoCapture

from interface.gui import GUI
from database.database import DatabaseConnection

cap: VideoCapture = VideoCapture(1)
db: DatabaseConnection = DatabaseConnection("data.db")
gui: GUI = GUI(cap, db)
cap.release()
db.close()