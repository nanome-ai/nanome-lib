

from nanome.util.logs import Logs
from nanome._internal.ui import _Menu
from nanome.util.stream import StreamCreationError
import nanome
from nanome.util import Logs, IntEnum, auto, reset_auto
from nanome.util import Logs
from nanome.util.enums import CommandEnum, Integrations, Permissions


def _advanced_settings(network, args, request_id):
    network.on_advanced_settings()


# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome


class Commands(CommandEnum):
    # Reset enum counter for Python 2.7
    reset_auto()  # Not an enum

    # Control
    connect = auto()
    run = auto()
    advanced_settings = auto()

    # UI
    menu_toggle = auto()
    button_press = auto()
    button_hover = auto()
    slider_release = auto()
    text_submit = auto()
    text_change = auto()
    slider_change = auto()
    image_press = auto()
    image_hold = auto()
    image_release = auto()
    dropdown_item_click = auto()
    menu_transform_response = auto()

    # Structure
    workspace_response = auto()
    complex_list_response = auto()
    complexes_response = auto()
    substructure_response = auto()
    structures_deep_update_done = auto()
    add_to_workspace_done = auto()
    position_structures_done = auto()
    complex_add = auto()
    complex_remove = auto()
    bonds_add_done = auto()
    dssp_add_done = auto()
    complex_updated = auto()
    selection_changed = auto()
    compute_hbonds_done = auto()

    # Stream
    stream_create_done = auto()
    stream_feed = auto()
    stream_feed_done = auto()
    stream_interrupt = auto()

    # File deprecated
    directory_response = auto()
    file_response = auto()
    file_save_done = auto()
    export_files_result = auto()

    # Files
    print_working_directory_response = auto()
    cd_response = auto()
    ls_response = auto()
    mv_response = auto()
    cp_response = auto()
    get_response = auto()
    put_response = auto()
    rm_response = auto()
    rmdir_response = auto()
    mkdir_response = auto()

    # Macro
    get_macros_response = auto()
    run_macro_result = auto()

    # Presenter
    presenter_info_response = auto()
    presenter_change = auto()
    controller_transforms_response = auto()

    # Shapes
    set_shape_result = auto()
    delete_shape_result = auto()

    # Other
    add_volume_done = auto()
    load_file_done = auto()
    integration = auto()

# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome


class Messages(CommandEnum):
    # Reset enum counter for Python 2.7
    reset_auto()

    # Control
    connect = auto()
    plugin_list_button_set = auto()

    # UI
    menu_update = auto()
    content_update = auto()
    node_update = auto()
    menu_transform_set = auto()
    menu_transform_request = auto()
    notification_send = auto()
    hook_ui_callback = auto()

    # Structure
    structures_deep_update = auto()
    structures_shallow_update = auto()
    structures_zoom = auto()
    structures_center = auto()
    workspace_update = auto()
    workspace_request = auto()
    add_to_workspace = auto()
    complexes_request = auto()
    complex_list_request = auto()
    substructure_request = auto()
    bonds_add = auto()
    dssp_add = auto()
    hook_complex_updated = auto()
    hook_selection_changed = auto()
    compute_hbonds = auto()

    # Streams
    stream_create = auto()
    stream_feed = auto()
    stream_destroy = auto()

    # Files Deprecated
    directory_request = auto()
    file_request = auto()
    file_save = auto()
    export_files = auto()

    # Files
    print_working_directory = auto()
    cd = auto()
    ls = auto()
    mv = auto()
    get = auto()
    put = auto()
    rm = auto()
    rmdir = auto()
    mkdir = auto()
    cp = auto()

    # Macro
    save_macro = auto()
    delete_macro = auto()
    run_macro = auto()
    stop_macro = auto()
    get_macros = auto()

    # Presenter
    presenter_info_request = auto()
    controller_transforms_request = auto()

    # Shapes
    set_shape = auto()
    delete_shape = auto()

    # Other
    add_volume = auto()
    open_url = auto()
    load_file = auto()
    integration = auto()
    set_skybox = auto()
    apply_color_scheme = auto()


class Integrations(CommandEnum):
    # Reset enum counter for Python 2.7
    reset_auto()

    # Hydrogens
    hydrogen_add = auto()
    hydrogen_remove = auto()
    structure_prep = auto()
    calculate_esp = auto()
    minimization_start = auto()
    minimization_stop = auto()
    export_locations = auto()
    generate_molecule_image = auto()
    export_file = auto()
    import_file = auto()
    export_smiles = auto()
    import_smiles = auto()


class Hashes():
    CommandHashes = [None] * len(Commands)
    MessageHashes = [None] * len(Messages)
    IntegrationHashes = [None] * len(Integrations)
    IntegrationRequestHashes = [None] * len(Integrations)
    PermissionRequestHashes = [None] * len(Permissions)
    HashToIntegrationName = dict()


a_char_value = ord('a')
z_char_value = ord('z')


def hash_command(str):
    result = 0
    hit = 0
    for i in range(6):
        idx = i * 3 % len(str)
        char_value = ord(str[idx].lower()) - a_char_value
        result <<= 5
        if char_value < 0 or char_value > z_char_value - a_char_value:
            continue
        result |= char_value + 1
        hit += 1
        if hit >= 6:
            break
    return result


