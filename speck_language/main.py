from tasks.task_1_1_A import task_1_1_A
from tasks.task_1_1_B import task_1_1_B
from tasks.task_1_1_C import task_1_1_C
from tasks.task_1_1_D import task_1_1_D
from tasks.task_1_1_E import task_1_1_E
from tasks.task_1_1_F import task_1_1_F
from tasks.task_1_2_A import task_1_2_A
from tasks.task_1_2_B import task_1_2_B
from tasks.task_1_2_C import task_1_2_C
from tasks.task_1_2_D import task_1_2_D
from tasks.task_1_2_E import task_1_2_E
from tasks.task_1_3_A import task_1_3_A
from tasks.task_1_3_B import task_1_3_B
from tasks.task_1_4_A import task_1_4_A
from tasks.task_1_4_B import task_1_4_B

def run_single_task(task_name):
    print(f"Running {task_name}...")
    if task_name == "task_1_1_A":
        task_1_1_A()
    elif task_name == "task_1_1_B":
        task_1_1_B()
    elif task_name == "task_1_1_C":
        task_1_1_C()
    elif task_name == "task_1_1_D":
        task_1_1_D()
    elif task_name == "task_1_1_E":
        task_1_1_E()
    elif task_name == "task_1_1_F":
        task_1_1_F()
    elif task_name == "task_1_2_A":
        task_1_2_A()
    elif task_name == "task_1_2_B":
        task_1_2_B()
    elif task_name == "task_1_2_C":
        task_1_2_C()
    elif task_name == "task_1_2_D":
        task_1_2_D()
    elif task_name == "task_1_2_E":
        task_1_2_E()
    elif task_name == "task_1_3_A":
        task_1_3_A()
    elif task_name == "task_1_3_B":
        task_1_3_B()
    elif task_name == "task_1_4_A":
        task_1_4_A()
    else:
        task_1_4_B()


if __name__ == "__main__":
    run_single_task("task_1_1_E")
