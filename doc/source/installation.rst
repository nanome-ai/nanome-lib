Installation
============

In order to install the Nanome Plugin API, you need a supported version of Python.
Then, use python's package manager, pip, to install nanome:

.. code-block:: bash

    $ pip install nanome

Or, to upgrade your current installation:

.. code-block:: bash

    $ pip install nanome --upgrade

Upon installation, nanome-lib adds two command line functions to your PATH.

* `nanome-setup-plugins`: Sets default system wide configs for your plugin. See `Arguments` section for config options
* `nanome-plugin-init`: Asks for plugin name and description, and sets up boilerplate code to quickly get started.


Server
^^^^^^

A Nanome Transport Server (NTS) is required to run your plugins and connect them to Nanome.
A public server will be available in the near future. If you need a NTS, please contact us.

Running Your First Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Starting a plugin is fairly easy. Copy this snippet into a file HelloNanomePlugin.py:

.. code-block:: python

  import nanome
  from nanome.api import Plugin, PluginInstance
  from nanome.util import Logs

  class HelloNanomePlugin(PluginInstance):
      """Get most basic plugin running."""
      
      def on_run(self):
          message = "Hello Nanome!"
          self.send_notification(nanome.util.enums.NotificationTypes.success, message)
          Logs.message(message)

  if __name__ == '__main__':
    # Information describing the plugin
    name = 'Hello Nanome'
    description = "Send a notification that says `Hello Nanome`"
    category = 'Demo'
    has_advanced = False  # Whether the plugin has advanced settings menu.

    # Create Plugin, and attach specific PluginInstance to it.
    plugin = Plugin.setup(name, description, category, has_advanced, HelloNanomePlugin)

.. code-block:: bash

    $ python HelloNanomePlugin.py -a <NTS_HOST> -p <NTS_PORT> *<args>

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
* -r: Enables Live Reload

On the VR Side
^^^^^^^^^^^^^^

In order to connect Nanome (VR) to your server, make sure that its configuration file (nanome-config.ini, located in its installation directory) contains the following:

  .. code-block:: none

    plugin-server-addr				= 127.0.0.1     # Use the correct address for your server
    plugin-server-port				= 8888          # Use the correct port for your server

Our Plugins
^^^^^^^^^^^

We have a growing list of plugins available on our `Github <https://github.com/nanome-ai>`_ (all repositories starting with "plugin-")

Please refer to each individual repository README for more information about our plugins
