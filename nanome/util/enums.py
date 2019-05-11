from . import IntEnum

class ControllerType(IntEnum):
    head = 0
    left = 1
    right = 2

class ControllerButtons(IntEnum):
    trigger = 0
    grip = 1
    button1 = 2
    button2 = 3

class ControllerEvents (IntEnum):
    pressed = 0
    held = 1
    released = 2