class StringBuilder:
    """
    | A class to build strings from lists of strings. This class is used internally.
    """

    def __init__(self):
        self.los = []

    def append(self, s):
        """
        | Converts an object to a string and appends it to this StringBuilder's list of strings.

        :param s: The object to be appended as a string.
        """
        self.los.append(str(s))

    def append_string(self, s):
        """
        | Appends a string to this StringBuilder's list of strings.

        :param s: The string to be appended.
        """
        self.los.append(s)

    def to_string(self, joiner=""):
        """
        | Return a string joined with joiner from this StringBuilder's list of strings.

        :param joiner: The string to join between each element of this StringBuilder's list of strings.
        :return: A new string created from this StringBuilder's list of strings.
        :rtype: :class:`str`
        """
        joined = joiner.join(self.los)
        self.los = [joined]
        return joined

    def clear(self):
        """
        | Clears this StringBuilder's list of strings.
        """
        del self.los[:]
