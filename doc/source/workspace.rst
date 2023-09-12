#############
Workspace API
#############

*******************
Structure hierarchy
*******************

Molecular structures are organized like so:

.. code-block:: none

    - Workspace
        - Complex
            - Molecule
                - Chain
                    - Residue
                        - Atom
                        - Bond

A complex is a group of molecules and has a position and rotation. In Nanome, the user can switch between the
molecules of a complex using the frame slider, in the information menu.


Index
=====

Each molecular structure has an index available as a base property.

This index is a unique identifier for structures uploaded to Nanome.
However, if a structure hasn't been added to Nanome's workspace yet, its index will be -1

To access this index:

.. code-block:: python

    if my_structure.index == -1:
        Logs.message("This structure hasn't been uploaded to Nanome")


Deep / Shallow
==============

Nanome has two molecular structure transmission mode: Deep and Shallow. Their goal is to make data transmission faster by requesting only the data needed.

- **Deep mode** will request/send the structure and its entire content. E.g. a molecule in deep mode will contain its name and any other property it might have + all its chains, residues, atoms and bonds
- **Shallow mode** will request/send only the structure itself. E.g. a molecule in shallow mode will only contain its name and any other property it might have

Whether a command requests one mode or the other is described in this documentation.


Coordinate Spaces
=================

When dealing with structures and objects in Nanome, there are 2 coordinate spaces to be aware of: global/workspace and local/complex.

- **Global (Workspace)** coordinate space is used for positioning and rotating objects in the Nanome Workspace relative to each other
- **Local (Complex)** coordinate space is used for positioning atoms within a complex

For example, when a complex is loaded into Nanome, the atom positions are all in the local coordinate space of the complex.
Moving and rotating this complex in the workspace will not affect the positions of the atoms within it. Consequently, if you have
2 complexes next to each other rotated differently and export both complexes to a file, the atom positions will not be relative to
each other from their original complex positions. In order to treat atom positions as relative to each other, you must first convert
their positions from local space to global space (or convert the positions of one complex into global space and back into local space
of the other complex). This can be done by using transformation matrices to multiply against the atom positions, where the matrices
come from ``Complex.get_complex_to_workspace_matrix`` and ``Complex.get_workspace_to_complex_matrix``.

.. code-block:: python

    @async_callback
    async def on_run(self):
        complex1, complex2 = await self.request_complexes([1, 2])
        c1_to_global_mat = complex1.get_complex_to_workspace_matrix()
        global_to_c2_mat = complex2.get_workspace_to_complex_matrix()

        for atom in complex1.atoms:
            global_pos = c1_to_global_mat * atom.position
            atom.position = global_to_c2_mat * global_pos

        complex1.io.to_sdf('complex1.sdf')
        complex2.io.to_sdf('complex2.sdf')

In the above example, the atoms of complex1 are converted from local space to global space, and then back to local space of complex2.
This makes it possible to pass the resulting sdf into a different program (such as docking) and have the atoms positions be relative
to each other as they were positioned inside Nanome.

*****************
Common Operations
*****************

Load PDB/SDF/MMCIF as a Nanome Complex
======================================
.. code-block:: python

    from nanome.api.structure import Complex

    pdb_path = '/path/to/file.pdb'
    sdf_path = '/path/to/file.sdf'
    mmcif_path = '/path/to/file.mmcif'
    comp = Complex.io.from_pdb(path=pdb_file)
    comp = Complex.io.from_sdf(path=sdf_file)
    comp = Complex.io.from_mmcif(path=mmcif_file)


Export Nanome Complex as PDB/SDF/MMCIF
======================================
.. code-block:: python

    from nanome.api.structure import Complex

    pdb_path = '/path/to/file.pdb'
    sdf_path = '/path/to/file.sdf'
    mmcif_path = '/path/to/file.mmcif'
    comp = Complex()
    comp.io.to_pdb(path=pdb_path)
    comp.io.to_sdf(path=sdf_path)
    comp.io.to_mmcif(path=mmcif_path)


Request entire workspace in deep mode
=====================================

.. code-block:: python

    @async_callback
    async def on_run(self):
        workspace = await self.request_workspace()

Request all complexes in the workspace in shallow mode
======================================================

.. code-block:: python

    @async_callback
    async def on_run(self):
        shallow_complexes = await self.request_complex_list()

Request a list of specific complexes in deep mode
=================================================

.. code-block:: python

    @async_callback
    async def on_run(self):
        deep_complexes = await self.request_complexes([1, 6, 5]) # Requests complexes with ID 1, 6 and 5

Update workspace to match exactly
=================================

.. code-block:: python

    @async_callback
    async def on_run(self):
        workspace = await self.request_workspace()
        # ...
        # Do something with workspace
        # ...
        self.update_workspace(workspace)

Add to workspace
================

.. code-block:: python

    @async_callback
    async def on_run(self):
        # ...
        # Create new complexes
        # ...
        self.add_to_workspace([new_complex1, new_complex2])

Remove from workspace
=====================

.. code-block:: python

    @async_callback
    async def on_run(self):
        # ...
        # Get list of complexes to remove
        # ...
        self.remove_from_workspace(complexes_to_remove)

Update specific structures
==========================

In shallow mode:

.. code-block:: python

    @async_callback
    async def on_run(self):
        shallow_complexes = await self.request_complex_list()
        # ...
        # Do something with shallow structures, i.e. move them, rename them
        # ...
        self.update_structures_shallow([complex, atom, residue])

In deep mode:

.. code-block:: python

    @async_callback
    async def on_run(self):
        deep_complexes = await self.request_complexes([1, 6, 5])
        # ...
        # Do something with deep structures, i.e. move them, rename them
        # ...
        self.update_structures_deep([complex])
