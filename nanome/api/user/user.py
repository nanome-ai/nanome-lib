from nanome._internal._user import _User
from nanome._internal._network._commands._callbacks import _Messages

class User (_User):
    def __init__(self, plugin_instance):
        super(User, self).__init__(plugin_instance)

    def register_callback(self, controller_type, controller_button, controller_event, callback):
        controller_button_events = self._callback_dict[controller_type][controller_button]
        remove_hook = callback == None

        if (not remove_hook):
            #send hook
            args = (controller_type, controller_button, controller_event)
            self._plugin_instance._network._send(_Messages.controller_hook, args)
        elif (remove_hook):
            #send remove
            args = (controller_type, controller_button, controller_event)
            self._plugin_instance._network._send(_Messages.controller_unhook, args)
        controller_button_events[controller_event] = callback
    
    def request_controller(self, controller_type, callback):
        """
        | Request the current status of a controller of the rooms presenter.

        :param controller_type: The controller you wish to request.
        :type controller_type: nanome.util.enums.ControllerType
        """
        id = self._plugin_instance._network._send(_Messages.controller_request, controller_type)
        self._plugin_instance._save_callback(id, callback)

_User._create = User