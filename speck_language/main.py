import os
from speckAST.SpeckAST import SpeckAST


# Tworzenie folderów do zapisu wyników
os.makedirs('programs', exist_ok=True)
os.makedirs('mutation', exist_ok=True)
os.makedirs('crossover', exist_ok=True)

# Tworzenie dwóch programów
program1 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)
program2 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)
program3 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)
program4 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)
program5 = SpeckAST(max_program_size=15, initial_program_size=7, max_variables=5, max_depth=10)

# Wyświetlanie początkowych programów
print("Początkowy Program 1:")
print(program1)

print("\nPoczątkowy Program 2:")
print(program2)

print("\nPoczątkowy Program 3:")
print(program3)

print("\nPoczątkowy Program 4:")
print(program4)

print("\nPoczątkowy Program 5:")
print(program5)

with open('programs/program1.txt', 'w') as f1, open('programs/program2.txt', 'w') as f2, open(
        'programs/program3.txt', 'w') as f3, open('crossover/program4.txt', 'w') as f4, open(
        'crossover/program5.txt', 'w') as f5:
    f1.write(str(program1))
    f2.write(str(program2))
    f3.write(str(program3))
    f4.write(str(program4))
    f5.write(str(program5))
