#############
Workspace API
#############

*******************
Structure hierarchy
*******************

Molecular structures are organized like so:

- **Workspace**
- ----**Complex**
- -------- **Molecule**
- -------------- **Chain**
- -------------------- **Residue**
- -------------------------- **Atom**
- -------------------------- **Bond**

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


*****************
Common Operations
*****************

Request entire workspace in deep mode
=====================================

.. code-block:: python

    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        pass


Request a list of specific complexes in deep mode
=================================================

.. code-block:: python

    def on_run(self):
        self.request_complexes([1, 6, 5], self.on_complexes_received) # Requests complexes with ID 1, 6 and 5

    def on_complexes_received(self, complex_list):
        pass

Request all complexes in the workspace in shallow mode
======================================================

.. code-block:: python

    def on_run(self):
        self.request_complex_list(self.on_complex_list_received)

    def on_complex_list_received(self, complex_list):
        pass

Update workspace to match exactly
=================================

.. code-block:: python

    def on_workspace_received(self, workspace):
        # ...
        # Do something with workspace
        # ...
        self.update_workspace(workspace)

Add to workspace
================

.. code-block:: python

    def on_run(self):
        # ...
        # Create new complexes
        # ...
        self.add_to_workspace([new_complex1, new_complex2])

Update specific structures
==========================

In shallow mode:

.. code-block:: python

    def on_complex_list_received(self, complex_list):
        # ...
        # Do something with shallow structures, i.e. move them, rename them
        # ...
        self.update_structures_shallow([complex, atom, residue])

In deep mode:

.. code-block:: python

    def on_workspace_received(self, complex_list):
        # ...
        # Do something with deep structures, i.e. move them, rename them
        # ...
        self.update_structures_deep([complex])
