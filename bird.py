import pygame
import random
from definitions import *
from nnet import Nnet
import numpy as np

class Bird():
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.set_position(BIRD_START_X,BIRD_START_Y)
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        # print("New bird")

    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

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

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        val = self.nnet.get_max_value(inputs)
        if val > JUMP_CHANCE:
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
            # print(self.time_lived)
        else:
            self.check_hits(pipes) 

    def assign_collision_fitness(self, p):
        gap_y = 0
        if p.pipe_type == PIPE_UPPER:
            gap_y = p.rect.bottom + VERTICAL_GAP / 2
        else:
            gap_y = p.rect.top - VERTICAL_GAP / 2

        self.fitness = -(abs(self.rect.centery - gap_y))

    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                self.assign_collision_fitness(p)
                # print(self.time_lived)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes)

    def get_inputs(self, pipes):
        closest = DISPLAY_W * 2 
        bottom_y = 0  

        for p in pipes:
            if p.pipe_type == PIPE_UPPER and p.rect.right < closest and p.rect.right > self.rect.left:
                closest = p.rect.right
                bottom_y = p.rect.bottom

        horizontal_distance = closest - self.rect.centerx
        vertical_distance = (self.rect.centery) - (bottom_y + VERTICAL_GAP / 2)

        inputs = [
            (horizontal_distance / closest),
            ((vertical_distance + Y_SHIFT)/ NORMALIZER)
        ]

        return inputs

    def create_offspring(p1, p2, gameDisplay):
        new_bird = Bird(gameDisplay)
        new_bird.nnet.create_mixed_weights(p1.nnet, p2.nnet)
        return new_bird

class BirdCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0,GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        for j in self.birds:
            j.update(dt, pipes)
            if j.state == BIRD_ALIVE:
                num_alive += 1
        return num_alive

    def evolve_population(self):
        for b in self.birds:
            b.fitness += b.time_lived * PIPE_SPEED
        self.birds.sort(key= lambda x: x.fitness, reverse= True)

        for bird in self.birds[0:10]:
            print('fitness', b.fitness)

        for bird in self.birds[2:-3]:
            bird.nnet.modify_weights()

        for bird in self.birds[-3:0]:
            bird.nnet.create_mixed_weights(self.birds[0].nnet, self.birds[1].nnet)

        self.create_new_generation()