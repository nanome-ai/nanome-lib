Nanome Plugin API
=================
The Nanome Plugin System is a Python-based API in order to connect external tools into the Nanome Virtual Reality Software Tool for Collaborative Molecular Modeling.


Getting Started
---------------
-Overview
-Repositories

Overview

The Nanome Plugin API provides a way to interface and integrate external software with Nanome's molecular modeling VR software. 
Through this API, users can link up external computational such as molecular dynamics or docking software. 
The extended functionality inclues the ability to create new windows inside of the virtual environment and is easily customizable through a drag and drop user interface.

Plugins can be designed and ran from different environments including Windows, Linux, and Mac operating systems depending on the requirements needed from the plugin.

Some examples of plugins that our customers love are:
- Running and viewing docking results
- Loading PDFs and PowerPoints
- Running custom molecular dynamics

The primary requirements for running plugins is the Nanome Virtual Reality Software and the Nanome Plugin Server (NTS). The Nanome Plugin Server acts as a relay to forward plugin information and processes into the Nanome virtual environment. 

The Nanome Virtual Reality Software can be acquired directly from Nanome or in any of the VR stores here:
* Oculus Store: https://www.oculus.com/experiences/rift/1873145426039242
* Viveport: https://www.viveport.com/apps/0a467f78-2ed2-43eb-ada8-9d677d5acf54
* Steam: https://store.steampowered.com/app/493430/Nanome/

Please contact sales@nanome.ai for the Nanome Plugin Server (NTS.exe)


Using Plugins
--------------

In order to use a plugin 

*Editing the Config File
First, you want to locate the Config file (nanome-config.ini) of the Nanome Application in the builds folder.
If you downloaded Nanome through the Oculus store, it will be available here:
C:\Program Files\Oculus\Software\Software\nanome-nanome\Build

Open the nanome-config.ini file in a text editor and scroll down to the section named ‘ Nanome plugin server config’ and change to the following:

Plugin-server-addr = 127.0.0.1
Plugin-server-port = 8888

*Launch a local Plugin Server
Next, we want to launch the Plugin Server locally. Go ahead and launch the NTS.exe file and a command prompt should open with the server running on port 8888.

<image>

Now, we want to check to make sure that the Plugin Server is connected. Go ahead and launch Nanome, then log in using your credentials. Create a room and Start in 2D and click on the Plugins Icon on the bottom of the Entry Menu.

You should see that the NTS is connected and there are no current running plugins. If it says that “No NTS is connected”, that means it is unable to see the Plugin server and it is entered incorrectly on the Config file or in the Admin settings for home.nanome.ai.

Let’s go ahead and run a basic plugin to make sure it is working…




Installing your first plugin: Nanome Web Loader
-----------------------------------------------

The Nanome Web Loader allows for the distribution of files (PDB, SDF, PDF, PPT) to be drag-and-dropped into a web interface and then available inside of the Nanome VR software.

*Windows
Required dependencies:
 - Python3 & Pip
 - Ghostscript
 - ImageMagick
 - Nanome Library
 - Nanome-Loaders Plugin

Instructions
First, you need to install Python 
https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe 
Don’t forget to click the checkbox to add Python3 to PATH
Open a command prompt
Type ‘python’ to verify the version is Python 3.0+, then exit()
Upgrade your Pip library
‘python -m pip install --upgrade pip’
Install GhostScript
https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs927/gs927w64.exe
Install ImageMagick
https://imagemagick.org/download/binaries/ImageMagick-7.0.8-50-Q16-x64-dll.exe
Install the latest Nanome Lib through Pip
enter ‘pip install nanome’
Install the Nanome Loaders Plugin
Enter ‘pip install nanome-loaders’
Run the Nanome Loaders’ WebLoader plugin 
Enter ‘nanome-web-loader -a localhost’
The ‘-a’ denotes the address of the Plugin Server IP


End temp
----------------

Requirements
------------
* `Python`_ 3.5.3+ or `Python`_ 2.7.16

.. _Python: https://www.python.org/downloads/

Dependencies
------------
None!

How-to
------

Example Plugin
^^^^^^^^^^^^^^

Here is a simple plugin example, removing all selected hydrogens in the workspace:

.. literalinclude:: ../../test_plugins/RemoveHydrogens.py
    :language: python

Installation
^^^^^^^^^^^^

In order to prepare your development environment and run your first plugins, follow this link:

.. toctree::
   :maxdepth: 1

   installation

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