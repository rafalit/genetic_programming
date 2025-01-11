import random
import numpy as np
import time
from .output_statement import OutputStatement
from .input_statement import InputStatement
from .assigment_statement import AssigmentStatement
from .condition_statement import ConditionStatement
from .loop_statement import LoopStatement
from .expression import Expression
from copy import deepcopy


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
        self.depth = 0  # Głębokość, która jest teraz przechowywana bezpośrednio w atrybucie 'depth'
        self.statement_with_body_initial_length = statement_with_body_initial_length
        self.fitness = float('-inf')

        # Ustawienia generowanych liczb
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
            if self.depth < self.max_depth:
                child = random.choice(self.allowed_children).generate(self, self.depth)
                self.children.append(child)
            else:
                break

    @classmethod
    def crossover(cls, program1, program2):
        program1 = deepcopy(program1)
        node_to_be_replaced = random.choice(program1.program_nodes())
        depth_of_replaced_node = node_to_be_replaced[-1].depth  # Uzyskujemy głębokość z istniejącego węzła

        nodes_for_replacing = program2.program_nodes()
        if isinstance(node_to_be_replaced[-1], Expression):
            nodes_for_replacing = list(filter(lambda node: isinstance(node[-1], Expression), nodes_for_replacing))
        else:
            nodes_for_replacing = list(filter(lambda node: not isinstance(node[-1], Expression), nodes_for_replacing))

        if not nodes_for_replacing:
            return program1.mutation()

        current_node = program1
        for index in node_to_be_replaced[:-2]:
            current_node = current_node.children[index]

        current_node.children[node_to_be_replaced[-2]] = deepcopy(random.choice(nodes_for_replacing)[-1])

        if hasattr(current_node.children[node_to_be_replaced[-2]], 'depth') and current_node.children[
            node_to_be_replaced[-2]].depth > program1.max_depth:
            current_node.children[node_to_be_replaced[-2]].depth = program1.max_depth

        return program1

    def mutation(self):
        mutated_program = deepcopy(self)
        node_to_be_replaced = random.choice(mutated_program.program_nodes())
        depth_of_replaced_node = node_to_be_replaced[-1].depth  # Uzyskujemy głębokość z istniejącego węzła

        new_node = None
        if isinstance(node_to_be_replaced[-1], Expression):
            new_node = Expression.generate(self, depth_of_replaced_node)
        else:
            new_node = random.choice(self.allowed_children).generate(self, depth_of_replaced_node)

        current_node = mutated_program
        for index in node_to_be_replaced[:-2]:
            current_node = current_node.children[index]

        current_node.children[node_to_be_replaced[-2]] = new_node
        return mutated_program

    def program_nodes(self):
        result = []
        for i, child in enumerate(self.children):
            result.extend([(i, *statement) for statement in child.node_list()])
        return result

    def get_program(self):
        program_str = ''
        for child in self.children:
            program_str += str(child) + '\n'
        return program_str
