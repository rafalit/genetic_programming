from .parse_tree_node import ParseTreeNode
from .expression import Expression


class OutputStatement(ParseTreeNode):
    def __str__(self):
        return f'out({str(self.children[0])});'

    def run(self, root):
        value = self.children[0].run(root)
        print(f"Output: {value}")

    @classmethod
    def generate(cls, root):
        return cls(root, [Expression.generate(root)])