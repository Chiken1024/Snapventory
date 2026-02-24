from opencv.camera import get_video_capture, get_camera_data, end_video_capture
from tesseract.scan import scan

print("""
OpenCV text scanner
Controls: 'ESC' to quit, 's' to scan
""")

cap = get_video_capture()

while True:
  frame, key = get_camera_data(cap)
  
  if key == 27: break
  elif key == ord("s"): print(scan(frame))

end_video_capture(cap)