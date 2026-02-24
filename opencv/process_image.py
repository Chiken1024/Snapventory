import cv2 as cv

def process_image(image: cv.Mat) -> cv.Mat:
  return cv.GaussianBlur(cv.cvtColor(image, cv.COLOR_BGR2GRAY), (3, 3), .0)