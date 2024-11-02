import numpy as np
import math

def generate_data_file_for_function_and_domain(function,
                                               number_of_variables,
                                               domain,
                                               number_of_examples,
                                               filename,
                                               number_of_random_constants,
                                               random_constant_lower_bound,
                                               random_constant_upper_bound):
  values = [
        np.linspace(domain[0], domain[1], number_of_examples)
         for _ in range(number_of_variables)
      ]
  for v in values:
    np.random.shuffle(v)

  with open(f'../data/data_variables_shuffled/{filename}', 'w') as file:
    first_line = f'{number_of_variables}\t{number_of_random_constants}\t{float(random_constant_lower_bound)}\t{float(random_constant_upper_bound)}\t{number_of_examples}\n'
    file.write(first_line)
    for i in range(number_of_examples):
      arguments = []
      string = ''
      for j in range(number_of_variables):
        value = round(values[j][i], 2)
        arguments.append(value)
        string += f'{value}\t'

      file.write(string + str(function(*arguments)) + '\n')


# f(x) = 5*x^3 - 2x^2 + 3x - 17 dziedzina: [-10, 10], [0,100], [-1, 1], [-1000, 1000]
# f(x) = sin(x) + cos(x) dziedzina: [-3.14, 3.14], [0,7], [0, 100], [-100, 100]
# f(x) = 2* ln(x+1) dziedzina: [0,4], [0, 9], [0,99], [0,999]
# f(x,y) = x + 2*y dziedzina: x i y [0, 1], [-10, 10], [0, 100], [-1000, 1000]
# f(x, y) = sin(x/2) + 2* cos(x) dziedzina x, y: [-3.14, 3.14], [0,7], [0, 100], [-100, 100]
# f(x,y) = x^2 + 3x*y - 7y + 1 dziedzina x,y: [-10, 10], [0,100], [-1, 1], [-1000, 1000]

def f1(x):
  return 5*x**3 - 2*x**2 + 3*x -17

generate_data_file_for_function_and_domain(f1, 1, [-10, 10], 100, 'problem1a.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f1, 1, [0,100], 100, 'problem1b.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f1, 1, [-1, 1], 100, 'problem1c.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f1, 1, [-1000, 1000], 200, 'problem1d.dat', 100, -10, 10)

def f2(x):
  return math.sin(x) + math.cos(x)

generate_data_file_for_function_and_domain(f2, 1, [-3.14, 3.14], 100, 'problem2a.dat', 50, -5, 5)
generate_data_file_for_function_and_domain(f2, 1, [0,7], 100, 'problem2b.dat', 50, -5, 5)
generate_data_file_for_function_and_domain(f2, 1, [0, 100], 100, 'problem2c.dat', 100, -5, 5)
generate_data_file_for_function_and_domain(f2, 1, [-100, 100], 100, 'problem2d.dat', 100, -5, 5)

def f3(x):
  return 2 * math.log(x+1)

generate_data_file_for_function_and_domain(f3, 1, [0,4], 100, 'problem3a.dat', 50, -5, 5)
generate_data_file_for_function_and_domain(f3, 1, [0, 9], 100, 'problem3b.dat', 50, -5, 5)
generate_data_file_for_function_and_domain(f3, 1, [0, 99], 100, 'problem3c.dat', 50, -5, 5)
generate_data_file_for_function_and_domain(f3, 1, [0, 999], 300, 'problem3d.dat', 50, -5, 5)

def f4(x,y):
  return x + 2*y

generate_data_file_for_function_and_domain(f4, 2, [0,1], 100, 'problem4a.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f4, 2, [-10, 10], 100, 'problem4b.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f4, 2, [0, 100], 100, 'problem4c.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f4, 2, [-1000, 1000], 300, 'problem4d.dat', 50, -3, 3)

def f5(x,y):
  return math.sin(x/2) + 2* math.cos(x)

generate_data_file_for_function_and_domain(f5, 2, [-3.14, 3.14], 100, 'problem5a.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f5, 2, [0,7], 100, 'problem5b.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f5, 2, [0, 100], 100, 'problem5c.dat', 50, -3, 3)
generate_data_file_for_function_and_domain(f5, 2, [-100, 100], 300, 'problem5d.dat', 50, -3, 3)

def f6(x,y):
  return x**2 + 3*x*y - 7*y + 1

generate_data_file_for_function_and_domain(f6, 2, [-10, 10], 100, 'problem6a.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f6, 2, [0,100], 100, 'problem6b.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f6, 2, [-1, 1], 100, 'problem6c.dat', 100, -10, 10)
generate_data_file_for_function_and_domain(f6, 2, [-1000, 1000], 200, 'problem6d.dat', 100, -10, 10)