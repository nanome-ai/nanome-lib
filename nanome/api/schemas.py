from marshmallow import fields
from nanome.api import structure
from nanome.util import enums
from . import structure_schemas as struct_schemas
from . import util_schemas


structure_schema_map = {
    structure.Atom: struct_schemas.AtomSchema(),
    structure.Bond: struct_schemas.BondSchema(),
    structure.Residue: struct_schemas.ResidueSchema(),
    structure.Chain: struct_schemas.ChainSchema(),
    structure.Molecule: struct_schemas.MoleculeSchema(),
    structure.Complex: struct_schemas.ComplexSchema(),
}


class RequestWorkspace:
    params = []
    output = struct_schemas.WorkspaceSchema()


class RequestComplexes:
    params = [fields.List(fields.Integer)]
    output = struct_schemas.ComplexSchema(many=True)


class RequestComplexList:
    params = []
    output = struct_schemas.ComplexSchema(many=True)


class UpdateStructuresShallow:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class UpdateStructuresDeep:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class UpdateWorkspace:
    params = [struct_schemas.WorkspaceSchema()]
    output = None


class SendNotification:
    params = [util_schemas.EnumField(enum=enums.NotificationTypes), fields.Str()]
    output = None


class ZoomOnStructures:
    params = [struct_schemas.StructureSchema(many=True)]
    output = None


class CenterOnStructures:
    params = [struct_schemas.StructureSchema(many=True)]
    output = None


class AddToWorkspace:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class AddBonds:
    params = [struct_schemas.ComplexSchema(many=True)]
    output = None


class OpenUrl:
    params = [fields.Str()]
    output = None


class CreateWritingStream:
    params = [fields.List(fields.Integer), fields.Integer()]
    output = struct_schemas.StreamSchema()


class StreamUpdate:
    params = [fields.Integer(), fields.List(fields.Integer)],
    output = None


class RequestPresenterInfo:
    params = []
    output = struct_schemas.PresenterInfoSchema()


class RequestControllerTransforms:
    params = []
    output = [
        util_schemas.Vector3Field(), util_schemas.QuaternionField(),
        util_schemas.Vector3Field(), util_schemas.QuaternionField(),
        util_schemas.Vector3Field(), util_schemas.QuaternionField()
    ]


api_function_definitions = {
    'request_workspace':RequestWorkspace(),
    'request_complexes': RequestComplexes(),
    'update_structures_shallow': UpdateStructuresShallow(),
    'update_structures_deep': UpdateStructuresDeep(),
    'request_complex_list': RequestComplexList(),
    'create_writing_stream': CreateWritingStream(),
    'stream_update': StreamUpdate(),
    'update_workspace': UpdateWorkspace(),
    'zoom_on_structures': ZoomOnStructures(),
    'send_notification': SendNotification(),
    'center_on_structures': CenterOnStructures(),
    'add_to_workspace': AddToWorkspace(),
    'add_bonds': AddBonds(),
    'open_url': OpenUrl(),
    'request_presenter_info': RequestPresenterInfo(),
    'request_controller_transforms': RequestControllerTransforms()
}
