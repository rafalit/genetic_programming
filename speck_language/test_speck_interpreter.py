# test_speck_interpreter.py
import unittest
from speck_interpreter import SpeckInterpreter

class TestSpeckInterpreter(unittest.TestCase):

    def test_input_from_file(self):
        input_file = "dane/input.txt"
        output_file = "dane/output.txt"
        with open(input_file, 'w') as f:
            f.write("4,2")

        # Definicja kodu operacji
        code = "in(x); in(y); out(x * y);"
        inputs = SpeckInterpreter.read_input_from_file(input_file)
        interpreter = SpeckInterpreter(code)
        outputs = interpreter.run_program(inputs)

        SpeckInterpreter.write_output_to_file(output_file, outputs)

        with open(output_file, 'r') as f:
            result = f.read().strip()
        self.assertEqual(result, "8")

    def test_input_file_with_invalid_data(self):
        input_file = "dane/input.txt"
        output_file = "dane/output.txt"
        with open(input_file, 'w') as f:
            f.write("4,abc")  # (błąd)

        # Oczekujemy, że funkcja podniesie ValueError
        with self.assertRaises(ValueError):
            SpeckInterpreter.read_input_from_file(input_file)

    def test_insufficient_inputs(self):
        code = "in(x); in(y); out(x + y);"
        inputs = [5]  # Zaledwie jedno wejście
        interpreter = SpeckInterpreter(code)
        with self.assertRaises(ValueError):  # Brak drugiego wejścia
            interpreter.run_program(inputs)

    def test_large_output(self):
        code = "in(x); out(x); out(x); out(x);"
        inputs = [5]
        interpreter = SpeckInterpreter(code)
        output = interpreter.run_program(inputs)
        self.assertTrue("OUTPUT_LIMIT_REACHED" in output)

    def test_output_limit(self):
        code = ";".join([f"out({i})" for i in range(101)])
        inputs = [0]
        interpreter = SpeckInterpreter(code)
        output = interpreter.run_program(inputs)
        self.assertTrue("OUTPUT_LIMIT_REACHED" in output)


if __name__ == "__main__":
    unittest.main()
