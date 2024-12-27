from .statement_with_body import StatementWithBody
from .expression import Expression


class ConditionStatement(StatementWithBody):
    def __str__(self):
        return f'if({self.children[0]})' + '{\n' + str(self.children[1]) + (' ' * self.indent) + '}'

    def run(self, root):
        condition = self.children[0].run(root)
        if condition > 0:
            self.children[1].run()

    @classmethod
    def generate(cls, root):
        condition = Expression.generate(root)
        body = root.__class__(max_program_size=root.max_program_size // 10,
                        initial_program_size=1,
                        max_variables=root.max_variables,
                        max_constants=root.max_constants,
                        number_const_list=root.number_const_list,
                        variables=root.variables,
                        constants=root.constants,
                        indent=root.indent + 4)
        return cls(root, [condition, body], indent=root.indent)
