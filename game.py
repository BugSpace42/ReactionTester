import pygame
import random
import time

def reaction_test():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    results = []

    for test_num in range(3):
        print(f"\nТест {test_num + 1}")

        # 1. Красный экран - ждем
        screen.fill((255, 0, 0))
        pygame.display.flip()

        # Случайная пауза
        wait_time = random.uniform(1, 2)
        time.sleep(wait_time)

        # 2. Зеленый экран - нажимаем
        screen.fill((0, 255, 0))
        pygame.display.flip()

        start_time = time.time()
        reacted = False

        # Ждем нажатия мыши
        while not reacted:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    reaction_time = (time.time() - start_time) * 1000  # мс
                    results.append(reaction_time)
                    print(f"  Время реакции: {reaction_time:.0f} мс")
                    reacted = True
                    break

            clock.tick(60)
        time.sleep(0.5)
    pygame.quit()
    return results