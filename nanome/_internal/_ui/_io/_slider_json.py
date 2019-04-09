from .. import _Slider

def parse_json(content_json):
    slider = _Slider._create()
    slider._current_value = float(content_json["current_value"])
    slider._min_value = float(content_json["min_value"])
    slider._max_value = float(content_json["max_value"])
    return slider

def write_json(slider):
    content_json = {}
    content_json["current_value"] = slider._current_value
    content_json["min_value"] = slider._min_value
    content_json["max_value"] = slider._max_value
    return content_json
