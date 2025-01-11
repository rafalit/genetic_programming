import random
from .SpeckAST import SpeckAST
import os


class GP:
    def __init__(self, population_size, max_program_size, initial_program_size, max_variables, max_depth,
                 tournament_size, crossover_rate, mutation_rate, fitness_function,
                 number_const_min=0, number_const_max=10, number_const_size=11, task_name=None, **kwargs):
        self.population_size = population_size
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_depth = max_depth
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function
        self.number_const_min = number_const_min
        self.number_const_max = number_const_max
        self.number_const_size = number_const_size
        self.task_name = task_name

        # Create 'result' folder if it doesn't exist
        if not os.path.exists('result'):
            os.makedirs('result')

        # Set result file name based on task_name
        self.result_file = f'result/{self.task_name}.txt'

        # Initialize population
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

    def evaluate_population(self, input_list, expected_output, time_limit):
        self.fitness_scores = [
            self.fitness_function(individual.run(input_list, len(expected_output), time_limit), expected_output)
            for individual in self.population
        ]

    def tournament_selection(self):
        selected = []
        for _ in range(self.tournament_size):
            competitors = random.sample(list(enumerate(self.fitness_scores)), self.tournament_size)
            winner = max(competitors, key=lambda x: x[1])  # Select the individual with the best fitness
            selected.append(self.population[winner[0]])
        return selected

    def evolve(self, input_list, expected_output, time_limit, generation):
        self.evaluate_population(input_list, expected_output, time_limit)

        selected_population = self.tournament_selection()

        new_population = selected_population[:]
        while len(new_population) < self.population_size:
            if random.random() < self.crossover_rate:
                parent1, parent2 = random.sample(selected_population, 2)
                child = SpeckAST.crossover(parent1, parent2)
            elif random.random() < self.mutation_rate:
                parent = random.choice(selected_population)
                child = parent.mutation()
            else:
                child = random.choice(selected_population)

            while child.depth > self.max_depth:
                if random.random() < self.crossover_rate:
                    parent1, parent2 = random.sample(selected_population, 2)
                    child = SpeckAST.crossover(parent1, parent2)
                else:
                    parent = random.choice(selected_population)
                    child = parent.mutation()

            new_population.append(child)

        self.population = new_population

    def run(self, generations, input_list, expected_output, time_limit):
        with open(self.result_file, 'w') as result_file:
            # Write header
            result_file.write("Generation, Best Fitness, Average Fitness\n")

            # Initialize a variable to track the overall best program
            overall_best_fitness = float('-inf')
            overall_best_program = None

            for generation in range(generations):
                self.evolve(input_list, expected_output, time_limit, generation)

                # Filter out -inf fitness values before calculating the average fitness
                valid_fitness_scores = [score for score in self.fitness_scores if score != float('-inf')]

                # If there are no valid fitness scores, set avg_fitness to 0
                if valid_fitness_scores:
                    avg_fitness = sum(valid_fitness_scores) / len(valid_fitness_scores)
                else:
                    avg_fitness = 0  # Or some other value to indicate no valid scores

                # Get best fitness (still considering -inf)
                best_fitness = max(self.fitness_scores)

                # Get the best individual and their program for this generation
                best_individual = self.population[self.fitness_scores.index(best_fitness)]
                best_program = best_individual.get_program()

                # Update overall best program if needed
                if best_fitness > overall_best_fitness:
                    overall_best_fitness = best_fitness
                    overall_best_program = best_program

                # Write to file the generation results
                result_file.write(f"{generation}, {best_fitness:.2f}, {avg_fitness:.2f}\n")

                # Print generation results
                print(
                    f"Generation {generation}: Best Fitness = {best_fitness:.2f}, Average Fitness = {avg_fitness:.2f}")

            # Blank line after all generations
            result_file.write("\n")

            # Write the final best program
            result_file.write(f"Final Best Program: {overall_best_program}\n")





