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

Entry points
^^^^^^^^^^^^

Overriding these functions in your plugin will give you several entry points:

.. code-block:: python

    # On plugin instantiation, when user clicked on "Activate" and a
    #   connection between Nanome and Plugin is established
    def start(self):
        pass

    # Provides a mean to regularly execute code. Called multiple times per second
    def on_update(self):
        pass

    # Called when user clicks on the "Run" button in Nanome
    def on_run(self):
        pass

    # Called when user clicks on the "Advanced Settings" button in Nanome.
    #   has_advanced should be set to True in nanome.Plugin constructor (see `Plugin description`_)
    def on_advanced_settings(self):
        pass

    # Called whenever a complex is added to the workspace.
    def on_complex_added(self):
        pass

    # Called whenever a complex is removed from the workspace.
    def on_complex_removed(self):
        pass