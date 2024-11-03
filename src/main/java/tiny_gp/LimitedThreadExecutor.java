package tiny_gp;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.Semaphore;

public class LimitedThreadExecutor extends Thread {

    public static void main(String[] args) {
        List<String> dataFileSuffixes = Arrays.asList(
                "7a","8a"
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
            semaphore.acquire();
            String filename = "data/data_variables_shuffled/problem" + dataFileSuffix + ".dat";
            String outputStatsFileName = "stats" + dataFileSuffix + ".csv";
            String outputFitnessFileName = "fitness" + dataFileSuffix + ".csv";
            String outputExpressionFileName = "expression" + dataFileSuffix + ".csv";

            TinyGP gp = new TinyGP(filename, -1, outputStatsFileName, outputFitnessFileName, outputExpressionFileName);
            gp.evolve();

            System.out.println("Task completed for data file suffix: " + dataFileSuffix);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            semaphore.release();
        }
    }
}
