Basics
======


What is a Plugin?
^^^^^^^^^^^^^^^^^

The Nanome Plugin API provides a way to interface and integrate external software with Nanome’s molecular modeling VR software.

Through this API, users can link up external computational such as molecular dynamics, docking software, and link custom databases.


There's 3 main classes we need to be concerned with right now.

    * **Plugin**: Handles Connections to NTS/ Low level packet stuff
    * **PluginInstance**: Collections of hooks and actions to interact with your Nanome Session
    * **AsyncPluginInstance**: Same as PluginInstance, but allows use of Python asyncio syntax (requirez Python >=3.7)

NTS
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

Entry points
^^^^^^^^^^^^

Overriding these functions in your plugin will give you several entry points:

.. code-block:: python

    def start(self):
        """
        | Called when user "Activates" the plugin
        """
        pass

    def update(self):
        """
        | Called when instance updates (multiple times per second)
        """
        pass

    def on_run(self):
        """
        | Called when user presses "Run"
        """
        pass

    def on_stop(self):
        """
        | Called when user disconnects or plugin crashes
        """
        pass

    def on_advanced_settings(self):
        """
        | Called when user presses "Advanced Settings"
        """
        pass

    def on_complex_added(self):
        """
        | Called whenever a complex is added to the workspace.
        """
        pass

    def on_complex_removed(self):
        """
        | Called whenever a complex is removed from the workspace.
        """
        pass

    def on_presenter_change(self):
        """
        | Called when room's presenter changes.
        """
        pass

    def on_advanced_settings(self):
        """
        | Called when user presses "Advanced Settings"
        """
        pass

    def on_presenter_change(self):
        """
        | Called when room's presenter changes.
        """
        pass
