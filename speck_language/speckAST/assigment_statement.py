from .parse_tree_node import ParseTreeNode
from .expression import Expression
import random


class AssigmentStatement(ParseTreeNode):
    def __str__(self):
        return f'{" " * (self.depth * 4)}{str(self.children[0])} = {str(self.children[1])};'

    def run(self, root):
        if self.time_limit_exceeded():
            return
        index = int(self.children[0][1:])
        value = self.children[1].run(root)
        if self.children[0][0] == 'x':
            root.variables[index] = value

    @classmethod
    def generate(cls, root, depth, variable_to_be_included=None):
        expression = Expression.generate(root, depth + 1)
        if variable_to_be_included:
            return cls(root, depth, [variable_to_be_included, expression])

        variable_index = random.randint(0, root.max_variables - 1)
        variable = f'x{variable_index}'

        return cls(root, depth, [variable, expression])