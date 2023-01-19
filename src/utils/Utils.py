import pygame
import os

pygame.font.init()

WIDTH = 500
HEIGHT = 800

GEN = 0
ALIVE = 0

IMAGINE_PERISOARA = pygame.transform.scale2x(pygame.image.load(os.path.join('imagini', 'perisoare.png')))
IMAGINE_SABIE = pygame.transform.scale2x(pygame.image.load(os.path.join('imagini', 'sabie.png')))
IMAGINE_FUNDAL = pygame.transform.scale2x(pygame.image.load(os.path.join('imagini', 'bucatarie.png')))

STAT_FONT = pygame.font.SysFont('Roboto', 50)
