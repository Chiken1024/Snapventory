import cv2 as cv

def get_capture() -> cv.VideoCapture: return cv.VideoCapture(0)

def get_data(cap: cv.VideoCapture) -> tuple[cv.Mat, int]:
  ret, frame = cap.read()
  
  if ret:
    cv.imshow("Webcam", frame)
    return frame, cv.waitKey(10)
  else:
    print("Camera quit unexpectedly")
    return frame, 27

def end_capture(cap: cv.VideoCapture) -> None:
  cap.release()
  cv.destroyAllWindows()