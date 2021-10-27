class PresenterInfo():
    """
    | Class to fetch information about the current nanome session's presenter.
    """

    def __init__(self):
        self._account_id = ""
        self._account_name = ""
        self._account_email = ""
        self._has_org = False
        self._org_id = 0
        self._org_name = ""

    @property
    def account_id(self):
        """
        | The Nanome account ID of the presenter

        :type: :class:`str`
        """
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def account_name(self):
        """
        | The Nanome account name of the presenter

        :type: :class:`str`
        """
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def account_email(self):
        """
        | The Nanome account email of the presenter

        :type: :class:`str`
        """
        return self._account_email

    @account_email.setter
    def account_email(self, value):
        self._account_email = value

    @property
    def has_org(self):
        """
        | If the presenter belongs to an organization

        :type: :class:`bool`
        """
        return self._has_org

    @has_org.setter
    def has_org(self, value):
        self._has_org = value

    @property
    def org_id(self):
        """
        | The ID of the organization the presenter belongs to

        :type: :class:`int`
        """
        return self._org_id

    @org_id.setter
    def org_id(self, value):
        self._org_id = value

    @property
    def org_name(self):
        """
        | The name of the organization the presenter belongs to

        :type: :class:`str`
        """
        return self._org_name

    @org_name.setter
    def org_name(self, value):
        self._org_name = value
