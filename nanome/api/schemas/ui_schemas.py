from marshmallow import fields, Schema, post_load
from operator import attrgetter

from nanome.util import enums, Color
from nanome.api import ui
from .util_schemas import EnumField


def init_object(obj, data: dict):
    for key in data:
        try:
            setattr(obj, key, data[key])
        except AttributeError:
            raise AttributeError('Could not set attribute {}'.format(key))


class FloatRoundedField(fields.Float):
    """If decimal part of float is 0, round to int."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value % 1 == 0:
            return int(value)
        else:
            return round(value, 5)


class PositionSchema(Schema):
    x = FloatRoundedField()
    y = FloatRoundedField()
    z = FloatRoundedField()


class ColorField(fields.Field):

    def _serialize(self, value: Color, attr, obj, **kwargs):
        return value._color

    def _deserialize(self, value, attr, data, **kwargs):
        return Color.from_int(value)


def create_multi_state_schema(field_class):
    """Create a schema that can serialize a MultiStateVariable  the provided type."""
    return Schema.from_dict({
        'idle': field_class(),
        'selected': field_class(),
        'highlighted': field_class(),
        'selected_highlighted': field_class(),
        'unusable': field_class(),
        'default': field_class(),
    })()


class ButtonSchema(Schema):
    name = fields.String()
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
    text_min_size = FloatRoundedField()
    text_max_size = FloatRoundedField()
    text_size = FloatRoundedField()
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
    text_color_idle = ColorField()
    text_color_selected = ColorField()
    text_color_highlighted = ColorField()
    text_color_selected_highlighted = ColorField()
    text_color_unusable = ColorField()
    text_padding_top = FloatRoundedField()
    text_padding_bottom = FloatRoundedField()
    text_padding_left = FloatRoundedField()
    text_padding_right = FloatRoundedField()
    text_line_spacing = FloatRoundedField()

    icon_active = fields.Bool()
    icon_color_idle = ColorField()
    icon_color_selected = ColorField()
    icon_color_highlighted = ColorField()
    icon_color_selected_highlighted = ColorField()
    icon_color_unusable = ColorField()
    icon_sharpness = FloatRoundedField()
    icon_size = FloatRoundedField()
    icon_ratio = FloatRoundedField()
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
    outline_size_idle = FloatRoundedField()
    outline_size_selected = FloatRoundedField()
    outline_size_highlighted = FloatRoundedField()
    outline_size_selected_highlighted = FloatRoundedField()
    outline_size_unusable = FloatRoundedField()
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

    def load(self, data, *args, **kwargs):
        data = dict(data)
        text_values = {
            'idle': data.pop('text_value_idle'),
            'selected': data.pop('text_value_selected'),
            'highlighted': data.pop('text_value_highlighted'),
            'selected_highlighted': data.pop('text_value_selected_highlighted'),
            'unusable': data.pop('text_value_unusable'),
        }
        outline_data = any([key.startswith('outline') for key in data.keys()])
        if outline_data:
            outline_values = {
                'active': data.pop('outline_active'),
                'size': {
                    'idle': data.pop('outline_size_idle'),
                    'selected': data.pop('outline_size_selected'),
                    'highlighted': data.pop('outline_size_highlighted'),
                    'selected_highlighted': data.pop('outline_size_selected_highlighted'),
                    'unusable': data.pop('outline_size_unusable'),
                },
                'color': {
                    'idle': data.pop('outline_color_idle'),
                    'selected': data.pop('outline_color_selected'),
                    'highlighted': data.pop('outline_color_highlighted'),
                    'selected_highlighted': data.pop('outline_color_selected_highlighted'),
                    'unusable': data.pop('outline_color_unusable'),
                }
            }
        btn = super().load(data, *args, **kwargs)
        schema = create_multi_state_schema(fields.String)
        multi_state_text = schema.load(text_values)
        btn.text.value.set_all("")  # Makes default empty string.
        btn.text.value.set_each(**multi_state_text)
        if outline_data:
            multi_state_color = create_multi_state_schema(ColorField).load(outline_values['color'])
            multi_state_size = create_multi_state_schema(FloatRoundedField).load(outline_values['size'])
            btn.outline.color.set_each(**multi_state_color)
            btn.outline.size.set_each(**multi_state_size)
        return btn

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Button()
        for key in data:
            try:
                setattr(new_obj, key, data[key])
            except AttributeError:
                raise AttributeError('Could not set attribute {}'.format(key))
        return new_obj

    def get_attribute(self, obj, attr, default):
        """If attr doesn't exist, search for it in nested objects.

        This works because the nested multi state values were named in 
        a way that you can replace underscores with dots to access them 
        from the root button
        """
        if hasattr(obj, attr):
            return getattr(obj, attr)
        dotted_path = attr.replace('_', '.')
        # Field names that contain underscores need to be switched back from dots.
        underscore_fields = [
            'selected.highlighted',
            'line.spacing',
            'positioning.target',
            'positioning.origin',
            'padding.top',
            'padding.bottom',
            'padding.left',
            'padding.right',
        ]
        for field_name in underscore_fields:
            if field_name in dotted_path:
                proper_field_name = field_name.replace('.', '_')
                dotted_path = dotted_path.replace(field_name, proper_field_name)
        output = attrgetter(dotted_path)(obj)
        return output


class MeshSchema(Schema):
    type_name = fields.String(required=True)
    mesh_color = ColorField()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Mesh()
        init_object(new_obj, data)
        return new_obj


class ImageSchema(Schema):
    type_name = fields.String(required=True)
    color = ColorField()
    file_path = fields.String()
    scaling_option = EnumField(enum=enums.ScalingOptions)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Image()
        init_object(new_obj, data)
        return new_obj


class LoadingBarSchema(Schema):
    type_name = fields.String(required=True)
    percentage = FloatRoundedField()
    title = fields.Str()
    description = fields.Str()
    failure = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.LoadingBar()
        init_object(new_obj, data)
        return new_obj


class LabelSchema(Schema):
    type_name = fields.String(required=True)
    text = fields.String(attribute='text_value')
    text_vertical_align = EnumField(enum=enums.VertAlignOptions)
    text_horizontal_align = EnumField(enum=enums.HorizAlignOptions)
    text_auto_size = fields.Bool()
    text_max_size = FloatRoundedField()
    text_min_size = FloatRoundedField()
    text_size = FloatRoundedField()
    text_color = ColorField()
    text_bold = fields.Bool()
    text_italics = fields.Bool()
    text_underlined = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Label()
        init_object(new_obj, data)
        return new_obj


class TextInputSchema(Schema):
    type_name = fields.String(required=True)
    max_length = fields.Int()
    placeholder_text = fields.Str()
    placeholder_text_color = ColorField()
    text_color = ColorField()
    background_color = ColorField()
    text_size = FloatRoundedField()
    text_horizontal_align = EnumField(enum=enums.HorizAlignOptions)
    text_vertical_align = EnumField(enum=enums.VertAlignOptions)
    padding_left = FloatRoundedField()
    padding_right = FloatRoundedField()
    padding_top = FloatRoundedField()
    padding_bottom = FloatRoundedField()
    password = fields.Bool()
    number = fields.Bool()
    multi_line = fields.Bool()
    input_text = fields.Str()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.TextInput()
        init_object(new_obj, data)
        return new_obj


class SliderSchema(Schema):
    type_name = fields.String(required=True)
    current_value = FloatRoundedField()
    min_value = FloatRoundedField()
    max_value = FloatRoundedField()
    type_name = fields.String()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Slider()
        init_object(new_obj, data)
        return new_obj


class DropdownItemSchema(Schema):
    name = fields.String()
    close_on_selected = fields.Bool()
    selected = fields.Bool()


class DropdownSchema(Schema):
    type_name = fields.String(required=True)
    permanent_title = fields.String()
    use_permanent_title = fields.Bool()
    max_displayed_items = fields.Integer(min=0)
    items = fields.List(fields.Nested(DropdownItemSchema))
    unusable = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Dropdown()
        init_object(new_obj, data)
        return new_obj


class UIListSchema(Schema):
    type_name = fields.String(required=True)
    display_columns = fields.Int()
    display_rows = fields.Int()
    total_columns = fields.Int()
    unusable = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.UIList()
        init_object(new_obj, data)
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
        'TextInput': TextInputSchema(),
        'Slider': SliderSchema(),
        'Dropdown': DropdownSchema(),
        'List': UIListSchema(),
        'LoadingBar': LoadingBarSchema()
    }

    def load(self, data, *args, **kwargs):
        type_name = data['type_name']
        correct_schema = self.type_name_schemas[type_name]
        return correct_schema.load(data, *args, **kwargs)

    def dump(self, obj, *args, **kwargs):
        type_name = obj.type_name
        correct_schema = self.type_name_schemas[type_name]
        return correct_schema.dump(obj, *args, **kwargs)


class LayoutNodeSchema(Schema):
    name = fields.String()
    enabled = fields.Boolean()
    layer = fields.Int()
    layout_orientation = EnumField(enum=enums.LayoutTypes)
    sizing_type = EnumField(enum=enums.SizingTypes)
    sizing_value = FloatRoundedField()
    forward_dist = FloatRoundedField()
    padding_type = EnumField(enum=enums.PaddingTypes)
    padding_x = FloatRoundedField()
    padding_y = FloatRoundedField()
    padding_z = FloatRoundedField()
    padding_w = FloatRoundedField()
    children = fields.List(fields.Nested(lambda: LayoutNodeSchema()))
    content = fields.Nested(lambda: ContentSchema(), allow_none=True)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.LayoutNode()
        init_object(new_obj, data)
        for child in new_obj.children:
            child._parent = new_obj
        return new_obj


class MenuSchema(Schema):
    is_menu = fields.Bool(default=True)
    title = fields.String()
    width = FloatRoundedField(max=1.0)
    height = FloatRoundedField(max=1.0)
    version = fields.Int(default=0)
    effective_root = fields.Nested(LayoutNodeSchema, attribute='root')

    @post_load
    def make_menu(self, data, **kwargs):
        new_obj = ui.Menu()
        init_object(new_obj, data)
        return new_obj
