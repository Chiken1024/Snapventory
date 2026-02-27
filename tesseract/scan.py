import PIL, pytesseract, re

from opencv.process_image import process_image

def scan(frame) -> str:
  edited_image = process_image(frame)
  image: PIL.Image.Image = PIL.Image.fromarray(edited_image)
  prices: list[float] = list(
    map(float, re.findall("[0-9]+[.][0-9]+", pytesseract.image_to_string(image)))
  )
  if prices != []: return prices
  else: return "Failed to read text"