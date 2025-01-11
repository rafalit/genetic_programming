from tasks.run_task import run_task


def fitness_function_task3(input, output, expected_output):
    score = 0
    if output == expected_output:
        return score

    if len(output) == 0:
        return -1000

    if output[0] in input:
        score -= 5 * sorted(input).index(output[0])
    else:
        score -= 100

    return score - abs(expected_output[0] - output[0])


run_task('task3', **{'fitness_function': fitness_function_task3})
