import re
import operator

# Define operator precedence and functions
ops = {
    '+': (1, operator.add),
    '-': (1, operator.sub),
    '*': (2, operator.mul),
    '/': (2, operator.truediv)
}

# Tokenize the input expression
def tokenize(expression):
    tokens = re.findall(r'\d+\.?\d*|[()+*/-]', expression)
    return tokens

# Parse tokens into an AST
def parse(tokens):
    def parse_expression(index=0, precedence=0):
        token = tokens[index]
        if token == '(':
            index, node = parse_expression(index + 1)
            assert tokens[index] == ')'
            return index + 1, node
        else:
            node = float(token) if token.isdigit() or '.' in token else token
            index += 1

        while index < len(tokens):
            token = tokens[index]
            if token == ')':
                break
            op_precedence, op_func = ops.get(token, (0, None))
            if op_precedence < precedence:
                break

            index, right = parse_expression(index + 1, op_precedence + 1)
            node = (op_func, node, right)

        return index, node

    _, ast = parse_expression()
    return ast

# Evaluate the AST
def evaluate(ast):
    if isinstance(ast, tuple):
        op_func, left, right = ast
        return op_func(evaluate(left), evaluate(right))
    else:
        return ast

# Main function to process expressions
def evaluate_expression(expression):
    tokens = tokenize(expression)
    ast = parse(tokens)
    return evaluate(ast)

# Example usage
expression = "3 + 5 * (2 - 8)"
result = evaluate_expression(expression)
print(f"Result: {result}")
