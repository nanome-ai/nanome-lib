import nanome
from . import UIBase
from nanome._internal._ui import _Image


class Image(_Image, UIBase):
    """
    | Represents an image in a menu
    """
    ScalingOptions = nanome.util.enums.ScalingOptions

    def __init__(self, file_path=""):
        _Image.__init__(self)
        UIBase.__init__(self)
        self._file_path = file_path

    @property
    def color(self):
        """
        | The color of the image

        :type: :class:`~nanome.ui.Color`
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def file_path(self):
        """
        | The file path to the image.
        | Setting this and calling update_content will change the image.

        :type: :class:`str`
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def scaling_option(self):
        """
        | Determines how the image scales.

        :type: :class:`~nanome.util.enums.ScalingOptions`
        """
        return self._scaling_option

    @scaling_option.setter
    def scaling_option(self, value):
        self._scaling_option = value

    def register_pressed_callback(self, func):
        """
        | Registers a function to be called when the image is pressed

        :param func: called the image is pressed
        :type func: method (:class:`~nanome.ui.Image`, :class:`int`, :class:`int`) -> None
        """
        _Image._register_pressed_callback(self, func)

    def register_held_callback(self, func):
        """
        | Registers a function to be called rapidly while the image is being pressed

        :param func: called while the image is being pressed
        :type func: method (:class:`~nanome.ui.Image`, :class:`int`, :class:`int`) -> None
        """
        _Image._register_held_callback(self, func)

    def register_released_callback(self, func):
        """
        | Registers a function to be called when the image is released

        :param func: called the image is released
        :type func: method (:class:`~nanome.ui.Image`, :class:`int`, :class:`int`) -> None
        """
        _Image._register_released_callback(self, func)


_Image._create = Image
