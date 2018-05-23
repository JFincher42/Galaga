'''
Galaga clone in Python
Using JFincher42's sprite library
'''
import pygame
import sprite
import random
import os

# Color constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# Width and height of the window
WIDTH  = 240
HEIGHT = 336

# Scaling factor to make it look better
SCALE  = 2

# How long should it take a star to get from the top to the bottom?
SECONDS_TO_CLEAR = 6000
STAR_SPEED = HEIGHT*SCALE/SECONDS_TO_CLEAR

# How many stars to have on screen at one time?
STARCOUNT = 100

## Global variable
global window, c
global stars
global ship
global path

def add_random_star(stars):
    """
    Adds a new star at a random location close to the bottom of the field

    :param stars: the current list of stars
    """
    xpos = 2*random.randint(1,WIDTH-1)              # Nothing on the edges
    ypos = 2*random.randint(1, 5)                   # Close to the top edge
    stars.append([xpos, ypos])

def setup():
    """
    Setup pygame and the global vars we need
    """
    # The window to draw on and a clock to steer her by
    global window, c
    # The list of background stars
    global stars

    # The ship sprite
    global ship

    # A list of visible enemies
    global enemies

    # The path the enemies follow
    global path

    # Initialize the main window and clock
    pygame.init()                                   # pylint: disable=E1101
    window = pygame.display.set_mode([WIDTH*SCALE, HEIGHT*SCALE])
    window.fill(BLACK)
    c = pygame.time.Clock()

    # The list of stars in teh background
    stars = []

    # The ship sprite
    ship = sprite.Sprite(os.path.join("images","Galaga ship.png"), WIDTH, HEIGHT*2-50)
    ship.scale = SCALE
    path = [[WIDTH, HEIGHT*2-50], [WIDTH*2-50, HEIGHT], [50, HEIGHT], [WIDTH, 50]]

    # List of enemies
    enemies = []

def animate_background():
    '''
    Keep the background stars moving up
    '''
    global stars
    window.fill(BLACK)

    # Which stars should we remove?
    stars_to_remove = []
    for star_index in range(len(stars)):
        # Draw the current star
        pygame.draw.circle(window, WHITE, stars[star_index],random.randint(1,2))
        # Figure out the new position
        stars[star_index][1]+=int(STAR_SPEED*c.get_time())

        # If the new position, is off the screen, mark it for removal
        if stars[star_index][1]>HEIGHT*SCALE:
            stars_to_remove.append(stars[star_index])

    # Remove all the marked stars
    for star in stars_to_remove:
        stars.remove(star)

def move_sprite_on_path(sprite, path, speed):
    '''
    Moves a sprite along a path defined by a set of points
    Figures out where the sprite is and moves it smoothly between points

    :param sprite The sprite we are moving
    :param path A list of points defining the points to follow
    :param speed How fast to move
    :return The remaining points on the path
    '''
    # First, set a threshold so we don't need to hit the point directly
    threshold = 10
    
    # We are always moving towards the first point in the path
    # When we get there, we remove that point in the array so we can move to the next point
    next_point = 0

    # Check to see if the sprite is there already
    are_we_there_yet = sprite_within(sprite, path[next_point], threshold)
    while next_point <= len(path):

        # Get the X and Y of that point
        # This loop travels the path until we get to that point
        next_x = path[next_point][0]
        next_y = path[next_point][1]
        if (sprite.center_x != path[next_point][0]) and (sprite.center_y != path[next_point][1]):
            x_dist = next_x - sprite.center_x
            y_dist = next_y - sprite.center_y
            new_angle = math.degrees(math.atan(y_dist/x_dist))
            # Add calculation is turn more slowly
            sprite.angle = new_angle

def game_loop():
    global ship, stars, enemies

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           # pylint: disable=E1101
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Need code to fire a missile
                    pass

        # Check for movement keypress

        # Add a star 20% of the time
        if random.randint(1,100) < 20:
            add_random_star(stars)
        
        # Animate the background
        animate_background()

        # Display the ship
        ship.draw()

        # Display the enemies
        #draw_enemies(enemies)

        # Set the timer and flip the display
        c.tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    print("Welcome to Galaga!")
    setup()
    game_loop()