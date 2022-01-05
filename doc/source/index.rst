Nanome Plugin API
=================
The Nanome Plugin System is a Python-based API that allows users to connect 3rd party tools into the Nanome Virtual Reality Software Tool for Collaborative Molecular Modeling.

-----------------
Table of Contents
-----------------
.. toctree::
   :maxdepth: 1

   architecture
   installation
   plugins
   workspace
   ui
   file
   streams
   shapes
   notification
   api
   


The Nanome Plugin API provides a way to interface and integrate external software with Nanome's molecular modeling VR software. 
Through this API, users can link up external computational such as molecular dynamics, docking software, and link custom databases.
The extended functionality includes the ability to create new windows inside of the virtual environment and is easily customizable through a drag and drop user interface.

Plugins can be designed and ran from different operating systems - Windows, Linux, and Mac  depending on the requirements needed from each plugin.

Some examples of plugins that our customers love are:
 - `Docking <'https://github.com/nanome-ai/plugin-docking'>`_
 - `Chemical Interactions <'https://github.com/nanome-ai/plugin-chemical-interactions'>`_
 - `Electrostatic Potential Map generation <'https://github.com/nanome-ai/plugin-esp'>`_
 - `Chemical Properties <'https://github.com/nanome-ai/plugin-chemical-properties'>`_
 - `Molecular dynamics <'https://github.com/nanome-ai/plugin-molecular-dynamics'>`_
 - Custom Database Integrations
 - Loading PDFs and PowerPoints
 - All of our public plugins are available on our `Github <https://github.com/nanome-ai>` (prefixed with "plugin-").

The primary requirements for running plugins are the Nanome Virtual Reality Software and access to the Nanome Plugin Server (NTS). The Nanome Plugin Server acts as a relay to forward plugin information and processes data coming into and going out of the Nanome virtual environment. 

The Nanome Virtual Reality Software can be acquired directly from Nanome or in any of the VR stores here:
 * Oculus Store: https://www.oculus.com/experiences/rift/1873145426039242
 * Viveport: https://www.viveport.com/apps/0a467f78-2ed2-43eb-ada8-9d677d5acf54
 * Steam: https://store.steampowered.com/app/493430/Nanome/
 * Direct Download: https://nanome.ai/setup
 * Sidequest: https://sidequestvr.com/app/333/nanome