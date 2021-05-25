from . import UIBase
from nanome._internal._ui import _LoadingBar


class LoadingBar(_LoadingBar, UIBase):
    """
    | Represents a loading bar that can display a percentage
    """

    def __init__(self):
        _LoadingBar.__init__(self)
        UIBase.__init__(self)

    @property
    def percentage(self):
        """
        | The load percentage to indicate

        :type: :class:`float`
        """
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        self._percentage = value

    @property
    def title(self):
        """
        | The title of the loading bar.
        | Appears over the loading bar

        :type: :class:`str`
        """
        return self._title

    @title.setter
    def title(self, value):
        if type(value) is not str:
            value = str(value)
        self._title = value

    @property
    def description(self):
        """
        | A description of what is being loaded.
        | Appears under the loading bar title

        :type: :class:`str`
        """
        return self._description

    @description.setter
    def description(self, value):
        if type(value) is not str:
            value = str(value)
        self._description = value

    @property
    def failure(self):
        """
        | Whether or not loading has failed
        | Setting this to true and updating the UI will make the loading bar appear red in Nanome

        :type: :class:`bool`
        """
        return self._failure

    @failure.setter
    def failure(self, value):
        self._failure = value


_LoadingBar._create = LoadingBar
