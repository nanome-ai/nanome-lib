############
Installation
############

.. note::
  Access to a Nanome Transport Server (NTS) is required to run plugins and connect them to Nanome. A public server will be available in the future. If you need access to NTS, please contact us.

******************
Install nanome-lib
******************

``nanome-lib`` is our Python package containing the Api for interacting programmatically with nanome.

To install nanome-lib, you need a supported version of Python. We recommend Python >= 3.7, although Python 2.7 can still be used.
Install using pip:

.. code-block:: bash

    $ pip install nanome

Upon installation, nanome-lib adds two useful command line functions to your PATH.

* ``nanome-setup-plugins``: Sets default system wide configs for your plugin. See `Arguments` section for configurable values
* ``nanome-plugin-init``: Asks for plugin name and description, and sets up boilerplate code to quickly get started.

***************
On the VR Side
***************

Please contact sales@nanome.ai to enable your account to use Plugins. 

After the Nanome team has configured your account to use Plugins, they will provide an NTS server location and port (e.g. organization.nanome.ai 8888).

If you see "Not connected to NTS", please contact support@nanome.ai or your dedicated Account Manager.


Editing the Config File
=======================

In some cases, you will need to manually point your Nanome application to your provided NTS credentials.
You'll want to locate the Config file (nanome-config.ini) of the Nanome Application in the builds folder.
If you downloaded Nanome through the Oculus store, it will be available here:

.. code-block :: none

  C:\\Program Files\\Oculus\\Software\\Software\\nanome-nanome\\Build

Open the nanome-config.ini file in a text editor and scroll down to the section named 'Nanome plugin server config' and change to the following:

.. code-block:: none

  plugin-server-addr = <YOUR NTS HOST>
  plugin-server-port = <YOUR NTS PORT>


You should see that the NTS is connected and there are no current running plugins. If it says that “No NTS is connected”, that means the credentials are entered incorrectly, or it may be blocked by a firewall.
