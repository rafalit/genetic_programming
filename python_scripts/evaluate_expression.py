import ast
import math

def safe_div(numerator, denominator):
    return numerator if abs(denominator) <= 0.001 else numerator / denominator

class SafeDivTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Div):
            return ast.Call(
                func=ast.Name(id="safe_div", ctx=ast.Load()),
                args=[node.left, node.right],
                keywords=[]
            )
        return node

def evaluate_expression(expr, x1, x2):
    tree = ast.parse(expr, mode='eval')
    transformer = SafeDivTransformer()
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)
    compiled = compile(tree, filename="<ast>", mode="eval")
    return eval(compiled, {"safe_div": safe_div, 'X1': x1, 'X2': x2, 'SIN': math.sin, 'COS': math.cos})