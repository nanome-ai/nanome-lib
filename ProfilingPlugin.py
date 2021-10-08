import nanome
import sys
import time


class UpdateWorkspace(nanome.PluginInstance):
    def start(self):
        print("Start UpdateWorkspace Plugin")

    def on_workspace_received(self, workspace):
        all_atom_indices = []
        self.all_atoms = []
        for complex in workspace.complexes:
            for atom in complex.atoms:
                self.all_atoms.append(atom)
                all_atom_indices.append(atom.index)
        self.create_stream(all_atom_indices, self.stream_created)

    def stream_created(self, stream, error):
        a_pos = []
        for atom in self.all_atoms:
            atom.position.y += 1
            a_pos.append(atom.position.x)
            a_pos.append((atom.position.y) % 100)
            a_pos.append(atom.position.z)

        def repeat():
            self.stream_created(stream, None)
        stream.update(a_pos, repeat)

    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def __init__(self):
        pass


if __name__ == "__main__":
    plugin = nanome.Plugin("Profile Streams", "", "Test", False)
    plugin.set_plugin_class(UpdateWorkspace)
    plugin.run('127.0.0.1', 8888)
