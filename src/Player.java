public class Player extends Entity {
    private String name = "";

    Player(String name, int age) {
        this.name = name;
        setAge(age);
        setLifespan(100);
    }
}
