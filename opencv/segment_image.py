import cv2 as cv
import numpy as np
from skimage.filters import threshold_local

def opencv_resize(image: cv.Mat, ratio: float) -> cv.Mat:
  return cv.resize(
    image, (int(image.shape[1] * ratio), int(image.shape[0] * ratio)),
    interpolation=cv.INTER_AREA
  )

def approximate_contour(contour: cv.Mat) -> cv.Mat:
  peri: float = cv.arcLength(contour, True)
  return cv.approxPolyDP(contour, .032 * peri, True)

def get_receipt_contour(contours: list[cv.Mat]) -> cv.Mat:
  for c in contours:
    approx: cv.Mat = approximate_contour(c)
    if len(approx) == 4: return approx

def contour_to_rect(contour: cv.Mat, resize_ratio: float):
  pts = contour.reshape(4, 2)
  rect = np.zeros((4, 2), dtype="float32")

  s = pts.sum(axis=1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]

  diff = np.diff(pts, axis=1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  return rect / resize_ratio

def wrap_perspective(image: cv.Mat, rect):
  (tl, tr, br, bl) = rect
  
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

  maxWidth: int = max(int(widthA), int(widthB))
  maxHeight: int = max(int(heightA), int(heightB))

  dst = np.array(
    [
      [0, 0], [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]
    ], dtype="float32"
  )

  M = cv.getPerspectiveTransform(rect, dst)

  return cv.warpPerspective(image, M, (maxWidth, maxHeight))

def bw_scanner(image):
  gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  T = threshold_local(gray, 21, offset=5, method="gaussian")
  return (gray > T).astype("uint8") * 255

def segment_image(mat: cv.Mat) -> cv.Mat | bool:
  original: cv.Mat = mat.copy()
  
  resize_ratio: float = 500. / mat.shape[0]
  
  image: cv.Mat = opencv_resize(mat, resize_ratio)
  grayscale: cv.Mat = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  blurred: cv.Mat = cv.GaussianBlur(grayscale, (5, 5), 0.)

  rect_kernel: cv.Mat = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
  dilated: cv.Mat = cv.dilate(blurred, rect_kernel)
  edged: cv.Mat = cv.Canny(dilated, 100., 200., apertureSize=3)

  contours, _ = cv.findContours(
    edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
  )
  largest_contours: list[cv.Mat] = sorted(
    contours, key=cv.contourArea, reverse=True
  )[:10]
  receipt_contour: cv.Mat | None = get_receipt_contour(largest_contours)

  try:
    scanned: cv.Mat = wrap_perspective(
      original.copy(), contour_to_rect(receipt_contour, resize_ratio)
    )

    return scanned
  except: return original