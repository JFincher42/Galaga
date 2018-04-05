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
    xpos = 2*random.randint(1,WIDTH-1)              # Nothing on the edges
    ypos = 2*random.randint(HEIGHT-5, HEIGHT)       # Close to the bottom edge
    stars.append([xpos, ypos])

def setup():
    global window, c
    global stars

    global ship
    global path

    pygame.init()                                   # pylint: disable=E1101
    window = pygame.display.set_mode([WIDTH*SCALE, HEIGHT*SCALE])
    window.fill(BLACK)
    c = pygame.time.Clock()

    stars = []

    ship = sprite.Sprite("Galaga ship.png", WIDTH, HEIGHT*2-50)
    path = [[WIDTH, HEIGHT*2-50], [WIDTH*2-50, HEIGHT], [50, HEIGHT], [WIDTH, 50]]

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

def move_sprite_on_path(sprite, path, speed):
    '''
    Moves a sprite along a path defined by a set of points
    Figures out where the sprite is and moves it smoothly between points
    '''

    # The next point in the path to which we are traveling
    # Keep traveling until we get there
    next_point = 1
    while next_point <= len(path):

        # Get the X and Y of that point
        # This loop travels the path until we get to that point
        next_x = path[next_point][0]
        next_y = path[next_point][1]
        while (sprite.center_x != path[next_point][0]) and (sprite.center_y != path[next_point][1]):
            sprite.angle = math.degrees(math.atan)

def game_loop():
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           # pylint: disable=E1101
                playing = False

        # Add a star 20% of the time
        #if random.randint(1,100) < 20:
        #    add_random_star(stars)

        # Animate the background
        #animate_background()
        c.tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    setup()
    game_loop()