# WRITE YOUR SOLUTION HERE:
from random import randint
import pygame

pygame.init()
window = pygame.display.set_mode((640, 480))

robot = pygame.image.load("robot.png")
asteroid = pygame.image.load("rock.png")
x = 0
y = 480-robot.get_height()

asteroids = []

def new_asteroid():
    chance = randint(0,1000)
    rand_x = randint(120,520)
    if chance >= 994:
        asteroids.append([rand_x, 0,True])

def move_asteroids():
    for asteroid in asteroids:
        asteroid[1] += 1

def game_over():
    for i in asteroids:
        if i[2] == True and i[1] + asteroid.get_height() > 480:
            return True

def collect_check():
    for asteroid in asteroids:
        if (x - 5 <= asteroid[0] <= x + 5 + robot.get_width()) and (y - 35 <= asteroid[1]):
            asteroid[2] = False

def score_check():
    score = 0
    for asteroid in asteroids:
        if asteroid[2] == False:
            score += 1
    return score
to_right = False
to_left = False
left_boundary = True
right_boundary = True
up_boundary = True
down_boundary = True
game_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

while True:
    if y + robot.get_height() >= 480:
        down = False
    if y - robot.get_height() <= -82:
        up = False
    if x - robot.get_width() >= 540:
        to_right = False
    if x + robot.get_width() <= 40:
        to_left = False    

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

    if to_right and right_boundary:
        x += 4
    if to_left and left_boundary:
        x -= 4

    window.fill((0, 0, 0))
    window.blit(robot, (x, y))
    collect_check()
    move_asteroids()
    new_asteroid()
    for i in asteroids:
        if i[2]:
            window.blit(asteroid, (i[0], i[1]))
    
    text = game_font.render(f"Score: {score_check()}", True, (255, 0, 0))
    window.blit(text, (540, 40))
    if game_over():
        exit()

    pygame.display.flip()

    clock.tick(60)