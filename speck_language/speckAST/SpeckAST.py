import random
import numpy as np
import time
from .output_statement import OutputStatement
from .input_statement import InputStatement
from .assigment_statement import AssigmentStatement
from .condition_statement import ConditionStatement
from .loop_statement import LoopStatement


class SpeckAST:
    def __init__(self, max_program_size, initial_program_size, max_variables, max_depth,
                 number_const_min=0, number_const_max=10, number_const_size=11,
                 number_const_list=None, variables=None, statement_with_body_initial_length=2):
        self.program_start = None
        self.time_limit = None
        self.current_input_index = None
        self.output_size = None
        self.input_list = None
        self.output_list = None
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

    def run(self, input_list, output_size, time_limit):
        self.input_list = np.array(input_list)
        self.current_input_index = 0
        self.output_list = []
        self.output_size = output_size
        self.time_limit = time_limit
        self.program_start = time.time()
        for child in self.children:
            child.run(self)
        return self.output_list

    def get_value_from_input(self):
        input_value = self.input_list[self.current_input_index]
        self.current_input_index = 0 if self.current_input_index + 1 >= len(self.input_list) \
            else self.current_input_index + 1
        return input_value

    def save_value_to_output(self, value):
        if len(self.output_list) >= self.output_size:
            return

        value = float(value)
        value = int(value) if value.is_integer() else value

        self.output_list.append(value)

    def generate_children(self, initial_program_size):
        for _ in range(initial_program_size):
            self.children.append(random.choice(self.allowed_children).generate(self, self.depth))
