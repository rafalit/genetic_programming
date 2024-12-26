from .parse_tree_node import ParseTreeNode
import random
import math

class Expression(ParseTreeNode):
    TERMINALS = ['+', '-', '/', '*', '>', '<', '==', '!=', '<=', '>=', 'and', 'or']

    def __str__(self):
        result = ''
        for child in self.children:
            result += str(child)

        if len(self.children) == 3:
            return f'({result})'

        return result

    def run(self, root):
        if len(self.children) == 1:
            if isinstance(self.children[0], str):
                index = int(self.children[0][1:])
                if self.children[0][0] == 'x':
                    return root.variables[index]
                return root.constants[index]
            return self.children[0]
        elif len(self.children) == 2 and self.children[0] == '!':
            expression_result = self.children[1].run(root)
            return -1 if expression_result > 0 else 1
        else:
            left = self.children[0].run(root)
            right = self.children[2].run(root)
            match self.children[1]:
                case '+':
                    return left + right
                case '-':
                    return left - right
                case '*':
                    return left * right
                case '/':
                    if math.isnan(left / right):
                        return left
                    return left / right
                case '>':
                    return 1 if left > right else -1
                case '<':
                    return 1 if left < right else -1
                case '==':
                    return 1 if left == right else -1
                case '!=':
                    return 1 if left != right else -1
                case '<=':
                    return 1 if left <= right else -1
                case '>=':
                    return 1 if left >= right else -1
                case 'and':
                    return 1 if left > 0 and right > 0 else -1
                case 'or':
                    return 1 if left > 0 or right > 0 else -1
                case _:
                    raise f'Error while evaluating the expression, this: {self.children[1]} should not be an operator'

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
        terminal_type = random.choice(['Number', 'Variable', 'Constant'])
        if terminal_type == 'Number':
            return cls(root, [random.choice(root.number_const_list)])
        if terminal_type == 'Variable':
            variable_index = random.randint(0, root.max_variables - 1)
            return cls(root, [f'x{variable_index}'])

        constant_index = random.randint(0, root.max_constants - 1)
        return cls(root, [f'X{constant_index}'])

    def mutate(self):
        mutation_type = random.choice(["replace_operator", "change_terminal", "rebuild_expression"])
        if mutation_type == "replace_operator":
            for i in range(len(self.children)):
                if self.children[i] in self.TERMINALS:
                    self.children[i] = random.choice(self.TERMINALS)
        elif mutation_type == "change_terminal":
            for i in range(len(self.children)):
                if isinstance(self.children[i], str) and self.children[i] not in self.TERMINALS:
                    if self.children[i][0] == 'x':
                        self.children[i] = f'x{random.randint(0, self.root.max_variables - 1)}'
                    elif self.children[i][0] == 'X':
                        self.children[i] = f'X{random.randint(0, self.root.max_constants - 1)}'
        elif mutation_type == "rebuild_expression":
            new_expression = self.generate_terminal_expression(self.root)
            self.children = new_expression.children