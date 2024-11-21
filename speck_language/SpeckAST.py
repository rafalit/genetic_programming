import random
import numpy as np
import copy
import os


class SpeckAST:
    def __init__(self, max_program_size, initial_program_size, max_variables, max_constants,
                 number_const_min=0, number_const_max=10, number_const_size=5,
                 number_const_list=None, variables=None, constants=None, indent=0):
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_constants = max_constants
        self.indent = indent

        if number_const_list is None:
            self.number_const_list = np.linspace(number_const_min, number_const_max, number_const_size)
        else:
            self.number_const_list = number_const_list

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
        def __init__(self, root, children=None):
            self.root = root  # Referencja do nadrzędnego SpeckAST
            self.children = children if children else []

        def mutate(self):
            pass

        def __str__(self):
            return ''

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
            return cls(root, [root.Expression.generate(root)])

    class InputStatement(ParseTreeNode):
        def __str__(self):
            return f'in({str(self.children[0])});'

        @classmethod
        def generate(cls, root):
            variable_index = random.randint(1, len(root.variables) + 1)
            variable_name = f'x{variable_index}'
            if variable_name not in root.variables:
                root.variables.append(variable_name)
            return cls(root, [variable_name])

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
                if expression_type == 0:
                    return cls(root, [variable_to_be_included])
                elif expression_type == 1:
                    return cls(root, [
                        cls(root, [variable_to_be_included]),
                        random.choice(cls.TERMINALS),
                        cls.generate_terminal_expression(root)
                    ])

            if expression_type == 0:
                return cls.generate_terminal_expression(root)
            elif expression_type == 1:
                return cls(root, [
                    cls.generate_terminal_expression(root),
                    random.choice(cls.TERMINALS),
                    cls.generate_terminal_expression(root)
                ])

        @classmethod
        def generate_terminal_expression(cls, root):
            if not root.variables and not root.constants:
                return cls(root, [random.choice(root.number_const_list)])

            terminal_type = random.choice(['Number', 'Variable'])
            if terminal_type == 'Number':
                return cls(root, [random.choice(root.number_const_list)])

            variable_or_constant = random.choice(root.variables + root.constants)
            return cls(root, [variable_or_constant])

        def mutate(self):
            mutation_type = random.choice(["replace_operator", "change_terminal", "rebuild_expression"])
            if mutation_type == "replace_operator":
                for i in range(len(self.children)):
                    if self.children[i] in self.TERMINALS:
                        self.children[i] = random.choice(self.TERMINALS)
            elif mutation_type == "change_terminal":
                for i in range(len(self.children)):
                    if isinstance(self.children[i], str) and self.children[i] not in self.TERMINALS:
                        if self.children[i] in self.root.variables:
                            self.children[i] = random.choice(self.root.variables)
                        elif self.children[i] in self.root.constants:
                            self.children[i] = random.choice(self.root.constants)
            elif mutation_type == "rebuild_expression":
                new_expression = self.generate_terminal_expression(self.root)
                self.children = new_expression.children

    class AssigmentStatement(ParseTreeNode):
        def __str__(self):
            return f'{str(self.children[0])} = {str(self.children[1])};'

        @classmethod
        def generate(cls, root, variable_to_be_included=None):
            expression = root.Expression.generate(root)
            if variable_to_be_included:
                return cls(root, [variable_to_be_included, expression])

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
                raise Exception('Something went wrong, the variable/constant was not generated')

            return cls(root, [variable_or_constant, expression])

        def mutate(self):
            if random.random() < 0.5:
                self.children[0] = random.choice(self.root.variables + self.root.constants)
            if random.random() < 0.5:
                self.children[1] = SpeckAST.Expression.generate(self.root)

    class StatementWithBody(ParseTreeNode):
        def __init__(self, root, children=None, indent=0):
            super().__init__(root, children)
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
                            indent=root.indent + 4)
            assigment_to_be_included = root.AssigmentStatement.generate(root, variable_to_be_included)
            return cls(root, [condition, body, assigment_to_be_included], indent=root.indent)

        def mutate(self):
            if random.random() < 0.5:
                variable = random.choice(self.root.variables)
                self.children[0] = self.root.Expression.generate(self.root, variable)
            self.children[1].mutate_program()

    class ConditionStatement(StatementWithBody):
        def __str__(self):
            return f'if({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * (self.indent + 4)) + \
                   str(self.children[2]) + '\n' + (' ' * self.indent) + '}'

    class LoopStatement(StatementWithBody):
        def __str__(self):
            return f'while({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * (self.indent + 4)) + \
                   str(self.children[2]) + '\n' + (' ' * self.indent) + '}'

    def mutate_program(self):
        #print("\nProgram przed mutacją:\n")
        #print(self)
        for child in self.children:
            if isinstance(child, SpeckAST.ParseTreeNode):
                child.mutate()
        #print("\nProgram po mutacji:\n")
        #print(self)

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

    def random_subtree(self, program):
        nodes = [(program, -1, None)]
        while nodes:
            node, idx, parent = nodes.pop(random.randint(0, len(nodes) - 1))
            if isinstance(node, SpeckAST.ParseTreeNode) and random.random() < 0.2:
                return node, (parent, idx)
            elif isinstance(node, SpeckAST.ParseTreeNode):
                nodes.extend([(child, idx, node) for idx, child in enumerate(node.children)])
        return None, None


