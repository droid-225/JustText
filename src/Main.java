import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        File memory = new File("memory.txt");
        int count = 0;
        boolean running = true;
        boolean error = false;

        // Read data from memory
        try {
            count = ReadData(memory);
        } catch(FileNotFoundException e) {
            error = true;
            System.out.println("File Specified not Found!");
            e.printStackTrace();
        }

        // main game loop
        while(!error && running) {
            System.out.println("Count: " + count);
            System.out.println("\n(1) Count up");
            System.out.println("(2) Count down");
            System.out.println("(3) Quit");

            switch(in.nextInt()) {
                case 1 -> count++;
                case 2 -> count--;
                case 3 -> running = false;
            }
        }

        in.close();

        // Save data to memory
        try {
            SaveData(count, memory);
        } catch (IOException e) {
            error = true;
            System.out.println("An Error Occurred Writing to Memory:");
            e.printStackTrace();
        }
    }

    public static void SaveData(int count, File file) throws IOException {
        FileWriter writer = new FileWriter(file);
        writer.write(String.valueOf(count));
        writer.close();
    }

    public static int ReadData(File file) throws FileNotFoundException {
        Scanner reader = new Scanner(file);
        int data = reader.nextInt();
        reader.close();

        return data;
    }
}
