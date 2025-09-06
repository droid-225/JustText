import json
import pygame
pygame.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Text")

FPS = 60 # might not need

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("comicsans", 20)

def draw(win, count, texts):
    y_buffer = 0

    count_text = FONT.render(f"Count: {count}", 1, WHITE)
    y_buffer += count_text.get_height()
    win.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, y_buffer - 10))

    for text in texts:
        text_text = FONT.render(f"{text}", 1, WHITE)
        y_buffer += text_text.get_height()

        win.blit(text_text, (WIDTH // 2 - 80, y_buffer))

def main():
    run = True
    #clock = pygame.time.Clock()

    with open("memory.json", "r") as f:
        data = json.load(f)

    count = data["count"]

    texts = ("(1) Count Up",
            "(2) Count Down",
            "(3) Quit")

    while run:
        WIN.fill(BLACK)
        #clock.tick(FPS)

        draw(WIN, count, texts)
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