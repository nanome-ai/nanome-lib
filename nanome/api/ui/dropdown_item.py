from nanome._internal._ui import _DropdownItem


class DropdownItem(_DropdownItem):
    """
    | Represents a dropdown item in a dropdown menu
    """

    def __init__(self, name="item"):
        _DropdownItem.__init__(self)
        self.name = name

    @property
    def name(self):
        """
        | The name of the Dropdown item.
        | This text is displayed on the item when the Dropdown expands
        | and in the collapsed Dropdown when the item is the selected item.

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def close_on_selected(self):
        """
        | Whether or not this item will close the Dropdown after being selected
        | Setting this value to false can allows for multiple items to be selected.

        :type: :class:`bool`
        """
        return self._close_on_selected

    @close_on_selected.setter
    def close_on_selected(self, value):
        self._close_on_selected = value

    @property
    def selected(self):
        """
        | Whether or not this item is selected.
        | In the case that a single DropdownItem is selected in a Dropdown,
        | the item's text will appear on the Dropdown when it is collapsed

        :type: :class:`bool`
        """
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    def clone(self):
        """
        | Returns a deep copy this DropdownItem.

        :type: :class:`~nanome.ui.DropdownItem`
        """
        return self._clone()


_DropdownItem._create = DropdownItem
