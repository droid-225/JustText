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

    count = 0

    texts = ("(1) Count Up",
            "(2) Count Down",
            "(3) Quit")

    while run:
        WIN.fill(BLACK)
        #clock.tick(FPS)

        draw(WIN, count, texts)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
    pygame.quit()

if __name__ == '__main__':
    main()