package tiny_gp;

import java.util.*;
import java.io.*;
import tiny_gp.functions.Function1;
import tiny_gp.functions.Function2;
import tiny_gp.functions.Function3;
import tiny_gp.functions.Function4;
import tiny_gp.functions.Function5;
import tiny_gp.functions.Function6;

public class TinyGP {
    private double[] fitness;
    private char[][] population;
    private static final Random random = new Random();

    // Constants for function set
    private static final int ADD = 110;
    private static final int SUB = 111;
    private static final int MUL = 112;
    private static final int DIV = 113;
    private static final int FSET_START = ADD;
    private static final int FSET_END = DIV;

    private static double[] x;
    private static double minRandom;
    private static double maxRandom;
    private static char[] program;
    private static int programCounter;
    private static int variableCount;
    private static int fitnessCases;
    private static double bestFitness = 0.0;
    private static double averageFitness = 0.0;
    private static long seed;
    private static double averageLength;

    private static final int MAX_LENGTH = 10;
    private static final int POPULATION_SIZE = 1000;
    private static final int DEPTH = 2;
    private static final int GENERATIONS = 100;
    private static final int TOURNAMENT_SIZE = 2;
    public static final double PMUT_PER_NODE = 0.03;
    public static final double CROSSOVER_PROB = 0.9;

    private static double[][] targets;

    private double[] computedValues;

    // Constructor
    public TinyGP(String filename, long seedValue) {
        fitness = new double[POPULATION_SIZE];
        seed = seedValue;

        if (seed >= 0) {
            random.setSeed(seed);
        }

        setupFitness(filename);
        initializeRandomVariables();
        population = createRandomPopulation(POPULATION_SIZE, DEPTH, fitness);
    }

    private void initializeRandomVariables() {
        x = new double[FSET_START];
        for (int i = 0; i < FSET_START; i++) {
            x[i] = (maxRandom - minRandom) * random.nextDouble() + minRandom;
        }
    }

    // Main method
    public static void main(String[] args) {
        String filename = "problem.dat"; // plik problem.dat musi być w folderze głównym
        long seedValue = -1;

        if (args.length == 2) {
            seedValue = Integer.parseInt(args[0]);
            filename = args[1];
        } else if (args.length == 1) {
            filename = args[0];
        }

        System.out.println(filename);

        TinyGP gp = new TinyGP(filename, seedValue);
        gp.evolve();
    }

    // Evolution process
    private void evolve() {
        int generation = 0;
        printParameters();
        stats(fitness, population, 0);

        for (generation = 1; generation < GENERATIONS; generation++) {
            if (bestFitness > -1e-5) {
                System.out.println("PROBLEM SOLVED");
                System.exit(0);
            }

            for (int i = 0; i < POPULATION_SIZE; i++) {
                char[] newIndividual;
                if (random.nextDouble() < CROSSOVER_PROB) {
                    int parent1 = tournament(fitness, TOURNAMENT_SIZE);
                    int parent2 = tournament(fitness, TOURNAMENT_SIZE);
                    newIndividual = crossover(population[parent1], population[parent2]);
                } else {
                    int parent = tournament(fitness, TOURNAMENT_SIZE);
                    newIndividual = mutation(population[parent], PMUT_PER_NODE);
                }
                double newFitness = fitnessFunction(newIndividual);
                int offspring = negativeTournament(fitness, TOURNAMENT_SIZE);
                population[offspring] = newIndividual;
                fitness[offspring] = newFitness;
            }
            stats(fitness, population, generation);
        }
        System.out.println("PROBLEM *NOT* SOLVED");
        System.exit(1);
    }

