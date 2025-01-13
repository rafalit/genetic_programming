import random
from .SpeckAST import SpeckAST
import os
import math


class GP:
    def __init__(self, population_size, max_program_size, initial_program_size, max_variables, max_depth,
                 tournament_size, crossover_rate, stagnation_crossover_rate, fitness_functions, stagnation_threshold,
                 survival_rate, use_unused_branches_pruning, number_const_min=0, number_const_max=10,
                 number_const_size=11, task_names=None, **kwargs):
        self.population_size = population_size
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_depth = max_depth
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.stagnation_crossover_rate = stagnation_crossover_rate
        self.fitness_functions = fitness_functions
        self.number_const_min = number_const_min
        self.number_const_max = number_const_max
        self.number_const_size = number_const_size
        self.task_names = task_names
        self.survival_rate = survival_rate
        self.use_unused_branches_pruning = use_unused_branches_pruning

        if not os.path.exists('result'):
            os.makedirs('result')

        self.result_file = f'result/{self.task_names[0]}.txt'

        self.population = [
            SpeckAST(
                max_program_size=max_program_size,
                initial_program_size=initial_program_size,
                max_variables=max_variables,
                max_depth=max_depth,
                number_const_min=number_const_min,
                number_const_max=number_const_max,
                number_const_size=number_const_size
            ) for _ in range(population_size)
        ]

        # For tracking stagnation
        self.stagnation_count = 0
        self.stagnation_threshold = stagnation_threshold
        self.original_crossover_rate = crossover_rate

    def evaluate_population(self, inputs, outputs, fitness_function_index, time_limit):

        for program in self.population:
            if program.fitness != float('-inf'):
                continue

            score = 0
            for input_list, expected_output in zip(inputs, outputs):
                output = program.run(input_list, len(expected_output), time_limit)
                score += self.fitness_functions[fitness_function_index](input_list, output, expected_output)
            program.fitness = score

    def tournament_selection(self):
        half_population = math.ceil(len(self.population) * self.survival_rate)
        self.population = self.population[:half_population]

    def prune_unused_branches(self):
        new_population = []
        for program in self.population:
            program.prune_unused_branches()

            if len(program.children) == 0:
                continue

            new_population.append(program)
            program.nullify_num_of_executions()
        self.population = new_population

    def evolve(self):
        self.tournament_selection()
        if self.use_unused_branches_pruning:
            self.prune_unused_branches()
        new_population = []

        while len(self.population) + len(new_population) < self.population_size:

            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)

            if random.random() < self.crossover_rate:
                child = SpeckAST.crossover(parent1, parent2)
            else:
                child = parent1.mutation()

            new_population.append(child)

        self.population.extend(new_population)

    def run(self, generations, test_cases, time_limit):

            overall_best_fitness = float('-inf')
            overall_best_program = None
            previous_task_name = None
            current_task_index = 0
            current_task_name = self.task_names[current_task_index]
            inputs = test_cases[current_task_name][0]
            outputs = test_cases[current_task_name][1]

            for generation in range(generations):

                if previous_task_name != current_task_name:
                    with open(self.result_file, 'w') as result_file:
                        result_file.write("Generation, Best Fitness, Average Fitness, Crossover Rate, Mutation Rate, Stagnation Count\n")
                    previous_task_name = current_task_name

                self.evaluate_population(inputs, outputs, current_task_index, time_limit)
                self.population.sort(key=lambda p: p.fitness, reverse=True)

                fitness_score_sum = 0
                for o in self.population:
                    fitness_score_sum += o.fitness

                avg_fitness = fitness_score_sum / len(self.population)
                best_individual = self.population[0]
                best_fitness = best_individual.fitness
                best_program = best_individual.get_program()

                if best_fitness > overall_best_fitness:
                    overall_best_fitness = best_fitness
                    overall_best_program = best_program
                    self.stagnation_count = 0
                else:
                    self.stagnation_count += 1


                if self.stagnation_count >= self.stagnation_threshold:
                    self.crossover_rate = self.stagnation_crossover_rate
                else:
                    if self.crossover_rate != self.original_crossover_rate:
                        self.crossover_rate = self.original_crossover_rate

                with open(self.result_file, 'a') as result_file:
                    result_file.write(f"{generation}, {overall_best_fitness:.2f}, {avg_fitness:.2f}, {self.crossover_rate:.2f}, {1 - self.crossover_rate:.2f}, {self.stagnation_count}\n")

                print(
                    f"Generation {generation + 1}: Best Fitness = {overall_best_fitness:.2f}, Average Fitness = {avg_fitness:.2f}, Crossover Rate = {self.crossover_rate:.2f}, Mutation Rate = {1 - self.crossover_rate:.2f}, Stagnation Count = {self.stagnation_count}")

                if overall_best_fitness == 0 or generation == generations - 1:
                    best_program_string = str(best_individual)
                    best_individual.prune_unused_branches()
                    best_program_pruned_string = str(best_individual)
                    with open(self.result_file, 'a') as result_file:
                        result_file.write("\n")
                        result_file.write(f"Final Best Program:\n {best_program_string}\n")
                        result_file.write(f"Final Best Program after pruning:\n {best_program_pruned_string}\n")

                    print(f"Best Fitness reached 0 at generation {generation + 1}.")
                    print(f'Best Program:\n {best_program_string}')
                    print(f'Best Program after pruning:\n {best_program_pruned_string}')
                    print('Best Programs outputs:')
                    for input, output in zip(inputs, outputs):
                        print(f'Input: {input}, output: {best_individual.run(input, len(output), time_limit)}')

                    if current_task_index == len(self.task_names) - 1:
                        break

                    current_task_index += 1
                    current_task_name = self.task_names[current_task_index]
                    inputs = test_cases[current_task_name][0]
                    outputs = test_cases[current_task_name][1]
                    self.result_file = f'result/{current_task_name}.txt'
                    overall_best_fitness = float('-inf')
                    overall_best_program = None
                    for p in self.population:
                        p.fitness = float('-inf')

                if generation != generations - 1:
                    self.evolve()


