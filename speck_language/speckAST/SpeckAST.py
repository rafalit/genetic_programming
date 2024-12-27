import random
import numpy as np
import os
import math
from .parse_tree_node import ParseTreeNode
from .output_statement import OutputStatement
from .input_statement import InputStatement
from .assigment_statement import AssigmentStatement
from .condition_statement import ConditionStatement
from .loop_statement import LoopStatement


class SpeckAST:
    def __init__(self, max_program_size, initial_program_size, max_variables,
                 number_const_min=0, number_const_max=10, number_const_size=11,
                 number_const_list=None, variables=None, indent=0):
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.indent = indent

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
            result += (' ' * self.indent) + str(child) + '\n'
        return result

    def run(self):
        for child in self.children:
            child.run(self)

    def generate_children(self, initial_program_size):
        for _ in range(initial_program_size):
            self.children.append(random.choice(self.allowed_children).generate(self))

    def mutate_program(self):
        for child in self.children:
            if isinstance(child, ParseTreeNode):
                child.mutate()

    def crossover(self, program1, program2, num_crossovers=3):
        """Perform multiple subtree swaps between two programs, ensuring logical correctness."""
        for _ in range(num_crossovers):
            # Losujemy punkty crossover w obu programach
            idx1 = random.randint(0, len(program1.children) - 1)
            idx2 = random.randint(0, len(program2.children) - 1)

            # Wybieramy poddrzewo (część programu) z obu programów
            subtree1 = program1.children[idx1]
            subtree2 = program2.children[idx2]

            # Jeśli poddrzewo to jest typu "if", "while" lub "assign", możemy je wymienić
            if isinstance(subtree1,
                          (ConditionStatement, LoopStatement, AssigmentStatement)) and \
                    isinstance(subtree2,
                               (ConditionStatement, LoopStatement, AssigmentStatement)):
                # Zamiana poddrzew
                program1.children[idx1] = subtree2
                program2.children[idx2] = subtree1

        return program1, program2

    def random_subtree(self, program):
        nodes = [(program, -1, None)]
        while nodes:
            node, idx, parent = nodes.pop(random.randint(0, len(nodes) - 1))
            if isinstance(node, ParseTreeNode) and random.random() < 0.2:
                return node, (parent, idx)
            elif isinstance(node, ParseTreeNode):
                nodes.extend([(child, idx, node) for idx, child in enumerate(node.children)])
        return None, None




