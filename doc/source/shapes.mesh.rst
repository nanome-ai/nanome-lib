###########
Shapes.Mesh API
###########

Nanome provides the ability to import 3D meshes to your workspace.

***********
Basic Usage
***********

.. code-block:: python

    from nanome.api.shapes import Mesh
    from nanome.util import Color, Vector3

    mesh = Mesh()
    #Create a cube
    mesh.vertices = [0.0, 1.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 1.0,  1.0, 1.0, 1.0,  0.0, 1.0, 0.0,  0.0, 0.0, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0, 0.0]
    mesh.normals = [-0.408, 0.408, 0.817,  -0.667, -0.667, 0.333,  0.408, -0.408, 0.817,  0.667, 0.667, 0.333,  -0.667, 0.667, -0.333,  -0.408, -0.408, -0.817,  0.667, -0.667, -0.333,  0.408, 0.408, -0.817]
    mesh.triangles = [0,1,2,  0,2,3,  7,6,5,  7,5,4,  3,2,6,  3,6,7,  4,0,3,  4,3,7,  4,5,1,  4,1,0,  1,5,6,  1,6,2]

    mesh.anchors[0].anchor_type = nanome.util.enums.ShapeAnchorType.Workspace
    mesh.anchors[0].position = Vector3(0, 0, 0)
    mesh.color = Color(255, 255, 255, 255)
    mesh.upload()

Triangle array is a list of 0-based, positive integers.
Vertices, normals and triangles are mandatory. Since 1.23.2, the normals are not mandatory and can be re-computed in Nanome.

*******************************
Mesh coloring
*******************************

There are several ways to color a mesh using the Shape API:

- Using the mesh color (`mesh.color = Color(255, 255, 255, 128)`) will uniformly color the mesh in transparent white.
- Using per-vertex colors (`mesh.colors = [1.0, 1.0, 1.0, 1.0, ...]`) will color the mesh per-vertex (alpha is ignored).
- Using a texture (`mesh.texture_path = 'path/to/img.png'`) will load the texture (jpeg or png format) and map it to the mesh using `mesh.uv`.


Note that the mesh color will blend with the per-vertex colors and the mesh texture.

Since Nanome 1.23.2, transparent meshes are also using textures and per-vertex colors.

As texturing the mesh uses the uv array, the texture will not be mapped if `mesh.uv` is not set.

**************
Example Plugin
**************

.. code-block:: python

    import nanome
    from nanome.api.shapes import Mesh
    from nanome.util import Color, Vector3
    from nanome.util.asyncio import async_callback

    class MeshExamplePlugin(nanome.AsyncPluginInstance):
        @async_callback
        async def on_run(self):
            mesh = Mesh()
            #Create a cube
            mesh.vertices = [0.0, 20.0, 20.0,  0.0, 0.0, 20.0,  20.0, 0.0, 20.0,  20.0, 20.0, 20.0,  0.0, 20.0, 0.0,  0.0, 0.0, 0.0,  20.0, 0.0, 0.0,  20.0, 20.0, 0.0]
            mesh.normals = [-0.408, 0.408, 0.817,  -0.667, -0.667, 0.333,  0.408, -0.408, 0.817,  0.667, 0.667, 0.333,  -0.667, 0.667, -0.333,  -0.408, -0.408, -0.817,  0.667, -0.667, -0.333,  0.408, 0.408, -0.817]
            mesh.triangles = [0,1,2,  0,2,3,  7,6,5,  7,5,4,  3,2,6,  3,6,7,  4,0,3,  4,3,7,  4,5,1,  4,1,0,  1,5,6,  1,6,2]

            mesh.anchors[0].anchor_type = nanome.util.enums.ShapeAnchorType.Workspace
            mesh.anchors[0].position = Vector3(0, 0, 0)
            mesh.color = Color(255, 255, 255, 255)
            mesh.colors = [1.0, 0.0, 0.0, 1.0,  1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0,  0.0, 0.0, 1.0, 1.0,  0.0, 0.0, 1.0, 1.0,  0.0, 0.0, 1.0, 1.0,  0.0, 0.0, 1.0, 1.0]
            mesh.upload()

    def main():
        plugin = nanome.Plugin('Mesh Example', 'Create a cube and color it with per-vertex colors', 'other', False)
        plugin.set_plugin_class(MeshExamplePlugin)
        plugin.run()
    
    if __name__ == '__main__':
        main()