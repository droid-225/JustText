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

def drawScreen1():
    y_buffer = 0

    HELLO_TEXT = "Welcome to Just Text!"
    rendered_text = FONT.render(HELLO_TEXT, 1, GREEN)
    y_buffer += rendered_text.get_height()

    WIN.blit(rendered_text, (y_buffer, y_buffer))

def main():
    run = True

    with open("memory.json", "r") as f:
        data = json.load(f)

    count = data["count"]

    while run:
        WIN.fill(BLACK)

        drawScreen1()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_3):
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    count += 1
                elif event.key == pygame.K_2:
                    count -= 1

        with open("memory.json", "w") as f:
            json.dump({"count": count}, f)
            
    pygame.quit()

if __name__ == '__main__':
    main()