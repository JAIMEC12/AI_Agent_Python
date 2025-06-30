import ast
import operator as op

# supported operators
operators = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg
}

def calculate(expression):
    try:
        return eval_ast(ast.parse(expression, mode='eval').body)
    except Exception as e:
        return f"Error: {e}"

def eval_ast(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](eval_ast(node.left), eval_ast(node.right))
    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](eval_ast(node.operand))
    else:
        raise TypeError(node)

# Example usage:
if __name__ == '__main__':
    print(calculate("3 + 7 * 2"))  # Should be 17
