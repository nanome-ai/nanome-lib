############
Plugin System Architecture
############

If you have any questions feel free to contact us on our user group slack. Join by going to https://nanome.ai/slack.


************
How it works
************

Nanome's Plugin System Architecture is a Client- Server Relay - Service type system. Hardware Devices such as Virtual Reality and Augmented Reality headsets, Laptops, and Mobile phones have a Nanome client-side application that is responsible for rendering and user inputs. When a user activates a Nanome plugin from the client, the Nanome client forwards the request to the Plugin Relay Server (called "NTS"). This relay service directs the user-input and necessary Nanome Workspace information to the appropriate plugin service (e.g. Minimization, Docking, Chemical Interactions). These plugin services are actually containerized (Docker) microservices that run on a linux server (virtual machine).

See the graphic below:

.. code-block:: none

   +---------------------------------+           +-------------------------------------------------+
   |                  +-----------+  |           |                                                 |
   |                  |Nanome User|  |           |                                                 |
   |                  |"Alice"    +<------------>+                                                 |
   |Room              +-----------+  |           |                                                 |
   |"Alice's Room"    +-----------+  |           |                                                 |
   |                  |Nanome User|  |           |                                                 |
   |                  |"Bob"      |  |           | NTS                                             |
   |                  +-----------+  |           |                                                 |
   +---------------------------------+           | - Session A: "Alice's Room" (Alice is presenter)|
   +---------------------------------+           | - Session B: "Dan's Room" (Carol is presenter)  |
   |                  +-----------+  |           |                                                 |
   |                  |Nanome User|  |           | - Plugin A: Docking Plugin                      |
   |                  |"Carol"    +<------------>+                                                 |
   |Room              +-----------+  |           |                                                 |
   |"Dan's Room"      +-----------+  |           |                                                 |
   |                  |Nanome User|  |           |                                                 |
   |                  |"Dan"      |  |           |                                                 |
   |                  +-----------+  |           |                                                 |
   +---------------------------------+           +---------------------^---------------------------+
                                                                       |
                                                     +-------------------------------------+
                                                     |                 |                   |
                                                     |          +------v-------+           |
                                                     |          |Docking Plugin|           |
                                                     |          +^------------^+           |
                                                     |           |            |            |
                                                     | +---------v-+         +v----------+ |
                                                     | |Sub-process|         |Sub-process| |
                                                     | |(Session A)|         |(Session B)| |
                                                     | +-----------+         +-----------+ |
                                                     +-------------------------------------+

1. The Plugin Relay Server (NTS) is aware of which specific plugins and sessions (Active Nanome Room) are connected to it, and has the information of who the presenter is for the Nanome Room (session).
2. When a Nanome Room is launched from within the client application, it first connects to NTS and creates a new "session". Depending on the configuration of the Nanome Account with NTS, a list of plugins available to the user is shown in the Nanome session via the Stacks Menu.
4. When a user wants to interact with a plugin, they first activate the plugin connection manually or it is done automatically through a "native integration". Native Integrations are specific hooks in the Nanome app which can be automatically triggered in Nanome's core feature functionality (e.g. auto-minimization)
3. After the user interacts and runs a plugins' functioanlity, NTS transfers the request to the designated plugin microservice
4. The plugin service creates a subprocess on it's local CPU, and instantiates its particular plugin class
5. the subprocess is typically the plugin business logic running and when completed, the subprocess transfers the response to the main process which in turn goes to NTS and then finally back to the Room Presenter. 
6. The plugin connection from user to NTS and from NTS to plugin service instance is established until the Nanome room presenter manually requests a disconnection, leaves the Nanome room, or if the plugin service is stopped.

Note that a plugin cannot talk to a Nanome session/user before being connected first. 

Nanome's network calls use Industry standard AES 512 bit encryption on all network traffic.

**************
API Structure
**************
The Nanome Plugin API is grouped into a few key submodules:

- :mod:`nanome.api.plugin_instance`: Contains PluginInstance class, which provides interface for interacting with your Nanome workspace
- :mod:`nanome.api.plugin`: Contains Plugin class, which manages networking and callbacks.
- :mod:`nanome.api.structure`: Workspace API. Used for modeling atomic structures and representations.
- :mod:`nanome.api.ui`: Build Menus and forms for your plugin.
- :mod:`nanome.api.shapes`: Render custom shapes, meshes, and lines into workspace. (does not serialize/save to Nanome Workspace file since it is a stream.
- :mod:`nanome.api.streams`: Real time updates to one or more objects in your workspace.
- :mod:`nanome.api.util`: Enums, data structures, and utility functions used throughout our plugins.
- :mod:`nanome.api.integrations`: Integrations allow plugins to hook into Nanome features (such as minimization or hydrogens calculations).
- :mod:`nanome.api.macros`: Enable macro scripts written in Lua to be run (not yet documented).

**********************
Development Tips
**********************

Thanks to this flexible architecture, developing plugins does not require the Nanome client-application to be restarted if your plugin crashes or you want to make a small change during development.

You will need a Nanome Plugin API Key in order to make a Nanome plugin. Please contact your sales representative for your organizations dedicated API key.

The Nanome client application's 2D mode is especially useful to do quick iterations and test them.
