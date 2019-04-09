Interactions with Nanome
========================

Basics
------

The parameters of nanome.Plugin define how your plugin will appear in the list:

.. code-block:: python

    plugin = nanome.Plugin(name, description, category, has_advanced)

- *category* will define in which category the plugin will be when Nanome User clicks on the plugin filter dropdown. This is currently unsupported.
- *has_advanced* defines if an "Advanced Settings" button should be displayed when user selects the plugin in Nanome

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
    #   has_advanced should be set to True in nanome.Plugin constructor (see above)
    def on_advanced_settings(self):
        pass

If you don't want to create a class, you can register callbacks for all functions before calling nanome.Plugin.run:

.. code-block:: python

    if __name__ == "__main__":
        plugin = nanome.Plugin(...)
        plugin.on_start(start_fct)
        plugin.on_update(update_fct)
        plugin.on_run(run_fct)
        # Same pattern works for all existing callbacks
        plugin.run('127.0.0.1', 8888)

Workspace
---------

Request entire workspace in deep mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_run(self):
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        pass


Request a list of specific complexes in deep mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_run(self):
        self.request_complexes([1, 6, 5], self.on_complexes_received) # Requests complexes with ID 1, 6 and 5

    def on_complexes_received(self, complex_list):
        pass

Request all complexes in the workspace in shallow mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_run(self):
        self.request_complex_list(self.on_complex_list_received)

    def on_complex_list_received(self, complex_list):
        pass

Update workspace to match exactly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_workspace_received(self, workspace):
        # ...
        # Do something with workspace
        # ...
        self.update_workspace(workspace)

Add to workspace
^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_run(self):
        # ...
        # Create new complexes
        # ...
        self.add_to_workspace([new_complex1, new_complex2])

Update specific complexes in shallow mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_complex_list_received(self, complex_list):
        # ...
        # Do something with shallow complex, i.e. move them, rename them
        # ...
        self.update_complex_list_shallow(complex_list_to_update)

Files
-----

Here is a simple example of File API usage, requesting directory and files, and writing files on Nanome machine.

.. literalinclude:: ../../file_api_test.py
    :language: python