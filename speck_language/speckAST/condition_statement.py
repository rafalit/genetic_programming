from .statement_with_body import StatementWithBody


class ConditionStatement(StatementWithBody):
    def __str__(self):
        return super().__str__('if')

    def run(self, root):
        if self.time_limit_exceeded():
            return
        condition = self.children[0].run(root)
        if condition > 0:
            for child in self.children[1:]:
                child.run(root)