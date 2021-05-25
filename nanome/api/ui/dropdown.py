from . import UIBase
from nanome._internal._ui import _Dropdown


class Dropdown(_Dropdown, UIBase):
    """
    | Represents a dropdown menu
    """

    def __init__(self):
        _Dropdown.__init__(self)
        UIBase.__init__(self)

    @property
    def permanent_title(self):
        """
        | The permanent text to display over the Dropdown's selected item area.

        :type: :class:`str`
        """
        return self._permanent_title

    @permanent_title.setter
    def permanent_title(self, value):
        self._permanent_title = value

    @property
    def use_permanent_title(self):
        """
        | Whether or not to display permanent text where the Dropdown would otherwise display the selected item

        :type: :class:`bool`
        """
        return self._use_permanent_title

    @use_permanent_title.setter
    def use_permanent_title(self, value):
        self._use_permanent_title = value

    @property
    def max_displayed_items(self):
        """
        | The maximum number of items to display at a time
        | If there are more items in the dropdown than this value,
        | a scrollbar will be appear on the dropdown.

        :type: :class:`int`
        """
        return self._max_displayed_items

    @max_displayed_items.setter
    def max_displayed_items(self, value):
        self._max_displayed_items = value

    @property
    def items(self):
        """
        | A list of DropdownItems in the list

        :type: :class:`list` <:class:`~nanome.ui.DropdownItem`>
        """
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def register_item_clicked_callback(self, func):
        """
        | Registers a function to be called when a dropdown item is pressed

        :param func: called when a dropdown item is pressed
        :type func: method (:class:`~nanome.ui.Dropdown`, :class:`~nanome.ui.DropdownItem`) -> None
        """
        _Dropdown._register_item_clicked_callback(self, func)


_Dropdown._create = Dropdown
