from .. import _UIList
from nanome.util.color import Color

def parse_json(content_json):
    list = _UIList._create()
    list._display_columns = int(float(content_json["display_columns"]))
    list._display_rows = int(float(content_json["display_rows"]))
    list._total_columns = int(float(content_json["total_columns"]))
    list._unusable = bool(content_json["unusable"])
    return list

def write_json(list):
    content_json = {}
    content_json["display_columns"] = list._display_columns
    content_json["display_rows"] = list._display_rows
    content_json["total_columns"] = list._total_columns
    content_json["unusable"] = list._unusable
    return content_json
