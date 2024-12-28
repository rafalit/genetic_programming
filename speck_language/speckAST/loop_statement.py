from .statement_with_body import StatementWithBody


class LoopStatement(StatementWithBody):
    def __str__(self):
        return super().__str__('while')

    def run(self, root):
        condition = self.children[0].run(root)
        while condition > 0:
            self.children[1].run()
            self.children[2].run(root)
