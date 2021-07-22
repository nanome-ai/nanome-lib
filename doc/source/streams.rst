###########
Streams API
###########

| Nanome provides **writing_streams** for updating Structures and Shapes in real-time
| (**reading_streams** will be coming soon)


*******************
How to use a Stream
*******************

| Instantiate by passing Pass list of structure indices, and stream type.
| :code:`stream, error = await self.create_writing_stream(indices, stream_type)`
| 	- StreamTypes enumerated in ``~nanome.utils.enums.StreamType``

| To write to a stream, create a list with all data to send to the stream.
| :code:`stream.update(stream_data)`
|	- If updating multiple objects, stream data is still a flat list of values. ``[x1, y1, z1, x2, y2, z2]``
|	- Each StreamType expects a different data format. See below for details.


***********
StreamTypes
***********
| The top row of each table represents a structure index passed to the stream.
| The bottom rows represent the expected data format to be sent to the stream for each index

| Note that it is important to keep the stream data the correct length, otherwise it  becomes misaligned, and will return the wrong results.


StreamType.color
================
| Sets the color for each atom in stream.

+-----------+-----------+
| a1        |     a2    |
+---+---+---+---+---+---+
| r | g | b | r | g | b |
+---+---+---+---+---+---+


StreamType.complex_position_rotation
======================================
| Sets the position for each complex in stream.

| Stream updates take x,y,z values from postition Vector3, and x,y,z,w from rotation Quaternion

+----------------------------------+----------------------------------+
| c1                               | c2                               |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
| px | py | pz | rx | ry | rz | rw | px | py | pz | rx | ry | rz | rw |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+


StreamType.label
================
| Set text for label on each atom in stream.

+-----+-----+
| a1  |  a2 |
+-----+-----+
| str | str |
+-----+-----+



StreamType.position
===================
| Set position for each atom in stream.

+-----------+-----------+
| a1        |     a2    |
+---+---+---+---+---+---+
| x | y | z | x | y | z |
+---+---+---+---+---+---+



StreamType.scale
================
| Changes the scale of each atom in stream

+-------+-------+
| a1    |   a2  |
+-------+-------+
| float | float |
+-------+-------+



StreamType.shape_color
======================
| Sets color of Shape object using RGBA values

+---------------+---------------+
| s1            | s2            |
+---+---+---+---+---+---+---+---+
| r | g | b | a | r | g | b | a |
+---+---+---+---+---+---+---+---+



StreamType.shape_position

==============
| Set position of center of shape.

+-----------+-----------+
| s1        |     s2    |
+---+---+---+---+---+---+
| x | y | z | x | y | z |
+---+---+---+---+---+---+



sphere_shape_radius
===================
| Set radius of sphere shape.

+-------+-------+
| s1    |   s2  |
+-------+-------+
| float | float |
+-------+-------+


**************
Example Plugin
**************
.. code-block:: python

	NAME = "Color Stream Test"
	DESCRIPTION = "Cycle atom colors through the rainbow."
	CATEGORY = "Test"
	HAS_ADVANCED_OPTIONS = False

	class StreamTest(nanome.AsyncPluginInstance):

	    @async_callback
	    async def on_run(self):
	        complex_indices = [comp.index for comp in await self.request_complex_list()]
	        complexes = await self.request_complexes(complex_indices)
	        
	        # Generate list of atom indices to add to stream.
	        atom_indices = []
	        for comp in complexes:
	            atom_indices.extend([a.index for a in comp.atoms])
	        
	        # Create a writing stream to set colors for every atom in the complexes. 
	        stream_type = StreamType.color
	        stream, error = await self.create_writing_stream(atom_indices, stream_type)

	        # RGB values of the rainbow
	        roygbiv = [
	            (255, 0 , 0),  # Red
	            (255, 127, 0),  # Orange
	            (255, 255, 0),  # Yellow
	            (0, 255, 0),  # Green
	            (0, 0, 255),  # Blue
	            (75, 0, 130),  # Indigo
	            (148, 0, 211),  # Violet
	        ]

	        # Every half second, change the color of all the atoms
	        sleep_time = 0.5
	        color_index = 0
	        while True:
	            time.sleep(sleep_time)
	            stream_data = []
	            new_color_rgba = roygbiv[color_index]
	            for atom in atom_indices:
	                stream_data.extend(new_color_rgba)
	            stream.update(stream_data)
	            color_index = (color_index + 1) % len(roygbiv)

	nanome.Plugin.setup(NAME, DESCRIPTION, CATEGORY, HAS_ADVANCED_OPTIONS, StreamTest)
