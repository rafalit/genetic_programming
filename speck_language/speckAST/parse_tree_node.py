class ParseTreeNode:
    def __init__(self, root, children=None):
        self.root = root
        self.children = children if children else []

    def mutate(self):
        pass

    def run(self, root):
        pass

    def __str__(self):
        return ''