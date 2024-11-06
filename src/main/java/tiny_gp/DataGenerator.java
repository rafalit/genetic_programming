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
import java.util.Random;

public class DataGenerator {

    public static void main(String[] args) {
        generateData("data/function5a.dat", -3.14, 3.14, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("data/function5b.dat", 0, 7, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("data/function5c.dat", 0, 100, 100, (x1, x2) -> Function5.evaluate(x1, x2));
        generateData("data/function5d.dat", -100, 100, 100, (x1, x2) -> Function5.evaluate(x1, x2));
    }
    private static void generateData(String filename, double minX, double maxX, int fitnessCases, FunctionInterface function) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
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
        Random random = new Random();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write("1 2 " + minX + " " + maxX + " " + fitnessCases + "\n");

            for (int i = 0; i <= fitnessCases; i++) {
                // Generowanie wartości x1 w równych odstępach w przedziale [minX, maxX]
                double x1 = minX + (maxX - minX) * i / fitnessCases;

                // Losowa wartość x2 w przedziale [minX, maxX]
                double x2 = minX + (maxX - minX) * random.nextDouble();

                // Oblicz wynik y na podstawie funkcji dla wylosowanych x1 i x2
                double y = function.evaluate(x1, x2);

                // Zapisz dane w odpowiednim formacie
                writer.write(x1 + "\t" + x2 + "\t" + y + "\n");
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
