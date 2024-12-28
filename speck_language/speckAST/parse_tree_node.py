import time


class ParseTreeNode:
    min_depth = 1

    def __init__(self, root, depth, children=None):
        self.root = root
        self.depth = depth
        self.children = children if children else []

    def mutate(self):
        pass

    def run(self, root):
        pass

    def time_limit_exceeded(self):
        if time.time() - self.root.program_start > self.root.time_limit:
            return True
        return False

    def __str__(self):
        return ''

    def node_list(self):
        result = [(self,)]
        for i, child in enumerate(self.children):
            if isinstance(child, ParseTreeNode):
                result.extend([(i, *statement) for statement in child.node_list()])
        return result
