from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    raise ("No OCR tool found")

tool = tools[0]

langs = tool.get_available_languages()
lang = langs[0]

builder = pyocr.builders.TextBuilder()


txt = tool.image_to_string(Image.open('/Users/Leslie/GitHub/WeiboFans/1.png'),
                           lang=lang,
                           builder=builder)


# Digits - Only Tesseract (not 'libtesseract' yet !)
digits = tool.image_to_string(
    Image.open('test-digits.png'),
    lang=lang,
    builder=pyocr.tesseract.DigitBuilder()
)


if tool.can_detect_orientation():
    try:
        orientation = tool.detect_orientation(
            Image.open('/Users/Leslie/GitHub/WeiboFans/1.png'),
            lang='fra'
        )
        print("Orientation: {}".format(orientation))
    except pyocr.PyocrException as exc:
        print("Orientation detection failed: {}".format(exc))