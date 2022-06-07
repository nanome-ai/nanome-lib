import os
import nanome
from nanome.util import async_callback
from nanome.api import schemas

# Config

NAME = "Serialize Workspace"
DESCRIPTION = "Load workspace and serialize as JSON."
HAS_ADVANCED_OPTIONS = False
CATEGORY = 'Testing'

# Plugin


class SerializeWorkspace(nanome.AsyncPluginInstance):

    @async_callback
    async def start(self):
        ws = await self.request_workspace()
        ws_schema = schemas.WorkspaceSchema()
        json_data = ws_schema.dumps(ws)
        file_path = os.path.join(os.getcwd(), 'serialized_workspace.json')
        with open(file_path, 'w') as f:
            f.write(json_data)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, SerializeWorkspace)
