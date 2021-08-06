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

On the VR Side
^^^^^^^^^^^^^^

Please contact sales@nanome.ai to enable your account to use Plugins. 

After the Nanome team has configured your account to use Plugins and has provided the target server location and port (NTS DNS and Port, e.g. organization.nanome.ai 8888), log into Nanome, create a room, and click on the purple "Stacks" button to the left of the Entry list. You should see an empty list or a list of plugins. If you see "Not connected to NTS", please contact support@nanome.ai or your dedicated Account Manager.

*Editing the Config File*

First, you want to locate the Config file (nanome-config.ini) of the Nanome Application in the builds folder.
If you downloaded Nanome through the Oculus store, it will be available here:

C:\\Program Files\\Oculus\\Software\\Software\\nanome-nanome\\Build

Open the nanome-config.ini file in a text editor and scroll down to the section named ‘ Nanome plugin server config’ and change to the following:

Plugin-server-addr = 127.0.0.1

Plugin-server-port = 8888

Now, we want to check to make sure that the Plugin Server is connected. Go ahead and launch Nanome, then log in using your credentials. Create a room and Start in 2D and click on the Plugins Icon on the bottom of the Entry Menu.

You should see that the NTS is connected and there are no current running plugins. If it says that “No NTS is connected”, that means it is unable to see the Plugin server and it is entered incorrectly on the Config file or in the Admin settings for home.nanome.ai. It could also be blocked by firewall.

In order to connect Nanome (VR) to your server, make sure that its configuration file (nanome-config.ini, located in its installation directory) contains the following:

  .. code-block:: none

    plugin-server-addr = 127.0.0.1  # Use the correct address for your server
    plugin-server-port = 8888  # Use the correct port for your server

Our Plugins
^^^^^^^^^^^

We have a growing list of plugins available on our `Github <https://github.com/nanome-ai>`_ (all repositories starting with "plugin-")

Please refer to each individual repository README for more information about our plugins
