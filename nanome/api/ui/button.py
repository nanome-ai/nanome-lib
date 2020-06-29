import copy
import nanome
from nanome._internal._ui import _Button
from . import UIBase

class Button(_Button, UIBase):
    HorizAlignOptions = nanome.util.enums.HorizAlignOptions
    VertAlignOptions = nanome.util.enums.VertAlignOptions

    def __init__(self, text = None, icon = None):
        # type: (str, str)
        _Button.__init__(self)
        UIBase.__init__(self)
        self.text = self._text
        self.icon = self._icon
        self.mesh = self._mesh
        self.outline = self._outline
        self.tooltip = self._tooltip
        if (text != None):
            self.text.value.set_all(text)
        if (icon != None):
            self.icon.value.set_all(icon)

    def register_pressed_callback(self, func):
        _Button._register_pressed_callback(self, func)

    def register_hover_callback(self, func):
        _Button._register_hover_callback(self, func)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def selected(self):
        # type: () -> bool
        return self._selected
    @selected.setter
    def selected(self, value):
        # type: (bool)
        self._selected = value

    @property
    def unusable(self):
        # type: () -> bool
        return self._unusable
    @unusable.setter
    def unusable(self, value):
        # type: (bool)
        self._unusable = value

    @property
    def disable_on_press(self):
        return self._disable_on_press

    @disable_on_press.setter
    def disable_on_press(self, value):
        self._disable_on_press = value

    class ButtonText(_Button._ButtonText):
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def bold(self):
            return self._bold
        
        @bold.setter
        def bold(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            return self._color
        
        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            # type: () -> bool
            return self._active
        @active.setter
        def active(self, value):
            # type: (bool)
            self._active = value

        @property
        def auto_size(self):
            # type: () -> bool
            return self._auto_size
        @auto_size.setter
        def auto_size(self, value):
            # type: (bool)
            self._auto_size = value

        @property
        def min_size(self):
            # type: () -> float
            return self._min_size
        @min_size.setter
        def min_size(self, value):
            # type: (float)
            self._min_size = value

        @property
        def max_size(self):
            # type: () -> float
            return self._max_size
        @max_size.setter
        def max_size(self, value):
            # type: (float)
            self._max_size = value

        @property
        def size(self):
            # type: () -> float
            return self._size
        @size.setter
        def size(self, value):
            # type: (float)
            self._size = value

        @property
        def underlined(self):
            # type: () -> bool
            return self._underlined
        @underlined.setter
        def underlined(self, value):
            # type: (bool)
            self._underlined = value

        @property
        def ellipsis(self):
            # type: () -> bool
            return self._ellipsis
        @ellipsis.setter
        def ellipsis(self, value):
            # type: (bool)
            self._ellipsis = value

        @property
        def padding_top(self):
            return self._padding_top
        @padding_top.setter
        def padding_top(self, value):
            self._padding_top = value

        @property
        def padding_bottom(self):
            return self._padding_bottom
        @padding_bottom.setter
        def padding_bottom(self, value):
            self._padding_bottom = value

        @property
        def padding_left(self):
            return self._padding_left
        @padding_left.setter
        def padding_left(self, value):
            self._padding_left = value

        @property
        def padding_right(self):
            return self._padding_right
        @padding_right.setter
        def padding_right(self, value):
            self._padding_right = value

        @property
        def line_spacing(self):
            return self._line_spacing
        @line_spacing.setter
        def line_spacing(self, value):
            self._line_spacing = value

        @property
        def vertical_align(self):
            # type: () -> VertAlignOptions
            return self._vertical_align
        @vertical_align.setter
        def vertical_align(self, value):
            # type: (VertAlignOptions)
            self._vertical_align = value

        @property
        def horizontal_align(self):
            # type: () -> HorizAlignOptions
            return self._horizontal_align
        @horizontal_align.setter
        def horizontal_align(self, value):
            # type: (HorizAlignOptions)
            self._horizontal_align = value
    _Button._ButtonText._create = ButtonText

    class ButtonIcon(_Button._ButtonIcon):
        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            return self._active
        @active.setter
        def active(self, value):
            self._active = value

        @property
        def sharpness(self):
            return self._sharpness
        @sharpness.setter
        def sharpness(self, value):
            self._sharpness = value

        @property
        def size(self):
            return self._size
        @size.setter
        def size(self, value):
            self._size = value

        @property
        def ratio(self):
            return self._ratio
        @ratio.setter
        def ratio(self, value):
            self._ratio = value

        @property
        def position(self):
            return self._position
        @position.setter
        def position(self, value):
            self._position = value

        @property
        def rotation(self):
            return self._rotation
        @rotation.setter
        def rotation(self, value):
            self._rotation = value
    _Button._ButtonIcon._create = ButtonIcon

    class ButtonMesh(_Button._ButtonMesh):
        @property
        def color(self):
            return self._color
        
        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def enabled(self):
            return self._enabled
        
        @enabled.setter
        def enabled(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            # type: () -> bool
            return self._active
        @active.setter
        def active(self, value):
            # type: (bool)
            self._active = value
    _Button._ButtonMesh._create = ButtonMesh

    class ButtonOutline(_Button._ButtonOutline):
        @property
        def size(self):
            return self._size
        
        @size.setter
        def size(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def color(self):
            return self._color
        
        @color.setter
        def color(self, value):
            raise ValueError("Cannot set multi-variable value directly. Specify the state or use set_all")

        @property
        def active(self):
            # type: () -> bool
            return self._active
        @active.setter
        def active(self, value):
            # type: (bool)
            self._active = value
    _Button._ButtonOutline._create = ButtonOutline

    class ButtonTooltip(_Button._ButtonTooltip):
        @property
        def title(self):
            # type: () -> bool
            return self._title
        @title.setter
        def title(self, value):
            # type: (bool)
            self._title = value

        @property
        def content(self):
            # type: () -> bool
            return self._content
        @content.setter
        def content(self, value):
            # type: (bool)
            self._content = value

        @property
        def bounds(self):
            # type: () -> bool
            return self._bounds
        @bounds.setter
        def bounds(self, value):
            # type: (bool)
            self._bounds = value

        @property
        def positioning_target(self):
            # type: () -> bool
            return self._positioning_target
        @positioning_target.setter
        def positioning_target(self, value):
            # type: (bool)
            self._positioning_target = value

        @property
        def positioning_origin(self):
            # type: () -> bool
            return self._positioning_origin
        @positioning_origin.setter
        def positioning_origin(self, value):
            # type: (bool)
            self._positioning_origin = value
    _Button._ButtonTooltip._create = ButtonTooltip

    class MultiStateVariable(_Button._MultiStateVariable):
        def __init__(self, default = None):
            _Button._MultiStateVariable.__init__(self, default)

        def set_all(self, value):
            """
            | Sets the value for every state
            """
            self.idle = copy.deepcopy(value)
            self.highlighted = copy.deepcopy(value)
            self.selected = copy.deepcopy(value)
            self.selected_highlighted = copy.deepcopy(value)
            self.unusable = copy.deepcopy(value)

        @property
        def idle(self):
            return self._idle
        
        @idle.setter
        def idle(self, value):
            self._idle = value

        @property
        def highlighted(self):
            return self._highlighted
        
        @highlighted.setter
        def highlighted(self, value):
            self._highlighted = value

        @property
        def selected(self):
            return self._selected
        
        @selected.setter
        def selected(self, value):
            self._selected = value

        @property
        def selected_highlighted(self):
            return self._selected_highlighted
        
        @selected_highlighted.setter
        def selected_highlighted(self, value):
            self._selected_highlighted = value

        @property
        def unusable(self):
            return self._unusable
        
        @unusable.setter
        def unusable(self, value):
            self._unusable = value
    _Button._MultiStateVariable._create = MultiStateVariable
_Button._create = Button