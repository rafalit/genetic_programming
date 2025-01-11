
from .parse_tree_node import ParseTreeNode
import random
import math


class Expression(ParseTreeNode):
    TERMINALS = ['+', '-', '/', '*', '>', '<', '==', '!=', '<=', '>=', 'and', 'or']

    def __str__(self):
        result = ''
        for child in self.children:
            result += str(child) + ' '

        result = result.strip()

        if len(self.children) == 3:
            return f'({result})'

        return result

    def run(self, root):
        if len(self.children) == 1:
            if isinstance(self.children[0], str):
                index = int(self.children[0][1:])
                return root.variables[index]

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
                    if right == 0:
                        return float('inf')
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
    def generate(cls, root, depth):
        expression_type = random.randint(0, 2)
        if expression_type == 0:
            return cls.generate_terminal_expression(root, depth)
        elif expression_type == 1:
            return cls(root, depth, [
                cls.generate_terminal_expression(root, depth + 1),
                random.choice(cls.TERMINALS),
                cls.generate_terminal_expression(root, depth + 1)
            ])
        elif expression_type == 2:
            return cls(root, depth, [
                '!',
                cls.generate_terminal_expression(root, depth + 1)
            ])

    @classmethod
    def generate_terminal_expression(cls, root, depth):
        terminal_type = random.choice(['Number', 'Variable'])
        if terminal_type == 'Number':
            return cls(root, depth, [random.choice(root.number_const_list)])
        if terminal_type == 'Variable':
            variable_index = random.randint(0, root.max_variables - 1)
            return cls(root, depth, [f'x{variable_index}'])
