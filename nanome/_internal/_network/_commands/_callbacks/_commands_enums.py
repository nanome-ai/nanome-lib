from nanome.util import IntEnum

class _Commands(IntEnum):
    connect = 0
    run = 1
    receive_workspace = 2
    receive_complex_list = 3 
    #UI callbacks======
    receive_menu = 4 
    menu_toggled = 5
    button_pressed = 6
    slider_released = 7
    text_submit = 8
    text_changed = 9 #TEST   
    slider_changed = 10 #TEST
    #Other callbacks
    receive_complexes = 11
    advanced_settings = 12
    receive_directory = 13
    receive_file = 14
    receive_file_save_result = 15
    complex_added = 16
    complex_removed = 17

class _Messages(IntEnum):
    connect = 0
    request_workspace = 1
    request_complex_list = 2 
    update_workspace =3 
    #4 free
    update_menu = 5 
    update_content = 6 
    request_complexes = 7
    add_to_workspace = 8
    request_directory = 9
    request_file = 10
    save_file = 11
    set_plugin_list_button = 12
    update_structures_deep = 13
    update_structures_shallow = 14
    send_notification = 25
