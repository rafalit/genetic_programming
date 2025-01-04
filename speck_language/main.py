from tasks.run_task import run_task

def main(task_name):
    tasks = {
        "task_1_1_A": ([1, 2, 3, 4], [1, 2, 3, 4]),
        "task_1_1_B": ([1, 2, 3, 4], [789]),
        "task_1_1_C": ([1], [31415]),
        "task_1_1_D": ([1, 2, 3, 4], [1]),
        "task_1_1_E": ([1, 2, 3, 4], [789, 42, 56, 99]),
        "task_1_1_F": ([1], [1]),
        "task_1_2_A": ([3, 5], [8]),
        "task_1_2_B": ([-4, 6], [2]),
        "task_1_2_C": ([1234, -5678], [-4444]),
        "task_1_2_D": ([5678, 1234], [4444]),
        "task_1_2_E": ([12, -7], [-84]),
        "task_1_3_A": ([3, 9], [9]),
        "task_1_3_B": ([-1234, 5678], [5678]),
        "task_1_4_A": ([10, 20, -10, 30, -30, 40, -40, 50, -50, 60], [4]),
        "task_1_4_B": ([4, 10, 20, 30, 40], [25]),

        #Jeden wybrany problem z BenchmarkSuiteGECCO2015 z zakresu 1-5 (strona 9) - zadanie 1
        "task_number_io": (
            [5, 3.2, -2, 7.1, 100, -100.5],
            [x + y for x, y in [(5, 3.2), (-2, 7.1), (100, -100.5)]],
            {
                "population_size": 50,
                "max_variables": 2,
                "mutation_rate": 0.4,
                "crossover_rate": 0.8,
            },
        ),

    }

    if task_name not in tasks:
        print(f"Unknown task: {task_name}")
        return

    # Rozpakowanie wartości: input_list, expected_output, config
    input_list, expected_output, config = tasks[task_name]
    print(f"Running {task_name} with config {config}...")
    run_task(input_list, expected_output, **config)

if __name__ == "__main__":
    main("task_number_io")