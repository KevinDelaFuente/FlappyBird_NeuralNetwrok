import pygame
from definitions import *
from pipe import PipeCollection
from bird import BirdCollection

def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS:', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time:', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration:', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive:', font, x_pos, y_pos + gap, gameDisplay)

def run_game():
    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
    pygame.display.set_caption("Learn to Fly")

    running = True
    bgImg = pygame.image.load(BG_FILENAME)
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)
    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    birds = BirdCollection(gameDisplay)

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    num_iterations = 1

    while running:
        dt = clock.tick(FPS)
        game_time += dt

        gameDisplay.blit(bgImg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                #uncomment to actually play and define a bird object
                #if event.key == pygame.K_SPACE:
                #    robin.jump()
                #else:
                running = False

        pipes.update(dt)
        num_alive = birds.update(dt, pipes.pipes)

        if num_alive == 0 or game_time >= 16000:
            pipes.create_new_set()
            game_time = 0
            birds.evolve_population()
            num_iterations += 1


        update_data_labels(gameDisplay, dt, game_time, num_iterations,num_alive, label_font)
        pygame.display.update()

if __name__ == "__main__":
    run_game()