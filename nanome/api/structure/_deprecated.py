from nanome.util import Logs
from nanome.util import Matrix


class AtomDeprecated(object):
    def __init__(self):
        super(AtomDeprecated, self).__init__()
        self._rendering = AtomDeprecated.Rendering(self)
        self._molecular = AtomDeprecated.Molecular(self)

    # region deprecated
    @property
    @Logs.deprecated()
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Rendering(object):
        def __init__(self, parent):
            self._parent = parent

        def set_visible(self, value):
            if value:
                self._parent._display_mode = 0xFFFFFFFF
            else:
                self._parent._display_mode = 0x00000000
            self._parent._hydrogened = value
            self._parent._watered = value
            self._parent._hetatomed = value

        @property
        def selected(self):
            return self._parent.selected

        @selected.setter
        def selected(self, value):
            self._parent.selected = value

        @property
        def atom_mode(self):
            return self._parent.atom_mode

        @atom_mode.setter
        def atom_mode(self, value):
            self._parent.atom_mode = value

        @property
        def labeled(self):
            return self._parent.labeled

        @labeled.setter
        def labeled(self, value):
            self._parent.labeled = value

        @property
        def label_text(self):
            return self._parent.label_text

        @label_text.setter
        def label_text(self, value):
            self._parent.label_text = value

        @property
        def atom_rendering(self):
            return self._parent.atom_rendering

        @atom_rendering.setter
        def atom_rendering(self, value):
            self._parent.atom_rendering = value

        @property
        def atom_color(self):
            return self._parent.atom_color

        @atom_color.setter
        def atom_color(self, value):
            self._parent.atom_color = value

        @property
        def surface_rendering(self):
            return self._parent.surface_rendering

        @surface_rendering.setter
        def surface_rendering(self, value):
            self._parent.surface_rendering = value

        @property
        def surface_color(self):
            return self._parent.surface_color

        @surface_color.setter
        def surface_color(self, value):
            self._parent.surface_color = value

        @property
        def surface_opacity(self):
            return self._parent.surface_opacity

        @surface_opacity.setter
        def surface_opacity(self, value):
            self._parent.surface_opacity = value

    class Molecular(object):
        def __init__(self, parent):
            self._parent = parent

        @property
        def symbol(self):
            return self._parent.symbol

        @symbol.setter
        def symbol(self, value):
            self._parent.symbol = value

        @property
        def serial(self):
            return self._parent.serial

        @serial.setter
        def serial(self, value):
            self._parent.serial = value

        @property
        def name(self):
            return self._parent.name

        @name.setter
        def name(self, value):
            self._parent.name = value

        @property
        def position(self):
            return self._parent.position

        @position.setter
        def position(self, value):
            self._parent.position = value

        @property
        def is_het(self):
            return self._parent.is_het

        @is_het.setter
        def is_het(self, value):
            self._parent.is_het = value
    # endregion


class BondDeprecated(object):

    def __init__(self):
        super(BondDeprecated, self).__init__()
        self._molecular = BondDeprecated.Molecular(self)

    # region deprecated
    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def kind(self):
            return self.parent.kind

        @kind.setter
        def kind(self, value):
            self.parent.kind = value
    # endregion


