"""Define the parameters and output structure of the Plugin APIs.

Not sure what to do with these yet.
"""

from marshmallow import fields
from nanome.util import enums
from . import structure_schemas as struct_schemas
from . import util_schemas

__all__ = [
    'RequestWorkspace',
    'RequestComplexes',
    'RequestComplexList',
    'UpdateStructuresShallow',
    'UpdateStructuresDeep',
    'UpdateWorkspace',
    'SendNotification',
    'ZoomOnStructures',
    'CenterOnStructures',
    'AddToWorkspace',
    'AddBonds',
    'OpenUrl',
    'CreateWritingStream',
    'StreamUpdate',
    'RequestPresenterInfo',
    'RequestControllerTransforms',
]


class RequestWorkspaceSchema:
    params = []
    output = struct_schemas.WorkspaceSchema()


class RequestComplexesSchema:
    params = [fields.List(fields.Integer)]
    output = struct_schemas.ComplexSchema(many=True)


class RequestComplexListSchema:
    params = []
    output = struct_schemas.ComplexSchema(many=True)


class UpdateStructuresShallowSchema:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class UpdateStructuresDeepSchema:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class UpdateWorkspaceSchema:
    params = [struct_schemas.WorkspaceSchema()]
    output = None


class SendNotificationSchema:
    params = [util_schemas.EnumField(enum=enums.NotificationTypes), fields.Str()]
    output = None


class ZoomOnStructuresSchema:
    params = [struct_schemas.StructureSchema(many=True)]
    output = None


class CenterOnStructuresSchema:
    params = [struct_schemas.StructureSchema(many=True)]
    output = None


class AddToWorkspaceSchema:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class AddBondsSchema:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class OpenUrlSchema:
    params = [fields.Str()]
    output = None


class CreateWritingStreamSchema:
    params = [fields.List(fields.Integer), fields.Integer()]
    output = struct_schemas.StreamSchema()


class StreamUpdateSchema:
    params = [fields.Integer(), fields.List(fields.Integer)],
    output = None


class RequestPresenterInfoSchema:
    params = []
    output = struct_schemas.PresenterInfoSchema()


class RequestControllerTransformsSchema:
    params = []
    output = [
        util_schemas.Vector3Field(), util_schemas.QuaternionField(),
        util_schemas.Vector3Field(), util_schemas.QuaternionField(),
        util_schemas.Vector3Field(), util_schemas.QuaternionField()
    ]


API_DEFINTION_MAP = {
    'request_workspace':RequestWorkspaceSchema(),
    'request_complexes': RequestComplexesSchema(),
    'update_structures_shallow': UpdateStructuresShallowSchema(),
    'update_structures_deep': UpdateStructuresDeepSchema(),
    'request_complex_list': RequestComplexListSchema(),
    'create_writing_stream': CreateWritingStreamSchema(),
    'stream_update': StreamUpdateSchema(),
    'update_workspace': UpdateWorkspaceSchema(),
    'zoom_on_structures': ZoomOnStructuresSchema(),
    'send_notification': SendNotificationSchema(),
    'center_on_structures': CenterOnStructuresSchema(),
    'add_to_workspace': AddToWorkspaceSchema(),
    'add_bonds': AddBondsSchema(),
    'open_url': OpenUrlSchema(),
    'request_presenter_info': RequestPresenterInfoSchema(),
    'request_controller_transforms': RequestControllerTransformsSchema()
}
