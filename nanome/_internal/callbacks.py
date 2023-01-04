from .enums import Hashes
import logging
from . import _PluginInstance

logger = logging.getLogger(__name__)


def advanced_settings(network, args, request_id):
    network.on_advanced_settings()


def receive_complexes(network, arg, request_id):
    for i in range(len(arg)):
        if arg[i]._index == -1:
            arg[i] = None
    network._call(request_id, arg)


def complex_updated(network, arg, request_id):
    _PluginInstance._on_complex_updated(arg[0], arg[1])


def connect(network, arg, request_id):
    pass


def receive_create_stream_result(network, result, request_id):
    from nanome.util.stream import StreamCreationError
    from nanome.api.streams import Stream
    if result[0] != StreamCreationError.NoError:
        network._call(request_id, None, result[0])

        if result[0] == StreamCreationError.UnsupportedStream:
            logger.error("Tried to create an unsupported type of stream")
        return

    stream = Stream(network, result[1], result[2], result[3])
    network._call(request_id, stream, StreamCreationError.NoError)


def feed_stream(network, result, request_id):
    from nanome.api.streams import Stream
    Stream._streams[result[0]]._update_received(result[1])


def integration(network, args, request_id):
    from nanome.api.integration import Integration, IntegrationRequest

    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)


def receive_interrupt_stream(network, result, request_id):
    from nanome.api.streams import Stream

    try:
        stream = Stream._streams[result[1]]
    except:
        logger.warning(
            f"Got an error for an unknown stream. Probably tried to update an unknown stream: {result[1]}")
        return

    stream._interrupt(result[0])


def receive_menu(network, arg, request_id):
    # unpacks the arg tuple.
    temp_menu = arg[0]
    temp_nodes = arg[1]
    temp_contents = arg[2]

    plugin_menu = network._plugin.menu  # dead API
    plugin_menu._copy_data(temp_menu)
    root_id = temp_menu._root_id

    live_nodes = plugin_menu._get_all_nodes()
    live_contents = plugin_menu._get_all_content()
    # creates map of live content
    content_dict = {}
    for content in live_contents:
        content_dict[content._id] = content
    # creates map of live nodes
    node_dict = {}
    for node in live_nodes:
        node_dict[node._id] = node
    # updates existing content with data.
    # adds any new content.
    for content in temp_contents:
        if content._content_id in content_dict:
            l_content = content_dict[content._content_id]
            l_content._copy_values_deep(content)
        else:
            content_dict[content._content_id] = content
    # updates existing nodes with data.
    # adds any new nodes.
    for node in temp_nodes:
        if node._id in node_dict:
            l_node = node_dict[node._id]
            l_node.copy_values_shallow(node)
        else:
            node_dict[node._id] = node
    # reconnects all the nodes and contents using ids.
    for node in temp_nodes:
        l_node = node_dict[node._id]
        l_node._clear_children()
        for child_id in node._child_ids:
            l_node._add_child(node_dict[child_id])
        del node._child_ids
        if (node._content_id == None):
            l_node._set_content(None)
        else:
            l_node._set_content(content_dict[node._content_id])
        del node._content_id
    # corrects the root.
    plugin_menu.root = node_dict[root_id]
    network._call(request_id, plugin_menu)


def presenter_change(network, arg, request_id):
    network._on_presenter_change()


def run(network, args, request_id):
    network._on_run()


def selection_changed(network, arg, request_id):
    _PluginInstance._on_selection_changed(arg[0], arg[1])


def simple_callback_arg_unpack(network, arg, request_id):
    network._call(request_id, *arg)


def simple_callback_arg(network, arg, request_id):
    network._call(request_id, arg)


def simple_callback_no_arg(network, arg, request_id):
    network._call(request_id)


def __find_content(network, content_id):
    for menu in network._plugin._menus.values():
        content = menu._find_content(content_id)
        if content is not None:
            return content
    return None


def menu_toggled(network, arg, request_id):
    index = arg[0]
    enabled = arg[1]
    active_menu = network._plugin._menus[index]
    if active_menu != None:
        active_menu._enabled = enabled
        if enabled == True:
            active_menu._on_opened_callback()
        elif enabled == False:
            active_menu._on_closed_callback()
    else:
        logger.warning("Can't find Menu for callback")


def slider_released(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_released()
    else:
        logger.warning("Can't find UI content for callback")


def slider_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_changed()
    else:
        logger.warning("Can't find UI content for callback")


def text_submit(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_submitted()
    else:
        logger.warning("Can't find UI content for callback")


def text_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_changed()
    else:
        logger.warning("Can't find UI content for callback")


def button_pressed(network, arg, request_id):
    content_id = arg[0]
    btn = __find_content(network, content_id)
    if btn != None:
        if btn._toggle_on_press:
            btn._selected = arg[1]
        btn._on_button_pressed()
    else:
        logger.warning("Can't find UI content for callback")


def button_hover(network, arg, request_id):
    content_id = arg[0]
    state = arg[1]
    btn = __find_content(network, content_id)
    if btn != None:
        btn._on_button_hover(state)
    else:
        logger.warning("Can't find UI content for callback")


def image_pressed(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_pressed(x, y)
    else:
        logger.warning("Can't find UI content for callback")


def image_held(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_held(x, y)
    else:
        logger.warning("Can't find UI content for callback")


def image_released(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_released(x, y)
    else:
        logger.warning("Can't find UI content for callback")


def dropdown_item_clicked(network, arg, request_id):
    content_id = arg[0]
    index = arg[1]
    dropdown = __find_content(network, content_id)

    if dropdown != None:
        for item in dropdown._items:
            item._selected = False
        clickedItem = dropdown._items[index]
        clickedItem._selected = True
        dropdown._on_item_clicked(clickedItem)
    else:
        logger.warning("Can't find UI content for callback")


def complex_added(network, arg, request_id):
    network.on_complex_added()


def complex_removed(network, arg, request_id):
    network.on_complex_removed()
