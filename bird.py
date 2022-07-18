import pygame
import random
from definitions import *

class Bird():
    def __init__(self, gameDisplay, x, y):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.set_position(x,y)
        print("Bird Moving")

    def set_position(self, x, y):
        self.rect.left =  x
        self.rect.top = y

    def move_position(self, dx,dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0:
            self.state = BIRD_DEAD
            print("Bird Dead")

    def update(self, dt):
        if self.state == BIRD_ALIVE:
            self.move_position(0, GRAVITY*dt)
            self.draw()
            self.check_status()