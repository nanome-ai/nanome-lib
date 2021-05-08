Basics
======

Plugin description
^^^^^^^^^^^^^^^^^^

The parameters of nanome.Plugin define how your plugin will appear in the list:

.. code-block:: python

    plugin = nanome.Plugin(name, description, category, has_advanced)

- *category* will define in which category the plugin will be when Nanome User clicks on the plugin filter dropdown. This is currently unsupported.
- *has_advanced* defines if an "Advanced Settings" button should be displayed when user selects the plugin in Nanome

Or, if using the one-line plugin setup:

.. code-block:: python

    nanome.Plugin.setup(name, description, category, has_advanced, plugin_class, host, port, key_file)

For Plugin examples and how-tos, check out our cookbook at
https://github.com/nanome-ai/plugin-cookbook

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
        | Called when when instance updates (multiple times per second)
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
