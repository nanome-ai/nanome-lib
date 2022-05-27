from nanome.util.vector3 import Vector3
import nanome
import random
import itertools
from nanome.api.shapes import Shape, Sphere, Line, Anchor, Label

# Config

NAME = "Test Shapes"
DESCRIPTION = "Tests for plugin shapes API"
CATEGORY = "Tests"
HAS_ADVANCED_OPTIONS = False


class TestShapes(nanome.PluginInstance):
    def start(self):
        sf = TestShapes.SphereFactory
        sf.parent = self
        lf = TestShapes.LineFactory
        lf.parent = self
        self.menu = nanome.ui.Menu()
        menu = self.menu
        menu.title = "Shapes"
        menu.width = 0.5
        menu.height = 0.5

        left = nanome.ui.LayoutNode()
        left.layout_orientation = nanome.util.enums.LayoutTypes.vertical

        ln_label = left.create_child_node()
        label = ln_label.add_new_label()
        label.text_value = "spheres"
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to workspace")
        btn.register_pressed_callback(sf.create_in_workspace)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to random complex")
        btn.register_pressed_callback(sf.create_in_complex)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Add to random atom")
        btn.register_pressed_callback(sf.create_in_atom)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Change anchor last created")
        btn.register_pressed_callback(sf.change_anchor)
        ln_btn = left.create_child_node()
        btn = ln_btn.add_new_button("Delete last created")
        btn.register_pressed_callback(sf.delete_last)

        right = nanome.ui.LayoutNode()
        right.layout_orientation = nanome.util.enums.LayoutTypes.vertical

        ln_label = right.create_child_node()
        label = ln_label.add_new_label()
        label.text_value = "lines"
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to workspace")
        btn.register_pressed_callback(lf.create_in_workspace)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to random complex")
        btn.register_pressed_callback(lf.create_in_complex)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Add to random atom")
        btn.register_pressed_callback(lf.create_in_atom)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Change anchor last created")
        btn.register_pressed_callback(lf.change_anchor)
        ln_btn = right.create_child_node()
        btn = ln_btn.add_new_button("Delete last created")
        btn.register_pressed_callback(lf.delete_last)

        menu.root.layout_orientation = nanome.util.enums.LayoutTypes.horizontal
        menu.root.add_child(left)
        menu.root.add_child(right)

    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    class SphereFactory():
        spheres = []
        parent = None

        @classmethod
        def create_in_workspace(cls, button):
            sphere = cls.create_random_sphere()

            def done(success):
                cls.spheres.append(sphere)
            sphere.upload(done)

        @classmethod
        def create_in_complex(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)

                spheres = []
                spheres.append(cls.create_random_sphere())
                anchor = spheres[0].anchors[0]
                anchor.anchor_type = nanome.util.enums.ShapeAnchorType.Complex
                anchor.target = workspace.complexes[c].index
                spheres.append(cls.create_random_sphere())
                anchor = spheres[1].anchors[0]
                anchor.anchor_type = nanome.util.enums.ShapeAnchorType.Complex
                anchor.target = workspace.complexes[c].index

                def done(success):
                    cls.spheres.append(spheres[0])
                    cls.spheres.append(spheres[1])
                Shape.upload_multiple(spheres, done)

            cls.parent.request_workspace(received)

        @classmethod
        def create_in_atom(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)
                atom_count = 0
                for _ in workspace.complexes[c].atoms:
                    atom_count += 1
                a = random.randrange(0, atom_count - 1)

                sphere = cls.create_random_sphere()
                if a == 0:
                    atom = next(workspace.complexes[c].atoms)
                else:
                    atom = next(itertools.islice(workspace.complexes[c].atoms, a, None))

                anchor = sphere.anchors[0]
                anchor.anchor_type = nanome.util.enums.ShapeAnchorType.Atom
                anchor.target = atom.index

                def done(success):
                    cls.spheres.append(sphere)
                sphere.upload(done)

            cls.parent.request_workspace(received)

        @classmethod
        def change_anchor(cls, button):
            if len(cls.spheres) == 0:
                return
            shape = cls.spheres[-1]
            anchor = shape.anchors[0]
            anchor.anchor_type = (anchor.anchor_type + 1) % len(nanome.util.enums.ShapeAnchorType)
            shape.upload()

        @classmethod
        def delete_last(cls, button):
            if len(cls.spheres) == 0:
                return
            Shape.destroy_multiple(cls.spheres)

        @classmethod
        def create_random_sphere(cls):
            sphere = Sphere()
            sphere.radius = random.uniform(0.5, 2.0)
            sphere.color = nanome.util.Color(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), random.randrange(100, 255))
            anchor = sphere.anchors[0]
            anchor.local_offset = nanome.util.Vector3(random.uniform(-.05, .05), random.uniform(-.05, .05), random.uniform(-.05, .05))
            return sphere

    class LineFactory():
        queued_anchor = None
        lines = []
        labels = []
        parent = None

        @classmethod
        def create_in_workspace(cls, button):
            cls.create_anchor(0, nanome.util.enums.ShapeAnchorType.Workspace)

        @classmethod
        def create_in_complex(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)

                cls.create_anchor(workspace.complexes[c].index, nanome.util.enums.ShapeAnchorType.Complex)

            cls.parent.request_workspace(received)

        @classmethod
        def create_in_atom(cls, button):
            def received(workspace):
                if len(workspace.complexes) == 0:
                    return
                elif len(workspace.complexes) == 1:
                    c = 0
                else:
                    c = random.randrange(0, len(workspace.complexes) - 1)
                atom_count = 0
                for _ in workspace.complexes[c].atoms:
                    atom_count += 1
                a = random.randrange(0, atom_count - 1)

                if a == 0:
                    atom = next(workspace.complexes[c].atoms)
                else:
                    atom = next(itertools.islice(workspace.complexes[c].atoms, a, None))

                cls.create_anchor(atom.index, nanome.util.enums.ShapeAnchorType.Atom)

            cls.parent.request_workspace(received)

        @classmethod
        def change_anchor(cls, button):
            if len(cls.lines) == 0:
                return
            line = cls.lines[-1]
            label = cls.labels[-1]
            anchor_type = (line.anchors[0].anchor_type + 1) % len(nanome.util.enums.ShapeAnchorType)
            line.anchors[0].anchor_type = anchor_type
            label.anchors[0].anchor_type = anchor_type
            line.upload()
            label.upload()

        @classmethod
        def delete_last(cls, button):
            if len(cls.lines) == 0:
                return
            shape = cls.lines.pop()
            shape.destroy()
            shape = cls.labels.pop()
            shape.destroy()

        @classmethod
        def create_anchor(cls, target, a_type):
            anchor = Anchor()
            anchor.target = target
            anchor.local_offset = nanome.util.Vector3(1, 0, 0)  # nanome.util.Vector3(random.uniform(-.05, .05), random.uniform(-.05, .05), random.uniform(-.05, .05))
            anchor.viewer_offset = nanome.util.Vector3(0, 0, .01)
            anchor.anchor_type = a_type
            if cls.queued_anchor == None:
                cls.queued_anchor = anchor
            else:
                cls.create_line(cls.queued_anchor, anchor)
                cls.queued_anchor = None

        @classmethod
        def create_anchor(cls, target, a_type):
            anchor = Anchor()
            anchor.target = target
            anchor.local_offset = nanome.util.Vector3(1, 0, 0)  # nanome.util.Vector3(random.uniform(-.05, .05), random.uniform(-.05, .05), random.uniform(-.05, .05))
            anchor.anchor_type = a_type
            if cls.queued_anchor == None:
                cls.queued_anchor = anchor
            else:
                cls.create_line(cls.queued_anchor, anchor)
                cls.queued_anchor = None

        @classmethod
        def copy_anchor(cls, other):
            anchor = Anchor()
            anchor.target = other.target
            anchor.local_offset = other.local_offset
            anchor.viewer_offset = other.viewer_offset
            anchor.anchor_type = other.anchor_type
            return anchor

        @classmethod
        def create_line(cls, anchor1, anchor2):
            line = Line()
            line.anchors = [anchor1, anchor2]
            line.dash_distance = .4
            line.thickness *= 2

            label = Label()
            label.anchors = [cls.copy_anchor(anchor1), cls.copy_anchor(anchor2)]
            label.anchors[0].viewer_offset = nanome.util.Vector3(0, 0, -.01)
            label.anchors[1].viewer_offset = nanome.util.Vector3(0, 0, -.01)
            label.text = "bloop"

            def done1(success):
                cls.lines.append(line)

            def done2(success):
                cls.labels.append(label)
            line.upload(done1)
            label.upload(done2)


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, TestShapes)
