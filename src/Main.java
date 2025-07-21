import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int numOfCarrots = 100;
        int year = 0;
        String input;
        Wolf wof;
        Rabbit rabi;

        System.out.println("\nWelcome to the Rabbit Wolf Simulation!");
        while(true) {
            if(year == 0) {
                System.out.println("Enter One of the Following Options:");
                System.out.println("(Q) Exit");
                System.out.println("(S) Start Simulation\n");
                input = in.next();

                if(input.equals("Q") || input.equals("q")) {
                    System.out.println("\nOkay, Bye!");
                    return;
                }
                else if(input.equals("S")) {
                    wof = new Wolf();
                    rabi = new Rabbit();
                    year++;
                    System.out.println("\nWelcome!");
                    System.out.println("Year: " + year);
                    System.out.println("Number of Carrots: " + numOfCarrots);
                    System.out.println("Number of Rabbits: " + Rabbit.rabbitCount);
                    System.out.println("Number of Wolves: " + Wolf.wolfCount);
                    //System.out.println("");
                    return;
                }
                else {
                    System.out.println("\nIncorrect Input!");
                }
            }
        }
    }
}