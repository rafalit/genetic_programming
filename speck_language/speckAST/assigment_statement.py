from .parse_tree_node import ParseTreeNode
from .expression import Expression
import random

class AssigmentStatement(ParseTreeNode):
    def __str__(self):
        return f'{str(self.children[0])} = {str(self.children[1])};'

    def run(self, root):
        index = int(self.children[0][1:])
        value = self.children[1].run(root)
        if self.children[0][0] == 'x':
            root.variables[index] = value
        root.constants[index] = value

    @classmethod
    def generate(cls, root, variable_to_be_included=None):
        expression = Expression.generate(root)
        if variable_to_be_included:
            return cls(root, [variable_to_be_included, expression])

        variable_index = random.randint(0, root.max_variables - 1)
        variable = f'x{variable_index}'

        return cls(root, [variable, expression])

    def mutate(self):
        if random.random() < 0.5:
            self.children[0] = f'x{random.randint(0, self.root.max_variables - 1)}'
        if random.random() < 0.5:
            self.children[1] = Expression.generate(self.root)