from nanome._internal import macro


class Macro(macro.models._Macro):
    def __init__(self, title="", logic=""):
        self.title = title
        self.logic = logic
        super(Macro, self).__init__()

    @classmethod
    def get_plugin_identifier(cls):
        return macro.models._Macro_Macro._plugin_identifier

    @classmethod
    def set_plugin_identifier(cls, value):
        macro.models._Macro._plugin_identifier = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, value):
        self._logic = value

    def save(self, all_users=False):
        self._save(all_users)

    def run(self, callback=None):
        return self._run(callback)

    def delete(self, all_users=False):
        self._delete(all_users)

    @classmethod
    def stop(cls):
        cls._stop()

    @classmethod
    def get_live(cls, callback=None):
        return cls._get_live(callback)


macro.models._Macro._create = Macro
