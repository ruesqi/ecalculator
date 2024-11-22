from flask import Flask, render_template, request, jsonify
import requests
from eternitycalculator import EternityCalculator

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

@app.route('/', methods=['GET', 'POST'])
def combined_calculator():
    error = None
    result = None
    if request.method == 'POST':
        input_expression = request.form.get('input_expression')

        try:
            # Send the request to the external server
            response = requests.post(
                'https://eternitycalculatorteamo.co/calculate',
                json={'expression': input_expression},
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer sk1_66727cad9e50a7c7a8d3db2ecc9c05de3cd87260c1cbf5d04c07d5e97829403d'  # Use Secret Key
                }
            )
            data = response.json()
            if response.status_code == 200:
                result = data.get('result', 'No result returned')
            else:
                error = data.get('error', 'An error occurred while calculating.')
        except ValueError as e:
            error = str(e)

    return render_template('combined_calculator_v3.html', result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
