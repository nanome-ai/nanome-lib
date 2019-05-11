from nanome.util.enums import ControllerType, ControllerButtons, ControllerEvents
from nanome._internal._network._commands._callbacks import _Messages

class _User (object):
    def create(self, plugin_instance):
        pass

    def __init__ (self, plugin_instance):
        self._plugin_instance = plugin_instance
        self._callback_dict = {
            ControllerType.left:{
                ControllerButtons.trigger: {
                    ControllerEvents.pressed: None,
                    ControllerEvents.held: None,
                    ControllerEvents.released: None,
                },
                ControllerButtons.grip: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
                ControllerButtons.button1: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
                ControllerButtons.button2: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
            },
            ControllerType.right:{
                ControllerButtons.trigger: {
                    ControllerEvents.pressed: None,
                    ControllerEvents.held: None,
                    ControllerEvents.released: None,
                },
                ControllerButtons.grip: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
                ControllerButtons.button1: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
                ControllerButtons.button2: {
                    ControllerEvents.pressed:None,
                    ControllerEvents.held:None,
                    ControllerEvents.released:None,
                },
            },
        }

    def _on_controller_callback(self, controller_type, controller_button, controller_event, controller):
        callback = self._callback_dict[controller_type][controller_button][controller_event]
        if (not callback == None):
            callback(controller)