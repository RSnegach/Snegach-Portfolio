from random import randint
import pygame

# initialize pygame
pygame.init()
window = pygame.display.set_mode((640, 480))

# define rendered images
robot = pygame.image.load("robot.png")
asteroid = pygame.image.load("rock.png")

# robot's starting coords
x = 0
y = 480-robot.get_height()

#initialize empty list of asteroids
asteroids = []

# create a new asteroid and add to asteroids
def new_asteroid():
    chance = randint(0,1000)
    rand_x = randint(120,520)
    if chance >= 994:
        asteroids.append([rand_x, 0,True]) # spawn asteroid at random x-position, at top of screen, with uncollected status True

# increment y-position of all asteroids by 1
def move_asteroids():
    for asteroid in asteroids:
        asteroid[1] += 1

# check if any asteroids touching ground, if yes then game over
def game_over():
    for i in asteroids:
        if i[2] == True and i[1] + asteroid.get_height() > 480:
            return True

# check if robot's hitbox overlaps with asteroid, if so remove asteroid from screen and increase score by one
def collect_check():
    for asteroid in asteroids:
        if (x - 5 <= asteroid[0] <= x + 5 + robot.get_width()) and (y - 35 <= asteroid[1]):
            asteroid[2] = False
# for all asteroids with uncollected status False, add 1 to player score
def score_check():
    score = 0
    for asteroid in asteroids:
        if asteroid[2] == False:
            score += 1
    return score

# direction checking variables
to_right = False
to_left = False
left_boundary = True
right_boundary = True

# variables to check if robot is touching sides of the screen
up_boundary = True
down_boundary = True

# game font, title and clock
game_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# execution loop
while True:
    # stop robot when it hits edges of screen
    if y + robot.get_height() >= 480:
        down = False
    if y - robot.get_height() <= -82:
        up = False
    if x - robot.get_width() >= 540:
        to_right = False
    if x + robot.get_width() <= 40:
        to_left = False    

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
                if x + robot.get_width() <= 40:
                    left_boundary = False
                else:
                    left_boundary = True
                
            if event.key == pygame.K_RIGHT:
                to_right = True
                if x - robot.get_width() >= 600:
                    right_boundary = False
                else:
                    right_boundary = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False

        if x - robot.get_width() >= 540:
            to_right = False
        if x + robot.get_width() <= 0:
            to_left = False

        if event.type == pygame.QUIT:
            exit()

    # if right/left keys pressed and robot not at edge, move accordingly
    if to_right and right_boundary:
        x += 4
    if to_left and left_boundary:
        x -= 4

    # draw world, then run all functions to update world
    window.fill((0, 0, 0))
    window.blit(robot, (x, y))
    collect_check()
    move_asteroids()
    new_asteroid()
    # draw all asteroids at new positions
    for i in asteroids:
        if i[2]:
            window.blit(asteroid, (i[0], i[1]))
    
    text = game_font.render(f"Score: {score_check()}", True, (255, 0, 0))
    window.blit(text, (540, 40))
    if game_over():
        exit()

    pygame.display.flip()

    clock.tick(60)
