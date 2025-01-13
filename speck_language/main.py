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


run_task(['task1'],
         **{
            'use_unused_branches_pruning': True})
