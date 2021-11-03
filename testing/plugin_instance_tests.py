import unittest
from unittest.mock import MagicMock

from nanome import PluginInstance

from nanome.api import structure, ui
from nanome.util import enums


class PluginInstanceTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin_instance = PluginInstance()

        # Attributes normally set by _PluginInstance Network Instantiation
        self.plugin_instance._run_text = "Run"
        self.plugin_instance._run_usable = True
        self.plugin_instance._advanced_settings_text = "Advanced Settings"
        self.plugin_instance._advanced_settings_usable = True
        self.plugin_instance._custom_data = {}
        self.plugin_instance._permissions = []
        self.plugin_instance._menus = {}

        self.plugin_instance._network = MagicMock()

    def test_on_advanced_settings(self):
        self.plugin_instance.on_advanced_settings()

    def test_on_complex_added(self):
        self.plugin_instance.on_complex_added()

    def test_on_complex_removed(self):
        self.plugin_instance.on_complex_removed()

    def test_on_presenter_change(self):
        self.plugin_instance.on_presenter_change()

    def test_on_run(self):
        self.plugin_instance.on_run()

    def test_on_stop(self):
        self.plugin_instance.on_stop()

    def test_add_bonds(self):
        comp = structure.Complex()
        self.plugin_instance.add_bonds([comp])

    def test_add_dssp(self):
        comp = structure.Complex()
        self.plugin_instance.add_dssp([comp])

    def test_add_to_workspace(self):
        comp = structure.Complex()
        self.plugin_instance.add_to_workspace([comp])

    def test_add_volume(self):
        comp = structure.Complex()
        volume = None
        properties = {}
        self.plugin_instance.add_volume(comp, volume, properties)

    def test_apply_color_scheme(self):
        color_scheme = enums.ColorScheme.Rainbow
        target = enums.ColorSchemeTarget.All
        only_carbons = False
        self.plugin_instance.apply_color_scheme(color_scheme, target, only_carbons)

    def test_center_on_structures(self):
        self.plugin_instance.center_on_structures([1])

    def test_create_atom_stream(self):
        index_list = [1, 2, 3]
        stream_type = enums.StreamType.color
        callback = None
        self.plugin_instance.create_atom_stream(index_list, stream_type, callback)

    def test_create_reading_stream(self):
        index_list = [1, 2, 3]
        stream_type = enums.StreamType.color
        self.plugin_instance.create_reading_stream(index_list, stream_type)

    def test_create_shape(self):
        shape_type = enums.ShapeType.Sphere
        self.plugin_instance.create_shape(shape_type)

    def test_create_stream(self):
        index_list = [1, 2, 3]
        stream_type = enums.StreamType.color
        self.plugin_instance.create_stream(index_list, stream_type)

    def test_create_writing_stream(self):
        index_list = [1, 2, 3]
        stream_type = enums.StreamType.color
        self.plugin_instance.create_writing_stream(index_list, stream_type)

    def test_open_url(self):
        url = 'https://nanome.ai'
        self.plugin_instance.open_url(url, desktop_browser=True)
        self.plugin_instance.open_url(url, desktop_browser=False)

    def test_plugin_files_path(self):
        self.plugin_instance.plugin_files_path

    def test_request_complex_list(self):
        self.plugin_instance.request_complex_list()

    def test_request_complexes(self):
        comp = structure.Complex()
        self.plugin_instance.request_complexes([comp.index])

    def test_request_controller_transforms(self):
        self.plugin_instance.request_controller_transforms()

    def test_request_directory(self):
        path = '/path/to/file'
        self.plugin_instance.request_directory(path)

    def test_request_export(self):
        self.plugin_instance.request_export(enums.ExportFormats.SDF)

    def test_request_files(self):
        self.plugin_instance.request_files([])

    def test_request_menu_transform(self):
        self.plugin_instance.request_menu_transform(0)

    def test_request_presenter_info(self):
        self.plugin_instance.request_presenter_info()

    def test_request_workspace(self):
        self.plugin_instance.request_workspace()

    def test_save_files(self):
        self.plugin_instance.save_files([])

    def test_send_files_to_load(self):
        self.plugin_instance.send_files_to_load([])

    def test_send_notification(self):
        notif_type = enums.NotificationTypes.success
        msg = 'Success!'
        self.plugin_instance.send_notification(notif_type, msg)

    def test_set_menu_transform(self):
        index = None
        position = None
        rotation = None
        scale = None
        self.plugin_instance.set_menu_transform(index, position, rotation, scale)

    def test_set_plugin_list_button(self):
        btn = ui.Button()
        self.plugin_instance.set_plugin_list_button(btn)

    def test_start(self):
        self.plugin_instance.start()

    def test_update(self):
        self.plugin_instance.update()

    def test_update_content(self):
        btn = ui.Button()
        self.plugin_instance.update_content(btn)

    def test_update_menu(self):
        menu = ui.Menu()
        self.plugin_instance.update_menu(menu)

    def test_update_node(self):
        node = ui.LayoutNode()
        self.plugin_instance.update_node(node)

    def test_update_structures_deep(self):
        comp = structure.Complex()
        self.plugin_instance.update_structures_deep([comp])

    def test_update_structures_shallow(self):
        comp = structure.Complex()
        self.plugin_instance.update_structures_shallow([comp])

    def test_update_workspace(self):
        workspace = structure.Workspace()
        self.plugin_instance.update_workspace(workspace)

    def test_zoom_on_structures(self):
        comp = structure.Complex()
        self.plugin_instance.zoom_on_structures([comp])
