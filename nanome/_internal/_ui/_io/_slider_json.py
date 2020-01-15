from .. import _Slider

def parse_json(content_json):
    slider = _Slider._create()
    slider._current_value = float(content_json["current_value"])
    slider._min_value = float(content_json["min_value"])
    slider._max_value = float(content_json["max_value"])
    return slider

def write_json(helper, slider):
    helper.write("current_value", slider._current_value)
    helper.write("min_value", slider._min_value)
    helper.write("max_value", slider._max_value)
