import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode([500, 500])
pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(100, 100, 300, 100))
pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(100, 100, 300, 100), np.pi / 2, np.pi, 1)
while pygame.events.get() != "QUIT":
    pygame.display.flip()