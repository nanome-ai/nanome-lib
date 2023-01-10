from .. import _Image


def parse_json(content_json):
    from nanome.util import enums
    image = _Image._create()
    image._color = content_json.read("color", image._color)
    image._file_path = content_json.read("file_path", image._file_path)
    image._scaling_option = enums.ScalingOptions(content_json.read("scaling_option", image._scaling_option))
    return image


def write_json(helper, image):
    helper.write("color", image._color._color)
    helper.write("file_path", image._file_path)
    helper.write("scaling_option", image._scaling_option)
