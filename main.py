from opencv import camera
from tesseract.scan import scan

print("""
OpenCV text scanner
Controls: 'ESC' to quit, 's' to scan
""")

cap = camera.get_capture()

while True:
  frame, key = camera.get_data(cap)
  
  if key == 27: break
  elif key == ord("s"): print(scan(frame))

camera.end_capture(cap)