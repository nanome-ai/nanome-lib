Streams API
===========

Nanome provides **writing_streams** for updating complexes and objects in real-time
(**reading_streams** will be coming soon)

StreamTypes: :attr:`~nanome.util.enums.StreamType`

Object attributes and sets of attributes that can be streamed to Nanome.

- **color**
- **complex_position_rotation**
- **label**
- **position**
- **scale**
- **shape_color**
- **shape_position**
- **sphere_shape_radius**

.. code-block:: python

	NAME = "Color Changer Test"
	DESCRIPTION = "Simple test for color streams"
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

