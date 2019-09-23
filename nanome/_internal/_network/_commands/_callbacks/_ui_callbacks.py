from nanome.util.logs import Logs
from nanome._internal._ui import _Menu

def _menu_toggled(network, arg, request_id):
    enabled = arg
    active_menu = network._plugin.menu
    if active_menu != None:
        active_menu._enabled = enabled
        if enabled == True:
            active_menu._on_opened_callback()
        elif enabled == False:
            active_menu._on_closed_callback()
    else:
        Logs.error("Can't find Menu for callback")

def _slider_released(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = network._plugin.menu._find_content(content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_released()
    else:
        Logs.error("Can't find UI content for callback")

def _slider_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = network._plugin.menu._find_content(content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_changed()
    else:
        Logs.error("Can't find UI content for callback")

def _text_submit(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = network._plugin.menu._find_content(content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_submitted()
    else:
        Logs.error("Can't find UI content for callback")

def _text_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = network._plugin.menu._find_content(content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_changed()
    else:
        Logs.error("Can't find UI content for callback")

def _button_pressed(network, arg, request_id):
    button_id = arg
    btn = network._plugin.menu._find_content(button_id)
    if btn != None:
        btn._on_button_pressed()
    else:
        Logs.error("Can't find UI content for callback")

def _button_hover(network, arg, request_id):
    button_id = arg
    btn = network._plugin.menu._find_content(button_id)
    if btn != None:
        btn._on_button_hover()
    else:
        Logs.error("Can't find UI content for callback")
        
def _image_pressed(network, arg, request_id):
    image_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = network._plugin.menu._find_content(image_id)
    if img != None:
        img._on_image_pressed(x, y)
    else:
        Logs.error("Can't find UI content for callback")

def _image_held(network, arg, request_id):
    image_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = network._plugin.menu._find_content(image_id)
    if img != None:
        img._on_image_held(x, y)
    else:
        Logs.error("Can't find UI content for callback")

def _image_released(network, arg, request_id):
    image_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = network._plugin.menu._find_content(image_id)
    if img != None:
        img._on_image_released(x, y)
    else:
        Logs.error("Can't find UI content for callback")