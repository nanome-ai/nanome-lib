######
Basics
######

*****************
What is a Plugin?
*****************

The Nanome Plugin API provides a way to interface and integrate external software with Nanome’s molecular modeling VR software.

Through this API, users can link up external computational such as molecular dynamics, docking software, and link custom databases.


There's 3 main classes we need to be concerned with right now.

    * ``Plugin``: Handles Connections to NTS/ Low level packet stuff
    * ``PluginInstance``: Collections of hooks and actions to interact with your Nanome Session
    * ``AsyncPluginInstance``: Same as PluginInstance, but allows use of Python asyncio syntax (requires Python >= 3.7)


*************************
Running Your First Plugin
*************************

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


To start the plugin, call HelloNanomePlugin.py and pass in arguments

.. code-block:: bash

    $ python HelloNanomePlugin.py -a <NTS_HOST> -p <NTS_PORT> <ARGS>


Arguments
=========

When starting a plugin, a few optional arguments are available:

* -h: Displays available arguments
* -a [IP]: Specifies NTS domain or ip address
* -p [PORT]: Specifies NTS port
* -k [FILE]: Specifies a key file to use (if NTS is protected by key)
* -v: Enables verbose mode, to display :func:`~nanome.util.logs.Logs.debug` messages
* -r: Enables Live Reload


*******************
Plugin Instance API
*******************
The following is a summary of the functions available to a PluginInstance object

Event Handlers
==============

* ``start``: Called when user “Activates” the plugin
* ``update``: Called when when instance updates (multiple times per second)
* ``on_run``: Called when user presses "Run"
* ``on_stop``: Called when user disconnects or plugin crashes
* ``on_advanced_settings``: Called when user presses "Advanced Settings"
* ``on_complex_added``: Called whenever a complex is added to the workspace.
* ``on_complex_removed``: Called whenever a complex is removed from the workspace.
* ``on_presenter_changed``: Called when room's presenter changes.

Spatial Actions
===============

* ``zoom_on_structures``: Repositions and resizes the workspace such that the provided structure(s) will be in the center of the users view.
* ``center_on_structures``: Repositions the workspace such that the provided structure(s) will be in the center of the world.
* ``request_presenter_info``: Requests presenter account info (unique ID, name, email)
* ``request_controller_transforms``: Requests presenter controller info (head position, head rotation, left controller position, left controller rotation, right controller position, right controller rotation)

IO/Streaming
============

* ``save_files``: Save files on the machine running Nanome, and returns result
* ``create_writing_stream``: Create a stream allowing to continuously update properties of many objects
* ``create_reading_stream``: Create a stream allowing to continuously receive properties of many objects
* ``open_url``: Opens a URL in Nanome's computer browser
* ``send_files_to_load``: Send file(s) to Nanome to load directly using Nanome's importers.
* ``request_export``: Request a file export using Nanome exporters
* ``set_plugin_list_button``: Set text and/or usable state of the buttons on the plugin connection menu in Nanome

Workspace API Actions
==========================

* ``request_workspace``: Request the entire workspace, in deep mode
* ``add_to_workspace``: Add a list of complexes to the current workspace
* ``request_complex_list``: Request the list of all complexes in the workspace, in shallow mode
* ``request_complexes``: Requests a list of complexes by their indices
* ``update_workspace``: Replace the current workspace in the scene by the workspace in parameter
* ``send_notification``: Send a notification to the user
* ``update_structures_deep``: Update the specific molecular structures in the scene to match the structures in parameter.
* ``update_structures_shallow``: Update the specific molecular structures in the scene to match the structures in parameter
* ``apply_color_scheme``: Apply a color scheme to selected atoms.

Menus/Stacks
============

* ``update_menu``: Update the menu in Nanome
* ``update_content``: Update specific UI elements (button, slider, list...)
* ``update_node``: Updates layout nodes and their children
* ``set_menu_transform``: Update the position, scale, and rotation of the menu
* ``request_menu_transform``: Requests spacial information of the plugin menu (position, rotation, scale)

Calculations
============

* ``add_bonds``: Calculate bonds
* ``add_dssp``: Use DSSP to calculate secondary structures
* ``add_volume``: ???
