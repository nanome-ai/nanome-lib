Notifications API
=================
Send a Notification of each type to the user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def on_run(self):
        self.send_notification(nanome.util.enums.NotificationTypes.error, "There was an error")
        self.send_notification(nanome.util.enums.NotificationTypes.message, "This is a message for the user")
        self.send_notification(nanome.util.enums.NotificationTypes.success, "Something good might have happened)
        self.send_notification(nanome.util.enums.NotificationTypes.warning, "Something bad might have happened")
