from .statement_with_body import StatementWithBody
import random
from .expression import Expression
from .assigment_statement import AssigmentStatement


class LoopStatement(StatementWithBody):
    def __str__(self):
        body = '\n'.join([' ' * (self.indent + 4) + str(child) for child in self.children[1:]])
        return f'while({self.children[0]})' + '{\n' + body + '\n' + (' ' * self.indent) + '}'


    def run(self, root):
        condition = self.children[0].run(root)
        while condition > 0:
            self.children[1].run()
            self.children[2].run(root)

