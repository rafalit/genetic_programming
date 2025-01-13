from .parse_tree_node import ParseTreeNode
from .expression import Expression
import random


class StatementWithBody(ParseTreeNode):
    min_depth = 2

    def __str__(self, statement_keyword):
        body = '\n'.join([str(child) for child in self.children[1:]])
        return f'{" " * (self.depth * 4)}{statement_keyword}({self.children[0]})' + '{\n' + body + '\n' + (
                    " " * (self.depth * 4)) + '}'

    def prune_unused_branches(self):
        new_children = [self.children[0]]

        for child in self.children[1:]:
            if not isinstance(child, ParseTreeNode):
                continue

            if child.num_of_executions > 0:
                if isinstance(child, StatementWithBody):
                    child.prune_unused_branches()
                new_children.append(child)

        self.children = new_children

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