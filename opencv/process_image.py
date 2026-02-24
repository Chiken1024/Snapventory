import cv2 as cv
from PIL import ImageTk, Image

def process_image(image: cv.Mat) -> cv.Mat:
  return cv.GaussianBlur(cv.cvtColor(image, cv.COLOR_BGR2GRAY), (1, 1), .0)

def to_imagetk(image: cv.Mat) -> ImageTk.PhotoImage:
  return ImageTk.PhotoImage(
    Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))
  )