import os
from speckAST.SpeckAST import SpeckAST


# Tworzenie folderów do zapisu wyników
os.makedirs('programs', exist_ok=True)
os.makedirs('mutation', exist_ok=True)
os.makedirs('crossover', exist_ok=True)

# Tworzenie dwóch programów
program1 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)
program2 = SpeckAST(max_program_size=10, initial_program_size=5, max_variables=3, max_depth=10)

# Wyświetlanie początkowych programów
print("Początkowy Program 1:")
print(program1)

print("\nPoczątkowy Program 2:")
print(program2)

program3 = SpeckAST.crossover(program1, program2)
print("Program 3 (crossing programów 1 i 2):")
print(program3)

program4 = program1.mutation()
print("Program 4 (mutacja programu 1):")
print(program4)

program5 = program2.mutation()
print("Program 5 (mutacja programu 2):")
print(program5)

with open('programs/program1.txt', 'w') as f1, open('programs/program2.txt', 'w') as f2, open(
        'crossover/program3.txt', 'w') as f3, open('mutation/program4.txt', 'w') as f4, open(
        'mutation/program5.txt', 'w') as f5:
    f1.write(str(program1))
    f2.write(str(program2))
    f3.write(str(program3))
    f4.write(str(program4))
    f5.write(str(program5))
