import random
import numpy as np
from .output_statement import OutputStatement
from .input_statement import InputStatement
from .assigment_statement import AssigmentStatement
from .condition_statement import ConditionStatement
from .loop_statement import LoopStatement


class SpeckAST:
    def __init__(self, max_program_size, initial_program_size, max_variables, max_depth,
                 number_const_min=0, number_const_max=10, number_const_size=11,
                 number_const_list=None, variables=None, statement_with_body_initial_length=2):
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_depth = max_depth
        self.depth = 0
        self.statement_with_body_initial_length = statement_with_body_initial_length

        if number_const_list is None:
            self.number_const_list = np.linspace(number_const_min, number_const_max, number_const_size)
        else:
            self.number_const_list = number_const_list

        self.children = []

        self.variables = variables if variables is not None else np.zeros(max_variables)
        self.allowed_children = [
            OutputStatement,
            InputStatement,
            AssigmentStatement,
            ConditionStatement,
            LoopStatement
        ]
        self.generate_children(initial_program_size)

    def __str__(self):
        result = ''
        for child in self.children:
            result += str(child) + '\n'
        return result

    def run(self):
        for child in self.children:
            child.run(self)

    def generate_children(self, initial_program_size):
        for _ in range(initial_program_size):
            self.children.append(random.choice(self.allowed_children).generate(self, self.depth))
