import PIL, pytesseract

from opencv.process_image import process_image

def scan(frame) -> str:
  edited_image = process_image(frame)
  image: PIL.Image.Image = PIL.Image.fromarray(edited_image)
  return pytesseract.image_to_string(image)