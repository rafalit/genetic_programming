from .statement_with_body import StatementWithBody
from .expression import Expression
import random

class ConditionStatement(StatementWithBody):
    def __str__(self):
        body = '\n'.join([' ' * (self.indent + 4) + str(child) for child in self.children[1:]])
        return f'if({self.children[0]})' + '{\n' + body + '\n' + (' ' * self.indent) + '}'

    def run(self, root):
        condition = self.children[0].run(root)
        if condition > 0:
            self.children[1].run()
