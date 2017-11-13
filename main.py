import sprites
import pygame
from genetic import *
from nn import *
from random import random

# Constants #

SCALAR = 3                  # The scaling factor applied to all images during initialization.
GRAVITY = 1 * SCALAR      # The gravitational force applied to the birds on each update.

VERTICAL_MOVEMENT = 1.33 * SCALAR
HORIZONTAL_MOVEMENT = .33 * SCALAR

SPACING = 75 * SCALAR       # The spacing between any two subsequent pipes.

def convert (image):
    """
    Converts a PIL Image object into a PyGame Surface object.
    """
    
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

background = convert(sprites.background(SCALAR))
upper_pipe = convert(sprites.upper_pipe(SCALAR))
lower_pipe = convert(sprites.lower_pipe(SCALAR))
foreground = convert(sprites.foreground(SCALAR))
bird = convert(sprites.bird(SCALAR))

pygame.init()

width, height = (143*SCALAR,256*SCALAR)
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#####################################################

distance = 0

population = 10
birds = [(width * .10, height * .50 - bird.get_height() / 2)] * population

weights_ih, weights_ho = initialize(population)
scores = [None] * population

pipes = []

def draw ():
    """
    
    """

    display.blit(background, (0,0))

    for (x, yu, yl) in pipes:
        display.blit(upper_pipe, (x,yu - upper_pipe.get_height()))
        display.blit(lower_pipe, (x,yl))

    display.blit(foreground, (-(distance % width) + foreground.get_width(), height - foreground.get_height()))
    display.blit(foreground, (-(distance % width), height - foreground.get_height()))

    for i, (x,y) in enumerate(birds):
        if not scores[i]:
            display.blit(bird, (x,y))

def update ():
    """
    
    """
    
    global weights_ih, weights_ho, population, scores, distance, birds, pipes

    if not None in scores:
        
        train(population, (weights_ih, weights_ho), numpy.array(scores))
        
        distance = 0

        population = 10
        birds = [(width * .10, height * .50 - bird.get_height() / 2)] * population
        pipes = []
        
        weights_ih, weights_ho = initialize(population)
        scores = [None] * population
        
        return

    distance += 1
    
    if len(pipes) == 0:
        spawn_pipe(SPACING)
    elif len(pipes) < 3:
        (x,_,_) = pipes[-1]
        spawn_pipe(x + SPACING)
    
    def intersects (bird_rect, pipe_rect):
        
        (l1, r1, t1, b1) = bird_rect
        (l2, r2, t2, b2) = pipe_rect
    
        horizontally = (r1 >= l2 and r1 <= r2) or (l1 <= r2 and l1 >= l2)
        vertically = (t1 <= b2 and t1 >= t2) or (b1 >= t2 and b1 <= b2)
    
        return (horizontally and vertically)
    
    inputs = []
    
    for px, pyu, pyl in pipes:
                
        if birds[0][0] < px + upper_pipe.get_width():

            for i, (bx,by) in enumerate(birds):
                
                if scores[i]:
                    inputs.append([0,0])
                    continue
                    
                bird_rect = (bx, bx + bird.get_width(), by, by + bird.get_height())
                
                if (by + bird.get_height() >= height - foreground.get_height()):
                    scores[i] = distance
                    inputs.append([0,0])
                    continue
    
                pipe_rect = (px, px + upper_pipe.get_width(), pyu - upper_pipe.get_height(), pyu)
                    
                if intersects(bird_rect, pipe_rect):
                    scores[i] = distance
                    inputs.append([0,0])
                    continue
                
                pipe_rect = (px, px + lower_pipe.get_width(), pyl, pyl + lower_pipe.get_height())
        
                if intersects(bird_rect, pipe_rect):
                    scores[i] = distance
                    inputs.append([0,0])
                    continue
                
                inputs.append([px - bx, pyu - by])
                        
            break
    
    for p in range(population):

        output = query(inputs[p], weights_ih[p], weights_ho[p])

        if output == 1:
            (x,y) = birds[p]
            birds[p] = (x,y+VERTICAL_MOVEMENT)
    
    birds = [(x,y - GRAVITY) for (x,y) in birds]
    pipes = [(x-HORIZONTAL_MOVEMENT,yu,yl) for (x,yu,yl) in pipes if x + upper_pipe.get_width() > 1]

def spawn_pipe (x):
    """
    
    """

    gap = .2
    
    h = height - foreground.get_height()

    r = 0
    while not (r >= 0.20 and r <= 0.80):
        r = random()
    
    if r <= .5:
        pipes.append((x, h * r,  h * (r + gap)))
    else:
        pipes.append((x, h * (r - gap), h * r))

crashed = False
while not crashed:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    update()
    draw()
    
    pygame.display.update()
    
    clock.tick(60)

pygame.quit()
quit()