import nanome
from .. import _Button

#region Text Deprecated Properties
@property
@nanome.util.Logs.deprecated("value.idle")
def value_idle(self):
    # type: () -> str
    return self.value.idle
@value_idle.setter
@nanome.util.Logs.deprecated("value.idle")
def value_idle(self, value):
    # type: (str)
    if type(value) is not str:
        value = str(value)
    self.value.idle = value

@property
@nanome.util.Logs.deprecated("value.selected")
def value_selected(self):
    # type: () -> str
    return self.value.selected
@value_selected.setter
@nanome.util.Logs.deprecated("value.selected")
def value_selected(self, value):
    # type: (str)
    if type(value) is not str:
        value = str(value)
    self.value.selected = value

@property
@nanome.util.Logs.deprecated("value.highlighted")
def value_highlighted(self):
    # type: () -> str
    return self.value.highlighted
@value_highlighted.setter
@nanome.util.Logs.deprecated("value.highlighted")
def value_highlighted(self, value):
    # type: (str)
    if type(value) is not str:
        value = str(value)
    self.value.highlighted = value

@property
@nanome.util.Logs.deprecated("value.selected_highlighted")
def value_selected_highlighted(self):
    # type: () -> str
    return self.value.selected_highlighted
@value_selected_highlighted.setter
@nanome.util.Logs.deprecated("value.selected_highlighted")
def value_selected_highlighted(self, value):
    # type: (str)
    if type(value) is not str:
        value = str(value)
    self.value.selected_highlighted = value

@property
@nanome.util.Logs.deprecated("value.unusable")
def value_unusable(self):
    # type: () -> str
    return self.value.unusable
@value_unusable.setter
@nanome.util.Logs.deprecated("value.unusable")
def value_unusable(self, value):
    # type: (str)
    if type(value) is not str:
        value = str(value)
    self.value.unusable = value
#endregion

_Button._ButtonText.value_idle = value_idle
_Button._ButtonText.value_selected = value_selected
_Button._ButtonText.value_highlighted = value_highlighted
_Button._ButtonText.value_selected_highlighted = value_selected_highlighted
_Button._ButtonText.value_unusable = value_unusable

@property
@nanome.util.Logs.deprecated("bold")
def _bolded(self):
    # type: () -> bool
    return self.bold.idle
@_bolded.setter
@nanome.util.Logs.deprecated("bold")
def _bolded(self, value):
    # type: (bool)
    self.bold.set_all(value)

_Button._ButtonText.bolded = _bolded

@nanome.util.Logs.deprecated("text.value.set_all")
def set_all_text(self, text):
    self.text.value.set_all(text)

_Button.set_all_text = set_all_text

@nanome.util.Logs.deprecated("icon.value.set_all")
def set_all_icon(self, icon):
    # type: (str)
    self.icon.active = True
    self.icon.value.set_all(icon)

_Button.set_all_icon = set_all_icon

#region Icon Deprecated Properties
@property
@nanome.util.Logs.deprecated("value.idle")
def value_idle(self):
    return self.value.idle
@value_idle.setter
@nanome.util.Logs.deprecated("value.idle")
def value_idle(self, value):
    if type(value) is not str:
        value = str(value)
    self.value.idle = value

@property
@nanome.util.Logs.deprecated("value.selected")
def value_selected(self):
    return self.value.selected
@value_selected.setter
@nanome.util.Logs.deprecated("value.selected")
def value_selected(self, value):
    if type(value) is not str:
        value = str(value)
    self.value.selected = value

@property
@nanome.util.Logs.deprecated("value.highlighted")
def value_highlighted(self):
    return self.value.highlighted
@value_highlighted.setter
@nanome.util.Logs.deprecated("value.highlighted")
def value_highlighted(self, value):
    if type(value) is not str:
        value = str(value)
    self.value.highlighted = value

@property
@nanome.util.Logs.deprecated("value.selected_highlighted")
def value_selected_highlighted(self):
    return self.value.selected_highlighted
@value_selected_highlighted.setter
@nanome.util.Logs.deprecated("value.selected_highlighted")
def value_selected_highlighted(self, value):
    if type(value) is not str:
        value = str(value)
    self.value.selected_highlighted = value

@property
@nanome.util.Logs.deprecated("value.unusable")
def value_unusable(self):
    return self.value.unusable
@value_unusable.setter
@nanome.util.Logs.deprecated("value.unusable")
def value_unusable(self, value):
    if type(value) is not str:
        value = str(value)
    self.value.unusable = value

@property
@nanome.util.Logs.deprecated("color.idle")
def color_idle(self):
    return self.color.idle
@color_idle.setter
@nanome.util.Logs.deprecated("color.idle")
def color_idle(self, value):
    self.color.idle = value

@property
@nanome.util.Logs.deprecated("color.selected")
def color_selected(self):
    return self.color.selected
@color_selected.setter
@nanome.util.Logs.deprecated("color.selected")
def color_selected(self, value):
    self.color.selected = value

@property
@nanome.util.Logs.deprecated("color.highlighted")
def color_highlighted(self):
    return self.color.highlighted
@color_highlighted.setter
@nanome.util.Logs.deprecated("color.highlighted")
def color_highlighted(self, value):
    self.color.highlighted = value

@property
@nanome.util.Logs.deprecated("color.selected_highlighted")
def color_selected_highlighted(self):
    return self.color.selected_highlighted
@color_selected_highlighted.setter
@nanome.util.Logs.deprecated("color.selected_highlighted")
def color_selected_highlighted(self, value):
    self.color.selected_highlighted = value

@property
@nanome.util.Logs.deprecated("color.unusable")
def color_unusable(self):
    return self.color.unusable
@color_unusable.setter
@nanome.util.Logs.deprecated("color.unusable")
def color_unusable(self, value):
    self.color.unusable = value
#endregion

_Button._ButtonIcon.value_idle = value_idle
_Button._ButtonIcon.value_selected = value_selected
_Button._ButtonIcon.value_highlighted = value_highlighted
_Button._ButtonIcon.value_selected_highlighted = value_selected_highlighted
_Button._ButtonIcon.value_unusable = value_unusable

_Button._ButtonIcon.color_idle = color_idle
_Button._ButtonIcon.color_selected = color_selected
_Button._ButtonIcon.color_highlighted = color_highlighted
_Button._ButtonIcon.color_selected_highlighted = color_selected_highlighted
_Button._ButtonIcon.color_unusable = color_unusable