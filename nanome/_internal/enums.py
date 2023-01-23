import sys
from nanome._internal.enum_utils import IntEnum, auto, reset_auto
import logging


logger = logging.getLogger(__name__)


class CommandEnum(IntEnum):
    if sys.version_info >= (3, 6):  # Tmp hack
        # Override for auto()
        def _generate_next_value_(name, start, count, last_values):
            return IntEnum._generate_next_value_(name, 0, count, last_values)


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


class IntegrationCommands(CommandEnum):
    """Command names for Integration calls that can be received from NTS."""
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


class Permissions(CommandEnum):
    # Reset enum counter for Python 2.7
    reset_auto()
    local_files_access = auto()
