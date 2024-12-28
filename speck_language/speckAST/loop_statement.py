from .statement_with_body import StatementWithBody


class LoopStatement(StatementWithBody):
    def __str__(self):
        return super().__str__('while')

    def run(self, root):
        if self.time_limit_exceeded():
            return
        condition = self.children[0].run(root)
        while condition > 0 and not self.time_limit_exceeded():
            for child in self.children[1:]:
                child.run(root)
