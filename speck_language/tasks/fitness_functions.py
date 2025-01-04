def fitness_function(output, expected_output):
    if len(output) != len(expected_output):
        return -float('inf')

    fitness = -sum((o - e) ** 2 for o, e in zip(output, expected_output))

    normalized_fitness = fitness / len(output)

    scale_factor = 0.1
    normalized_fitness *= scale_factor

    penalty_threshold = 50
    for o, e in zip(output, expected_output):
        if abs(o - e) > penalty_threshold:
            normalized_fitness -= 0.1

    print(f"Normalized Fitness: {normalized_fitness:.1f}")
    return normalized_fitness
