from speckAST.GP import GP
from .fitness_functions import fitness_function
import json

def run_task(task_name, **config):
    default_config = {
        "population_size": 1000,
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
        "task_name": task_name,
    }
    default_config.update(config)

    gp = GP(**default_config)
    inputs, outputs = extract_inputs(task_name)

    gp.run(100, inputs, outputs, time_limit=0.01)


def extract_inputs(task_name):
    data = None
    with open(f'./dane/{task_name}.json') as f:
        data = json.load(f)

    inputs, outputs = [], []

    for d in data:
        inputs.append(d['input'])
        outputs.append(d['output'])

    return inputs, outputs
