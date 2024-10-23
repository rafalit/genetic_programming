package tiny_gp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Converter {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Converter <inputFile> <outputFile>");
            System.exit(1);
        }

        String inputFile = args[0];
        String outputFile = args[1];

        convert(inputFile, outputFile);
    }

    private static void convert(String inputFile, String outputFile) {
        try (BufferedReader reader = new BufferedReader(new FileReader("data/" + inputFile)); // zmiana na "data/"
             BufferedWriter writer = new BufferedWriter(new FileWriter("output/" + outputFile))) {

            String line;

            // Zapisz nagłówki CSV
            writer.write("X,Y\n");

            // Przetwarzaj dane z TinyGP
            while ((line = reader.readLine()) != null) {
                String[] tokens = line.split("\\s+");
                if (tokens.length >= 2) {
                    // Zakładamy, że pierwszy token to x, a drugi to y
                    writer.write(tokens[0] + "," + tokens[1] + "\n");
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
