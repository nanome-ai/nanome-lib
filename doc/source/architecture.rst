############
Architecture
############

The overall architecture of this plugin system is designed to enable plugin creators to iterate fast and efficiently when developing, improving, or debugging a plugin for Nanome.

If you have any feedback or question, don't hesitate to contact us or to directly contribute to our `Github <https://github.com/nanome-ai>`_


How it works
^^^^^^^^^^^^

Here is a simple way to represent the Plugin System architecture:

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

1. NTS (the plugin server) is aware of which plugins and sessions are connected to it, and who is the presenter of each session.
2. A session asks to connect to a plugin
3. NTS transfers the request to the target plugin
4. The plugin creates a subprocess on its computer, and instantiates its plugin class
5. The subprocess replies to its main process, which transfers the reply to NTS, which transfers the reply to the room presenter
6. Connection is established until the presenter requests a disconnection or the plugin is stopped.

NB: A plugin cannot talk to a Nanome session/user before being connected to it.
NB2: Communications are encrypted from Nanome to NTS and from NTS to Plugins


Development iterations
^^^^^^^^^^^^^^^^^^^^^^

As a result of this flexible architecture, no need to restart Nanome if your plugin crashes, or if you need to improve it:

1. Stop your plugin. All sessions connected to it will be disconnected.
2. Modify the python script
3. Restart it
4. Reconnect to it in Nanome. Using the 2D mode of Nanome might be useful in order to reconnect and test faster without having to wear your VR headset everytime.
