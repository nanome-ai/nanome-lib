Installation
============

In order to install the Nanome Plugin API, you need a supported version of Python.
Then, use python's package manager, pip, to install nanome:

.. code-block:: bash

    $ pip install nanome

Or, to upgrade your current installation:

.. code-block:: bash

    $ pip install nanome --upgrade

Server
^^^^^^

A Nanome Transport Server (NTS) is required to run your plugins and connect them to Nanome.
A public server will be available in the near future. If you need a NTS, please contact us.

Running Your First Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Starting a plugin is fairly easy. If you copy-pasted the example plugin on the home page, in a file named "RemoveHydrogens.py", you can start your plugin like this:

.. code-block:: bash

    $ python RemoveHydrogens.py

Or on Linux (python 3 is still preferred when available):

.. code-block:: bash

    $ python3 RemoveHydrogens.py

To choose the IP address and the port of your server, you have two options:

Short term, testing: **Using arguments**

  .. code-block:: bash

    $ python RemoveHydrogens.py -a 123.456.789.0 -p 4567

Long term, for production: **Changing the script** (call to plugin.run, last line of the example script above)

  .. code-block:: python

    plugin.run('123.456.789.0', 4567)

Arguments
^^^^^^^^^

When starting a plugin, a few optional arguments are available:

* -h: Displays available arguments
* -a [IP]: Specifies NTS address
* -p [PORT]: Specifies NTS port
* -k [FILE]: Specifies a key file to use (if NTS is protected by key)
* -v: Enables verbose mode, to display :func:`~nanome.util.logs.Logs.debug` messages

On the VR Side
^^^^^^^^^^^^^^

In order to connect Nanome (VR) to your server, make sure that its configuration file (nanome-config.ini, located in its installation directory) contains the following:

  .. code-block:: none

    plugin-server-addr				= 127.0.0.1     # Use the correct address for your server
    plugin-server-port				= 8888          # Use the correct port for your server

Our Plugins
^^^^^^^^^^^

We have a growing list of plugins available on our `Github <https://github.com/nanome-ai>`_ (all repositories starting with "plugin-")

In order to install them, you have 2 possibilities: Use pip or manually download them from github.

Using pip
---------

This is the easiest way.
For instance, to install and run URLLoader, simply use:

.. code-block:: bash

  $ pip install nanome-loaders
  $ nanome-url-loader -a address_of_your_nts

And it will be up and running
Please refer to each individual repository README for more information about our plugins