Nanome Plugin API
=================
The Nanome Plugin System is a Python-based API that allows users to connect 3rd party tools into the Nanome Virtual Reality Software Tool for Collaborative Molecular Modeling.


-----------------
Table of Contents
-----------------
.. toctree::
   :maxdepth: 1

   general
   basics
   workspace
   ui
   file
   notification
   api
   

**Overview**

The Nanome Plugin API provides a way to interface and integrate external software with Nanome's molecular modeling VR software. 
Through this API, users can link up external computational such as molecular dynamics, docking software, and link custom databases.
The extended functionality includes the ability to create new windows inside of the virtual environment and is easily customizable through a drag and drop user interface.

Plugins can be designed and ran from different operating systems - Windows, Linux, and Mac  depending on the requirements needed from each plugin.

Some examples of plugins that our customers love are:
 - Docking
 - Molecular Dynamics
 - Custom Database Integration
 - Loading PDFs and PowerPoints
 - Running custom molecular dynamics
 - All of our public plugins are available on our `Github <https://github.com/nanome-ai>`_.

The primary requirements for running plugins is the Nanome Virtual Reality Software and access to the Nanome Plugin Server (NTS). The Nanome Plugin Server acts as a relay to forward plugin information and processes data in and out of the Nanome virtual environment. 

The Nanome Virtual Reality Software can be acquired directly from Nanome or in any of the VR stores here:

 * Oculus Store: https://www.oculus.com/experiences/rift/1873145426039242
 * Viveport: https://www.viveport.com/apps/0a467f78-2ed2-43eb-ada8-9d677d5acf54
 * Steam: https://store.steampowered.com/app/493430/Nanome/
 * Direct Download: https://nanome.ai/setup
 * SideQuest: https://xpan.cc/a-333

Please contact sales@nanome.ai to enable your account to use Plugins. 


Using Plugins
--------------

**In order to use a plugin**

*Editing the Config File*

First, you want to locate the Config file (nanome-config.ini) of the Nanome Application in the builds folder.
If you downloaded Nanome through the Oculus store, it will be available here:

C:\\Program Files\\Oculus\\Software\\Software\\nanome-nanome\\Build

Open the nanome-config.ini file in a text editor and scroll down to the section named ‘ Nanome plugin server config’ and change to the following:

Plugin-server-addr = 127.0.0.1

Plugin-server-port = 8888

Now, we want to check to make sure that the Plugin Server is connected. Go ahead and launch Nanome, then log in using your credentials. Create a room and Start in 2D and click on the Plugins Icon on the bottom of the Entry Menu.

You should see that the NTS is connected and there are no current running plugins. If it says that “No NTS is connected”, that means it is unable to see the Plugin server and it is entered incorrectly on the Config file or in the Admin settings for home.nanome.ai. It could also be blocked by firewall.

Let’s go ahead and run a basic plugin to make sure it is working.

*Installing your first plugin: Basic Plugin*

*Example Plugin*

First, download the RemoveHydrogen.py basic plugin here: 

This is a simple plugin example to remove all of the selected hydrogens in the workspace:

.. literalinclude:: ../../test_plugins/RemoveHydrogens.py
    :language: python

Development
^^^^^^^^^^^^

In order to prepare your development environment and create your own first plugins, follow this link:

.. toctree::
   :maxdepth: 1

   installation
