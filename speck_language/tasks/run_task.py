from speckAST.GP import GP
from .fitness_functions import fitness_function
import json

def run_task(task_names, **config):
    default_config = {
        "population_size":2000,
        "max_program_size": 20,
        "initial_program_size": 10,
        "max_variables": 5,
        "max_depth": 20,
        "tournament_size": 4,
        "crossover_rate": 0.8,
        "stagnation_crossover_rate": 0.5,
        'stagnation_threshold': 10,
        "fitness_functions": [fitness_function],
        "number_const_min": 0,
        "number_const_max": 1000,
        "number_const_size": 1001,
        "task_names": task_names,
        "survival_rate": 0.3,
        "use_unused_branches_pruning": False
    }
    default_config.update(config)

    gp = GP(**default_config)
    test_cases = extract_inputs(task_names)

    gp.run(150, test_cases, time_limit=0.01)


def extract_inputs(task_names):
    result = {}

    for task_name in task_names:
        data = None
        with open(f'./dane/{task_name}.json') as f:
            data = json.load(f)

        inputs, outputs = [], []

        for d in data:
            inputs.append(d['input'])
            outputs.append(d['output'])

        result[task_name] = [inputs, outputs]

    return result
