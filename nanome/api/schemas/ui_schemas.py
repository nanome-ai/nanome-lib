from marshmallow import fields, Schema, post_load, pre_dump

from nanome.util import enums, Color, Vector3
from nanome.api import ui
from .util_schemas import EnumField


def init_object(obj, data: dict):
    for key in data:
        if not hasattr(obj, key):
            continue
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


class Vector3Schema(Schema):
    x = FloatRoundedField()
    y = FloatRoundedField()
    z = FloatRoundedField()

    @post_load
    def make_vector3(self, data, **kwargs):
        new_obj = Vector3(**data)
        return new_obj


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


class ButtonTextSchema(Schema):
    value = create_multi_state_schema(fields.String)
    bold = fields.Boolean()
    color = ColorField()
    active = fields.Boolean()
    auto_size = fields.Boolean()
    min_size = fields.Float()
    max_size = fields.Float()
    size = fields.Float()
    underlined = fields.Boolean()
    ellipsis = fields.Boolean()
    padding_top = fields.Float()
    padding_bottom = fields.Float()
    padding_left = fields.Float()
    padding_right = fields.Float()
    line_spacing = fields.Float()
    vertical_align = EnumField(enum=enums.VertAlignOptions)
    horizontal_align = EnumField(enum=enums.HorizAlignOptions)


class ButtonIconSchema(Schema):
    value = create_multi_state_schema(fields.String)
    color = create_multi_state_schema(ColorField)
    active = fields.Boolean()
    sharpness = fields.Float(min=0, max=1)
    size = fields.Boolean()
    ratio = fields.Float(min=0, max=1)
    position = fields.Nested(PositionSchema)
    rotation = fields.Nested(PositionSchema)
    min_size = fields.Float()
    max_size = fields.Float()
    size = fields.Float()
    padding_top = fields.Float()
    padding_bottom = fields.Float()
    padding_left = fields.Float()
    padding_right = fields.Float()
    vertical_align = EnumField(enum=enums.VertAlignOptions)
    horizontal_align = EnumField(enum=enums.HorizAlignOptions)


class ButtonMeshSchema(Schema):
    color = ColorField()
    enabled = create_multi_state_schema(fields.Boolean)
    active = fields.Boolean()


class ButtonOutlineSchema(Schema):
    size = create_multi_state_schema(FloatRoundedField)
    color = ColorField()
    active = fields.Boolean()


class ButtonSwitchSchema(Schema):
    active = fields.Boolean()
    on_color = ColorField()
    off_color = ColorField()


class ButtonToolTipSchema(Schema):
    title = fields.String()
    content = fields.String()
    bounds = fields.Nested(Vector3Schema())
    positioning_target = EnumField(enum=enums.ToolTipPositioning)
    positioning_origin = EnumField(enum=enums.ToolTipPositioning)


