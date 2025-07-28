import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int numOfCarrots = 100;
        int year = 0;
        String input;
        Wolf wof = new Wolf();
        Rabbit rabi = new Rabbit();

        System.out.println("\nWelcome to the Rabbit Wolf Simulation!");
        while(true) {
            if(year == 0) {
                System.out.println("Enter One of the Following Options:");
                System.out.println("(S) Start Simulation");
                System.out.println("(Q) Exit\n");
                input = in.next();

                if(input.equals("Q") || input.equals("q")) {
                    System.out.println("\nOkay, Bye!");
                    return;
                }
                else if(input.equals("S") || input.equals("s")) {
                    year++;
                    System.out.println("\nWelcome!");
                    System.out.println("Year: " + year);
                    System.out.println("Number of Carrots: " + rabi.getNumOfCarrots());
                    System.out.println("Number of Rabbits: " + Rabbit.rabbitCount);
                    System.out.println("Number of Wolves: " + Wolf.wolfCount);
                    System.out.println("\nEnter Next Move:");
                    System.out.println("(C) Continue");
                    System.out.println("(Q) Exit");
                }
                else {
                    System.out.println("\nIncorrect Input!");
                }
            }

            input = in.next();

            if(input.equals("C") || input.equals("c")) {
                year++;
                rabi.ageUp();
                wof.ageUp();
                System.out.println("\nYear: " + year);
                System.out.println("Number of Carrots: " + rabi.getNumOfCarrots());
                System.out.println("Number of Rabbits: " + Rabbit.rabbitCount);
                System.out.println("Number of Wolves: " + Wolf.wolfCount);
                System.out.println("\nEnter Next Move:");
                System.out.println("(C) Continue");
                System.out.println("(Q) Exit");
            }
            else if(input.equals("Q") || input.equals("q")) {
                System.out.println("\nOkay, Bye!");
                return;
            }
            else {
                System.out.println("\nIncorrect Input!");
                System.out.println("\nEnter Next Move:");
                System.out.println("(C) Continue");
                System.out.println("(Q) Exit");
            }
        }
    }
}