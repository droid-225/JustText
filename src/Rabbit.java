import java.util.HashMap;
import java.util.Map;

public class Rabbit extends Entity {
    public static int rabbitCount = 0;
    public static Map<Rabbit, Boolean> rabbits = new HashMap<>();
    private double hunger = 0;
    private int litterSize;
    private int numOfCarrots;

    Rabbit() {
        rabbitCount++;
        setAge(0);
        setLifespan(9);
        rabbits.put(this, true);
    }

    @Override
    public void ageUp() {
        if (isAlive()) {
            setAge(getAge() + 1);
            hunger += 0.1;

            if(hunger >= 0.5 && numOfCarrots > 0) {
                eatCarrots();
            }
            else if(getAge() >= 1) {
                litterSize = (int)(Math.random() * 7) + 1;

                while(litterSize != 0) {
                    rabbits.put(new Rabbit(), true);
                    litterSize--;
                }
            }

            if(hunger > 0.8) {
                setLifespan(getLifespan() - 1);
            }

            if(getAge() == getLifespan() + 1) {
                die();
                rabbitCount--;
                rabbits.remove(this);
            }
        }
    }

    private void eatCarrots() {
        hunger = 0;
        setNumOfCarrots(getNumOfCarrots() - 1);
    }

    public void setNumOfCarrots(int newNumOfCarrots) {
        numOfCarrots = newNumOfCarrots;
    }

    public int getNumOfCarrots() {
        return numOfCarrots;
    }
}
