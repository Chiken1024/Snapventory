import pytesseract, re

from opencv.segment_image import segment_image

CONFIG: str = r"--oem 3 --psm 6"

def scan(frame) -> str:
  segmented_image = segment_image(frame)
  
  frame_text: str = pytesseract.image_to_string(frame, config=CONFIG)
  segmented_text: str = pytesseract.image_to_string(segmented_image, config=CONFIG)

  text: str = ""

  if len(segmented_text) > len(frame_text):
    text = segmented_text
  else: text = frame_text

  prices: list[float] = list(
    map(float, re.findall("[0-9]+[.][0-9]{2}", text))
  )
  if prices != []: return "Price: " + str(max(prices)) + "\nItems:\n"
  else: return "Failed to read text"