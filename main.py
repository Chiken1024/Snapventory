from cv2 import VideoCapture

from interface.gui import GUI

print("""
OpenCV text scanner
Controls: SPACE to scan
""")

cap: VideoCapture = VideoCapture(0)

gui: GUI = GUI(cap)

gui.update()

cap.release()