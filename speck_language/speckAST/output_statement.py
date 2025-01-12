from .parse_tree_node import ParseTreeNode
from .expression import Expression


class OutputStatement(ParseTreeNode):
    def __str__(self):
        return f'{" " * (self.depth * 4)}out({str(self.children[0])});'

    def run(self, root):
        if self.time_limit_exceeded():
            return

        self.num_of_executions += 1
        value = self.children[0].run(root)
        root.save_value_to_output(value)

    @classmethod
    def generate(cls, root, depth):
        return cls(root, depth, [Expression.generate(root, depth + 1)])