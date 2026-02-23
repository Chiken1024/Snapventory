import cv2 as cv
import pytesseract
import PIL

def scan(frame: cv.Mat) -> str:
  edited_image: cv.Mat = cv.GaussianBlur(
    cv.cvtColor(frame, cv.COLOR_BGR2GRAY), (3, 3), .0
  )
  image: PIL.Image.Image = PIL.Image.fromarray(edited_image)
  return pytesseract.image_to_string(image)

cap: cv.VideoCapture = cv.VideoCapture(0)

print("""
OpenCV text scanner
Controls: 'ESC' to quit, 's' to scan
""")

while True:
  ret, frame = cap.read()
  
  if ret:
    cv.imshow("Webcam", frame)
    key: int = cv.waitKey(10)
    if key == ord("s"): print(scan(frame))
    elif key == 27: break
  else: break

cap.release()
cv.destroyAllWindows()