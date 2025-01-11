from speckAST.GP import GP
from .fitness_functions import fitness_function

def run_task(input_list, expected_output, **config):
    # Domyślne ustawienia
    default_config = {
        "population_size": 50,
        "max_program_size": 20,
        "initial_program_size": 2,
        "max_variables": 2,
        "max_depth": 6,
        "tournament_size": 4,
        "crossover_rate": 0.7,
        "mutation_rate": 0.3,
        "fitness_function": fitness_function,
        "number_const_min": 0,
        "number_const_max": 10,
        "number_const_size": 11,
        "task_name": "...",
    }
    # Nadpisz domyślne ustawienia
    default_config.update(config)

    # Tworzymy instancję GP z nową konfiguracją
    gp = GP(**default_config)

    # Uruchom algorytm genetyczny
    gp.run(50, input_list, expected_output, time_limit=0.1)
