import json
import pygame
pygame.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Just Text")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

FONT = pygame.font.SysFont("pixelpurl", 30)

def drawScreen0(): # Main Menu Screen
    HELLO_TEXT = "Welcome to Just Text!"
    MAIN_MENU_OPTIONS = ["(1) New Game",
                         "(2) Load Game",
                         "(3) Settings",
                         "(4) Quit"]
    y_buffer = 0
    x_buffer = 0

    rendered_text = FONT.render(HELLO_TEXT, 1, GREEN)
    y_buffer = rendered_text.get_height()
    x_buffer = y_buffer 

    WIN.blit(rendered_text, (x_buffer, y_buffer))

    for option in MAIN_MENU_OPTIONS:
        rendered_text = FONT.render(option, 1, WHITE)
        y_buffer += rendered_text.get_height() + 10

        WIN.blit(rendered_text, (x_buffer, y_buffer))

def main():
    run = True
    screen = 0

    with open("memory.json", "r") as f:
        data = json.load(f)

    count = data["count"]

    while run:
        WIN.fill(BLACK)

        drawScreen0()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                match screen:
                    case 0:
                        if event.key == pygame.K_1:
                            print("New Game Chosen!")
                            # TODO: switch to new game screen
                        elif event.key == pygame.K_2:
                            print("Load Game Chosen!")
                            # TODO: switch to load game screen
                        elif event.key == pygame.K_3:
                            print("Setting Chosen!")
                            # TODO: switch to settings screen
                        elif event.key == pygame.K_4:
                            run = False
                            break
                    case _:
                        print("Screen Tracking Error!")

        with open("memory.json", "w") as f:
            json.dump({"count": count}, f)
            
    pygame.quit()

if __name__ == '__main__':
    main()