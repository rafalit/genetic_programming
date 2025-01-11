import random
from .SpeckAST import SpeckAST
import os
import math


class GP:
    def __init__(self, population_size, max_program_size, initial_program_size, max_variables, max_depth,
                 tournament_size, crossover_rate, stagnation_crossover_rate, fitness_function, stagnation_threshold,
                 survival_rate, number_const_min=0, number_const_max=10, number_const_size=11, task_name=None, **kwargs):
        self.population_size = population_size
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_depth = max_depth
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.stagnation_crossover_rate = stagnation_crossover_rate
        self.fitness_function = fitness_function
        self.number_const_min = number_const_min
        self.number_const_max = number_const_max
        self.number_const_size = number_const_size
        self.task_name = task_name
        self.survival_rate = survival_rate

        if not os.path.exists('result'):
            os.makedirs('result')

        self.result_file = f'result/{self.task_name}.txt'

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

    def evaluate_population(self, inputs, outputs, time_limit):

        for program in self.population:
            if program.fitness != float('-inf'):
                continue

            score = 0
            for input_list, expected_output in zip(inputs, outputs):
                output = program.run(input_list, len(expected_output), time_limit)
                score += self.fitness_function(input_list, output, expected_output)
            program.fitness = score

    def tournament_selection(self):
        self.population.sort(key=lambda p: p.fitness, reverse=True)
        half_population = math.ceil(len(self.population) * self.survival_rate)
        self.population = self.population[:half_population]

    def evolve(self):
        self.tournament_selection()
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

    def run(self, generations, inputs, outputs, time_limit):
        with open(self.result_file, 'w') as result_file:
            result_file.write("Generation, Best Fitness, Average Fitness\n")

            overall_best_fitness = float('-inf')
            overall_best_program = None

            for generation in range(generations):
                self.evaluate_population(inputs, outputs, time_limit)
                if generation == 0:
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

                result_file.write(f"{generation}, {overall_best_fitness:.2f}, {avg_fitness:.2f}\n")

                print(
                    f"Generation {generation + 1}: Best Fitness = {overall_best_fitness:.2f}, Average Fitness = {avg_fitness:.2f}")

                if overall_best_fitness == 0:
                    print(f"Best Fitness reached 0 at generation {generation + 1}. Stopping the program.")
                    break

                if self.stagnation_count >= self.stagnation_threshold:
                    self.crossover_rate = self.stagnation_crossover_rate
                else:
                    if self.crossover_rate != self.original_crossover_rate:
                        self.crossover_rate = self.original_crossover_rate

                if generation != generations - 1:
                    self.evolve()

            result_file.write("\n")
            result_file.write(f"Final Best Program:\n {overall_best_program}\n")
