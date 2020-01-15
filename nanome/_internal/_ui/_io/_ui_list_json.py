from .. import _UIList
from nanome.util.color import Color

def parse_json(content_json):
    list = _UIList._create()
    list._display_columns = content_json.read("display_columns", 0)
    list._display_rows = content_json.read("display_rows", 0)
    list._total_columns = content_json.read("total_columns", 0)
    list._unusable = content_json.read("unusable", False)
    return list

def write_json(helper, list):
    helper.write("display_columns", list._display_columns)
    helper.write("display_rows", list._display_rows)
    helper.write("total_columns", list._total_columns)
    helper.write("unusable", list._unusable)
