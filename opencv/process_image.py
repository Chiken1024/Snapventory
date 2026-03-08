import cv2 as cv
import numpy as np
from PIL import ImageTk, Image

def mat_to_photoimage(image: cv.Mat) -> ImageTk.PhotoImage:
  return ImageTk.PhotoImage(
    Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))
  )

def path_to_photoimage(path: str) -> ImageTk.PhotoImage:
  image: Image = Image.open(path)
  image.thumbnail((640, 480))
  return ImageTk.PhotoImage(image)

def path_to_mat(path: str) -> cv.Mat:
  return cv.imread(path)