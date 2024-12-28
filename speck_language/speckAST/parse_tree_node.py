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

    def __str__(self):
        return ''