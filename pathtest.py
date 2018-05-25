'''
Galaga clone in Python
Using JFincher42's sprite library
'''
import pygame
import sprite
import random
import os
import math
from vectors import Point, Vector

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

    # Initial velocity is to the left
    ship.velocity = Vector(-1,0)

    # List of way points
    path = [Vector(25, HEIGHT), Vector(WIDTH, 25), Vector(SCALE*WIDTH-25, HEIGHT), Vector(WIDTH, SCALE*HEIGHT-25)]

def sprite_within(sprite, point, threshold):
    """
    Determines if a sprite is within a certain threshold of a point

    :param sprite The sprite to check
    :param point The point we are trying to hit. Assumes a list.
    :param threshold How close do we need to get to be there
    :return True if we are within threshold pixels of the point, False otherwise
    """
    x_dist = point.x - sprite.center_x
    y_dist = point.y - sprite.center_y
    dist = math.sqrt(x_dist*x_dist + y_dist*y_dist)
    return dist <= threshold

def game_loop():
    global ship, path

    playing = True
    next_point = 0
    zero_degrees = Vector(1,0)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           # pylint: disable=E1101
                playing = False

        # Follow the path

        # First, set a threshold so we don't need to hit the point directly
        threshold = 20
    
        # We are always moving towards the first point in the path
        # When we get there, we remove that point in the array so we can move to the next point
        #next_point = 0

        # Check to see if the sprite is there already
        if sprite_within(ship, path[next_point], threshold):
            next_point+=1
            if next_point >= len(path):
                next_point = 0

        # Figure out our new direction vector
        desired_velocity = Vector.from_list(ship.center) - path[next_point]
        desired_velocity = desired_velocity.unit().multiply(0.1 * c.get_time())
        steering_force = Vector.multiply(ship.velocity - desired_velocity, 0.1)
        ship.velocity += steering_force
        if ship.velocity.magnitude() > 5:
            ship.velocity = ship.velocity.unit().multiply(5)

        #ship.direction = Vector.from_points(Point.from_list(ship.center), path[next_point]).unit()
        #new_direction = ship.direction.multiply(ship.speed*c.get_time())
        ship.center_x += ship.velocity.x
        ship.center_y += ship.velocity.y
        new_angle = ship.velocity.angle(zero_degrees)
        if ship.velocity.y < 0:
            new_angle *= -1
        ship.angle = (new_angle+270)%360

        # Move the sprite towards the point
        ship.scale = SCALE

        #ship.center = (sprite_x, sprite_y)

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