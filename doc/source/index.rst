Nanome Plugin API
=================

Nanome Plugin API provides a way for Nanome users to extend the software capabilities depending of their needs

Requirements
------------
* `Python`_ 3.5.3+ / Coming Soon: `Python`_ 2.7.16

.. _Python: https://www.python.org/downloads/

Dependencies
------------
* **Optional**: brotli python package. If available, Nanome will automatically compress network packets

How-to
------

Example Plugin
^^^^^^^^^^^^^^
.. literalinclude:: ../../RemoveHydrogens.py
    :language: python

Start the plugin
^^^^^^^^^^^^^^^^
Starting a plugin is fairly easy:

.. code-block:: bash

    $ python RemoveHydrogens.py

To choose the IP address and the port of your server, you have two options:

Using arguments. More temporary
  .. code-block:: bash

    $ python RemoveHydrogens.py -a 123.456.789.0 -p 4567

Changing the script (plugin.run, last line in the previous example). More permanent
  .. code-block:: python

    plugin.run('123.456.789.0', 4567)

Table of Contents
-----------------
.. toctree::
   :maxdepth: 1

   interactions
   structure
   ui
   api