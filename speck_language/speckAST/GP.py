import random
from .SpeckAST import SpeckAST


class GP:
    def __init__(self, population_size, max_program_size, initial_program_size, max_variables, max_depth,
                 tournament_size, crossover_rate, mutation_rate, fitness_function, log_file="programs_log.txt"):
        self.population_size = population_size
        self.max_program_size = max_program_size
        self.initial_program_size = initial_program_size
        self.max_variables = max_variables
        self.max_depth = max_depth
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function
        self.log_file = log_file

        self.population = [
            SpeckAST(max_program_size, initial_program_size, max_variables, max_depth)
            for _ in range(population_size)
        ]
        self.fitness_scores = [None] * population_size

    def log_program(self, program, generation, event_type):
        """Log the generated program to a file"""
        with open(self.log_file, "a") as log:
            log.write(f"Generation {generation} - {event_type}:\n")
            log.write(str(program) + "\n\n")

    def evaluate_population(self, input_list, expected_output, time_limit):
        print("Evaluating population...")
        self.fitness_scores = [
            self.fitness_function(individual.run(input_list, len(expected_output), time_limit), expected_output)
            for individual in self.population
        ]

        print(f"Fitness scores: {self.fitness_scores}")

    def tournament_selection(self):
        print("Selecting individuals by tournament...")
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
                print(f"Crossover happened between two individuals")
                self.log_program(child, generation, "Crossover")
            elif random.random() < self.mutation_rate:
                parent = random.choice(selected_population)
                child = parent.mutation()
                print(f"Mutation happened on an individual")
                self.log_program(child, generation, "Mutation")
            else:
                child = random.choice(selected_population)
                print(f"Copying an individual without change")
                self.log_program(child, generation, "Copy")

            while child.depth > self.max_depth:
                print(f"Child depth exceeded max depth of {self.max_depth}, regenerating...")
                if random.random() < self.crossover_rate:
                    parent1, parent2 = random.sample(selected_population, 2)
                    child = SpeckAST.crossover(parent1, parent2)
                else:
                    parent = random.choice(selected_population)
                    child = parent.mutation()

            new_population.append(child)

        self.population = new_population

    def run(self, generations, input_list, expected_output, time_limit):
        for generation in range(generations):
            print(f"\nGeneration {generation}")
            self.evolve(input_list, expected_output, time_limit, generation)
            best_fitness = max(self.fitness_scores)
            print(f"Best fitness in this generation: {best_fitness:.1f}")




