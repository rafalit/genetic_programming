from .GP import GP
from .SpeckAST import SpeckAST


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


if __name__ == "__main__":
    gp = GP(
        population_size=20,
        max_program_size=20,
        initial_program_size=4,
        max_variables=5,
        max_depth=6,
        tournament_size=7,
        crossover_rate=0.8,
        mutation_rate=0.4,
        fitness_function=fitness_function
    )

    input_list = [1, 2, 3, 4]
    expected_output = [10, 20, 30, 40]
    time_limit = 1.0

    gp.run(10, input_list, expected_output, time_limit)
