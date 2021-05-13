class PresenterInfo():
    """
    | Class to fetch information about the current nanome session's presenter.
    """
    def __init__(self):
        self._account_id = ""
        self._account_name = ""
        self._account_email = ""

    @property
    def account_id(self):
        """
        Get the nanome account ID of the presenter

        :type: string
        """
        return self._account_id
    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def account_name(self):
        """
        Get the nanome account name of the presenter
        
        :type: string
        """
        return self._account_name
    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def account_email(self):
        """
        Get the nanome account email of the presenter
        
        :type: string
        """
        return self._account_email
    @account_email.setter
    def account_email(self, value):
        self._account_email = value