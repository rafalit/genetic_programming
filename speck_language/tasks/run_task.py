from speckAST.GP import GP
from .fitness_functions import fitness_function

def run_task(input_list, expected_output):
    # Logika zadania
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

    # Uruchomienie GP z danymi wejściowymi i wyjściowymi
    gp.run(10, input_list, expected_output, time_limit=1.0)