# Tworzenie folderów do zapisu wyników
os.makedirs('programs', exist_ok=True)
os.makedirs('mutation', exist_ok=True)
os.makedirs('crossover', exist_ok=True)

# Tworzenie dwóch programów
program1 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_constants=3)
program2 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_constants=3)
program3 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_constants=3)
program4 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_constants=3)
program5 = SpeckAST(max_program_size=15, initial_program_size=7, max_variables=5, max_constants=5)

# Wyświetlanie początkowych programów
print("Początkowy Program 1:")
print(program1)

print("\nPoczątkowy Program 2:")
print(program2)

print("\nPoczątkowy Program 3:")
print(program3)

print("\nPoczątkowy Program 4:")
print(program4)

print("\nPoczątkowy Program 5:")
print(program5)

# Zapisanie początkowych programów do folderu programs
with open('programs/program1.txt', 'w') as f1, open('programs/program2.txt', 'w') as f2, open('programs/program3.txt', 'w') as f3, open('crossover/program4.txt', 'w') as f4, open('crossover/program5.txt', 'w') as f5:
    f1.write(str(program1))
    f2.write(str(program2))
    f3.write(str(program3))
    f4.write(str(program4))
    f5.write(str(program5))

# Mutacja programów
print("\nMutowanie Programów...")

print("\nMutowanie Programu 1...")
program1.mutate_program()

print("Mutowanie Programu 2...")
program2.mutate_program()

print("Mutowanie Programu 3...\n")
program3.mutate_program()



# Zapisanie programów po mutacji do folderu mutation
with open('mutation/program1_mutation.txt', 'w') as f1, open('mutation/program2_mutation.txt', 'w') as f2, open('mutation/program3_mutation.txt', 'w') as f3:
    f1.write(str(program1))
    f2.write(str(program2))
    f3.write(str(program3))

print("Crossowanie Programów...\n")
print("Crossowanie Programu 4 z Programem 5...\n")

# Wykonanie crossover pomiędzy programem 4 a programem 5
program4, program5 = program4.crossover(program4, program5, num_crossovers=4)

# Wyświetlenie programów po crossoverze


# Zapisanie programów po crossoverze do folderu 'mutation'
with open('crossover/program4_crossover.txt', 'w') as f4, open('crossover/program5_crossover.txt', 'w') as f5:
    f4.write(str(program4))
    f5.write(str(program5))


