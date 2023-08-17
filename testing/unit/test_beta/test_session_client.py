import asyncio
import json
import os
import unittest
from nanome.util import enums
from nanome.api import ui, structure
from nanome.beta.nanome_sdk.session import SessionClient
from nanome._internal.enums import Messages
from unittest.mock import MagicMock, patch, ANY


test_assets = os.getcwd() + ("/testing/test_assets")


class TestSessionClient(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        version_table_file = os.path.join(test_assets, "version_table_1_24_2.json")
        with open(version_table_file, 'r') as f:
            cls.version_table = json.load(f)
        cls.plugin_id = 21
        cls.session_id = 42

    def setUp(self):
        self.client = SessionClient(self.plugin_id, self.session_id, self.version_table)
        self.client.writer = MagicMock()

        # Mock request futs
        self.request_id = 1
        response_fut = asyncio.Future()
        response_fut.set_result(MagicMock())
        self.client.request_futs[self.request_id] = response_fut

    def test_send_message(self):
        # Use open url message to test client
        message_type = Messages.open_url
        url = "https://nanome.ai"
        desktop_browser = False
        expects_response = False
        args = (url, desktop_browser)

        self.client._send_message(message_type, args, expects_response)
        self.client.writer.write.assert_called_once()

    def test_update_menu(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            menu = ui.Menu()
            shallow = True
            expects_response = False
            self.client.update_menu(menu, shallow=shallow)
            mock_send_message.assert_called_once_with(Messages.menu_update, [menu, True], expects_response)

    async def test_request_complex_list(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            expects_response = True
            await self.client.request_complex_list()
            mock_send_message.assert_called_once_with(Messages.complex_list_request, None, expects_response)

    async def test_request_workspace(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            expects_response = True
            await self.client.request_workspace()
            mock_send_message.assert_called_once_with(Messages.workspace_request, None, expects_response)

    async def test_request_complexes(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            comp_indices = [1, 2, 3]  # comp indices
            expects_response = True
            await self.client.request_complexes(comp_indices)
            mock_send_message.assert_called_once_with(Messages.complexes_request, comp_indices, expects_response)

    def test_update_workspace(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            workspace = structure.Workspace()
            expects_response = False
            self.client.update_workspace(workspace)
            mock_send_message.assert_called_once_with(Messages.workspace_update, [workspace], expects_response)

    async def test_send_notification(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            notification_type = enums.NotificationTypes.success
            message = 'test notification'
            expects_response = False
            await self.client.send_notification(notification_type, message)
            mock_send_message.assert_called_once_with(Messages.notification_send, [notification_type, message], expects_response)

    async def test_update_structures_deep(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            atom = structure.Atom()
            comp = structure.Complex()
            expects_response = True
            await self.client.update_structures_deep([atom, comp])
            mock_send_message.assert_called_once_with(Messages.structures_deep_update, [atom, comp], expects_response)

    def test_update_structures_shallow(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            atom = structure.Atom()
            comp = structure.Complex()
            expects_response = True
            self.client.update_structures_shallow([atom, comp])
            mock_send_message.assert_called_once_with(Messages.structures_shallow_update, [atom, comp], expects_response)

    def test_zoom_on_structures(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            atom = structure.Atom()
            expects_response = False
            self.client.zoom_on_structures([atom])
            mock_send_message.assert_called_once_with(Messages.structures_zoom, [atom], expects_response)

    def test_center_on_structures(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            atom = structure.Atom()
            expects_response = False
            self.client.center_on_structures([atom])
            mock_send_message.assert_called_once_with(Messages.structures_center, [atom], expects_response)

    async def test_add_to_workspace(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            comp = structure.Complex()
            expects_response = True
            await self.client.add_to_workspace([comp])
            mock_send_message.assert_called_once_with(Messages.add_to_workspace, [comp], expects_response)

    async def test_remove_from_workspace(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            comp = structure.Complex()
            expects_response = True
            await self.client.remove_from_workspace([comp])
            mock_send_message.assert_called_once_with(Messages.structures_deep_update, [ANY], expects_response)

    def test_update_content(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            btn = ui.Button()
            expects_response = False
            self.client.update_content(btn)
            mock_send_message.assert_called_once_with(Messages.content_update, [btn], expects_response)

    def test_update_node(self):
        with patch.object(self.client, '_send_message') as mock_send_message:
            mock_send_message.return_value = self.request_id
            ln = ui.LayoutNode()
            expects_response = False
            self.client.update_node(ln)
            mock_send_message.assert_called_once_with(Messages.node_update, (ln,), expects_response)
