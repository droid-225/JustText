import java.util.Scanner;

public class SimpleTesting {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int wolves;
        int rabbits;
        int carrots;
        int year = 0;
        int input;

        System.out.println("Welcome!");
        System.out.println("Enter the Initial Number of Wolves:");
        wolves = in.nextInt();

        System.out.println("Enter the Initial Number of Rabbits:");
        rabbits = in.nextInt();

        System.out.println("Enter the Initial Number of Carrots:");
        carrots = in.nextInt();

        while(wolves > 0 && rabbits > 0 && carrots > 0) {
            if(year == 0) {
                System.out.println("\nYear: " + year);
                System.out.println("Wolves: " + wolves);
                System.out.println("Rabbits: " + rabbits);
                System.out.println("Carrots: " + carrots);

                System.out.println("\nEnter an Option:");
                System.out.println("(1) Continue");
                System.out.println("(2) Quit");
            }

            year++;
            input = in.nextInt();

            if(input == 1) {
                carrots -= (int)(Math.random() * rabbits) + 1;
                rabbits -= (int)(Math.random() * wolves) + 1;

                if(carrots > 0 && carrots >= rabbits)
                    rabbits += (int)(Math.random() * 7) + 1;
                else
                    rabbits -= rabbits - carrots;

                if(rabbits > 0 && rabbits >= wolves)
                    wolves += (int)(Math.random() * 3) + 1;
                else
                    wolves -= wolves - rabbits;

                System.out.println("\nYear: " + year);
                System.out.println("Wolves: " + wolves);
                System.out.println("Rabbits: " + rabbits);
                System.out.println("Carrots: " + carrots);

                System.out.println("\nEnter an Option:");
                System.out.println("(1) Continue");
                System.out.println("(2) Quit");
            }
            else if(input == 2) {
                break;
            }
            else {
                System.out.println("\nIncorrect Input!");
                System.out.println("Enter an Option:");
                System.out.println("(1) Continue");
                System.out.println("(2) Quit");
            }
        }

        System.out.println("\nGoodbye!");
    }
}
