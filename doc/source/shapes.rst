###########
Shapes API
###########

Nanome provides the ability to draw shapes to your workspace.

.. |pic1| image:: network.png
  :width: 45%
  :alt: shapes_png

.. |pic2| image:: interactions.png
  :width: 45%
  :alt: interactions_png

|pic2| |pic1|


***********
Shape Types
***********
- Sphere
- Line
- Label
- Mesh

***********
Basic Usage
***********

.. code-block:: python

	from nanome.api.shapes import Shape, Sphere
	from nanome.util import Color
	
	sphere = Sphere(radius=1.0, color=Color(1.0, 0.0, 0.0))
	Shape.upload(sphere)

*******************************
Positioning Shapes with Anchors
*******************************
Shapes are positioned using associated `Anchors`

There are 3 main types of anchors, as enumerated in `nanome.util.enums.ShapeAnchorType`

ShapeAnchorTypes
================

- `Workspace`:
	- :code:`anchor.local_offset=Vector3()`
	- Use anchor.local_offset to position the shape in the workspace
- `Complex`:
	- :code:`anchor.target=int`. (Complex Index)
	- Set anchor.target to the complex index, and Shape will be centered at the origin of the complex's local coordinate space.
- `Atom`:
	- :code:`anchor.target=int`.  (Atom Index)
	- Set anchor.target to the atom index, and Shape will be centered on the provided atom.

Anchor Tips
===========

- Lines require 2 anchors.
- If multiple anchors are added to a shape, the shape will be positioned at the center of all the anchors.
- anchor.local_offset and anchor.global_offset can be used to offset the shape from the anchor point.

**************
Example Plugin
**************

.. code-block:: python

	import nanome
	from nanome.api import structure
	from nanome.api.shapes import Anchor, Label, Line, Shape, Sphere
	from nanome.util import Vector3, enums, Color
	from nanome.util.asyncio import async_callback

	class ShapesExamplePlugin(nanome.AsyncPluginInstance):

		@async_callback
		async def on_run(self):
			workspace = structure.Workspace()
			self.update_workspace(workspace)

			radius = 5
			sphere1_position = Vector3(25, 100, 50)
			sphere2_position = Vector3(50, 100, 50)

			# Draw sphere anchored to point in Workspace
			sphere1 = Sphere()
			sphere1.radius = radius
			sphere1.color = Color.Blue()
			anchor1 = sphere1.anchors[0]
			anchor1.anchor_type == enums.ShapeAnchorType.Workspace
			anchor1.local_offset = sphere1_position
			
			# Create atom, and draw sphere anchored to it
			comp = self.add_complex(sphere2_position)
			comp = (await self.add_to_workspace([comp]))[0]
			atom = next(comp.atoms)

			anchor2 = Anchor()
			anchor2.anchor_type = enums.ShapeAnchorType.Atom
			anchor2.target = atom.index
			
			sphere2 = Sphere()
			sphere2.radius = radius
			sphere2.color = Color.Blue()
			sphere2.anchors = [anchor2]

			# Draw line between spheres.
			line = Line()
			line.thickness = 1
			line.dash_distance = .75
			line.color = Color.White()
			line.anchors = [anchor1, anchor2]
			await Shape.upload_multiple([sphere1, sphere2, line])

			# Lets add a label that's centered on the line.
			line_label = Label()
			line_label.text = 'Label'
			line_label.anchors = line.anchors
			for anchor in line_label.anchors:
				anchor.viewer_offset = Vector3(0, 0, -.1)
			await Shape.upload(line_label)

		def add_complex(self, position):
			"""Add a Complex containing one atom to the workspace."""
			comp = structure.Complex()
			mol = structure.Molecule()
			chain = structure.Chain()
			res = structure.Residue()
			atom = structure.Atom()

			atom.label_text = 'Atom'
			atom.position = position
			res.add_atom(atom)
			chain.add_residue(res)
			mol.add_chain(chain)
			comp.add_molecule(mol)
			comp.name = "Test Complex"
			return comp


	def main():
		plugin = nanome.Plugin('Shape Example', 'Draw some shapes with different anchor types', 'other', False)
		plugin.set_plugin_class(ShapesExamplePlugin)
		plugin.run()


	if __name__ == '__main__':
		main()
