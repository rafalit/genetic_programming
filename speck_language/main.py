from tasks.run_task import run_task

def main(task_name):
    tasks = {
        "task_1_1_A": ([1, 2, 3, 4], [1, 2, 3, 4]),
        "task_1_1_B": ([1, 2, 3, 4], [789], {"number_const_min": 0,"number_const_max": 800, "number_const_size": 801,}),
        "task_1_1_C": ([1], [31415], {"number_const_max": 31415, "number_const_size": 31416,}),
        "task_1_1_D": ([1, 2, 3, 4], [1]),
        "task_1_1_E": ([1, 2, 3, 4], [789, 42, 56, 99], {"number_const_max": 800, "number_const_size": 801,}),
        "task_1_1_F": ([1], [1]),
        "task_1_2_A": ([3, 5], [8], {"number_const_max": 9, "number_const_size": 10,}),
        "task_1_2_B": ([-4, 6], [2], {"number_const_min": -9, "number_const_max": 9, "number_const_size": 19,}),
        "task_1_2_C": ([-1234, 5678], [4444],
                       {
                           "population_size": 50,
                           "max_program_size": 40,
                           "initial_program_size": 10,
                           "max_depth": 8,
                           "max_variables": 5,
                           "tournament_size": 10,
                           "crossover_rate": 0.7,
                           "mutation_rate": 0.3,
                           "number_const_min": -9999,
                           "number_const_max": 9999,
                           "number_const_size": 19999,
                       }
                       ),
        "task_1_2_D": ([5678, 1234], [4444], {"number_const_max": 9999, "number_const_size": 10000,},),
        "task_1_2_E": ([12, -7], [-84], {"number_const_max": 9999, "number_const_size": 10000,}),
        "task_1_3_A": ([3, 9], [9], {"number_const_max": 9, "number_const_size": 10,}),
        "task_1_3_B": ([-1234, 5678], [5678], {"number_const_min": -9999, "number_const_max": 9999, "number_const_size": 19999,}),
        "task_1_4_A": ([10, 20, -10, 30, -30, 40, -40, 50, -50, 60], [4], {"number_const_min": -99, "number_const_max": 99, "number_const_size": 199,}),
        "task_1_4_B": ([4, 10, 20, 30, 40], [25], {"number_const_min": -99, "number_const_max": 99, "number_const_size": 199}),

        "task_number_io_1": (
            [0.2, -0.95, 0.3, 0.5, -0.75, 0.6],
            [x + y for x, y in [(0.2, -0.95), (0.3, 0.5), (-0.75, 0.6)]],
            {
                "population_size": 150,
                "max_variables": 2,
                "mutation_rate": 0.6,
                "crossover_rate": 0.9,
                "max_depth": 7,
                "initial_program_size": 4,
                "max_program_size": 25,
                "number_const_min": -1,
                "number_const_max": 1,
                "number_const_size": 21,
            },
        ),

        "task_number_io_10": (
            [2, -1.5, 3, 5, -7.5, 6],
            [x + y for x, y in [(2, -1.5), (3, 5), (-7.5, 6)]],
            {
                "population_size": 200,
                "max_variables": 2,
                "mutation_rate": 0.8,
                "crossover_rate": 0.8,
                "max_depth": 8,
                "initial_program_size": 5,
                "max_program_size": 10,
                "number_const_min": -10,
                "number_const_max": 10,
                "number_const_size": 21,
            },
        ),

        "task_number_io_100": (
            [20, -15, 30, 50, -75, 60],
            [x + y for x, y in [(20, -15), (30, 50), (-75, 60)]],
            {
                "population_size": 150,
                "max_variables": 2,
                "mutation_rate": 0.7,
                "crossover_rate": 0.7,
                "max_depth": 6,
                "initial_program_size": 6,
                "max_program_size": 15,
                "number_const_min": -100,
                "number_const_max": 100,
                "number_const_size": 51,
            },
        ),
    }

    if task_name not in tasks:
        print(f"Unknown task: {task_name}")
        return

    # Rozpakowanie wartości: input_list, expected_output, config
    task = tasks[task_name]
    input_list, expected_output = task[:2]
    config = task[2] if len(task) > 2 else {}

    config["task_name"] = task_name

    print(f"Running {task_name} with config {config}...")

    run_task(input_list, expected_output, **config)

if __name__ == "__main__":
    main("task_1_1_A")