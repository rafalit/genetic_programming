from .parse_tree_node import ParseTreeNode
from .expression import Expression
import random

class StatementWithBody(ParseTreeNode):
    def __init__(self, root, children=None, indent=0):
        super().__init__(root, children)
        self.indent = indent

    @classmethod
    def generate(cls, root):
        condition = Expression.generate(root)
        body = [random.choice(root.allowed_children).generate(root) for _ in range(root.statement_with_body_initial_length)]
        return cls(root, [condition, *body], indent=root.indent + 4)

    def mutate(self):
        if random.random() < 0.5:
            variable = random.choice(self.root.variables)
            self.children[0] = Expression.generate(self.root, variable)
        self.children[1].mutate_program()