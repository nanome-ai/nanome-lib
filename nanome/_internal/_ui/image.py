import nanome
from . import _UIBase
from nanome.util import Color


class _Image(_UIBase):
    ScalingOptions = nanome.util.enums.ScalingOptions

    @classmethod
    def _create(cls):
        return cls()

    def __init__(self):
        super(_Image, self).__init__()
        self._file_path = ""
        self._color = Color.White()
        self._scaling_option = _Image.ScalingOptions.stretch
        self._pressed_callback = None
        self._held_callback = None
        self._released_callback = None

    def _on_image_pressed(self, x, y):
        if self._pressed_callback != None:
            self._pressed_callback(self, x, y)

    def _on_image_held(self, x, y):
        if self._held_callback != None:
            self._held_callback(self, x, y)

    def _on_image_released(self, x, y):
        if self._released_callback != None:
            self._released_callback(self, x, y)

    def _register_pressed_callback(self, func):
        if func == None and self._pressed_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(nanome._internal._network._commands._serialization._UIHook.Type.image_pressed)
        self._pressed_callback = func

    def _register_held_callback(self, func):
        if func == None and self._held_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(nanome._internal._network._commands._serialization._UIHook.Type.image_held)
        self._held_callback = func

    def _register_released_callback(self, func):
        if func == None and self._released_callback == None:  # Low hanging filter but there may be others
            return
        self._send_hook(nanome._internal._network._commands._serialization._UIHook.Type.image_released)
        self._released_callback = func

    def _send_hook(self, hook_type):
        try:
            nanome._internal._network.PluginNetwork._instance._send(
                nanome._internal._network._commands._callbacks._Messages.hook_ui_callback,
                (hook_type, self._content_id),
                False)
        except:
            nanome.util.Logs.error("Could not register hook")

    def _copy_values_deep(self, other):
        super()._copy_values_deep(other)
        self._color = other._color
        self._scaling_option = other._scaling_option
        self._file_path = other._file_path
        self._pressed_callback = other._pressed_callback
        self._held_callback = other._held_callback
        self._released_callback = other._released_callback
