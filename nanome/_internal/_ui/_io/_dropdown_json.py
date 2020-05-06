from .. import _Dropdown
from .. import _DropdownItem

def parse_json(content_json):
    dropdown = _Dropdown._create()
    dropdown._use_permanent_title = content_json.read("use_permanent_title", dropdown._use_permanent_title)
    dropdown._permanent_title = content_json.read("permanent_title", dropdown._permanent_title)
    dropdown._max_displayed_items = content_json.read("max_displayed_items", dropdown._max_displayed_items)
    dropdown._items = content_json.read("items", dropdown._items)
    return dropdown

def write_json(helper, dropdown):
    helper.write("use_permanent_title", dropdown._use_permanent_title)
    helper.write("permanent_title", dropdown._permanent_title)
    helper.write("max_displayed_items", dropdown._max_displayed_items)
    helper.write("items", dropdown._Items)

def _parse_item(content_json):
    item = _DropdownItem._create()
    item._name = content_json.read("name", item._name)
    item._close_on_selected = content_json.read("close_on_selected", item._close_on_selected)
    item._selected = content_json.read("selected", item._selected)
    return item

def _write_item(helper, item):
    helper.write("name", item._name)
    helper.write("close_on_selected", item._close_on_selected)
    helper.write("selected", item._selected)