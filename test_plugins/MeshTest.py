from nanome.util.vector3 import Vector3
import nanome
from nanome.api import shapes
from nanome.util import Logs

import open3d as o3d
import numpy as np

# Config

NAME = "Mesh loading Test"
DESCRIPTION = "Test for shape meshes"
CATEGORY = "Test"
HAS_ADVANCED_OPTIONS = False

# Plugin


class MeshLoadingTest(nanome.PluginInstance):
    def on_run(self):
        m = self.make_mesh()
        m.upload()

    def make_mesh(self):
        print("Creating mesh")
        mesh = shapes.Mesh()
        mesh.uv = []

        filename = "test_plugins/objs/bananome.obj"
        image_path = "test_plugins/objs/bananome.png"
        img = o3d.io.read_image(image_path)

        # Read mesh
        o3dmesh = o3d.io.read_triangle_mesh(filename)
        # Center it
        o3dmesh.translate(-o3dmesh.get_center())
        # Scale it 50 times
        o3dmesh.scale(50.0, o3dmesh.get_center())

        # Compute normals if needed
        if not o3dmesh.has_vertex_normals():
            o3dmesh.compute_vertex_normals()
        # Use vertex colors if there are ones
        if o3dmesh.has_vertex_colors():
            mesh.colors = np.asarray(o3dmesh.vertex_colors).flatten()
        if o3dmesh.has_triangle_uvs():
            mesh.uv = np.asarray(o3dmesh.triangle_uvs).flatten()

        # Extract vertex colors based on texture if no vertex colors already set
        if not o3dmesh.has_vertex_colors() and o3dmesh.has_triangle_uvs():
            mesh.colors = []
            imgarray = np.asarray(img)
            imgw, imgh, imgc = imgarray.shape - np.asarray([1, 1, 0])
            for uv in np.asarray(o3dmesh.triangle_uvs):
                coord = (imgw, imgh) * uv
                coord = coord.astype(int)
                vcol = imgarray[-coord[1]][coord[0]] / 255.0
                mesh.colors.append(vcol[0])
                mesh.colors.append(vcol[1])
                mesh.colors.append(vcol[2])
                mesh.colors.append(1.0)  # vcol[3])

        mesh.vertices = np.asarray(o3dmesh.vertices).flatten()
        mesh.normals = np.asarray(o3dmesh.vertex_normals).flatten()
        mesh.triangles = np.asarray(o3dmesh.triangles).flatten()
        mesh.anchors[0].position = nanome.util.Vector3(0, 0, 0)
        mesh.color = nanome.util.Color(255, 255, 255, 255)

        # Fill colors and UVs if empty
        if len(mesh.uv) == 0:
            mesh.uv = np.repeat([0.0, 0.0], len(mesh.vertices) / 3)
        if len(mesh.colors) == 0:
            mesh.colors = np.repeat([1.0, 1.0, 1.0, 1.0], len(mesh.vertices) / 3)

        print("Done creating mesh")
        return mesh


nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, MeshLoadingTest)
