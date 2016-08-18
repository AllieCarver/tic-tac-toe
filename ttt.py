import pygame
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((100,100))

pygame.display.flip()

while 1:
    for event in pygame.event.get():
        print event

