class Variable:
    """ With a name and a truth value represents a logic variable. """

    def __init__(self, name):
        self.name = name
        self.value = False

    def get_logic_value(self):
        return self.value

    def __str__(self):
        return self.name
