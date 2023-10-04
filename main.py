# Complete your game here
import pygame

pygame.init()
window = pygame.display.set_mode((1000, 640))

#representations of robot [y_vel,image] and ball [x_pos, y_pos, x_vel, y_vel, image] and CPU player [y_vel,image,moving state, grounded state (true = not jumping)]
robot = [0,pygame.image.load("robot.png")]
ball = [480,0,0,5,pygame.image.load("coin.png")]
ai = [0, pygame.image.load("robot.png"), False, True]
#gravity (9.8m/s^2)
gravity = .98
#goals tally
goals = {"PLAYER": 0, "CPU": 0}
#coordinates of robot
x = 0
y = 480-robot[1].get_height()
#coordinates of cpu
x_ai = 950
y_ai = 640 - ai[1].get_height()
#reset the ball at top of the screen
def ball_fall():
    ball[0] = 480
    ball[1] = 0
    ball[2] = 0
    ball[3] = 0

#check if a goal is scored
def goal_check():

    score_rect1 = pygame.Rect((990, 400, 10, 240))
    score_rect2 = pygame.Rect((10, 400, 10, 240))

    if ball_rect.colliderect(score_rect1):
        ball[0] = 420
        ball[1] = 0
        ball[2] = 0
        ball[3] = 0
        goals["PLAYER"] += 1

    elif ball_rect.colliderect(score_rect2):
        ball[0] = 420
        ball[1] = 0
        ball[2] = 0
        ball[3] = 0
        goals["CPU"] += 1

#check for winner
def winner():
    score = 0
    winner = ''
    for player in goals:
        if goals[player] > score:
            score = goals[player]
            winner = player
    return winner
#check for game over
def game_over():
    for player in goals:
        if goals[player] == 11:
            return True
#robot movement and game boundary conditions 
to_right = False
to_left = False
left_boundary = True
right_boundary = True

#font and title
game_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Mini Football")
#set game clock
pygame.time.set_timer(pygame.USEREVENT, 10)
clock = pygame.time.Clock()

