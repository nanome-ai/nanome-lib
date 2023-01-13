import sys
from nanome._internal.enum_utils import IntEnum
import logging
from enum import Enum


logger = logging.getLogger(__name__)


# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome


class Commands(int, Enum):

    # Control
    connect = 0
    run = 1
    advanced_settings = 2

    # UI
    menu_toggle = 3
    button_press =4
    button_hover =5 
    slider_release =6 
    text_submit =7 
    text_change =8
    slider_change =9
    image_press =10 
    image_hold =11
    image_release =12
    dropdown_item_click =13 
    menu_transform_response =14 
 
    # Structure
    workspace_response = 15
    complex_list_response = 16
    complexes_response = 17 
    substructure_response = 18
    structures_deep_update_done = 19 
    add_to_workspace_done = 20
    position_structures_done = 21
    complex_add = 22
    complex_remove = 23
    bonds_add_done = 24
    dssp_add_done = 25
    complex_updated = 26
    selection_changed = 27
    compute_hbonds_done = 28
 
    # Stream
    stream_create_done = 29
    stream_feed = 30
    stream_feed_done = 31
    stream_interrupt = 32

    # File deprecated
    directory_response = 33
    file_response = 34
    file_save_done = 35
    export_files_result = 36

    # Files
    print_working_directory_response = 37
    cd_response = 38
    ls_response = 39
    mv_response = 40
    cp_response = 41
    get_response = 42
    put_response = 43
    rm_response = 44
    rmdir_response = 45
    mkdir_response = 46
 
    # Macro
    get_macros_response = 47
    run_macro_result = 48

    # Presenter
    presenter_info_response = 49
    presenter_change = 50
    controller_transforms_response = 51

    # Shapes
    set_shape_result = 52
    delete_shape_result = 53

    # Other
    add_volume_done = 54
    load_file_done = 55
    integration = 56

# /!\ /!\ /!\
# Values names are really important here, as they are hashed, and need to match Nanome


class Messages(int, Enum):
    # Control
    connect = 0
    plugin_list_button_set = 1

    # UI
    menu_update = 2
    content_update = 3
    node_update = 4
    menu_transform_set = 5
    menu_transform_request = 6
    notification_send = 7
    hook_ui_callback = 8

    # Structure
    structures_deep_update = 9
    structures_shallow_update = 10
    structures_zoom = 11
    structures_center = 12
    workspace_update = 13
    workspace_request = 14
    add_to_workspace = 15
    complexes_request = 16
    complex_list_request = 17
    substructure_request = 18
    bonds_add = 19
    dssp_add = 20
    hook_complex_updated = 21
    hook_selection_changed = 22
    compute_hbonds = 23

    # Streams
    stream_create = 24
    stream_feed = 25
    stream_destroy = 26

    # Files Deprecated
    directory_request = 27
    file_request = 28
    file_save = 29
    export_files = 30

    # Files
    print_working_directory = 31
    cd = 32
    ls = 33
    mv = 34
    get = 35
    put = 36
    rm = 37
    rmdir = 38
    mkdir = 39
    cp = 40

    # Macro
    save_macro = 41
    delete_macro = 42
    run_macro = 43
    stop_macro = 44
    get_macros = 45

    # Presenter
    presenter_info_request = 46
    controller_transforms_request = 47

    # Shapes
    set_shape = 48
    delete_shape = 49

    # Other
    add_volume = 50
    open_url = 51
    load_file = 52
    integration = 53
    set_skybox = 54
    apply_color_scheme = 55


class IntegrationCommands(IntEnum):
    """Command names for Integration calls that can be received from NTS."""
    hydrogen_add = 0
    hydrogen_remove = 1
    structure_prep = 2
    calculate_esp = 3
    minimization_start = 4
    minimization_stop = 5
    export_locations = 6
    generate_molecule_image = 7
    export_file = 8
    import_file = 9
    export_smiles = 10
    import_smiles = 11


class Permissions(IntEnum):
    local_files_access = 0
