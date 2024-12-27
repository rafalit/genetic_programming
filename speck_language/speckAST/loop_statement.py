from .statement_with_body import StatementWithBody
import random
from .expression import Expression
from .assigment_statement import AssigmentStatement


class LoopStatement(StatementWithBody):
    def __str__(self):
        return f'while({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * (self.indent + 4)) + \
            str(self.children[2]) + '\n' + (' ' * self.indent) + '}'

    def run(self, root):
        condition = self.children[0].run(root)
        while condition > 0:
            self.children[1].run()
            self.children[2].run(root)

    @classmethod
    def generate(cls, root):
        variable_to_be_included = f'x{random.randint(0, root.max_variables - 1)}'
        condition = Expression.generate(root, variable_to_be_included)
        body = root.__class__(max_program_size=root.max_program_size // 10,
                        initial_program_size=1,
                        max_variables=root.max_variables,
                        number_const_list=root.number_const_list,
                        variables=root.variables,
                        indent=root.indent + 4)
        assigment_to_be_included = AssigmentStatement.generate(root, variable_to_be_included)
        return cls(root, [condition, body, assigment_to_be_included], indent=root.indent)
