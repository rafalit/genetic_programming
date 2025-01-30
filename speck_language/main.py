from tasks.run_task import run_task

def fitness_function_task1(input, output, expected_output):
    if output == expected_output:
        return 0

    if len(output) == 0 or output[0] not in input:
        return -1000

    input_sorted = sorted(input)

    if output[0] == input_sorted[0]:
        return 0
    elif output[0] == input_sorted[1]:
        return -10
    elif output[0] == input_sorted[2]:
        return -25
    return -50

def fitness_function_task2(input, output, expected_output):
    if output == expected_output:
        return 0

    if len(output) == 0 or output[0] not in input:
        return -1000

    if output[0] in sorted(input, reverse=True)[:2]:
        return -50

    return 0

def fitness_function_task3(input, output, expected_output):
    if output == expected_output:
        return 0

    if len(output) == 0:
        return -1000

    if output[0] in input:
        return -10 * sorted(input).index(output[0])
    else:
        return -1000

def fitness_function_task2(input, output, expected_output):
    score = 0

    score += ((len(output) - len(expected_output)) ** 2) * -10

    for i, o, e in zip(input, output, expected_output):
        if o == e:
            continue
        if i > 0:
            if o != i:
                score -= 20
            else:
                score -= 40

    return score

def fitness_function_task1_1_e(input, output, expected_output):
    score = 0

    if len(output) == 0:
        return -1000
    score -= abs(output[0] - expected_output[0])**2

    return score


run_task(['task1.1.E'],
         **{ 'fitness_functions': [fitness_function_task1_1_e],
            'use_unused_branches_pruning': True})
