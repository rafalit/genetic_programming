# speck_interpreter.py
class SpeckInterpreter:
    def __init__(self, code, max_output=100):
        self.code = code
        self.output = []
        self.max_output = max_output

    def run_program(self, inputs):
        if len(inputs) < self.code.count("in("):
            raise ValueError("Not enough inputs provided.")
        self.inputs = inputs
        self.input_index = 0
        self.output = []
        self.execute_code()
        return self.output

    def execute_code(self):
        for line in self.code.split(';'):
            line = line.strip()
            if line.startswith("in("):
                var_name = line[3:-1]
                if self.input_index < len(self.inputs):
                    globals()[var_name] = self.inputs[self.input_index]
                    self.input_index += 1
                else:
                    globals()[var_name] = None

            elif line.startswith("out("):
                expression = line[4:-1]
                try:
                    result = eval(expression, globals())
                    # Sprawdzamy, czy liczba wyników przekroczyła limit
                    if len(self.output) < self.max_output:
                        self.output.append(result)
                    else:
                        self.output.append("OUTPUT_LIMIT_REACHED")
                        return  # Zakończenie po osiągnięciu limitu
                except Exception as e:
                    self.output.append(f"ERROR: {e}")

    @staticmethod
    def read_input_from_file(filepath):
        try:
            with open(filepath, 'r') as file:
                data = file.read().strip()
                return list(map(int, data.split(',')))
        except ValueError as e:
            # Obsługuje błędy konwersji danych na liczby
            raise ValueError(f"Invalid data in input file: {e}")

    @staticmethod
    def write_output_to_file(filepath, outputs):
        with open(filepath, 'w') as file:
            file.write(','.join(map(str, outputs)))

