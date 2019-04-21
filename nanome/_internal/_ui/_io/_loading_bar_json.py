from .. import _LoadingBar
from nanome.util.color import Color

def parse_json(content_json):
    loading_bar = _LoadingBar._create()
    loading_bar._percentage = float(content_json["percentage"])
    loading_bar._title = str(content_json["title"])
    loading_bar._description = str(content_json["description"])
    loading_bar._failure = bool(content_json["failure"])
    return loading_bar

def write_json(loading_bar):
    content_json = {}
    content_json["percentage"] = loading_bar._percentage
    content_json["title"] = loading_bar._title
    content_json["description"] = loading_bar._description
    content_json["failure"] = loading_bar._failure
    return content_json
