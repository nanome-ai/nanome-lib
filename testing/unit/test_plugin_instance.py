import os
import sys
import unittest
import uuid

from nanome import PluginInstance
from nanome.api.plugin_instance import _DefaultPlugin
from nanome.api import structure, ui
from nanome.util import enums, Vector3, Quaternion, config

if sys.version_info.major >= 3:
    from unittest.mock import MagicMock
else:
    # Python 2.7 way of getting magicmock. Requires pip install mock
    from mock import MagicMock


class PluginInstanceTestCase(unittest.TestCase):

    def setUp(self):
        self.custom_data = {'a': 'b'}
        self.plugin_instance = PluginInstance()
        # Mock args that are passed to setup plugin instance networking
        session_id = plugin_network = pm_queue_in = pm_queue_out = \
            log_pipe_conn = original_version_table = permissions = MagicMock()

        self.plugin_instance._setup(
            session_id, plugin_network, pm_queue_in, pm_queue_out, log_pipe_conn,
            original_version_table, self.custom_data, permissions
        )
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
        url = 'nanome.ai'
        self.plugin_instance.open_url(url, desktop_browser=True)
        self.plugin_instance.open_url(url, desktop_browser=False)

    def test_plugin_files_path(self):
        # Change config to be a file that doesn't exist, so we test creating new directory.
        starting_file_path = config.fetch('plugin_files_path')
        new_file_path = '/tmp/' + str(uuid.uuid4())
        config.set('plugin_files_path', new_file_path)
        self.plugin_instance.plugin_files_path
        config.set('plugin_files_path', starting_file_path)

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
        entity = structure.Complex()
        self.plugin_instance.request_export(enums.ExportFormats.SDF, entities=entity)

    def test_request_files(self):
        self.plugin_instance.request_files([])

    def test_request_menu_transform(self):
        self.plugin_instance.request_menu_transform(0)

    def test_request_presenter_info(self):
        self.plugin_instance.request_presenter_info()

    def test_menu(self):
        self.plugin_instance.menu
        self.plugin_instance.menu = ui.Menu()
        self.plugin_instance.menu

    def test_request_workspace(self):
        self.plugin_instance.request_workspace()

    def test_save_files(self):
        self.plugin_instance.save_files([])

    def test_send_files_to_load(self):
        test_assets = os.getcwd() + ("/testing/test_assets")
        test_path = test_assets + "/test_menu.json"
        # Test different input formats supported by function
        file_list = [test_path]
        test_tuple = (test_path, 'test_menu.json')
        self.plugin_instance.send_files_to_load(file_list)
        self.plugin_instance.send_files_to_load(test_path)
        self.plugin_instance.send_files_to_load(test_tuple)

    def test_send_notification(self):
        notif_type = enums.NotificationTypes.success
        msg = 'Success!'
        self.plugin_instance.send_notification(notif_type, msg)

    def test_set_menu_transform(self):
        index = 1
        position = Vector3(0, 0, 0)
        rotation = Quaternion(1, 1, 1, 1)
        scale = Vector3(1, 2, 3)
        self.plugin_instance.set_menu_transform(index, position, rotation, scale)

    def test_set_plugin_list_button(self):
        btn_type = enums.PluginListButtonType.run
        self.plugin_instance.set_plugin_list_button(btn_type)
        advanced_settings_btn_type = enums.PluginListButtonType.advanced_settings
        self.plugin_instance.set_plugin_list_button(
            advanced_settings_btn_type, text='test_text', usable=True)

    def test_start(self):
        self.plugin_instance.start()

    def test_update(self):
        self.plugin_instance.update()

    def test_update_content(self):
        btn = ui.Button()
        self.plugin_instance.update_content(btn)
        self.plugin_instance.update_content([btn])

    def test_update_menu(self):
        menu = ui.Menu()
        self.plugin_instance.update_menu(menu)

    def test_update_node(self):
        node = ui.LayoutNode()
        self.plugin_instance.update_node(node)
        self.plugin_instance.update_node([node])

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

    def test_default_plugin(self):
        # Make sure we can instantiate _DefaultPlugin
        default_plugin = _DefaultPlugin()
        self.assertTrue(isinstance(default_plugin, PluginInstance))

    def test_custom_data(self):
        self.assertEqual(self.plugin_instance.custom_data, self.custom_data)
