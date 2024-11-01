package tiny_gp;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import tiny_gp.functions.Function1;
import tiny_gp.functions.Function2;
import tiny_gp.functions.Function3;
import tiny_gp.functions.Function4;
import tiny_gp.functions.Function5;
import tiny_gp.functions.Function6;

public class DataGenerator {
    public static void main(String[] args) {
        // Funkcje z jednym argumentem
        generateData("../data/function1a.dat", -10, 10, 100, Function1::evaluate);
        generateData("../data/function1b.dat", 0, 100, 100, Function1::evaluate);
        generateData("../data/function1c.dat", -1, 1, 100, Function1::evaluate);
        generateData("../data/function1d.dat", -1000, 1000, 100, Function1::evaluate);

        generateData("../data/function2a.dat", -3.14, 3.14, 100, Function2::evaluate);
        generateData("../data/function2b.dat", 0, 7, 100, Function2::evaluate);
        generateData("../data/function2c.dat", 0, 100, 100, Function2::evaluate);
        generateData("../data/function2d.dat", -100, 100, 100, Function2::evaluate);

        generateData("../data/function3a.dat", 0, 4, 100, Function3::evaluate);
        generateData("../data/function3b.dat", 0, 9, 100, Function3::evaluate);
        generateData("../data/function3c.dat", 0, 99, 100, Function3::evaluate);
        generateData("../data/function3d.dat", 0, 999, 100, Function3::evaluate);

        // Funkcje, które wymagają dwóch argumentów
        generateData("../data/function4a.dat", 0, 1, 100, (x1, x2) -> Function4.evaluate(x1, x2));
        generateData("../data/function4b.dat", -10, 10, 100, (x1, x2) -> Function4.evaluate(x1, x2));
        generateData("../data/function4c.dat", 0, 100, 100, (x1, x2) -> Function4.evaluate(x1, x2));
        generateData("../data/function4d.dat", -100, 100, 100, (x1, x2) -> Function4.evaluate(x1, x2));


        generateData("../data/function5a.dat", -3.14, 3.14, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("../data/function5b.dat", 0, 7, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("../data/function5c.dat", 0, 100, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("../data/function5d.dat", -100, 100, 100, (x1, x2) -> Function5.evaluate(x1, x2));

        generateData("../data/function6a.dat", -10, 10, 100, (x1, x2) -> Function6.evaluate(x1, x2));
        generateData("../data/function6b.dat", 0, 100, 100, (x1, x2) -> Function6.evaluate(x1, x2));
        generateData("../data/function6c.dat", -1, 1, 100, (x1, x2) -> Function6.evaluate(x1, x2));
        generateData("../data/function6d.dat", -1000, 1000, 100, (x1, x2) -> Function6.evaluate(x1, x2));
    }

    private static void generateData(String filename, double minX, double maxX, int fitnessCases, FunctionInterface function) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("data/" + filename))) {
            writer.write("1 1 " + minX + " " + maxX + " " + fitnessCases + "\n");

            for (int i = 0; i <= fitnessCases; i++) {
                double x = minX + (maxX - minX) * i / fitnessCases; // Generowanie wartości x
                double y = function.evaluate(x); // Oblicz wynik y na podstawie x
                writer.write(x + "\t" + y + "\n"); // Zapisz dane w odpowiednim formacie
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void generateData(String filename, double minX, double maxX, int fitnessCases, BiFunctionInterface function) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("data/" + filename))) {
            writer.write("1 2 " + minX + " " + maxX + " " + fitnessCases + "\n");

            for (int i = 0; i <= fitnessCases; i++) {
                double x1 = minX + (maxX - minX) * i / fitnessCases; // Generate x1
                double x2 = minX + (maxX - minX) * (i + 1) / fitnessCases; // Generate x2
                double y = function.evaluate(x1, x2); // Compute result y
                writer.write(x1 + "\t" + x2 + "\t" + y + "\n"); // Save x1, x2, and y
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Interfejs funkcyjny do obsługi funkcji z jednym argumentem
    @FunctionalInterface
    interface FunctionInterface {
        double evaluate(double x);
    }

    // Interfejs funkcyjny do obsługi funkcji z dwoma argumentami
    @FunctionalInterface
    interface BiFunctionInterface {
        double evaluate(double x1, double x2);
    }
}
