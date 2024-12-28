from .parse_tree_node import ParseTreeNode
from .expression import Expression
import random

class StatementWithBody(ParseTreeNode):
    min_depth = 2

    @classmethod
    def generate(cls, root, depth):
        condition = Expression.generate(root, depth + 1)
        body = [random.choice(cls.allowed_children_for_current_depth(root, depth)).generate(root, depth + 1)
                for _ in range(root.statement_with_body_initial_length)]
        return cls(root, depth, [condition, *body])

    @classmethod
    def allowed_children_for_current_depth(cls, root, depth):
        if root.max_depth - depth - 1 <= 1:
            return list(filter(lambda node_class: node_class.min_depth == 1, root.allowed_children))

        return root.allowed_children

    def mutate(self):
        if random.random() < 0.5:
            variable = random.choice(self.root.variables)
            self.children[0] = Expression.generate(self.root, variable)
        self.children[1].mutate_program()