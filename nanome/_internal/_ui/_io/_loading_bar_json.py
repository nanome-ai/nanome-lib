from .. import _LoadingBar
from nanome.util.color import Color

def parse_json(content_json):
    loading_bar = _LoadingBar._create()
    loading_bar._percentage = content_json.read("percentage", 0.0)
    loading_bar._title = content_json.read("title", "")
    loading_bar._description = content_json.read("description", "")
    loading_bar._failure = content_json.read("failure", False)
    return loading_bar

def write_json(helper, loading_bar):
    helper.write("percentage", loading_bar._percentage)
    helper.write("title", loading_bar._title)
    helper.write("description", loading_bar._description)
    helper.write("failure", loading_bar._failure)
