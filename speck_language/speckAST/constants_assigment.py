from .parse_tree_node import ParseTreeNode
from .assigment_statement import AssigmentStatement


class ConstantsAssigment(ParseTreeNode):
    def __str__(self):
        return '\n'.join([str(child) for child in self.children])

    def run(self, root):
        for child in self.children:
            child.run(root)

    @classmethod
    def generate(cls, root):
        children = [AssigmentStatement.generate(root, f'X{i}') for i in range(root.max_constants)]
        return cls(root, children)