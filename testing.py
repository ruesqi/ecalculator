from flask import Flask, render_template, request
from calculator import EternityCalculator
import ast

app = Flask(__name__)


# Mapping user-friendly function names to calculator methods
function_mapping = {
    'log_b': lambda calc, base, value: calc.calculate_logarithm(value, base),
    'arccos': lambda calc, x: calc.calculate_arccos(x),
    'exp': lambda calc, a, b, x: calc.calculate_exponential(a, b, x),
    'gamma': lambda calc, x: calc.calculate_gamma(x),
    'mad': lambda calc, *arr: calc.calculate_mad(*arr),
    'standard_deviation': lambda calc, *arr: calc.calculate_standard_deviation(*arr),
    'sinh': lambda calc, x: calc.calculate_hyperbolic_sine(x),
    'power': lambda calc, base, exponent: calc.PowerOf(base, exponent),
}


def safe_eval(expression, calculator):
    """
    Safely evaluates a user-provided mathematical expression.
    Supports functions defined in function_mapping.
    """
    # Parse the user input as an AST (Abstract Syntax Tree)
    node = ast.parse(expression, mode='eval')

    def eval_node(node):
        try:
            if isinstance(node, ast.BinOp):  # For binary operators like +, -, *, /
                left = eval_node(node.left)
                right = eval_node(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    return left / right
                else:
                    raise ValueError("Unsupported operator")
            elif isinstance(node, ast.UnaryOp):  # For unary operations like negation (-x)
                if isinstance(node.op, ast.USub):  # Handle negation
                    return -eval_node(node.operand)
                else:
                    raise ValueError("Unsupported unary operation")
            elif isinstance(node, ast.Call):  # For function calls
                func_name = node.func.id
                if func_name in function_mapping:
                    args = [eval_node(arg) for arg in node.args]
                    return function_mapping[func_name](calculator, *args)
                else:
                    raise ValueError(f"Unsupported function: {func_name}")
            elif isinstance(node, ast.Num):  # For numbers
                return node.n
            else:
                raise ValueError("Unsupported expression")
        except TypeError as e:
            raise ValueError(f"TypeError: {str(e)}. Check your function arguments.")

    return eval_node(node.body)



@app.route('/', methods=['GET', 'POST'])
def combined_calculator():
    error = None
    result = None
    if request.method == 'POST':
        input_expression = request.form.get('input_expression')

        try:
            calculator = EternityCalculator()
            result = safe_eval(input_expression, calculator)
        except ValueError as e:
            error = str(e)

    return render_template('combined_calculator_v3.html', result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
