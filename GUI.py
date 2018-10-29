import pygame

class SnakeGUI():
    def __init__(self, dim=(500,500)):
        self.window = pygame.display.set_mode(dim)
        pygame.display.set_caption('Super AI Snake')
        self.fps = pygame.time.Clock()

    def update(self, snakeBody, food, score):
        self.window.fill(pygame.Color(0, 0, 0))

        # draw snake
        for pos in snakeBody:
            pygame.draw.rect(self.window, pygame.Color(0, 225, 0), pygame.Rect(pos[0], pos[1], 10, 10))

        # draw food
        pygame.draw.rect(self.window, pygame.Color(225, 0, 0), pygame.Rect(food[0], food[1], 10, 10))

        pygame.display.set_caption('Super AI Snake | Score: ' + str(score))
        pygame.display.flip()

        # increas pace with scpore
        self.fps.tick(int((10000 + score) / 1000))