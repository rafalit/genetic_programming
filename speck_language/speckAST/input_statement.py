from .parse_tree_node import ParseTreeNode
import random


class InputStatement(ParseTreeNode):
    def __str__(self):
        return f'{" " * (self.depth * 4)}in({str(self.children[0])});'

    def run(self, root):
        if self.time_limit_exceeded():
            return
        self.num_of_executions += 1
        variable_name = self.children[0]
        variable_index = int(variable_name[1:])
        if variable_name[0] == 'x':
            root.variables[variable_index] = root.get_value_from_input()
        else:
            raise ValueError(f"Invalid variable name: {variable_name}")

    @classmethod
    def generate(cls, root, depth):
        variable_index = random.randint(0, root.max_variables - 1)
        variable_name = f'x{variable_index}'
        return cls(root, depth, [variable_name])