    // Fitness setup method
    private void setupFitness(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) { // zmiana na "problem.dat"
            String line = reader.readLine();
            StringTokenizer tokens = new StringTokenizer(line);

            int randomCount = Integer.parseInt(tokens.nextToken().trim());
            variableCount = Integer.parseInt(tokens.nextToken().trim());
            minRandom = Double.parseDouble(tokens.nextToken().trim());
            maxRandom = Double.parseDouble(tokens.nextToken().trim());
            fitnessCases = Integer.parseInt(tokens.nextToken().trim());

            targets = new double[fitnessCases][variableCount + 1];

            if (variableCount + randomCount >= FSET_START) {
                throw new IllegalArgumentException("Too many variables and constants");
            }

            for (int i = 0; i < fitnessCases; i++) {
                line = reader.readLine();
                tokens = new StringTokenizer(line);
                for (int j = 0; j <= variableCount; j++) {
                    targets[i][j] = Double.parseDouble(tokens.nextToken().trim());
                }
            }
        } catch (FileNotFoundException e) {
            System.err.println("ERROR: Please provide a data file");
            System.exit(0);
        } catch (Exception e) {
            System.err.println("ERROR: Incorrect data format");
            System.exit(0);
        }
    }

    // Fitness function implementation
    private double fitnessFunction(char[] prog) {
        double fit = 0.0;
        computedValues = new double[fitnessCases]; // Store computed values per fitness case

        for (int i = 0; i < fitnessCases; i++) {
            for (int j = 0; j < variableCount; j++) {
                x[j] = targets[i][j];
            }
            program = prog;
            programCounter = 0;
            double result = run();
            computedValues[i] = result;  // Store the computed result for this fitness case
            fit += Math.abs(result - targets[i][variableCount]);
        }

        return -fit;  // Normalized by fitnessCases
    }

    // Run interpreter
    private double run() {
        char primitive = program[programCounter++];
        if (primitive < FSET_START) {
            return x[primitive];
        }

        switch (primitive) {
            case ADD:
                return run() + run();
            case SUB:
                return run() - run();
            case MUL:
                return run() * run();
            case DIV:
                double num = run();
                double den = run();
                return Math.abs(den) <= 0.001 ? num : num / den;
        }
        return 0.0; // should never get here
    }

    // Traversal method
    private int traverse(char[] buffer, int bufferCount) {
        if (buffer[bufferCount] < FSET_START) {
            return ++bufferCount;
        }

        switch (buffer[bufferCount]) {
            case ADD:
            case SUB:
            case MUL:
            case DIV:
                return traverse(buffer, traverse(buffer, ++bufferCount));
        }
        return 0; // should never get here
    }

    // Random individual creation
    private char[] createRandomIndividual(int depth) {
        char[] individual;
        int length;

        length = grow(buffer, 0, MAX_LENGTH, depth);

        while (length < 0) {
            length = grow(buffer, 0, MAX_LENGTH, depth);
        }

        individual = new char[length];
        System.arraycopy(buffer, 0, individual, 0, length);
        return individual;
    }

    // Population creation
    private char[][] createRandomPopulation(int n, int depth, double[] fitness) {
        char[][] pop = new char[n][];
        for (int i = 0; i < n; i++) {
            pop[i] = createRandomIndividual(depth);
            fitness[i] = fitnessFunction(pop[i]);
        }
        return pop;
    }

    // Create random individual with grow method
    private static char[] buffer = new char[MAX_LENGTH];
    private int grow(char[] buffer, int pos, int max, int depth) {
        char prim = (char) random.nextInt(2);
        int oneChild;

        if (pos >= max) return -1;

        if (pos == 0) prim = 1;

        if (prim == 0 || depth == 0) {
            prim = (char) random.nextInt(variableCount + FSET_END - FSET_START + 1);
            buffer[pos] = prim;
            return pos + 1;
        } else {
            prim = (char) (random.nextInt(FSET_END - FSET_START + 1) + FSET_START);
            buffer[pos] = prim;
            oneChild = grow(buffer, pos + 1, max, depth - 1);
            if (oneChild < 0) return -1;
            return grow(buffer, oneChild, max, depth - 1);
        }
    }

    // Mutation method
    private char[] mutation(char[] parent, double pmut) {
        int len = traverse(parent, 0);
        char[] parentCopy = new char[len];

        System.arraycopy(parent, 0, parentCopy, 0, len);
        for (int i = 0; i < len; i++) {
            if (random.nextDouble() < pmut) {
                int mutSite = i;
                if (parentCopy[mutSite] < FSET_START) {
                    parentCopy[mutSite] = (char) random.nextInt(variableCount + FSET_END - FSET_START + 1);
                } else {
                    switch (parentCopy[mutSite]) {
                        case ADD:
                        case SUB:
                        case MUL:
                        case DIV:
                            parentCopy[mutSite] = (char) (random.nextInt(FSET_END - FSET_START + 1) + FSET_START);
                            break;
                    }
                }
            }
        }
        return parentCopy;
    }

    // Crossover method
    private char[] crossover(char[] parent1, char[] parent2) {
        int len1 = traverse(parent1, 0);
        int len2 = traverse(parent2, 0);
        int crossSite1 = random.nextInt(len1);
        int crossSite2 = random.nextInt(len2);

        char[] offspring = new char[len1 + len2];
        System.arraycopy(parent1, 0, offspring, 0, crossSite1);
        System.arraycopy(parent2, crossSite2, offspring, crossSite1, len2 - crossSite2);
        System.arraycopy(parent1, crossSite1, offspring, crossSite1 + len2 - crossSite2, len1 - crossSite1);
        return offspring;
    }

    // Tournament selection method
    private int tournament(double[] fitness, int size) {
        int bestIndex = random.nextInt(POPULATION_SIZE);
        double bestFitness = fitness[bestIndex];

        for (int i = 1; i < size; i++) {
            int contender = random.nextInt(POPULATION_SIZE);
            if (fitness[contender] > bestFitness) {
                bestFitness = fitness[contender];
                bestIndex = contender;
            }
        }
        return bestIndex;
    }

    // Negative tournament selection method
    private int negativeTournament(double[] fitness, int size) {
        int worstIndex = random.nextInt(POPULATION_SIZE);
        double worstFitness = fitness[worstIndex];

        for (int i = 1; i < size; i++) {
            int contender = random.nextInt(POPULATION_SIZE);
            if (fitness[contender] < worstFitness) {
                worstFitness = fitness[contender];
                worstIndex = contender;
            }
        }
        return worstIndex;
    }

    // Print parameters method
    private void printParameters() {
        System.out.println("-- TINY GP (Java version) --");
        System.out.printf("SEED=%d\nMAX_LEN=%d\nPOPSIZE=%d\nDEPTH=%d\nCROSSOVER_PROB=%.2f\nPMUT_PER_NODE=%.2f\nMIN_RANDOM=%.2f\nMAX_RANDOM=%.2f\nGENERATIONS=%d\nTSIZE=%d\n",
                seed, MAX_LENGTH, POPULATION_SIZE, DEPTH, CROSSOVER_PROB, PMUT_PER_NODE, minRandom, maxRandom, GENERATIONS, TOURNAMENT_SIZE);
        System.out.println("----------------------------------");
    }

    // Stats method for calculating statistics of the population
    // Stats method for calculating statistics of the population
    // Stats method for calculating statistics of the population
    private void stats(double[] fitness, char[][] population, int generation) {
        double sumFitness = 0.0;
        int bestIndex = 0;

        for (int i = 0; i < fitness.length; i++) {
            sumFitness += fitness[i];
            if (fitness[i] > fitness[bestIndex]) {
                bestIndex = i;
            }
        }

        bestFitness = fitness[bestIndex];
        averageFitness = sumFitness / fitness.length;

        // Display progress in the terminal
        System.out.printf("Generation %d: Best Fitness = %.5f, Average Fitness = %.5f%n", generation, bestFitness, averageFitness);

        // Save data to the file with targets and computed values
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output/stats5d.csv", generation == 1))) { // Overwrites on first generation
            // Write the header

            if (variableCount == 1) {
                writer.write("x1, Expected Value, Function Value\n");
            } else if (variableCount == 2) {
                writer.write("x1, x2, Expected Value, Function Value\n");
            }
            // Write an empty line for spacing before new generation data
            writer.write("\n");

            for (int i = 0; i < fitnessCases; i++) {
                StringBuilder line = new StringBuilder();
                for (int j = 0; j < variableCount; j++) {
                    line.append(targets[i][j]).append(", ");
                }
                line.append(targets[i][variableCount]).append(", ")
                        .append(computedValues[i]);
                writer.write(line.toString() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Save generation statistics to fitness file
        try {
            File fitnessDir = new File("fitness");
            if (!fitnessDir.exists()) {
                fitnessDir.mkdirs(); // Create the fitness directory if it does not exist
            }

            // Append to the fitness file
            try (BufferedWriter fitnessWriter = new BufferedWriter(new FileWriter("fitness/fitness5d.csv", generation != 1))) {
                if (generation == 1) {
                    fitnessWriter.write("Generation, Best Fitness, Average Fitness\n"); // Write header on the first write
                }
                fitnessWriter.write(String.format("%d, %.5f, %.5f%n", generation, bestFitness, averageFitness));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
