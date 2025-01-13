from tasks.run_task import run_task


def fitness_function_task3(input, output, expected_output):
    if output == expected_output:
        return 0

    if len(output) == 0:
        return -1000

    if output[0] in input:
        return -10 * sorted(input).index(output[0])
    else:
        return -1000


run_task(['task3a', 'task3b', 'task3'],
         **{'fitness_functions': [fitness_function_task3, fitness_function_task3, fitness_function_task3],
            'use_unused_branches_pruning': True})
