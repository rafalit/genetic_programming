from speckAST.GP import GP
from .fitness_functions import fitness_function
import json

def run_task(task_name, **config):
    default_config = {
        "population_size": 1000,
        "max_program_size": 20,
        "initial_program_size": 10,
        "max_variables": 5,
        "max_depth": 20,
        "tournament_size": 4,
        "crossover_rate": 0.7,
        "stagnation_crossover_rate": 0.3,
        'stagnation_threshold': 10,
        "fitness_function": fitness_function,
        "number_const_min": 0,
        "number_const_max": 10,
        "number_const_size": 11,
        "task_name": task_name,
        "survival_rate": 0.3,
        "use_unused_branches_pruning": False
    }
    default_config.update(config)

    gp = GP(**default_config)
    inputs, outputs = extract_inputs(task_name)

    gp.run(50, inputs, outputs, time_limit=0.01)


def extract_inputs(task_name):
    data = None
    with open(f'./dane/{task_name}.json') as f:
        data = json.load(f)

    inputs, outputs = [], []

    for d in data:
        inputs.append(d['input'])
        outputs.append(d['output'])

    return inputs, outputs
