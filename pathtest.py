'''
Galaga clone in Python
Using JFincher42's sprite library
'''
import pygame
import sprite
import random
import os
import math

# Color constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

# Width and height of the window
WIDTH  = 240
HEIGHT = 336

# Scaling factor to make it look better
SCALE  = 2

# How long should it take a star to get from the top to the bottom?
SECONDS_TO_CLEAR = 6000
STAR_SPEED = HEIGHT*SCALE/SECONDS_TO_CLEAR

## Global variable
global window, c
global ship
global path

def setup():
    """
    Setup pygame and the global vars we need
    """
    # The window to draw on and a clock to steer her by
    global window, c
    # The ship sprite
    global ship

    # The path the enemies follow
    global path

    # Initialize the main window and clock
    pygame.init()                                   # pylint: disable=E1101
    window = pygame.display.set_mode([WIDTH*SCALE, HEIGHT*SCALE])
    window.fill(BLACK)
    c = pygame.time.Clock()

    # The ship sprite
    ship = sprite.Sprite(os.path.join("images","Galaga ship.png"), WIDTH+50, HEIGHT-100)
    ship.scale = SCALE
    path = [[25, HEIGHT], [WIDTH, 25], [SCALE*WIDTH-25, HEIGHT], [WIDTH, SCALE*HEIGHT-25]]

def sprite_within(sprite, point, threshold):
    """
    Determines if a sprite is within a certain threshold of a point

    :param sprite The sprite to check
    :param point The point we are trying to hit. Assumes a list.
    :param threshold How close do we need to get to be there
    :return True if we are within threshold pixels of the point, False otherwise
    """
    x_dist = point[0] - sprite.center_x
    y_dist = point[1] - sprite.center_y
    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist)
    return dist <= threshold

def quadrant(x,y):
    """
    Figures out the quadrant based on the x and y difference

    :param x The x difference
    :param y The y difference
    :returns A tuple with multipliers
    """
    return (abs(x)/x, abs(y)/y)

def game_loop():
    global ship, path

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           # pylint: disable=E1101
                playing = False

        # Follow the path

        # First, set a threshold so we don't need to hit the point directly
        threshold = 10
    
        # We are always moving towards the first point in the path
        # When we get there, we remove that point in the array so we can move to the next point
        next_point = 0

        # Check to see if the sprite is there already
        if sprite_within(ship, path[next_point], threshold):
            next_point+=1
            if next_point >= len(path):
                next_point = 0

        # Get the X and Y of the next point and the sprite
        next_x, next_y = path[next_point]
        sprite_x, sprite_y = ship.center
        angle=0
        if (next_x - sprite_x) == 0:
            angle = math.pi
            y_part = math.sin(angle) * .1 * c.get_time()
        else:
            angle = math.atan((next_y - sprite_y)/(next_x - sprite_x))
            x_mult, y_mult = quadrant(next_x - sprite_x, next_y - sprite_y)
            x_part = x_mult * math.cos(angle) * .1 * c.get_time()
            y_part = y_mult * math.sin(angle) * .1 * c.get_time()

        # Move the sprite towards the point
        sprite_x += x_part
        sprite_y += y_part
        ship.scale = SCALE

        ship.center = (sprite_x, sprite_y)

        window.fill(BLACK)

        # Display the ship
        ship.draw()

        # Set the timer and flip the display
        c.tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    print("Welcome to Galaga!")
    setup()
    game_loop()