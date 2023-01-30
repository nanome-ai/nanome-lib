import json
import os
import unittest

from nanome import util
from nanome._internal import network
from nanome._internal.enums import Messages
from nanome.api.serializers import CommandMessageSerializer
from nanome.api import structure, shapes, ui
from nanome.util import enums

test_assets = os.getcwd() + ("/testing/test_assets")


class CommandDeserializerTestCase(unittest.TestCase):

    def setUp(self):
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)
        self.serializer = CommandMessageSerializer()

    def test_registered_commands(self):
        self.assertEqual(len(self.serializer._commands), 57)

    def test_deserialize_command(self):
        """Test that we can deserialze bytes from test ReceiveWorkspace Message."""
        bytes_file = os.path.join(test_assets, "ReceiveWorkspaceMessage.bin")
        with open(bytes_file, 'rb') as f:
            payload = f.read()
        received_object, command_hash, request_id = self.serializer.deserialize_command(payload, self.version_table)
        self.assertTrue(isinstance(received_object, structure.Workspace))
        self.assertEqual(command_hash, 783319662)
        self.assertEqual(request_id, 2)

    def test_deserialize_integration_command(self):
        """Test that we can deserialze bytes from test StructurePrep Integeration."""
        bytes_file = os.path.join(test_assets, "structureprep.bin")
        with open(bytes_file, 'rb') as f:
            payload = f.read()
        request_id, command_hash, received_obj_list = self.serializer.deserialize_command(payload, self.version_table)[0]
        self.assertTrue(isinstance(received_obj_list[0], structure.Complex))
        self.assertEqual(command_hash, 660242612)
        self.assertEqual(request_id, 7)


class MessageSerializeTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin_id = 7
        self.request_id = 1
        self.serializer = CommandMessageSerializer()
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            self.version_table = json.load(f)

    def test_registered_messages(self):
        self.assertEqual(len(self.serializer._messages), 56)

    def test_connect(self):
        message_type = Messages.connect
        arg = None
        expects_response = True
        args = [network.Packet.packet_type_plugin_connection, self.version_table]
        payload = self.serializer.serialize_message(self.request_id, message_type, arg, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_plugin_list_button_set(self):
        message_type = Messages.plugin_list_button_set
        arg = [enums.PluginListButtonType.run, "Button Text!", True]
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, arg, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_serialize_message_complex_list_request(self):
        """Test that the serializer returns a set of bytes."""
        message_type = Messages.complex_list_request
        arg = None
        version_table = self.version_table
        expects_response = False
        context = self.serializer.serialize_message(self.request_id, message_type, arg, version_table, expects_response)
        self.assertTrue(isinstance(context, memoryview))

    def test_serialize_message_menu_update(self):
        """Test that the serializer returns a set of bytes."""
        message_type = Messages.menu_update
        menu = ui.Menu.io.from_json(os.path.join(test_assets, "test_menu_smina.json"))
        shallow = False
        args = [menu, shallow]
        version_table = self.version_table
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_content_update(self):
        """Test that the serializer returns a set of bytes."""
        message_type = Messages.content_update
        args = [ui.Button(), ui.Slider()]
        version_table = self.version_table
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_node_update(self):
        message_type = Messages.node_update
        args = [ui.LayoutNode()]
        version_table = self.version_table
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_menu_transform_set(self):
        message_type = Messages.menu_transform_set
        menu_index = 1
        position = util.Vector3(0, 0, 0)
        rotation = util.Quaternion(0, 0, 0, 1)
        scale = util.Vector3(1, 1, 1)
        args = [menu_index, position, rotation, scale]
        version_table = self.version_table
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_menu_transform_request(self):
        message_type = Messages.menu_transform_request
        menu_index = 1
        args = menu_index
        version_table = self.version_table
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_structures_deep_update(self):
        message_type = Messages.structures_deep_update
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_structures_shallow_update(self):
        message_type = Messages.structures_shallow_update
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_structures_zoom(self):
        message_type = Messages.structures_zoom
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_structures_center(self):
        message_type = Messages.structures_center
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_workspace_update(self):
        message_type = Messages.workspace_update
        workspace = structure.Workspace()
        workspace.complexes = [structure.Complex(), structure.Complex()]
        args = workspace
        expects_response = False
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_workspace_request(self):
        message_type = Messages.workspace_request
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_add_to_workspace(self):
        message_type = Messages.add_to_workspace
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_complexes_request(self):
        message_type = Messages.complexes_request
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_complex_list_request(self):
        message_type = Messages.complex_list_request
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_substructure_request(self):
        message_type = Messages.substructure_request
        molecule_index = 1
        args = [molecule_index, enums.SubstructureType.Protein]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_bonds_add(self):
        message_type = Messages.bonds_add
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_dssp_add(self):
        message_type = Messages.dssp_add
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_compute_hbonds(self):
        message_type = Messages.compute_hbonds
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_stream_create(self):
        message_type = Messages.stream_create
        atom_indices = [1, 2, 3]
        stream_type = enums.StreamType.color
        stream_direction = enums.StreamDirection.writing
        args = [stream_type, atom_indices, stream_direction]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_stream_feed(self):
        message_type = Messages.stream_feed
        stream_id = 1
        data = [1, 2, 3]
        data_type = enums.StreamDataType.float
        args = [stream_id, data, data_type]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_stream_destroy(self):
        message_type = Messages.stream_destroy
        stream_id = 1
        args = stream_id
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_presenter_info_request(self):
        message_type = Messages.presenter_info_request
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_controller_transforms_request(self):
        message_type = Messages.controller_transforms_request
        args = []
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_set_shape(self):
        message_type = Messages.set_shape
        args = [shapes.Sphere()]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_delete_shape(self):
        message_type = Messages.delete_shape
        shape_index = 2
        args = [shape_index]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_open_url(self):
        message_type = Messages.open_url
        use_desktop_browser = False
        args = ["nanome.ai", use_desktop_browser]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_set_skybox(self):
        message_type = Messages.set_skybox
        args = enums.SkyBoxes.Sunset
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))

    def test_apply_color_scheme(self):
        message_type = Messages.apply_color_scheme
        color_scheme = enums.ColorScheme.Rainbow
        color_scheme_target = enums.ColorSchemeTarget.All
        only_carbons = True
        args = [color_scheme, color_scheme_target, only_carbons]
        expects_response = True
        payload = self.serializer.serialize_message(self.request_id, message_type, args, self.version_table, expects_response)
        self.assertTrue(isinstance(payload, memoryview))
