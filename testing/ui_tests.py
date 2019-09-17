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
    value.set_all_icon('')
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
    options = TestOptions(ignore_vars=["_name"])
    run_test(test_ui, counter)
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