import cv2 as cv

def get_video_capture() -> cv.VideoCapture: return cv.VideoCapture(0)

def get_camera_data(cap: cv.VideoCapture) -> tuple[cv.Mat, int]:
  ret, frame = cap.read()
  
  if ret: return frame, cv.waitKey(10)
  else:
    print("Camera quit unexpectedly")
    return frame, 27

def end_video_capture(cap: cv.VideoCapture) -> None:
  cap.release()
  cv.destroyAllWindows()