from nanome._internal._ui import _UIList
from . import UIBase


class UIList(_UIList, UIBase):
    """
    | A class representing a list of UI elements.
    """

    def __init__(self):
        _UIList.__init__(self)
        UIBase.__init__(self)

    @property
    def items(self):
        """
        | LayoutNodes items to be displayed in the list.

        :type: :class:`list` <:class:`~nanome.ui.LayoutNode`>
        """
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def display_columns(self):
        """
        | Number of columns of items to display simultaneously.

        :type: :class:`int`
        """
        return self._display_columns

    @display_columns.setter
    def display_columns(self, value):
        self._display_columns = value

    @property
    def display_rows(self):
        """
        | Number of rows of items to display simultaneously.

        :type: :class:`int`
        """
        return self._display_rows

    @display_rows.setter
    def display_rows(self, value):
        self._display_rows = value

    @property
    def total_columns(self):
        """
        | Total number of columns to display across scrolling.
        | i.e. If there are 2 display columns and 4 total columns,
        | the horizontal scroll bar will have two possible positions.

        :type: :class:`int`
        """
        return self._total_columns

    @total_columns.setter
    def total_columns(self, value):
        self._total_columns = value

    @property
    def unusable(self):
        """
        | Whether or not the UI list is usable.

        :type: :class:`bool`
        """
        return self._unusable

    @unusable.setter
    def unusable(self, value):
        self._unusable = value


_UIList._create = UIList