class ButtonSchema(Schema):
    type_name = fields.String()
    name = fields.String()
    selected = fields.Bool()
    unusable = fields.Bool()
    # ButtonText
    text_active = fields.Bool()
    text_value_idle = fields.String()
    text_value_selected = fields.String()
    text_value_highlighted = fields.String()
    text_value_selected_highlighted = fields.String()
    text_value_unusable = fields.String()
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
    text_auto_size = fields.Bool()
    text_min_size = FloatRoundedField()
    text_max_size = FloatRoundedField()
    text_size = FloatRoundedField()
    text_underlined = fields.Bool()
    text_vertical_align = EnumField(enum=enums.VertAlignOptions)
    text_horizontal_align = EnumField(enum=enums.HorizAlignOptions)
    text_ellipsis = fields.Boolean()
    text_padding_top = FloatRoundedField()
    text_padding_bottom = FloatRoundedField()
    text_padding_left = FloatRoundedField()
    text_padding_right = FloatRoundedField()
    text_line_spacing = FloatRoundedField()
    # Icon fields
    icon_active = fields.Bool()
    icon_value_idle = fields.Str()
    icon_value_selected = fields.Str()
    icon_value_highlighted = fields.Str()
    icon_value_selected_highlighted = fields.Str()
    icon_value_unusable = fields.Str()
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
    # Mesh Fields
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
    # Outline fields
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
    # Tooltip fields
    tooltip_title = fields.String()
    tooltip_content = fields.String()
    tooltip_bounds = fields.Nested(PositionSchema)
    tooltip_positioning_target = EnumField(enum=enums.ToolTipPositioning)
    tooltip_positioning_origin = EnumField(enum=enums.ToolTipPositioning)
    # Switch fields
    disable_on_press = fields.Bool()
    toggle_on_press = fields.Bool()
    switch_active = fields.Bool()
    switch_on_color = ColorField()
    switch_off_color = ColorField()
    # backwards compatibility
    text_bolded = fields.Bool()

    @pre_dump
    def flatten_attributes(self, obj, *args, **kwargs):
        """Add flattened attributes from nested fields to object."""
        key_map = {
            # Switch fields
            'switch_active': obj.switch.active,
            'switch_on_color': obj.switch.on_color,
            'switch_off_color': obj.switch.off_color,
            # icon fields
            'icon_color_idle': obj.icon.color.idle,
            'icon_color_selected': obj.icon.color.selected,
            'icon_color_highlighted': obj.icon.color.highlighted,
            'icon_color_selected_highlighted': obj.icon.color.selected_highlighted,
            'icon_color_unusable': obj.icon.color.unusable,
            'icon_sharpness': obj.icon.sharpness,
            'icon_active': obj.icon.active,
            'icon_size': obj.icon.size,
            'icon_ratio': obj.icon.ratio,
            'icon_position': obj.icon.position,
            'icon_rotation': obj.icon.rotation,
            'icon_value_idle': obj.icon.value.idle,
            'icon_value_selected': obj.icon.value.selected,
            'icon_value_highlighted': obj.icon.value.highlighted,
            'icon_value_selected_highlighted': obj.icon.value.selected_highlighted,
            'icon_value_unusable': obj.icon.value.unusable,
            # Outline fields.
            'outline_active': obj.outline.active,
            'outline_size_idle': obj.outline.size.idle,
            'outline_size_selected': obj.outline.size.selected,
            'outline_size_highlighted': obj.outline.size.highlighted,
            'outline_size_selected_highlighted': obj.outline.size.selected_highlighted,
            'outline_size_unusable': obj.outline.size.unusable,
            'outline_color_idle': obj.outline.color.idle,
            'outline_color_selected': obj.outline.color.selected,
            'outline_color_highlighted': obj.outline.color.highlighted,
            'outline_color_selected_highlighted': obj.outline.color.selected_highlighted,
            'outline_color_unusable': obj.outline.color.unusable,
            # ButtonText fields
            'text_value_idle': obj.text.value.idle,
            'text_value_highlighted': obj.text.value.highlighted,
            'text_value_selected': obj.text.value.selected,
            'text_value_unusable': obj.text.value.unusable,
            'text_value_selected_highlighted': obj.text.value.selected_highlighted,
            'text_bold_idle': obj.text.bold.idle,
            'text_bold_highlighted': obj.text.bold.highlighted,
            'text_bold_selected': obj.text.bold.selected,
            'text_bold_selected_highlighted': obj.text.bold.selected_highlighted,
            'text_bold_unusable': obj.text.bold.unusable,
            'text_color_idle': obj.text.color.idle,
            'text_color_highlighted': obj.text.color.highlighted,
            'text_color_selected': obj.text.color.selected,
            'text_color_selected_highlighted': obj.text.color.selected_highlighted,
            'text_color_unusable': obj.text.color.unusable,
            'text_min_size': obj.text.min_size,
            'text_max_size': obj.text.max_size,
            'text_size': obj.text.size,
            'text_underlined': obj.text.underlined,
            'text_vertical_align': obj.text.vertical_align,
            'text_horizontal_align': obj.text.horizontal_align,
            'text_ellipsis': obj.text.ellipsis,
            'text_padding_top': obj.text.padding_top,
            'text_padding_bottom': obj.text.padding_bottom,
            'text_padding_left': obj.text.padding_left,
            'text_padding_right': obj.text.padding_right,
            'text_line_spacing': obj.text.line_spacing,
            # Mesh
            'mesh_active': obj.mesh.active,
            'mesh_enabled_idle': obj.mesh.enabled.idle,
            'mesh_enabled_selected': obj.mesh.enabled.selected,
            'mesh_enabled_highlighted': obj.mesh.enabled.highlighted,
            'mesh_enabled_selected_highlighted': obj.mesh.enabled.selected_highlighted,
            'mesh_enabled_unusable': obj.mesh.enabled.unusable,
            'mesh_color_idle': obj.mesh.color.idle,
            'mesh_color_selected': obj.mesh.color.selected,
            'mesh_color_highlighted': obj.mesh.color.highlighted,
            'mesh_color_selected_highlighted': obj.mesh.color.selected_highlighted,
            'mesh_color_unusable': obj.mesh.color.unusable,
            # Tooltip
            'tooltip_title': obj.tooltip.title,
            'tooltip_content': obj.tooltip.content,
            'tooltip_bounds': obj.tooltip.bounds,
            'tooltip_positioning_target': obj.tooltip.positioning_target,
            'tooltip_positioning_origin': obj.tooltip.positioning_origin,
        }
        for key, value in key_map.items():
            setattr(obj, key, value)
        return obj

    def load(self, data, *args, **kwargs):
        data = dict(data)
        btn = super().load(data, *args, **kwargs)
        self.load_text_values(data, btn)
        self.load_outline_values(data, btn)
        self.load_icon_values(data, btn)
        self.load_mesh_values(data, btn)
        self.load_tooltip_values(data, btn)
        return btn

    def load_text_values(self, data: dict, btn: ui.Button):
        text_values = {
            'idle': data.pop('text_value_idle'),
            'selected': data.pop('text_value_selected'),
            'highlighted': data.pop('text_value_highlighted'),
            'selected_highlighted': data.pop('text_value_selected_highlighted'),
            'unusable': data.pop('text_value_unusable'),
        }
        if any(key.startswith('text_color') for key in data.keys()):
            text_color = {
                'idle': data.pop('text_color_idle'),
                'selected': data.pop('text_color_selected'),
                'highlighted': data.pop('text_color_highlighted'),
                'selected_highlighted': data.pop('text_color_selected_highlighted'),
                'unusable': data.pop('text_color_unusable'),
            }
            color_schema = create_multi_state_schema(ColorField)
            colors_data = color_schema.load(text_color)
            btn.text.color.set_each(**colors_data)

        if any(key.startswith('text_bold_') for key in data.keys()):
            text_bold = {
                'idle': data.pop('text_bold_idle'),
                'selected': data.pop('text_bold_selected'),
                'highlighted': data.pop('text_bold_highlighted'),
                'selected_highlighted': data.pop('text_bold_selected_highlighted'),
                'unusable': data.pop('text_bold_unusable'),
            }
            bold_schema = create_multi_state_schema(fields.Bool)
            bolds_data = bold_schema.load(text_bold)
            btn.text.bold.set_each(**bolds_data)

        string_schema = create_multi_state_schema(fields.String)
        values_data = string_schema.load(text_values)
        btn.text.value.set_all("")  # Makes default empty string.
        btn.text.value.set_each(**values_data)

    def load_outline_values(self, data, btn):
        if any(key.startswith('outline') for key in data.keys()):
            outline_data = {
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
            multi_state_color = create_multi_state_schema(ColorField).load(outline_data['color'])
            multi_state_size = create_multi_state_schema(FloatRoundedField).load(outline_data['size'])
            btn.outline.color.set_each(**multi_state_color)
            btn.outline.size.set_each(**multi_state_size)

    def load_icon_values(self, data, btn):
        has_icon_data = any(key.startswith('icon') for key in data.keys())
        if has_icon_data:
            icon_data = {
                'active': data.pop('icon_active'),
                'sharpness': data.pop('icon_sharpness'),
                'size': data.pop('icon_size'),
                'ratio': data.pop('icon_ratio'),
                'position': data.pop('icon_position'),
                'rotation': data.pop('icon_rotation'),
                'padding_left': data.pop('icon_padding_left', 0),
                'padding_right': data.pop('icon_padding_right', 0),
                'padding_top': data.pop('icon_padding_top', 0),
                'padding_bottom': data.pop('icon_padding_bottom', 0),
            }
            icon_color = {
                'idle': data.pop('icon_color_idle'),
                'selected': data.pop('icon_color_selected'),
                'highlighted': data.pop('icon_color_highlighted'),
                'selected_highlighted': data.pop('icon_color_selected_highlighted'),
                'unusable': data.pop('icon_color_unusable')
            }
            # Icon values aren't present in json exported directly from StackStudio
            if any(key.startswith('icon_value') for key in data.keys()):
                icon_values = {
                    'idle': data.pop('icon_value_idle'),
                    'selected': data.pop('icon_value_selected'),
                    'highlighted': data.pop('icon_value_highlighted'),
                    'selected_highlighted': data.pop('icon_value_selected_highlighted'),
                    'unusable': data.pop('icon_value_unusable')
                }
                loaded_icon_values = create_multi_state_schema(fields.Str).load(icon_values)
                btn.icon.value.set_each(**loaded_icon_values)
            validated_icon_data = ButtonIconSchema().load(icon_data)
            for key, value in validated_icon_data.items():
                setattr(btn.icon, key, value)
            loaded_icon_color = create_multi_state_schema(ColorField).load(icon_color)
            btn.icon.color.set_each(**loaded_icon_color)

    def load_mesh_values(self, data, btn):
        has_mesh_data = any(key.startswith('mesh') for key in data.keys())
        if has_mesh_data:
            mesh_data = {
                'active': data.pop('mesh_active'),
            }
            mesh_enabled = {
                'idle': data.pop('mesh_enabled_idle'),
                'selected': data.pop('mesh_enabled_selected'),
                'highlighted': data.pop('mesh_enabled_highlighted'),
                'selected_highlighted': data.pop('mesh_enabled_selected_highlighted'),
                'unusable': data.pop('mesh_enabled_unusable'),
            }
            mesh_color = {
                'idle': data.pop('mesh_color_idle'),
                'selected': data.pop('mesh_color_selected'),
                'highlighted': data.pop('mesh_color_highlighted'),
                'selected_highlighted': data.pop('mesh_color_selected_highlighted'),
                'unusable': data.pop('mesh_color_unusable'),
            }
            for key, value in mesh_data.items():
                setattr(btn.mesh, key, value)
            multi_state_color = create_multi_state_schema(ColorField).load(mesh_color)
            multi_state_enabled = create_multi_state_schema(fields.Boolean).load(mesh_enabled)
            btn.mesh.color.set_each(**multi_state_color)
            btn.mesh.enabled.set_each(**multi_state_enabled)

    def load_tooltip_values(self, data, btn):
        has_tooltip_data = any(key.startswith('tooltip') for key in data.keys())
        if has_tooltip_data:
            tooltip_data = {
                'title': data.pop('tooltip_title'),
                'content': data.pop('tooltip_content'),
                'bounds': data.pop('tooltip_bounds'),
                'positioning_target': data.pop('tooltip_positioning_target'),
                'positioning_origin': data.pop('tooltip_positioning_origin'),
            }
            validated_data = ButtonToolTipSchema().load(tooltip_data)
            for key, value in validated_data.items():
                setattr(btn.tooltip, key, value)

    def load_switch_values(self, data, btn):
        has_switch_data = any(key.startswith('switch') for key in data.keys())
        if has_switch_data:
            switch_data = {
                'active': data.pop('switch_active'),
                'on_color': data.pop('switch_on_color'),
                'off_color': data.pop('switch_off_color'),
            }
            validated_data = ButtonSwitchSchema().load(switch_data)
            for key, value in validated_data.items():
                setattr(btn.switch, key, value)

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
    type_name = fields.String()
    mesh_color = ColorField()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Mesh()
        init_object(new_obj, data)
        return new_obj


class ImageSchema(Schema):
    type_name = fields.String()
    color = ColorField()
    file_path = fields.String()
    scaling_option = EnumField(enum=enums.ScalingOptions)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Image()
        init_object(new_obj, data)
        return new_obj


class LoadingBarSchema(Schema):
    type_name = fields.String()
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
    type_name = fields.String()
    text = fields.String(attribute='text_value')
    text_vertical_align = EnumField(enum=enums.VertAlignOptions)
    text_horizontal_align = EnumField(enum=enums.HorizAlignOptions)
    text_auto_size = fields.Bool()
    text_max_size = FloatRoundedField()
    text_min_size = FloatRoundedField()
    text_size = FloatRoundedField()
    text_color = ColorField()
    text_bold = fields.Bool()
    text_italic = fields.Bool(data_key='text_italics')
    text_underlined = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Label()
        init_object(new_obj, data)
        return new_obj


class TextInputSchema(Schema):
    type_name = fields.String()
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
    type_name = fields.String()
    current_value = FloatRoundedField()
    min_value = FloatRoundedField()
    max_value = FloatRoundedField()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Slider()
        init_object(new_obj, data)
        return new_obj


class DropdownItemSchema(Schema):
    name = fields.String()
    close_on_selected = fields.Bool()
    selected = fields.Bool()

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.DropdownItem()
        init_object(new_obj, data)
        return new_obj


class DropdownSchema(Schema):
    type_name = fields.String()
    permanent_title = fields.String()
    use_permanent_title = fields.Bool()
    max_displayed_items = fields.Integer(min=0)
    items = fields.List(fields.Nested(DropdownItemSchema))
    unusable = fields.Bool(default=False)

    @post_load
    def make_obj(self, data, **kwargs):
        new_obj = ui.Dropdown()
        init_object(new_obj, data)
        return new_obj


class UIListSchema(Schema):
    type_name = fields.String()
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
    type_name = fields.String()
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
        'UIList': UIListSchema(),
        'LoadingBar': LoadingBarSchema()
    }

    def load(self, data, *args, **kwargs):
        type_name = data['type_name']
        correct_schema = self.type_name_schemas[type_name]
        return correct_schema.load(data, *args, **kwargs)

    def dump(self, obj, *args, **kwargs):
        type_name = obj.__class__.__name__
        schema = self.type_name_schemas[type_name]
        dump_data = schema.dump(obj, *args, **kwargs)
        dump_data['type_name'] = type_name
        return dump_data


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
        padding_data = {
            'left': data.pop('padding_x', None),
            'right': data.pop('padding_y', None),
            'top': data.pop('padding_z', None),
            'down': data.pop('padding_w', None)
        }
        new_obj.set_padding(**padding_data)
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
    root = fields.Nested(LayoutNodeSchema, data_key='effective_root')
    enabled = fields.Boolean()
    index = fields.Int()
    locked = fields.Boolean()

    @post_load
    def make_menu(self, data, **kwargs):
        new_obj = ui.Menu()
        init_object(new_obj, data)
        return new_obj
