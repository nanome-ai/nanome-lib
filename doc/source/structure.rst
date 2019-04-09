Structure
=========

Deep / Shallow
--------------

Nanome has two molecular structure transmission mode: Deep and Shallow. Their goal is to make data transmission
faster by requesting only the data needed.

- Deep mode will request the structure and its entire content. E.g. a molecule in deep mode will contain its name and any other property it might have + all its chains, residues, atoms and bonds
- Shallow mode will request only the structure itself. E.g. a molecule in shallow mode will only contain its name and any other property it might have

Whether a command requests one mode or the other is described in this documentation.

Structure hierarchy
-------------------

Molecular structures are organized like so:

- **Complex**
- ---- **Molecule**
- ---------- **Chain**
- ---------------- **Residue**
- ---------------------- **Atom**
- ---------------------- **Bond**

A complex is a group of molecules and has a position and rotation. In Nanome, the user can switch between the
molecules of a complex using the frame slider, in the information menu.