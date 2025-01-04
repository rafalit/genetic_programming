from speckAST.GP import GP
from .fitness_functions import fitness_function

def run_task(input_list, expected_output, **config):
    # Ustawienia domyślne
    default_config = {
        "population_size": 20,
        "max_program_size": 20,
        "initial_program_size": 4,
        "max_variables": 5,
        "max_depth": 6,
        "tournament_size": 7,
        "crossover_rate": 0.8,
        "mutation_rate": 0.4,
        "fitness_function": fitness_function,
    }
    # Nadpisujemy ustawienia domyślne
    default_config.update(config)

    # Tworzymy instancję GP z nową konfiguracją
    gp = GP(**default_config)

    gp.run(10, input_list, expected_output, time_limit=1.0)