class ResidueDeprecated(object):

    def __init__(self):
        super(ResidueDeprecated, self).__init__()
        self._rendering = ResidueDeprecated.Rendering(self)
        self._molecular = ResidueDeprecated.Molecular(self)

    # region deprecated
    @property
    @Logs.deprecated()
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Rendering(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def ribboned(self):
            return self.parent.ribboned

        @ribboned.setter
        def ribboned(self, value):
            self.parent.ribboned = value

        @property
        def ribbon_size(self):
            return self.parent.ribbon_size

        @ribbon_size.setter
        def ribbon_size(self, value):
            self.parent.ribbon_size = value

        @property
        def ribbon_mode(self):
            return self.parent.ribbon_mode

        @ribbon_mode.setter
        def ribbon_mode(self, value):
            self.parent.ribbon_mode = value

        @property
        def ribbon_color(self):
            return self.parent.ribbon_color

        @ribbon_color.setter
        def ribbon_color(self, value):
            self.parent.ribbon_color = value

        @property
        def labeled(self):
            return self.parent.labeled

        @labeled.setter
        def labeled(self, value):
            self.parent.labeled = value

        @property
        def label_text(self):
            return self.parent.label_text

        @label_text.setter
        def label_text(self, value):
            self.parent.label_text = value

    class Molecular(object):

        def __init__(self, parent):
            self.parent = parent

        @property
        def type(self):
            return self.parent.type

        @type.setter
        def type(self, value):
            self.parent.type = value

        @property
        def serial(self):
            return self.parent.serial

        @serial.setter
        def serial(self, value):
            self.parent.serial = value

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value

        @property
        def secondary_structure(self):
            return self.parent.secondary_structure

        @secondary_structure.setter
        def secondary_structure(self, value):
            self.parent.secondary_structure = value
    # endregion


class ChainDeprecated(object):

    # region deprecated
    def __init__(self):
        super(ChainDeprecated, self).__init__()
        self._molecular = ChainDeprecated.Molecular(self)

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value

    # endregion


class MoleculeDeprecated(object):

    def __init__(self):
        super(MoleculeDeprecated, self).__init__()
        self._molecular = MoleculeDeprecated.Molecular(self)

    # region deprecated
    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value
    # endregion


class ComplexDeprecated(object):

    def __init__(self):
        super(ComplexDeprecated, self).__init__()
        self._rendering = ComplexDeprecated.Rendering(self)
        self._molecular = ComplexDeprecated.Molecular(self)
        self._transform = ComplexDeprecated.Transform(self)

    # region deprecated

    @property
    @Logs.deprecated()
    def rendering(self):
        return self._rendering

    @property
    @Logs.deprecated()
    def molecular(self):
        return self._molecular

    @property
    @Logs.deprecated()
    def transform(self):
        return self._transform

    class Rendering(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def boxed(self):
            return self.parent._boxed

        @boxed.setter
        def boxed(self, value):
            self.parent.boxed = value

        @property
        def locked(self):
            return self.parent.locked

        @locked.setter
        def locked(self, value):
            self.parent.locked = value

        @property
        def visible(self):
            return self.parent.visible

        @visible.setter
        def visible(self, value):
            self.parent.visible = value

        @property
        def computing(self):
            return self.parent.computing

        @computing.setter
        def computing(self, value):
            self.parent.computing = value

        @property
        def current_frame(self):
            return self.parent.current_frame

        @current_frame.setter
        def current_frame(self, value):
            self.parent.current_frame = value

        # returns true if the complex is selected on nanome.
        def get_selected(self):
            return self.parent.selected

        def set_surface_needs_redraw(self):
            self.parent.surface_dirty = True

        @property
        def box_label(self):
            return self._box_label

        @box_label.setter
        def box_label(self, value):
            self._box_label = value

    class Molecular(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def name(self):
            return self.parent.name

        @name.setter
        def name(self, value):
            self.parent.name = value

        @property
        def index_tag(self):
            return self.parent.index_tag

        @index_tag.setter
        def index_tag(self, value):
            self.parent.index_tag = value

        @property
        def split_tag(self):
            return self.parent.split_tag

        @split_tag.setter
        def split_tag(self, value):
            self.parent.split_tag = value

    class Transform(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def position(self):
            return self.parent.position

        @position.setter
        def position(self, value):
            self.parent.position = value

        @property
        def rotation(self):
            return self.parent.rotation

        @rotation.setter
        def rotation(self, value):
            self.parent.rotation = value

        def get_workspace_to_complex_matrix(self):
            rotation = Matrix.from_quaternion(self.parent.rotation)
            rotation.transpose()

            translation = Matrix.identity(4)
            translation[0][3] = -self.parent.position.x
            translation[1][3] = -self.parent.position.y
            translation[2][3] = -self.parent.position.z

            transformation = rotation * translation
            return transformation

        def get_complex_to_workspace_matrix(self):
            result = self.parent.get_workspace_to_complex_matrix()
            result = result.get_inverse()
            return result

    # endregion


class WorkspaceDeprecated:
    # region deprecated
    def __init__(self):
        super(WorkspaceDeprecated, self).__init__()
        self._transform = WorkspaceDeprecated.Transform(self)

    @property
    @Logs.deprecated()
    def transform(self):
        return self._transform

    class Transform(object):
        def __init__(self, parent):
            self.parent = parent

        @property
        def position(self):
            return self.parent.position

        @position.setter
        def position(self, value):
            self.parent.position = value

        @property
        def rotation(self):
            return self.parent.rotation

        @rotation.setter
        def rotation(self, value):
            self.parent.rotation = value

        @property
        def scale(self):
            return self.parent.scale

        @scale.setter
        def scale(self, value):
            self.parent.scale = value

    # endregion
