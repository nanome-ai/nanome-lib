from . import *

# classes
from .ui_base import UIBase
from .mesh import Mesh
from .image import Image
from .loading_bar import LoadingBar
from .label import Label
from .text_input import TextInput
from .slider import Slider
from .button import Button
from .dropdown import Dropdown
from .dropdown_item import DropdownItem
from .ui_list import UIList

from .layout_node import LayoutNode
from .menu import Menu
from . import serializers
# folders
from . import io, messages, callbacks

from nanome._internal.enums import Commands, Messages
from nanome.util import simple_callbacks

registered_commands = [
    (Commands.menu_toggle, messages.MenuCallback(), callbacks.menu_toggled),
    (Commands.button_press, messages.ButtonCallback(), callbacks.button_pressed),
    (Commands.button_hover, messages.ButtonCallback(), callbacks.button_hover),
    (Commands.slider_release, messages.SliderCallback(), callbacks.slider_released),
    (Commands.slider_change, messages.SliderCallback(), callbacks.slider_changed),
    (Commands.text_submit, messages.TextInputCallback(), callbacks.text_submit),
    (Commands.text_change, messages.TextInputCallback(), callbacks.text_changed),
    (Commands.image_press, messages.ImageCallback(), callbacks.image_pressed),
    (Commands.image_hold, messages.ImageCallback(), callbacks.image_held),
    (Commands.image_release, messages.ImageCallback(), callbacks.image_released),
    (Commands.dropdown_item_click, messages.DropdownCallback(), callbacks.dropdown_item_clicked),
    (Commands.menu_transform_response, messages.GetMenuTransformResponse(), simple_callbacks.simple_callback_arg_unpack),
]

registered_messages = [
    (Messages.menu_update, messages.UpdateMenu()),
    (Messages.content_update, messages.UpdateContent()),
    (Messages.node_update, messages.UpdateNode()),
    (Messages.menu_transform_set, messages.SetMenuTransform()),
    (Messages.menu_transform_request, messages.GetMenuTransform()),
    (Messages.notification_send, messages.SendNotification()),
    (Messages.hook_ui_callback, messages.UIHook()),
]
