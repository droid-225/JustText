import java.util.Scanner;

public class SimpleTesting {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int wolves;
        int rabbits;
        int carrots;
        int year = 1;
        int input;

        System.out.println("Welcome!");
        System.out.println("Enter the Initial Number of Wolves:");
        wolves = in.nextInt();

        System.out.println("Enter the Initial Number of Rabbits:");
        rabbits = in.nextInt();

        System.out.println("Enter the Initial Number of Wolves:");
        carrots = in.nextInt();

        while(true) {
            System.out.println("\nYear: " + year);
            System.out.println("Wolves: " + wolves);
            System.out.println("Rabbits: " + rabbits);
            System.out.println("Carrots: " + carrots);

            System.out.println("\nEnter an Option:");
            System.out.println("(1) Continue");
            System.out.println("(2) Quit");
            input = in.nextInt();

            if(input == 1) {
                year++;
            }
            else if(input == 2) {
                return;
            }
            else {
                System.out.println("\nIncorrect Input!");
                System.out.println("Enter an Option:");
                System.out.println("(1) Continue");
                System.out.println("(2) Quit");
            }
        }
    }
}
