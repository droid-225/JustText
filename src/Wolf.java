import java.util.HashMap;
import java.util.Map;

public class Wolf extends Entity {
    public static int wolfCount = 0;
    private double hunger;
    public static Map<Wolf, Boolean> wolves = new HashMap<>();
    private int numOfPups;

    Wolf() {
        setAge(0);
        setLifespan(15);
        this.hunger = 0;
        wolfCount++;
        wolves.put(this, true);
    }

    @Override
    public void ageUp() {
        if (isAlive()) {
            setAge(getAge() + 1);
            hunger += 0.1;

            if(hunger >= 0.5 && Rabbit.rabbitCount > 0) {
                eatRabbit();
            }
            else if(getAge() >= 3) {
                numOfPups = (int)(Math.random() * 3) + 1;

                while(numOfPups != 0) {
                    wolves.put(new Wolf(), true);
                    numOfPups--;
                }
            }

            if(hunger > 0.8) {
                setLifespan(getLifespan() - 1);
            }

            if(getAge() == getLifespan() + 1) {
                die();
                wolfCount--;
                wolves.remove(this);
            }
        }
    }

    public void eatRabbit() {
        Rabbit.rabbitCount--;
        hunger = 0;
    }
}
