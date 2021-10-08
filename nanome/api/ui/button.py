from copy import deepcopy
import nanome
from nanome._internal._ui import _Button
from . import UIBase


class Button(_Button, UIBase):
    """
    | Represents a clickable button on a menu
    """
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions

    def __init__(self, text=None, icon=None):
        _Button.__init__(self)
        UIBase.__init__(self)
        self.text = self._text
        self.icon = self._icon
        self.mesh = self._mesh
        self.outline = self._outline
        self.switch = self._switch
        self.tooltip = self._tooltip
        if (text != None):
            self.text.value.set_all(text)
        if (icon != None):
            self.icon.value.set_all(icon)

    def register_pressed_callback(self, func):
        """
        | Registers a function to be called when the button is pressed/clicked

        :param func: called when a button is pressed
        :type func: method (:class:`~nanome.ui.Button`) -> None
        """
        _Button._register_pressed_callback(self, func)

    def register_hover_callback(self, func):
        """
        | Registers a function to be called when the button is hovered over

        :param func: called when a button is hovered over
        :type func: method (:class:`~nanome.ui.Button`) -> None
        """
        _Button._register_hover_callback(self, func)

    @property
    def name(self):
        """
        | The name of the button

        :type: :class:`str`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def selected(self):
        """
        | Whether or not the button is selected
        | Corresponds to a potentially visually distinct UI state

        :type: :class:`bool`
        """
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def unusable(self):
        """
        | Whether or not the button is unusable
        | Corresponds to a potentially visually distinct UI state

        :type: :class:`bool`
        """
        return self._unusable

    @unusable.setter
    def unusable(self, value):
        self._unusable = value

    @property
    def disable_on_press(self):
        """
        | Whether or not to disable the button after it has been pressed once.

        :type: :class:`bool`
        """
        return self._disable_on_press

    @disable_on_press.setter
    def disable_on_press(self, value):
        self._disable_on_press = value

    @property
    def toggle_on_press(self):
        """
        | Whether or not to toggle the selected state of the button when it is pressed.

        :type: :class:`bool`
        """
        return self._toggle_on_press

    @toggle_on_press.setter
    def toggle_on_press(self, value):
        self._toggle_on_press = value

    class ButtonText(_Button._ButtonText):
        @property
        def value(self):
            """
            | The text displayed by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._value

        @value.setter
        def value(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def bold(self):
            """
            | Whether or not the text is bold by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._bold

        @bold.setter
        def bold(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            """
            | The color of the text by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._color

        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            """
            | Whether or not the button text is visible

            :type: :class:`bool`
            """
            return self._active

        @active.setter
        def active(self, value):
            self._active = value

        @property
        def auto_size(self):
            """
            | Whether or not to automatically scale the font size of the text
            | based on the size of the button

            :type: :class:`bool`
            """
            return self._auto_size

        @auto_size.setter
        def auto_size(self, value):
            self._auto_size = value

        @property
        def min_size(self):
            """
            | The minimum font size the text will display
            | This is the lower bound for auto sizing.

            :type: :class:`float`
            """
            return self._min_size

        @min_size.setter
        def min_size(self, value):
            self._min_size = value

        @property
        def max_size(self):
            """
            | The maximum font size the text will display
            | This is the upper bound for auto sizing.

            :type: :class:`float`
            """
            return self._max_size

        @max_size.setter
        def max_size(self, value):
            self._max_size = value

        @property
        def size(self):
            """
            | The font size of the text displayed

            :type: :class:`float`
            """
            return self._size

        @size.setter
        def size(self, value):
            self._size = value

        @property
        def underlined(self):
            """
            | Whether or not the button text is underlined.

            :type: :class:`bool`
            """
            return self._underlined

        @underlined.setter
        def underlined(self, value):
            self._underlined = value

        @property
        def ellipsis(self):
            """
            | Whether or not to use an ellipsis if there is too much text to display

            :type: :class:`bool`
            """
            return self._ellipsis

        @ellipsis.setter
        def ellipsis(self, value):
            self._ellipsis = value

        @property
        def padding_top(self):
            """
            | The padding above the text

            :type: :class:`float`
            """
            return self._padding_top

        @padding_top.setter
        def padding_top(self, value):
            self._padding_top = value

        @property
        def padding_bottom(self):
            """
            | The padding below the text

            :type: :class:`float`
            """
            return self._padding_bottom

        @padding_bottom.setter
        def padding_bottom(self, value):
            self._padding_bottom = value

        @property
        def padding_left(self):
            """
            | The padding to the left of the text

            :type: :class:`float`
            """
            return self._padding_left

        @padding_left.setter
        def padding_left(self, value):
            self._padding_left = value

        @property
        def padding_right(self):
            """
            | The padding to the right of the text

            :type: :class:`float`
            """
            return self._padding_right

        @padding_right.setter
        def padding_right(self, value):
            self._padding_right = value

        @property
        def line_spacing(self):
            """
            | The space between lines of text

            :type: :class:`float`
            """
            return self._line_spacing

        @line_spacing.setter
        def line_spacing(self, value):
            self._line_spacing = value

        @property
        def vertical_align(self):
            """
            | The vertical alignment of the text

            :type: :class:`~nanome.util.enums.VertAlignOptions`
            """
            return self._vertical_align

        @vertical_align.setter
        def vertical_align(self, value):
            self._vertical_align = value

        @property
        def horizontal_align(self):
            """
            | The horizontal alignment of the text

            :type: :class:`~nanome.util.enums.HorizAlignOptions`
            """
            return self._horizontal_align

        @horizontal_align.setter
        def horizontal_align(self, value):
            self._horizontal_align = value
    _Button._ButtonText._create = ButtonText

    class ButtonIcon(_Button._ButtonIcon):
        @property
        def value(self):
            """
            | The file paths to the icon image by button state.

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._value

        @value.setter
        def value(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            """
            | The color of the image by button state.

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._color

        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            """
            | Whether or not the icon is visible

            :type: :class:`bool`
            """
            return self._active

        @active.setter
        def active(self, value):
            self._active = value

        @property
        def sharpness(self):
            """
            | The sharpness of the icon image (between 0 and 1)

            :type: :class:`float`
            """
            return self._sharpness

        @sharpness.setter
        def sharpness(self, value):
            self._sharpness = value

        @property
        def size(self):
            """
            | The size of the icon image
            | A size of 1 represents the full size.

            :type: :class:`float`
            """
            return self._size

        @size.setter
        def size(self, value):
            self._size = value

        @property
        def ratio(self):
            """
            | The ratio of height to height + width for the icon.
            | A size of 0.5 represents equal width and height

            :type: :class:`float`
            """
            return self._ratio

        @ratio.setter
        def ratio(self, value):
            self._ratio = value

        @property
        def position(self):
            """
            | The position of the icon
            | A position of (1, 1, 1) represents right, top, front,
            | whereas (0, 0, 0) represents the middle.

            :type: :class:`tuple` <:class:`float`, :class:`float`, :class:`float`>
            """
            return self._position

        @position.setter
        def position(self, value):
            self._position = value

        @property
        def rotation(self):
            """
            | The rotation of the icon about each axis.
            | A position of (90, 90, 90) represents a quarter rotation
            | about each of the X, Y and Z axes, whereas (0, 0, 0) represents no rotation.

            :type: :class:`tuple` <:class:`float`, :class:`float`, :class:`float`>
            """
            return self._rotation

        @rotation.setter
        def rotation(self, value):
            self._rotation = value
    _Button._ButtonIcon._create = ButtonIcon

    class ButtonMesh(_Button._ButtonMesh):
        @property
        def color(self):
            """
            | The color of the mesh by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._color

        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def enabled(self):
            """
            | Whether or not the mesh is visible by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._enabled

        @enabled.setter
        def enabled(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            """
            | Whether or not the mesh is visible

            :type: :class:`bool`
            """
            return self._active

        @active.setter
        def active(self, value):
            self._active = value
    _Button._ButtonMesh._create = ButtonMesh

    class ButtonOutline(_Button._ButtonOutline):
        @property
        def size(self):
            """
            | The line thickness of the outline by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            return self._size

        @size.setter
        def size(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            """
            | The color of the outline by button state

            :type: :class:`~nanome.ui.Button.MultiStateVariable`
            """
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            """
            | Whether or not the outline is visible

            :type: :class:`bool`
            """
            return self._active

        @active.setter
        def active(self, value):
            self._active = value
    _Button._ButtonOutline._create = ButtonOutline

    class ButtonSwitch(_Button._ButtonSwitch):
        @property
        def active(self):
            """
            | Whether or not the button is visible

            :type: :class:`bool`
            """
            return self._active

        @active.setter
        def active(self, value):
            self._active = value

        @property
        def on_color(self):
            """
            | The color for the button when it is on

            :type: :class:`~nanome.ui.Color`
            """
            return self._on_color

        @on_color.setter
        def on_color(self, value):
            self._on_color = value

        @property
        def off_color(self):
            """
            | The color for the button when it is off

            :type: :class:`~nanome.ui.Color`
            """
            return self._off_color

        @off_color.setter
        def off_color(self, value):
            self._off_color = value
    _Button._ButtonSwitch._create = ButtonSwitch

    class ButtonTooltip(_Button._ButtonTooltip):
        @property
        def title(self):
            """
            | The title of the tooltip

            :type: :class:`str`
            """
            return self._title

        @title.setter
        def title(self, value):
            self._title = value

        @property
        def content(self):
            """
            | The main textual content of the tooltip

            :type: :class:`str`
            """
            return self._content

        @content.setter
        def content(self, value):
            self._content = value

        @property
        def bounds(self):
            """
            | The bounds of the tooltip

            :type: :class:`tuple` <:class:`float`, :class:`float`, :class:`float`>
            """
            return self._bounds

        @bounds.setter
        def bounds(self, value):
            self._bounds = value

        @property
        def positioning_target(self):
            """
            | Determines which side of the button the tooltip (origin) will appear on
            | Refers to the tooltip's button

            :type: :class:`~nanome.util.enums.ToolTipPositioning`
            """
            return self._positioning_target

        @positioning_target.setter
        def positioning_target(self, value):
            self._positioning_target = value

        @property
        def positioning_origin(self):
            """
            | Determines which part of the tooltip is closest to the button (target)
            | Refers to the tooltip

            :type: :class:`~nanome.util.enums.ToolTipPositioning`
            """
            return self._positioning_origin

        @positioning_origin.setter
        def positioning_origin(self, value):
            self._positioning_origin = value
    _Button._ButtonTooltip._create = ButtonTooltip

    class MultiStateVariable(_Button._MultiStateVariable):
        def __init__(self, default=None):
            _Button._MultiStateVariable.__init__(self, default)

        def set_all(self, value):
            """
            | Sets the value for every state
            """
            self._set_all(value)

        def set_each(self, idle=None, selected=None, highlighted=None, selected_highlighted=None, unusable=None, default=None):
            """
            | Sets the value for each state
            """
            self._set_each(idle, selected, highlighted, selected_highlighted, unusable, default)

        @property
        def idle(self):
            """
            | Represents the idle state where the element is not being hovered and is not selected

            :type: Any
            """
            return self._idle

        @idle.setter
        def idle(self, value):
            self._idle = value

        @property
        def highlighted(self):
            """
            | Represents the highlighted state where the element is being hovered

            :type: Any
            """
            return self._highlighted

        @highlighted.setter
        def highlighted(self, value):
            self._highlighted = value

        @property
        def selected(self):
            """
            | Represents the highlighted state where the element has been selected

            :type: Any
            """
            return self._selected

        @selected.setter
        def selected(self, value):
            self._selected = value

        @property
        def selected_highlighted(self):
            """
            | Represents the selected, highlighted state where the element has been selected and is being hovered over

            :type: Any
            """
            return self._selected_highlighted

        @selected_highlighted.setter
        def selected_highlighted(self, value):
            self._selected_highlighted = value

        @property
        def unusable(self):
            """
            | Represents the unusable state where the element cannot be interacted with

            :type: Any
            """
            return self._unusable

        @unusable.setter
        def unusable(self, value):
            self._unusable = value
    _Button._MultiStateVariable._create = MultiStateVariable


_Button._create = Button
