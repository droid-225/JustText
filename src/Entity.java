public class Entity {
    public static int entityCount = 0;
    private int age = 0;
    private int lifespan;
    private boolean alive = true;

    Entity() {
        entityCount++;
    }

    public void ageUp() {
        if (alive) {
            age++;

            if(age == lifespan + 1)
                die();
        }
    }

    public void setAge(int newAge) {
        age = newAge;
    }

    public int getAge() {
        return age;
    }

    public boolean isAlive() {
        return alive;
    }

    public void die() {
        alive = false;
    }

    public int getLifespan() {
        return lifespan;
    }

    public void setLifespan(int newLifespan) {
        lifespan = newLifespan;
    }
}
