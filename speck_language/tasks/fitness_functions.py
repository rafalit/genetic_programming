def fitness_function(input, output, expected_output):
    if len(output) != len(expected_output):
        return -1000

    fitness = -sum((o - e) ** 2 for o, e in zip(output, expected_output))

    if len(output) > 0:
        normalized_fitness = fitness / len(output)
    else:
        normalized_fitness = fitness

    scale_factor = 0.1
    normalized_fitness *= scale_factor

    penalty_threshold = 0.1 * (max(expected_output) - min(expected_output))

    for o, e in zip(output, expected_output):
        if abs(o - e) > penalty_threshold:
            normalized_fitness -= 0.5

    return normalized_fitness