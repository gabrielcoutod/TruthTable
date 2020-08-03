class Formula:
    """ Represents a logic formula. """

    def __init__(self, operands, operator):
        """
        Operands has to be a list of formulas or list of variables even if the logic formula
        has only one variable(ex: ~p). The leaves of the tree will be variables.
        """
        self.operands = operands
        self.operator = operator

    def get_logic_value(self):
        if self.operator == "~":
            return not self.operands[0].get_logic_value()
        elif self.operator == "v":
            return self.operands[0].get_logic_value() or self.operands[1].get_logic_value()
        elif self.operator == "^":
            return self.operands[0].get_logic_value() and self.operands[1].get_logic_value()
        elif self.operator == "->":
            # uses the equivalence p->q = ~p v q
            return not self.operands[0].get_logic_value() or self.operands[1].get_logic_value()

    def __str__(self):
        if self.operator == "~":
            return f"~{self.operands[0]}"
        elif self.operator == "v":
            return f"({self.operands[0]} v {self.operands[1]})"
        elif self.operator == "^":
            return f"({self.operands[0]} ^ {self.operands[1]})"
        elif self.operator == "->":
            return f"({self.operands[0]} -> {self.operands[1]})"
