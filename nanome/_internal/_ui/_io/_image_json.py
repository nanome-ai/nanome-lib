from .. import _Image
from nanome.util.color import Color
from nanome.util.image_settings import ScalingOptions

def parse_json(content_json):
    image = _Image._create()
    image._color = Color.from_int(int(float((content_json["color"]))))
    image._file_path = str(content_json["file_path"])
    if ("scaling_option" in content_json):
        image._scaling_option = ScalingOptions(int(float(content_json["scaling_option"])))
    return image

def write_json(image):
    content_json = {}
    content_json["color"] = image._color._color
    content_json["file_path"] = image._file_path
    content_json["scaling_option"] = image._scaling_option
    return content_json
