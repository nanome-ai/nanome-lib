from nanome.util.logs import Logs
from nanome._internal._ui import _Menu


def __find_content(network, content_id):
    for menu in network._plugin._menus.values():
        content = menu._find_content(content_id)
        if content is not None:
            return content
    return None


def _menu_toggled(network, arg, request_id):
    index = arg[0]
    enabled = arg[1]
    active_menu = network._plugin._menus[index]
    if active_menu != None:
        active_menu._enabled = enabled
        if enabled == True:
            active_menu._on_opened_callback()
        elif enabled == False:
            active_menu._on_closed_callback()
    else:
        Logs.warning("Can't find Menu for callback")


def _slider_released(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_released()
    else:
        Logs.warning("Can't find UI content for callback")


def _slider_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_changed()
    else:
        Logs.warning("Can't find UI content for callback")


def _text_submit(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_submitted()
    else:
        Logs.warning("Can't find UI content for callback")


def _text_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_changed()
    else:
        Logs.warning("Can't find UI content for callback")


def _button_pressed(network, arg, request_id):
    content_id = arg[0]
    btn = __find_content(network, content_id)
    if btn != None:
        if btn._toggle_on_press:
            btn._selected = arg[1]
        btn._on_button_pressed()
    else:
        Logs.warning("Can't find UI content for callback")


def _button_hover(network, arg, request_id):
    content_id = arg[0]
    state = arg[1]
    btn = __find_content(network, content_id)
    if btn != None:
        btn._on_button_hover(state)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_pressed(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_pressed(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_held(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_held(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_released(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_released(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _dropdown_item_clicked(network, arg, request_id):
    content_id = arg[0]
    index = arg[1]
    dropdown = __find_content(network, content_id)

    if dropdown != None:
        for item in dropdown._items:
            item._selected = False
        clickedItem = dropdown._items[index]
        clickedItem._selected = True
        dropdown._on_item_clicked(clickedItem)
    else:
        Logs.warning("Can't find UI content for callback")
