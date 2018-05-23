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
    #ship.scale = SCALE
    path = [[25, HEIGHT], [WIDTH, 25], [SCALE*WIDTH-25, HEIGHT], [WIDTH, SCALE*HEIGHT-25]]


def game_loop():
    global ship, path

    angle = 0.0
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           # pylint: disable=E1101
                playing = False

        # Just spin around in a circle
        angle +=.1*c.get_time()
        angle %= 360

        # Constraing the display angles to 15 degree increments
        # This matches the display of sprites in the game
        display_angle = 15 * (int(angle)//15)

        # How far to move each frame?
        dist = .1

        # Figure out the distance we moved along each component of the vector
        x_part = math.cos(math.radians(angle)) * dist * c.get_time()
        y_part = -math.sin(math.radians(angle)) * dist * c.get_time()  # Because y-axis is flipped

        # Move the sprite towards the point
        ship.center_x += x_part
        ship.center_y += y_part

        # Rotate along the constrained angle
        ship.angle = display_angle-90  # Correction because default icon is rotated
        ship.scale = SCALE

        # Now we can draw everything...
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