import random
import numpy as np
import copy
import os


class SpeckAST:
    def __init__(self, max_program_size, initial_program_size, max_variables, max_constants, number_const_min=None,
                 number_const_max=None, number_const_size=None, number_const_list=None, variables=None, constants=None,
                 indent=0):
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_constants = max_constants
        self.indent = indent

        if isinstance(number_const_list, np.ndarray):
            self.number_const_list = number_const_list
        else:
            self.number_const_list = np.linspace(number_const_min, number_const_max, number_const_size)

        self.variables = variables if variables else []
        self.constants = constants if constants else []
        self.children = []
        self.allowed_children = [
            self.OutputStatement,
            self.InputStatement,
            self.AssigmentStatement
        ]
        self.allowed_children_when_variables_exist = [
            self.ConditionStatement,
            self.LoopStatement
        ]
        self.generate_children(initial_program_size)

    class ParseTreeNode:
        def __init__(self, children=None):
            self.children = children if children else []

        def __str__(self):
            pass

        def mutate(self):
            pass

    def __str__(self):
        result = ''
        for child in self.children:
            result += (' ' * self.indent) + str(child) + '\n'
        return result

    def generate_children(self, initial_program_size):
        for _ in range(initial_program_size):
            allowed_children = self.allowed_children
            if self.variables:
                allowed_children.extend(self.allowed_children_when_variables_exist)
            self.children.append(random.choice(allowed_children).generate(self))

    class OutputStatement(ParseTreeNode):
        def __str__(self):
            return f'out({str(self.children[0])});'

        @classmethod
        def generate(cls, root):
            return cls([root.Expression.generate(root)])

    class InputStatement(ParseTreeNode):
        def __str__(self):
            return f'in({str(self.children[0])});'

        @classmethod
        def generate(cls, root):
            variable_index = random.randint(1, len(root.variables) + 1)
            variable_name = f'x{variable_index}'
            if variable_name not in root.variables:
                root.variables.append(variable_name)

            return cls([variable_name])

    class Expression(ParseTreeNode):
        TERMINALS = ['+', '-', '/', '*', '>', '<', '==', '!=', '<=', '>=']

        def __str__(self):
            result = ''
            for child in self.children:
                result += str(child)
            return result

        @classmethod
        def generate(cls, root, variable_to_be_included=None):
            expression_type = random.randint(0, 1)

            if variable_to_be_included:
                if expression_type == 0:  # terminal (number or the variable/constant)
                    return cls([variable_to_be_included])
                elif expression_type == 1:  # expression
                    expression_children = []
                    expression_children.extend([
                        cls([variable_to_be_included]),
                        random.choice(root.Expression.TERMINALS),
                        cls.generate_terminal_expression(root)
                    ])
                    return cls(expression_children)

            if expression_type == 0:  # terminal (number or the variable/constant)
                return cls.generate_terminal_expression(root)
            elif expression_type == 1:  # expression
                expression_children = []
                expression_children.extend([
                    cls.generate_terminal_expression(root),
                    random.choice(root.Expression.TERMINALS),
                    cls.generate_terminal_expression(root)
                ])
                return cls(expression_children)

        @classmethod
        def generate_terminal_expression(cls, root):
            if not root.variables and not root.constants:
                return cls([random.choice(root.number_const_list)])

            terminal_type = random.choice(['Number', 'Variable'])
            if terminal_type == 'Number':
                return cls([random.choice(root.number_const_list)])

            variable_or_constant = random.choice(root.variables + root.constants)
            return cls([variable_or_constant])

    class AssigmentStatement(ParseTreeNode):
        def __str__(self):
            return f'{str(self.children[0])} = {str(self.children[1])};'

        @classmethod
        def generate(cls, root, variable_to_be_included=None):
            expression = root.Expression.generate(root)
            if variable_to_be_included:
                return cls([variable_to_be_included, expression])

            variable_or_constant = None

            assigment_type = random.choice(['Variable', 'Constant'])
            if assigment_type == 'Variable' or len(root.constants) == root.max_constants:
                variable_index = random.randint(1, len(root.variables) + 1)
                variable_or_constant = f'x{variable_index}'
                if variable_or_constant not in root.variables:
                    root.variables.append(variable_or_constant)
            else:
                constant_index = len(root.constants)
                variable_or_constant = f'X{constant_index}'
                root.constants.append(variable_or_constant)

            if not variable_or_constant:
                raise 'Something went wrong, the variable/constant was not generated'

            return cls([variable_or_constant, expression])

    class StatementWithBody(ParseTreeNode):
        def __init__(self, children=None, indent=0):
            super().__init__(children)
            self.indent = indent

        @classmethod
        def generate(cls, root):
            variable_to_be_included = random.choice(root.variables)
            condition = root.Expression.generate(root, variable_to_be_included)
            body = SpeckAST(max_program_size=root.max_program_size // 10,
                            initial_program_size=1,
                            max_variables=root.max_variables,
                            max_constants=root.max_constants,
                            number_const_list=root.number_const_list,
                            variables=copy.deepcopy(root.variables),
                            constants=copy.deepcopy(root.constants),
                            indent=root.indent + 4
                            )
            assigment_to_be_included = root.AssigmentStatement.generate(root, variable_to_be_included)
            return cls([condition, body, assigment_to_be_included], indent=root.indent)

    class ConditionStatement(StatementWithBody):
        def __str__(self):
            return f'if({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * (self.indent + 4)) + \
                   str(self.children[2]) + '\n' + (' ' * self.indent) + '}'

    class LoopStatement(StatementWithBody):
        def __str__(self):
            return f'while({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * (self.indent + 4)) + \
                   str(self.children[2]) + '\n' + (' ' * self.indent) + '}'

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
                          (program1.ConditionStatement, program1.LoopStatement, program1.AssigmentStatement)) and \
                    isinstance(subtree2,
                               (program2.ConditionStatement, program2.LoopStatement, program2.AssigmentStatement)):
                # Zamiana poddrzew
                program1.children[idx1] = subtree2
                program2.children[idx2] = subtree1

        return program1, program2


def save_program_to_file(folder, filename, program):
    # Upewnij się, że folder istnieje
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, filename)
    with open(file_path, 'w') as f:
        f.write(str(program))


# Tworzymy dwa programy
program1 = SpeckAST(1000, 10, 10, 10, -5, 6, 100)
program2 = SpeckAST(1000, 10, 10, 10, -5, 6, 100)

# Zapisz programy przed crossoverem
save_program_to_file("crossover", "program1_before_crossover.txt", program1)
save_program_to_file("crossover", "program2_before_crossover.txt", program2)

# Wykonaj crossover na dwóch programach
program1, program2 = program1.crossover(program1, program2, num_crossovers=3)

# Zapisz programy po crossoverze
save_program_to_file("crossover", "program1_after_crossover.txt", program1)
save_program_to_file("crossover", "program2_after_crossover.txt", program2)

print("Programy zapisane do folderu crossover.")
