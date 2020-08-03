import argparse
import itertools
import tabulate
from variable import Variable
from formula import Formula


class TruthTable:
    """
    From a given string, creates a truth table.
    Given a string, to convert it to a formula object the string will be transformed
    into an RPN list with tokens using the shunting yard algorithm and
    then the formula object will be created from the RPN list.
    """

    def __init__(self, string=""):
        # string to be read and information about the string
        self.string = string
        self.string_len = len(self.string)
        self.string_index = 0
        # the formula object
        self.formula = None
        # variables in the formula object
        self.variables = []
        # truth table
        self.table = None

    @staticmethod
    def parse_args():
        """ Parses a string given as command line argument. """
        parser = argparse.ArgumentParser(description="Creates a truth table from a given formula")
        parser.add_argument("formula", metavar="FORMULA", type=str, help="truth table formula")
        return parser.parse_args()

    def create_formula(self):
        rpn = self.get_rpn()[::-1]  # reverses the list to read from the end using rpn.pop()
        stack = []
        while rpn:
            value = rpn.pop()
            if TruthTable.is_operator(value):
                if value == "~":
                    operands = [stack.pop()]
                else:
                    operand_2 = stack.pop()
                    operand_1 = stack.pop()
                    operands = [operand_1, operand_2]
                value = Formula(operands, value)
            stack.append(value)
        self.formula = stack.pop()

    def get_rpn(self):
        """ Transforms the input string in an RPN string using the shunting yard algorithm. """
        oper_stack = []
        out_queue = []
        token = self.read_token()
        while token:
            if token in "->v^~":
                while oper_stack and TruthTable.greater_op(oper_stack[-1], token) and oper_stack[-1] != "(":
                    out_queue.append(oper_stack.pop())
                oper_stack.append(token)
            elif "(" == token:
                oper_stack.append("(")
            elif ")" == token:
                while oper_stack and oper_stack[-1] != "(":
                    out_queue.append(oper_stack.pop())
                if oper_stack[-1] == "(":
                    oper_stack.pop()
            elif token.isalpha():
                out_queue.append(self.add_variable(token))
            token = self.read_token()
        out_queue.extend(oper_stack[::-1])
        return out_queue

    def read_token(self):
        token = ""
        while self.string_index < self.string_len and not TruthTable.is_operator_char(self.string[self.string_index]):
            token += self.string[self.string_index]
            self.string_index += 1
        token = token.strip()
        # if couldn't read any non operator chars tries to read operator chars
        return token if token else self.read_operator()

    def read_operator(self):
        operator = ""
        # Checks not TruthTable.is_operator(operator) so it doesn't read two different operators together ex: ~(
        while self.string_index < self.string_len and not TruthTable.is_operator(operator)  \
                and TruthTable.is_operator_char(self.string[self.string_index]):
            operator += self.string[self.string_index]
            self.string_index += 1
        return operator

    @staticmethod
    def is_operator_char(char):
        return char in "->^v~()"

    @staticmethod
    def is_operator(string):
        return string in ["->", "^", "v", "~", "(", ")"]

    @staticmethod
    def greater_op(operator_1, operator_2):
        """ Returns True if operator_1 has a higher precedence that operator_2, else returns False. """
        if operator_1 == "~":
            return True if operator_2 != "~" else False
        elif operator_1 in "v^":
            return True if operator_2 not in "~v^" else False
        elif operator_1 == "->":
            return False

    def add_variable(self, new_var_name):
        """
        Creates a variable using new_var_name, adds it to the variables list and returns it.
        If a variable with that name already exists,  returns it and doesn't create a new variable.
        """
        var = self.get_var(new_var_name)
        if not var:
            var = Variable(new_var_name)
            self.variables.append(var)
        return var

    def get_var(self, var_name):
        """ Retuns the variable with the same name as var_name, returns None if no such variable is found. """
        for var in self.variables:
            if var.name == var_name:
                return var
        return None

    def create_table(self):
        self.table = []
        self.table.append(self.get_table_header())
        self.table.extend(self.get_table_rows())

    def get_table_header(self):
        table_header = self.get_var_names()
        table_header.append(str(self.formula))
        return table_header

    def get_table_rows(self):
        table_rows = []
        evaluations = [list(i) for i in itertools.product([False, True], repeat=len(self.variables))]
        for evaluation in evaluations:
            self.set_evaluation(evaluation)
            evaluation.append(self.formula.get_logic_value())
            table_rows.append(evaluation)
        return table_rows

    def get_var_names(self):
        var_names = []
        for var in self.variables:
            var_names.append(var.name)
        return var_names

    def set_evaluation(self, evaluation):
        """ Given a list of boolean values, changes the boolean values of the variables in the formula. """
        for i in range(len(self.variables)):
            self.variables[i].value = evaluation[i]

    def print_table(self):
        print(tabulate.tabulate(self.table[1:], headers=self.table[0]))


if __name__ == '__main__':
    formula_str = TruthTable.parse_args().formula.strip()
    table = TruthTable(formula_str)
    table.create_formula()
    table.create_table()
    table.print_table()
