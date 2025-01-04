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
    }

    if task_name not in tasks:
        print(f"Unknown task: {task_name}")
        return

    input_list, expected_output = tasks[task_name]
    print(f"Running {task_name}...")
    run_task(input_list, expected_output)


if __name__ == "__main__":
    main("task_1_1_E")  # Zmień nazwę zadania, aby uruchomić inne
