from nanome.api import structure, schemas
from nanome.util import enums
from marshmallow import fields


structure_schema_map = {
    structure.Atom: schemas.AtomSchema(),
    structure.Bond: schemas.BondSchema(),
    structure.Residue: schemas.ResidueSchema(),
    structure.Chain: schemas.ChainSchema(),
    structure.Molecule: schemas.MoleculeSchema(),
    structure.Complex: schemas.ComplexSchema(),
}


class RequestWorkspace:
    params = []
    output = schemas.WorkspaceSchema()


class RequestComplexes:
    params = [fields.List(fields.Integer)]
    output = schemas.ComplexSchema(many=True)


class RequestComplexList:
    params = []
    output = schemas.ComplexSchema(many=True)


class UpdateStructuresShallow:
    params = [schemas.ComplexSchema(many=True)]
    output = None


class UpdateStructuresDeep:
    params = [schemas.ComplexSchema(many=True)]
    output = None


class UpdateWorkspace:
    params = [schemas.WorkspaceSchema()]
    output = None


class SendNotification:
    params = [schemas.EnumField(enum=enums.NotificationTypes), fields.Str()]
    output = None


class ZoomOnStructures:
    params = [schemas.StructureSchema(many=True, partial=True)]
    output = None


class CenterOnStructures:
    params = [schemas.StructureSchema(many=True)]
    output = None


class AddToWorkspace:
    params = [schemas.ComplexSchema(many=True)]
    output = None


class AddBonds:
    params = [schemas.ComplexSchema(many=True)]
    output = None


class OpenUrl:
    params = [fields.Str()]
    output = None


class CreateWritingStream:
    params = [fields.List(fields.Integer), fields.Integer()]
    output = schemas.StreamSchema()


class StreamUpdate:
    params = [fields.Integer(), fields.List(fields.Integer)]
    output = None


class RequestPresenterInfo:
    params = []
    output = schemas.PresenterInfoSchema()


class RequestControllerTransforms:
    params = []
    output = [
        schemas.Vector3Field(), schemas.QuaternionField(),
        schemas.Vector3Field(), schemas.QuaternionField(),
        schemas.Vector3Field(), schemas.QuaternionField()
    ]


class ApplyColorScheme:
    params = [
        schemas.EnumField(enum=enums.ColorScheme),
        schemas.EnumField(enum=enums.ColorSchemeTarget),
        fields.Boolean()
    ]
    output = None


api_function_definitions = {
    'request_workspace': RequestWorkspace(),
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
    'request_controller_transforms': RequestControllerTransforms(),
    'apply_color_scheme': ApplyColorScheme(),
}
