from sympy import sympify
import os


equations_folder = '../output_with_sin_cos/expressions'
simplified_equations_folder = '../output_with_sin_cos/simplified_expressions'

if not os.path.exists(simplified_equations_folder):
    os.makedirs(simplified_equations_folder)

directory = os.fsencode(equations_folder)

for equation_file in os.listdir(directory):
    filename = os.fsdecode(equation_file)
    path = os.path.join(equations_folder, filename)

    expression = ''

    with open(path, 'r') as file:
      expression = file.read()

    expression = expression.replace('SIN', 'sin')
    expression = expression.replace('COS', 'cos')
    try:
        expression_simplified = str(sympify(expression))
    except:
        print(f'Could not simplify the expression: {equation_file}')
        continue


    simplified_equation_path = os.path.join(simplified_equations_folder, f'simplified_{filename}')

    with open(simplified_equation_path, 'w') as file:
      file.write(expression_simplified)
