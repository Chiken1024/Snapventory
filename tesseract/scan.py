import pytesseract, re
import cv2 as cv

from opencv.process_image import process_image
from opencv.segment_image import segment_image

def scan(frame) -> str:
  segmented_image = segment_image(frame)
  cv.imshow("Segmented Image", segmented_image)
  
  frame_text: str = pytesseract.image_to_string(frame)
  segmented_text: str = pytesseract.image_to_string(segmented_image)

  text: str = ""

  if len(segmented_text) > len(frame_text):
    text = segmented_text
  else: text = frame_text

  prices: list[float] = list(
    map(float, re.findall("[0-9]+[.][0-9]{2}", text))
  )
  if prices != []: return "Price: " + str(max(prices)) + "\nItems:\n"
  else: return "Failed to read text"