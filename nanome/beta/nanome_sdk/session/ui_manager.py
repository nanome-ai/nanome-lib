import asyncio
import functools
import inspect
import logging

from nanome.api import ui
from nanome.api._hashes import Hashes
from collections import defaultdict
from nanome._internal.enums import Commands

logger = logging.getLogger(__name__)

__all__ = ["UIManager"]


class UIManager:

    def __init__(self):
        self.callbacks = defaultdict(dict)
        self._menus = []
        self.__hash_cache = {}

    def __new__(cls):
        # Create Singleton object
        if not hasattr(cls, 'instance'):
            cls.instance = super(UIManager, cls).__new__(cls)
        return cls.instance

    def create_new_menu(self, json_path=None):
        if json_path:
            menu = ui.Menu.io.from_json(json_path)
        else:
            menu = ui.Menu()
        self._menus.append(menu)
        return menu

    def register_btn_pressed_callback(self, btn: ui.Button, callback_fn):
        # hook_ui_callback = Messages.hook_ui_callback
        ui_hook = Commands.button_press
        content_id = btn._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    def register_slider_change_callback(self, sld: ui.Slider, callback_fn):
        ui_hook = Commands.slider_change
        content_id = sld._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    def register_slider_released_callback(self, sld: ui.Slider, callback_fn):
        ui_hook = Commands.slider_release
        content_id = sld._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    def register_dropdown_item_clicked_callback(self, dd: ui.Dropdown, callback_fn):
        ui_hook = Commands.dropdown_item_click
        content_id = dd._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    def register_text_change_callback(self, textinput: ui.TextInput, callback_fn):
        ui_hook = Commands.text_change
        content_id = textinput._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    def register_text_submit_callback(self, textinput: ui.TextInput, callback_fn):
        ui_hook = Commands.text_submit
        content_id = textinput._content_id
        self.callbacks[content_id][ui_hook] = callback_fn

    async def handle_ui_command(self, command, received_obj_list):
        content_id, val = received_obj_list
        menu_content = self.__find_content(content_id)
        if not menu_content:
            logger.warning(f"No callback registered for button {content_id}")
            return

        # Handle different command types
        if command == Commands.button_press:
            btn = menu_content
            if btn._toggle_on_press:
                btn._selected = val
        elif command in [Commands.slider_change, Commands.slider_release]:
            sld = menu_content
            sld.current_value = val
        elif command in [Commands.text_change, Commands.text_submit]:
            textinput = menu_content
            textinput.input_text = val
        elif command == Commands.dropdown_item_click:
            dd = menu_content
            clicked_item_index = val
            for i, item in enumerate(dd._items):
                item._selected = i == clicked_item_index
        else:
            logger.debug('huh?')

        callback_fn = self.callbacks[content_id].get(command)
        is_async_fn = inspect.iscoroutinefunction(callback_fn)
        is_async_partial = isinstance(callback_fn, functools.partial) and \
            inspect.iscoroutinefunction(callback_fn.func)

        if is_async_fn or is_async_partial:
            # await callback_fn(menu_content)
            asyncio.create_task(callback_fn(menu_content))
        elif callback_fn:
            callback_fn(menu_content)
        else:
            # no callback registered
            logger.debug(f"No callback registered for content {content_id}")

    def __find_content(self, content_id):
        content = None
        for menu in self._menus:
            content = menu.find_content(content_id)
            if content:
                break
        return content

    def find_command(self, command_hash):
        if command_hash in self.__hash_cache:
            return self.__hash_cache[command_hash]
        # Look up hash in registered commands, and save to cache
        cmds = [tup[0] for tup in ui.registered_commands]
        command = None
        for cmd in cmds:
            if Hashes.hash_command(cmd.name) == command_hash:
                command = cmd
                self.__hash_cache[command_hash] = command
                break
        return command
