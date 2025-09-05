package non;

public class Wolf {
    public static int wolfCount = 0;
    private int age;
    private int lifespan = 9;
    private double hunger;
    private boolean isAlive;
    private int food;

    public Wolf(int food) {
        wolfCount++;
        age = 0;
        hunger = 1;
        isAlive = true;
        this.food = food;
    }

    public int ageUp() {
        if(isAlive) {
            age++;

            if(food > 0)
                food = eat(food);
            else
                hunger -= 0.1;

            if(hunger < 0.8)
                lifespan--;

            if(age > lifespan) {
                die();
                wolfCount--;
            }
        }

        return food;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int newAge) {
        age = newAge;
    }

    public int getLifespan() {
        return lifespan;
    }

    public void setLifespan(int newLifespan) {
        lifespan = newLifespan;
    }

    public double getHunger() {
        return hunger;
    }

    public void setHunger(int newHunger) {
        hunger = newHunger;
    }

    public boolean getIsAlive() {
        return isAlive;
    }

    public void setIsAlive(boolean isAlive) {
        this.isAlive = isAlive;
    }

    public void die() {
        isAlive = false;
    }

    public int eat(int amountOfFood) {
        hunger++;
        return amountOfFood - 1;
    }
}