def init_hashes():
    hashes = dict()
    i = -1
    for command in Commands:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Command hash collision detected:",
                       command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        Hashes.CommandHashes[i] = hash

    hashes.clear()
    i = -1

    for command in Messages:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Message hash collision detected:",
                       command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        Hashes.MessageHashes[i] = hash

    hashes.clear()
    i = -1

    for command in Integrations:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Integration hash collision detected:",
                       command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        Hashes.IntegrationHashes[i] = hash
        Hashes.HashToIntegrationName[hash] = command.name

    hashes.clear()
    i = -1

    for command in Integrations:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Integration request hash collision detected:",
                       command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        Hashes.IntegrationRequestHashes[i] = hash

    hashes.clear()
    i = -1

    for command in Permissions:
        i += 1
        hash = hash_command(command.name)
        if hash in hashes:
            Logs.error("Permission request hash collision detected:",
                       command.name, "and", hashes[hash])
            continue
        hashes[hash] = command.name
        Hashes.PermissionRequestHashes[i] = hash


init_hashes()


def _receive_complexes(network, arg, request_id):
    for i in range(len(arg)):
        if arg[i]._index == -1:
            arg[i] = None
    network._call(request_id, arg)


def _complex_updated(network, arg, request_id):
    nanome._internal._PluginInstance._on_complex_updated(arg[0], arg[1])


def _connect(network, arg, request_id):
    pass


def _receive_create_stream_result(network, result, request_id):
    if result[0] != StreamCreationError.NoError:
        network._call(request_id, None, result[0])

        if result[0] == StreamCreationError.UnsupportedStream:
            Logs.error("Tried to create an unsupported type of stream")
        return

    from nanome.api.streams import Stream
    stream = Stream(network, result[1], result[2], result[3])
    network._call(request_id, stream, StreamCreationError.NoError)


def _feed_stream(network, result, request_id):
    from nanome.api.streams import Stream
    Stream._streams[result[0]]._update_received(result[1])


def _integration(network, args, request_id):
    from nanome.api.integration import Integration, IntegrationRequest

    integration = network._plugin.integration
    request = IntegrationRequest(args[0], args[1], args[2], network)
    name = Hashes.HashToIntegrationName[args[1]]
    Integration._call(integration, name, request)


def _receive_interrupt_stream(network, result, request_id):
    from nanome.api.streams import Stream

    try:
        stream = Stream._streams[result[1]]
    except:
        Logs.warning(
            "Got an error for an unknown stream. Probably tried to update an unknown stream:", result[1])
        return

    stream._interrupt(result[0])


def _receive_menu(network, arg, request_id):
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


def _presenter_change(network, arg, request_id):
    network._on_presenter_change()


def _run(network, args, request_id):
    network._on_run()


def _selection_changed(network, arg, request_id):
    nanome._internal._PluginInstance._on_selection_changed(arg[0], arg[1])


def _simple_callback_arg_unpack(network, arg, request_id):
    network._call(request_id, *arg)


def _simple_callback_arg(network, arg, request_id):
    network._call(request_id, arg)


def _simple_callback_no_arg(network, arg, request_id):
    network._call(request_id)


def __find_content(network, content_id):
    for menu in network._plugin._menus.values():
        content = menu._find_content(content_id)
        if content is not None:
            return content
    return None


def _menu_toggled(network, arg, request_id):
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
        Logs.warning("Can't find Menu for callback")


def _slider_released(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_released()
    else:
        Logs.warning("Can't find UI content for callback")


def _slider_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    slider_value = tuple_obj[1]
    active_slider = __find_content(network, content_id)
    if active_slider != None:
        active_slider.current_value = slider_value
        active_slider._on_slider_changed()
    else:
        Logs.warning("Can't find UI content for callback")


def _text_submit(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_submitted()
    else:
        Logs.warning("Can't find UI content for callback")


def _text_changed(network, arg, request_id):
    tuple_obj = arg
    content_id = tuple_obj[0]
    text_value = tuple_obj[1]
    active_txt = __find_content(network, content_id)
    if active_txt != None:
        active_txt.input_text = text_value
        active_txt._on_text_changed()
    else:
        Logs.warning("Can't find UI content for callback")


def _button_pressed(network, arg, request_id):
    content_id = arg[0]
    btn = __find_content(network, content_id)
    if btn != None:
        if btn._toggle_on_press:
            btn._selected = arg[1]
        btn._on_button_pressed()
    else:
        Logs.warning("Can't find UI content for callback")


def _button_hover(network, arg, request_id):
    content_id = arg[0]
    state = arg[1]
    btn = __find_content(network, content_id)
    if btn != None:
        btn._on_button_hover(state)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_pressed(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_pressed(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_held(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_held(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _image_released(network, arg, request_id):
    content_id = arg[0]
    x = arg[1]
    y = arg[2]
    img = __find_content(network, content_id)
    if img != None:
        img._on_image_released(x, y)
    else:
        Logs.warning("Can't find UI content for callback")


def _dropdown_item_clicked(network, arg, request_id):
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
        Logs.warning("Can't find UI content for callback")


def _complex_added(network, arg, request_id):
    network.on_complex_added()


def _complex_removed(network, arg, request_id):
    network.on_complex_removed()
