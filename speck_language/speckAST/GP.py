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
        self.stagnation_threshold = 5  # Threshold for considering stagnation
        self.original_crossover_rate = crossover_rate
        self.original_mutation_rate = mutation_rate

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
        half_population = len(self.population) // 5
        self.population = self.population[:half_population]

    def evolve(self, inputs, outputs, time_limit):
        self.evaluate_population(inputs, outputs, time_limit)
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
        # Otwieramy plik do zapisu wyników
        with open(self.result_file, 'w') as result_file:
            # Zapiszemy nagłówek do pliku
            result_file.write("Generation, Best Fitness, Average Fitness\n")

            # Zmienna do śledzenia najlepszego programu w całej ewolucji
            overall_best_fitness = float('-inf')
            overall_best_program = None

            for generation in range(generations):
                # Przeprowadzamy ewolucję w każdej generacji
                self.evolve(inputs, outputs, time_limit)

                # Zbieramy wyniki fitness dla wszystkich programów w populacji
                valid_fitness_scores = [p.fitness for p in self.population if p.fitness != float('-inf')]

                # Jeśli są ważne wyniki, obliczamy średni fitness
                if valid_fitness_scores:
                    avg_fitness = sum(valid_fitness_scores) / len(valid_fitness_scores)
                else:
                    avg_fitness = 0  # Jeśli nie ma ważnych wyników, ustawiamy na 0

                # Zbieramy najlepszy fitness w tej generacji
                best_fitness = max(valid_fitness_scores) if valid_fitness_scores else float('-inf')

                # Wybieramy najlepszego osobnika z populacji (na podstawie najlepszego fitness)
                best_individual = max(self.population, key=lambda p: p.fitness)
                best_program = best_individual.get_program()

                # Jeśli najlepszy fitness w tej generacji jest lepszy od dotychczasowego najlepszego, aktualizujemy
                if best_fitness > overall_best_fitness:
                    overall_best_fitness = best_fitness
                    overall_best_program = best_program
                    self.stagnation_count = 0  # Reset stagnation counter because we improved
                else:
                    self.stagnation_count += 1  # Increment stagnation counter if no improvement

                # Zapisujemy wyniki dla tej generacji do pliku
                result_file.write(f"{generation}, {overall_best_fitness:.2f}, {avg_fitness:.2f}\n")

                # Drukujemy wyniki na ekran
                print(
                    f"Generation {generation + 1}: Best Fitness = {overall_best_fitness:.2f}, Average Fitness = {avg_fitness:.2f}")

                # Sprawdzamy, czy osiągnęliśmy best_fitness = 0, jeśli tak, kończymy program
                if overall_best_fitness == 0:
                    print(f"Best Fitness reached 0 at generation {generation + 1}. Stopping the program.")
                    break

                # Jeśli stagnacja trwa przez zbyt wiele generacji, zmieniamy współczynniki
                if self.stagnation_count >= self.stagnation_threshold:
                    print(f"Stagnation detected! Increasing mutation and reducing crossover.")
                    self.crossover_rate = 0.0
                    self.mutation_rate = 1.0
                else:
                    # Jeśli stagnacja została przerwana, przywracamy oryginalne wartości
                    if self.crossover_rate != self.original_crossover_rate or self.mutation_rate != self.original_mutation_rate:
                        print(f"Improvement detected! Restoring original crossover and mutation rates.")
                        self.crossover_rate = self.original_crossover_rate
                        self.mutation_rate = self.original_mutation_rate

            # Po zakończeniu wszystkich generacji zapisujemy najlepszego programu
            result_file.write("\n")
            result_file.write(f"Final Best Program:\n {overall_best_program}\n")
