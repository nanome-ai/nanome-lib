import nanome
import os
# from nanome import UI
import nanome.api.ui as UI
from nanome._internal._ui._serialization import _LayoutNodeSerializer, _UIBaseSerializer
from nanome._internal._network._serialization._context import _ContextDeserialization, _ContextSerialization
# from nanome.serialization.commands import ReceiveMenu, UpdateMenu
from testing.utilities import *

#testing structures
def test_ui():
    button = UI.Button()
    label = UI.Label()
    mesh = UI.Mesh()
    slider = UI.Slider()
    text_input = UI.TextInput()
    image = UI.Image()
    loading_bar = UI.LoadingBar()
    _list = UI.UIList()
    # ui_base = UI.UIBase()
    menu = UI.Menu()

def test_deprecated_button():
    from functools import partial
    import copy
    import collections
    button = UI.Button()
    FP = collections.namedtuple("FP", ["fset","fget"])
    def get_property(obj, attr):
        for obj in [obj] + obj.__class__.mro():
            if attr in obj.__dict__:
                prop = obj.__dict__[attr]
                fset = partial(prop.fset, obj)
                fget = partial(prop.fget, obj)
                fp = FP(fset, fget)
                return fp
        raise AttributeError
    test_multi_var(button.text.value, 
                   get_property(button.text, "value_idle"),
                   get_property(button.text, "value_selected"),
                   get_property(button.text, "value_highlighted"),
                   get_property(button.text, "value_selected_highlighted"),
                   get_property(button.text, "value_unusable"),
                   button.set_all_text)

def test_multi_var(multi, idle, selected, highlighted, selected_highlighted, unusable, set_all):
    temp_warning = nanome.util.Logs.warning
    warned = False
    def confirm_warning(txt):
        nonlocal warned
        warned = True
    nanome.util.Logs.warning = confirm_warning
    def assert_warning():
        nonlocal warned
        assert(warned)
        warned = False
    def test_var(single, deprecated):
        deprecated.fset("val1")
        assert_warning()
        assert(single == deprecated.fget())
        assert_warning()

    test_var(multi.idle, idle)
    test_var(multi.selected, selected)
    test_var(multi.highlighted, highlighted)
    test_var(multi.selected_highlighted, selected_highlighted)
    test_var(multi.unusable, unusable)

    value = "value1234"
    set_all(value)
    assert(multi.idle == value)
    assert(multi.selected == value)
    assert(multi.highlighted == value)
    assert(multi.selected_highlighted == value)
    assert(multi.unusable == value)

    nanome.util.Logs.warning = temp_warning

def prefab_button_pressed_callback(btn):
    pass

def CreateMenu():
    value = UI.Menu()
    value = alter_object(value)
    value.root.name = "node"
    return value
def CreateButton():
    value = UI.Button()
    value = alter_object(value)
    return value
def CreateMesh():
    value = UI.Mesh()
    value = alter_object(value)
    return value
def CreateSlider():
    value = UI.Slider()
    value = alter_object(value)
    return value
def CreateTextInput():
    value = UI.TextInput()
    value = alter_object(value)
    return value
def CreateLabel():
    value = UI.Label()
    value = alter_object(value)
    return value
def CreateList():
    prefab = nanome.ui.LayoutNode()
    prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.vertical
    child1 = nanome.ui.LayoutNode()
    child1.sizing_type = nanome.ui.LayoutNode.SizingTypes.ratio
    child1.sizing_value = .3
    child1.name = "label"
    child1.forward_dist = .01
    child2 = nanome.ui.LayoutNode()
    child2.name = "button"
    child2.forward_dist =.01
    prefab.add_child(child1)
    prefab.add_child(child2)
    prefabLabel = nanome.ui.Label()
    prefabLabel.text_value = "Molecule Label"
    prefabButton = nanome.ui.Button()
    prefabButton.text.active = True
    prefabButton.set_all_text("Molecule Button")
    prefabButton.register_pressed_callback(prefab_button_pressed_callback)
    child1.set_content(prefabLabel)
    child2.set_content(prefabButton)

    list_content = []
    for _ in range(0, 10):
        clone = prefab.clone()
        list_content.append(clone)

    list = nanome.ui.UIList()
    list.display_columns = 1
    list.display_rows = 1
    list.total_columns = 1
    list.items = list_content
    return list
def CreateLayoutNode():
    value = UI.LayoutNode()
    value = alter_object(value)
    value.name = "node"
    return value

class FakeNetwork():
    def __init__(self, original):
        self.original = original
        pass
    def on_menu_received(self, menu):
        #del menu._root_id
        menu._id = 0
        self.original._id = 0
        assert(self.original != menu)
        assert_equal(self.original, menu)

# def test_menu_serialization():
#     obj_to_test = CreateMenu()
#     serializer = UpdateMenu()
#     deserializer = ReceiveMenu()
#     context_s = ContextSerialization()
#     serializer.serialize(obj_to_test, context_s)
#     context_d = ContextDeserialization(context_s.to_array())
#     result = deserializer.deserialize(context_d)
#     import nanome.core
#     import nanome.api.menu
#     nanome.api.menu.receive_menu(FakeNetwork(obj_to_test), result)

def run(counter):
    options = TestOptions(ignore_vars=["_name", "icon", "_icon"])
    run_test(test_ui, counter)
    run_test(test_deprecated_button, counter)
    run_test(create_test("button_test", test_serializer, (_UIBaseSerializer(), CreateButton(), options)), counter)
    run_test(create_test("mesh_test", test_serializer, (_UIBaseSerializer(), CreateMesh(), options)), counter)
    run_test(create_test("slider_test", test_serializer, (_UIBaseSerializer(), CreateSlider(), options)), counter)
    run_test(create_test("text_input_test", test_serializer, (_UIBaseSerializer(), CreateTextInput(), options)), counter)
    run_test(create_test("label_test", test_serializer, (_UIBaseSerializer(), CreateLabel(), options)), counter)
    run_test(create_test("list_and_clone_test", test_serializer, (_UIBaseSerializer(), CreateList(), options)), counter)
    test_node = CreateLayoutNode()
    test_node._child_ids = []
    test_node._content_id = None
    run_test(create_test("layout_test", test_serializer, (_LayoutNodeSerializer(), test_node)), counter)

    # run_test(test_menu_serialization, counter)