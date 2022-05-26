from marshmallow import fields, Schema, post_load
from .util_schemas import EnumField
from nanome.util import enums
from nanome.api import ui


class PositionSchema(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()


class ColorField(fields.Int):
    pass


class ButtonSchema(Schema):
    type_name = fields.String(required=True)
    selected = fields.Bool()
    unusable = fields.Bool()
    text_active = fields.Bool()
    text_value_idle = fields.String()
    text_value_selected = fields.String()
    text_value_highlighted = fields.String()
    text_value_selected_highlighted = fields.String()
    text_value_unusable = fields.String()
    text_auto_size = fields.Bool()
    text_min_size = fields.Float()
    text_max_size = fields.Float()
    text_size = fields.Float()
    text_underlined = fields.Bool()
    text_bolded = fields.Bool()
    text_vertical_align = EnumField(enum=enums.VertAlignOptions)
    text_horizontal_align = EnumField(enum=enums.HorizAlignOptions)
    type_name = fields.String()
    text_ellipsis = fields.Boolean()
    text_bold_idle = fields.Bool()
    text_bold_selected = fields.Bool()
    text_bold_highlighted = fields.Bool()
    text_bold_selected_highlighted = fields.Bool()
    text_bold_unusable = fields.Bool()
    text_color_idle = fields.Int()
    text_color_selected = fields.Int()
    text_color_highlighted = fields.Int()
    text_color_selected_highlighted = fields.Int()
    text_color_unusable = fields.Int()
    text_padding_top = fields.Float()
    text_padding_bottom = fields.Float()
    text_padding_left = fields.Float()
    text_padding_right = fields.Float()
    text_line_spacing = fields.Float()

    icon_active = fields.Bool()
    icon_color_idle = fields.Int()
    icon_color_selected = fields.Int()
    icon_color_highlighted = fields.Int()
    icon_color_selected_highlighted = fields.Int()
    icon_color_unusable = fields.Int()
    icon_sharpness = fields.Float()
    icon_size = fields.Float()
    icon_ratio = fields.Float()
    icon_position = fields.Nested(PositionSchema)
    icon_rotation = fields.Nested(PositionSchema)

    mesh_active = fields.Boolean()
    mesh_enabled_idle = fields.Boolean()
    mesh_enabled_selected = fields.Boolean()
    mesh_enabled_highlighted = fields.Boolean()
    mesh_enabled_selected_highlighted = fields.Boolean()
    mesh_enabled_unusable = fields.Boolean()
    mesh_color_idle = ColorField()
    mesh_color_selected = ColorField()
    mesh_color_highlighted = ColorField()
    mesh_color_selected_highlighted = ColorField()
    mesh_color_unusable = ColorField()
    outline_active = fields.Boolean()
    outline_size_idle = fields.Float()
    outline_size_selected = fields.Float()
    outline_size_highlighted = fields.Float()
    outline_size_selected_highlighted = fields.Float()
    outline_size_unusable = fields.Float()
    outline_color_idle = ColorField()
    outline_color_selected = ColorField()
    outline_color_highlighted = ColorField()
    outline_color_selected_highlighted = ColorField()
    outline_color_unusable = ColorField()
    tooltip_title = fields.String()
    tooltip_content = fields.String()
    tooltip_bounds = fields.Nested(PositionSchema)
    tooltip_positioning_target = fields.Integer()
    tooltip_positioning_origin = fields.Integer()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Button()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj

class MeshSchema(Schema):
    type_name = fields.String(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Mesh()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class ImageSchema(Schema):
    type_name = fields.String(required=True)
    
    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Image()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class LoadingBarSchema(Schema):
    type_name = fields.String(required=True)
    percentage = fields.Float()
    title = fields.Str()
    description = fields.Str()
    failure = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.LoadingBar()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class LabelSchema(Schema):
    type_name = fields.String(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Label()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class TextInputSchema(Schema):
    type_name = fields.String(required=True)
    max_length = fields.Int()
    placeholder_text = fields.Str()
    input_text = fields.Str()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.TextInput()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class SliderSchema(Schema):
    type_name = fields.String(required=True)
    current_value = fields.Float()
    min_value = fields.Float()
    max_value = fields.Float()
    type_name = fields.String()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Slider()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class DropdownSchema(Schema):
    type_name = fields.String(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Dropdown()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj


class DropdownItemSchema(Schema):
    type_name = fields.String(required=True)
    pass


class UIListSchema(Schema):
    type_name = fields.String(required=True)
    display_columns = fields.Int()
    display_rows = fields.Int()
    total_columns = fields.Int()
    unusable = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.UIList()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj

class ContentSchema(Schema):
    """Uses the type_name field to identify the type of content to be loaded/dumped."""
    type_name = fields.String(required=True)
    type_name_schemas = {
        'Button': ButtonSchema(),
        'Mesh': MeshSchema(),
        'Image': ImageSchema(),
        'Label': LabelSchema(),
        'Text Input': TextInputSchema(),
        'Slider': SliderSchema(),
        'Dropdown': DropdownSchema(),
        'DropdownItem': DropdownItemSchema(),
        'List': UIListSchema(),
        'LoadingBar': LoadingBarSchema()
    }

    def load(self, data, *args, **kwargs):
        type_name = data['type_name']
        correct_schema = self.type_name_schemas[type_name]
        return correct_schema.load(data, *args, **kwargs)


class LayoutNodeSchema(Schema):
    name = fields.String()
    enabled = fields.Boolean()
    layer = fields.Int()
    layout_orientation = EnumField(enum=enums.LayoutTypes)
    sizing_type = EnumField(enum=enums.SizingTypes)
    sizing_value = fields.Float()
    forward_dist = fields.Float()
    padding_type = EnumField(enum=enums.PaddingTypes)
    padding_x = fields.Float()
    padding_y = fields.Float()
    padding_z = fields.Float()
    padding_w = fields.Float()
    children = fields.List(fields.Nested(lambda: LayoutNodeSchema()))
    content = fields.Nested(lambda: ContentSchema(), allow_none=True)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.LayoutNode()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        for child in new_obj.children:
            child._parent = new_obj
        return new_obj


class MenuSchema(Schema):
    is_menu = fields.Bool(default=True)
    title = fields.String()
    width = fields.Float(max=1.0)
    height = fields.Float(max=1.0)
    version = fields.Int(default=0)
    effective_root = fields.Nested(LayoutNodeSchema, attribute='root')

    @post_load
    def make_menu(self, data, **kwargs):
        new_obj = ui.Menu()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        # new_obj.root = new_obj.effective_root
        return new_obj
