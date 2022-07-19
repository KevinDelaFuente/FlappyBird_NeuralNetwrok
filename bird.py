import pygame
import random
from definitions import *

class Bird():
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.set_position(BIRD_START_X,BIRD_START_Y)
        self.speed = 0
        self.time_lived = 0
        print("New bird")

    def set_position(self, x, y):
        self.rect.left =  x
        self.rect.top = y

    def move(self, dt):
        distance = 0 
        new_speed = 0

        distance = self.speed * dt + 0.5*(GRAVITY* dt**2)
        new_speed = self.speed + GRAVITY * dt

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self):
        self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
            print(self.time_lived)
        else:
            self.check_hits(pipes) 

    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                print(self.time_lived)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.draw()
            self.check_status(pipes)