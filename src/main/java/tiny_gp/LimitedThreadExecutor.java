package tiny_gp;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.Semaphore;

public class LimitedThreadExecutor extends Thread {

    public static void main(String[] args) {

        // List of suffixes for data files
        List<String> dataFileSuffixes = Arrays.asList(
                "1b", "1c", "1d",
                "2a", "2b", "2c", "2d",
                "3a", "3b", "3c", "3d",
                "4a", "4b", "4c", "4d",
                "5a", "5b", "5c", "5d",
                "6a", "6b", "6c", "6d"
        );
        int MAX_CONCURRENT_THREADS = 4;
        Semaphore semaphore = new Semaphore(MAX_CONCURRENT_THREADS);

        for (String suffix : dataFileSuffixes) {
            System.out.println(suffix);
            new Thread(new Worker(semaphore, suffix)).start();
        }

    }
}

class Worker implements Runnable {
    private final Semaphore semaphore;
    private final String dataFileSuffix;

    Worker(Semaphore semaphore, String _dataFileSuffix) {
        this.semaphore = semaphore;
        this.dataFileSuffix = _dataFileSuffix;
    }

    @Override
    public void run() {
        try {
            semaphore.acquire();  // Acquire a permit
            String filename = "data/data_variables_shuffled/problem" + dataFileSuffix + ".dat";
            String outputStatsFileName = "stats" + dataFileSuffix + ".csv";
            String outputFitnessFileName = "fitness" + dataFileSuffix + ".csv";
            String outputExpressionFileName = "expression" + dataFileSuffix + ".csv";

            // Create TinyGP instance and evolve
            TinyGP gp = new TinyGP(filename, -1, outputStatsFileName, outputFitnessFileName, outputExpressionFileName);
            gp.evolve();

            System.out.println("Task completed for data file suffix: " + dataFileSuffix);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            semaphore.release();  // Release the permit
        }
    }
}
