from .parse_tree_node import ParseTreeNode
import random


class InputStatement(ParseTreeNode):
    def __str__(self):
        return f'in({str(self.children[0])});'

    def run(self, root):
        variable_name = self.children[0]
        variable_index = int(variable_name[1:])
        if variable_name[0] == 'x':  # Zmienna
            value = float(input(f"Enter value for variable {variable_name}: "))
            root.variables[variable_index] = value
        else:
            raise ValueError(f"Invalid variable name: {variable_name}")

    @classmethod
    def generate(cls, root):
        variable_index = random.randint(0, root.max_variables - 1)
        variable_name = f'x{variable_index}'
        return cls(root, [variable_name])