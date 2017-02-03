from PIL import Image
import pyocr
import pyocr.builders
import tesserocr
from tesserocr import PyTessBaseAPI, PSM

tools = pyocr.get_available_tools()
if len(tools) == 0:
    raise ("No OCR tool found")

tool = tools[0]
langs = tool.get_available_languages()
lang = langs[0]
builder = pyocr.builders.TextBuilder()

txt = tool.image_to_string(Image.open('/Users/Leslie/GitHub/WeiboFans/1.tif'),
                           lang=lang,
                           builder=builder)
print('text:', txt)


print(tesserocr.get_languages())
print('text:', tesserocr.file_to_text('/Users/Leslie/GitHub/WeiboFans/img.jpg'))



# Orientation and script detection (OSD):
from PIL import Image
from tesserocr import PyTessBaseAPI, PSM

with PyTessBaseAPI(psm=PSM.AUTO_OSD) as api:
    image = Image.open("/Users/Leslie/GitHub/WeiboFans/1.tif")
    api.SetImage(image)
    api.Recognize()

    it = api.AnalyseLayout()
    orientation, direction, order, deskew_angle = it.Orientation()
    print("Orientation: {:d}".format(orientation))
    print("WritingDirection: {:d}".format(direction))
    print("TextlineOrder: {:d}".format(order))
    print("Deskew angle: {:.4f}".format(deskew_angle))