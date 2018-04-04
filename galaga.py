'''
Galaga clone in Python
Using JFincher42's sprite library
'''
import pygame
import sprite
import random

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

WIDTH  = 240
HEIGHT = 336
SCALE  = 2
SECONDS_TO_CLEAR = 6000
STAR_SPEED = HEIGHT*2/SECONDS_TO_CLEAR

STARCOUNT = 100

def add_random_star(stars):
    xpos = 2*random.randint(1,WIDTH-1)            # Nothing on the edges
    ypos = 2*random.randint(HEIGHT-5, HEIGHT)     # Close to the bottom edge
    stars.append([xpos, ypos])

def setup():
    global window, c
    global stars

    pygame.init()
    window = pygame.display.set_mode([WIDTH*SCALE, HEIGHT*SCALE])
    window.fill(BLACK)
    c = pygame.time.Clock()

    stars = []

def animate_background():
    window.fill(BLACK)
    stars_to_remove = []
    for star_index in range(len(stars)):
        pygame.draw.circle(window, WHITE, stars[star_index],2)
        stars[star_index][1]-=int(STAR_SPEED*c.get_time())
        if stars[star_index][1]<0:
            stars_to_remove.append(stars[star_index])

    for star in stars_to_remove:
        stars.remove(star)

def game_loop():
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        # Add a star 20% of the time
        if random.randint(1,100) < 20:
            add_random_star(stars)

        # Animate the background
        animate_background()
        c.tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    setup()
    game_loop()