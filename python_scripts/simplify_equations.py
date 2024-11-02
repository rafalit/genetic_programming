from sympy import sympify
import os


equations_folder = 'equations'
simplified_equations_folder = 'simplified_equations'

if not os.path.exists(simplified_equations_folder):
    os.makedirs(simplified_equations_folder)

directory = os.fsencode(equations_folder)

for equation_file in os.listdir(directory):
    if not os.path.isfile(equation_file):
      continue
    filename = os.fsdecode(equation_file)
    path = os.path.join(equations_folder, filename)

    expression = ''

    with open(path, 'r') as file:
      expression = file.read()

    expression = expression.replace('SIN', 'sin')
    expression = expression.replace('COS', 'cos')
    print(expression)
    expression_simplified = str(sympify(expression))

    simplified_equation_path = os.path.join(simplified_equations_folder, f'simplified_{filename}')

    with open(simplified_equation_path, 'w') as file:
      file.write(expression_simplified)
