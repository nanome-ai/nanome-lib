Nanome Plugin API
=================

Nanome Plugin API provides a way for Nanome users to extend the software capabilities depending of their needs, by executing their own operations or calling external softwares

Requirements
------------
* `Python`_ 3.5.3+ or `Python`_ 2.7.16

.. _Python: https://www.python.org/downloads/

Dependencies
------------
None!

How-to
------

Example Plugin
^^^^^^^^^^^^^^

Here is a simple plugin example, removing all selected hydrogens in the workspace:

.. literalinclude:: ../../test_plugins/RemoveHydrogens.py
    :language: python

Installation
^^^^^^^^^^^^

In order to prepare your development environment and run your first plugins, follow this link:

.. toctree::
   :maxdepth: 1

   installation

Table of Contents
-----------------
.. toctree::
   :maxdepth: 1

   general
   basics
   workspace
   ui
   file
   notification
   api