while True:
    #draw goals
    window.fill((135, 206, 235))
    pygame.draw.rect(window,(124,252,0),(0,590,1000,640))
    pygame.draw.line(window,(255,255,255),(480,640),(470,590),5)
    pygame.draw.rect(window, (255, 255, 255), (950, 390, 1000, 640),5)
    pygame.draw.rect(window, (255, 255, 255), (0, 390, 50, 640),5)

    #prevent ball from going through top of goals
    goal1 = pygame.Rect((950, 390, 50, 10))
    goal2 = pygame.Rect((0, 390, 50, 10))
    robot_rect = pygame.Rect(x,y,robot[1].get_width(),robot[1].get_height())
    ball_rect = pygame.Rect(ball[0],ball[1],ball[4].get_width(),ball[4].get_height())
    ai_rect = pygame.Rect(x_ai,y_ai,ai[1].get_width(),ai[1].get_height())

    if ball_rect.colliderect(goal1) or ball_rect.colliderect(goal2):
        ball[3] += 3

    #check if goal is scored
    goal_check()

    #prevent robot from exiting screen
    if x >= 950:
        to_right = False
    if x + robot[1].get_width() <= 40:
        to_left = False    

    #prevent cpu from exiting screen
    if x_ai >= 950:
        ai[2] = False
    elif x_ai <= 40:
        ai[2] = False
    else:
        ai[2] = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #apply gravity to robot, cpu and ball every second
        if event.type == pygame.USEREVENT:
            if y >= 640-robot[1].get_height():
                 y = 640-robot[1].get_height()
                 robot[0] = 0
            else:
                robot[0] -= gravity
            if y_ai >= 640-ai[1].get_height():
                 y_ai = 640-ai[1].get_height()
                 ai[0] = 0
                 ai[3] = True
            else:
                ai[0] -= gravity
            if ball[1] >= 595:
                ball[3] = 0
            ball[3] -= .15
        #handle key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
                if x + robot[1].get_width() <= 40:
                    left_boundary = False
                else:
                    left_boundary = True
                
            if event.key == pygame.K_RIGHT:
                to_right = True
                if x - robot[1].get_width() >= 950:
                    right_boundary = False
                else:
                    right_boundary = True

            if event.key == pygame.K_SPACE:
                robot[0] = 20
                y -= 1

            #reset game
            if event.key == pygame.K_r:
                for player in goals:
                    goals[player] = 0
                ball[0] = 1500
                ball[1] = 0
                ball[2] = 0
                ball[3] = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False

        if x - robot[1].get_width() >= 950:
            to_right = False
        if x + robot[1].get_width() <= 0:
            to_left = False

        #check for collisions between ball and robot
        if robot_rect.colliderect(ball_rect):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball[3] += 3
            if y-12 <= ball[1] <= y+12:
                if x-12 <= ball[0] <= (x+robot[1].get_width()+12):
                    ball[3] += 3
            elif ball[0] <= x:
                ball[2] = -10
                ball[3] += 1
            elif ball[0] >= x:
                ball[2] = 10
                ball[3] += 1

        #check for collisions between ball and cpu
        if ai_rect.colliderect(ball_rect):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball[3] += 3
            if y_ai-12 <= ball[1] <= y_ai+12:
                if x_ai-12 <= ball[0] <= (x_ai+ai[1].get_width()+12):
                    ball[3] += 3
            elif ball[0] <= x_ai:
                ball[2] = -10
                ball[3] += 1
            elif ball[0] >= x_ai:
                ball[2] = 10
                ball[3] += 1
            
        #cpu logic
        if ai[2]:
            if ball[0] - x_ai >= 0:
                #adaptive difficulty
                if goals["CPU"] < goals["PLAYER"]:
                    x_ai += 5
                else:
                    x_ai += 3
            elif ball[0] - x_ai < 0:
                if goals["CPU"] < goals["PLAYER"]:
                    x_ai -= 5
                else:
                    x_ai -= 3

            
            if ball[1] >= 200 and abs(ball[0] - x_ai) < 100 and ai[3]:
                if goals["CPU"] < goals["PLAYER"]:
                    ai[0] = 20
                else:
                    ai[0] = 18
                y_ai -= 1
                ai[3] = False
        #prevent ai from moving off screen
        if x_ai >= 950:
            ai[2] = False
            x_ai -= 5
        elif x_ai + ai[1].get_width() <= 40:
            ai[2] = False
            x_ai += 5
        else:
            ai[2] = True

    #check if ball hits wall
        ball[0] += ball[2]
        if ball[0] <= 0:
            ball[0] = 1
            ball[2] = -ball[2]
        elif ball[0] >= 970:
            ball[0] = 969
            ball[2] = -ball[2]

        ball[2] *= .996
    #check if robot is on floor (stop from falling through floor)     
        if y >= 640-robot[1].get_height():
            robot[0] = 0
        else:
            y -= robot[0]
    #check if cpu is on floor (stop from falling through floor)  
        if y_ai >= 640-ai[1].get_height():
            ai[0] = 0
        else:
            y_ai -= ai[0]
        #move robot
        if to_right and right_boundary:
            x += 5
        if to_left and left_boundary:
            x -= 5
        #bounce ball
        if ball[1] >= 595:
            ball[3] += 7
        ball[1] -= ball[3]
    #draw robot
    window.blit(robot[1], (x, y))
    #draw cpu
    window.blit(ai[1],(x_ai,y_ai))
    #draw ball
    window.blit(ball[4], (ball[0], ball[1]))
    #display controls
    controls = game_font.render(f"Controls:  Move Left and Right with arrow keys  Jump - Space  Reset - R  First to 11 goals wins!", True, (255, 0, 0))
    window.blit(controls,(100,150))
    #display score
    player = game_font.render(f"PLAYER: {goals['PLAYER']}", True, (255, 0, 0))
    cpu = game_font.render(f"CPU: {goals['CPU']}", True, (255, 0, 0))
    window.blit(player, (420, 40))
    window.blit(cpu, (420, 80))
    #check for game over
    if game_over():
        ball[0] = 1500
        ball[1] = 0
        ball[2] = 0
        ball[3] = 0
        game_winner = winner()
        victory_text = game_font.render(f"{game_winner} WINS!", True, (255, 0, 0))
        window.blit(victory_text, (420, 320))

    pygame.display.flip()

    clock.tick(60)