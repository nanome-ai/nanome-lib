from .. import _Image
from nanome.util.color import Color

def parse_json(content_json):
    image = _Image._create()
    image._color = Color.from_int(int(float((content_json["color"]))))
    image._file_path = str(["file_path"])
    return image

def write_json(image):
    content_json = {}
    content_json["color"] = image._color._color
    content_json["file_path"] = image._file_path
    return content_json
