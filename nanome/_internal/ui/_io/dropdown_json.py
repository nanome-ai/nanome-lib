from .. import _Dropdown
from .. import _DropdownItem


def parse_json(content_json):
    dropdown = _Dropdown._create()
    dropdown._use_permanent_title = content_json.read("use_permanent_title", dropdown._use_permanent_title)
    dropdown._permanent_title = content_json.read("permanent_title", dropdown._permanent_title)
    dropdown._max_displayed_items = content_json.read("max_displayed_items", dropdown._max_displayed_items)
    item_list = content_json.read_objects("items")
    for item_obj in item_list:
        dropdown._items.append(_parse_item(item_obj))
    dropdown._unusable = content_json.read("unusable", dropdown._unusable)
    return dropdown


def write_json(helper, dropdown):
    helper.write("use_permanent_title", dropdown._use_permanent_title)
    helper.write("permanent_title", dropdown._permanent_title)
    helper.write("max_displayed_items", dropdown._max_displayed_items)
    items = []
    for item in dropdown._items:
        c_helper = helper.make_instance()
        _write_item(c_helper, item)
        items.append(c_helper.get_dict())
    helper.write("unusable", dropdown._unusable)


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
