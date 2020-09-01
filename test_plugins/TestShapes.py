import nanome
import random

# Config

NAME = "Test Shapes"
DESCRIPTION = "Tests for plugin shapes API"
CATEGORY = "Tests"
HAS_ADVANCED_OPTIONS = False

class TestShapes(nanome.PluginInstance):
    def start(self):
        self.menu = nanome.ui.Menu()
        self.shapes = []
        menu = self.menu
        menu.title = "Shapes API"
        menu.width = 0.5
        menu.height = 0.7

        ln = nanome.ui.LayoutNode()
        ln.layout_orientation = nanome.util.enums.LayoutTypes.vertical

        btn = ln.add_new_button("Add to workspace")
        btn.register_pressed_callback(self.create_in_workspace)
        btn = ln.add_new_button("Add to random complex")
        btn.register_pressed_callback(self.create_in_complex)
        btn = ln.add_new_button("Add to random atom")
        btn.register_pressed_callback(self.create_in_atom)
        btn = ln.add_new_button("Delete last created")
        btn.register_pressed_callback(self.delete_last)

        menu.root.add_child(ln)

    def create_in_workspace(self, button):
        sphere = self.create_random_sphere()
        def done(success):
            self.shapes.append(sphere)
        sphere.upload(done)

    def create_in_complex(self, button):
        def received(workspace):
            if len(workspace.complexes) == 0:
                return
            c = random.randrange(0, len(workspace.complexes) - 1)
            
            sphere = self.create_random_sphere()
            sphere.anchor = nanome.util.enums.ShapeAnchorType.Complex
            sphere.target = workspace.complexes[c].index
            def done(success):
                self.shapes.append(sphere)
            sphere.upload(done)

        self.request_workspace(received)

    def create_in_atom(self, button):
        def received(workspace):
            if len(workspace.complexes) == 0:
                return
            c = random.randrange(0, len(workspace.complexes) - 1)
            atom_count = 0
            for _ in workspace.complexes[c]:
                atom_count += 1
            a = random.randrange(0, len(atom_count) - 1)
            
            sphere = self.create_random_sphere()
            sphere.anchor = nanome.util.enums.ShapeAnchorType.Atom
            sphere.target = workspace.complexes[c].atoms[a].index
            sphere.position = nanome.util.Vector3()
            def done(success):
                self.shapes.append(sphere)
            sphere.upload(done)

        self.request_workspace(received)

    def delete_last(self, button):
        if len(self.shapes) == 0:
            return
        shape = self.shapes.pop()
        shape.destroy()

    def create_random_sphere(self):
        sphere = self.create_shape(nanome.util.enums.ShapeType.Sphere)
        sphere.radius = random.uniform(0.5, 2.0)
        sphere.position = nanome.util.Vector3(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
        sphere.color = nanome.util.Color(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), random.randrange(100, 255))
        return sphere

nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, TestShapes)