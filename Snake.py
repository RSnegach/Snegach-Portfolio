import pygame
from random import randint
# initialize game parameters (window, font, title, clock)
pygame.init()
window = pygame.display.set_mode((640,640))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Mini Football")

# the node class - the snake is made up of individual, doubly linked Node segments
class Node():
    def __init__(self, x_pos: int, y_pos:int, direction: str, prev, next):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.next = next
        self.prev = prev
        self.direction = direction

# the coin class representing coins which the snake must collect to grow
class Coin():

    def __init__(self, x_pos: int, y_pos:int, collected: bool):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.collected = collected

# head node of snake
head = Node(0,600,"right", None, None)

#returns the current tail of the snake
def tail(node):
    if node.prev == None:
        return node
    else:
        tail(node.prev)
# add a Node at the tail when a dot is eaten
def add_tail(node):
    if node.prev == None:
        if node.direction == "left":
            node.prev = Node(node.x_pos + 40, node.y_pos, node.direction, None, node)
        elif node.direction == "right":
            node.prev = Node(node.x_pos - 40, node.y_pos, node.direction, None, node)
        elif node.direction == "up":
            node.prev = Node(node.x_pos, node.y_pos + 40, node.direction, None, node)
        elif node.direction == "down":
            node.prev = Node(node.x_pos, node.y_pos - 40, node.direction, None, node)
    else:
        add_tail(node.prev)
# add a node at the head of the current snake
def add_head(node):
    global head
    if node.direction == "left":
        node.next = Node(node.x_pos - 40, node.y_pos, node.direction, head, None)
        head = node.next
    elif node.direction == "right":
        node.next = Node(node.x_pos + 40, node.y_pos, node.direction, head, None)
        head = node.next
    elif node.direction == "up":
        node.next = Node(node.x_pos, node.y_pos - 40, node.direction, head, None)
        head = node.next
    elif node.direction == "down":
        node.next = Node(node.x_pos, node.y_pos + 40, node.direction, head, None)
        head = node.next
#remove tail from body of current snake
def remove_tail(node):
    if node.prev == None:
        node.next.prev = None
        node = None
    else:
        remove_tail(node.prev)

# repetitive logic for move function abstracted (ONLY MOVES SINGLE HEAD NODE - snake's body moves by removing tail and adding at head)
def move_helper(node):
    if node.direction == "left":
        node.x_pos -= 40
    elif node.direction == "right":
        node.x_pos += 40
    elif node.direction == "up":
        node.y_pos -= 40
    elif node.direction == "down":
        node.y_pos += 40

# move snake by removing tail and adding a new head in front of current head
def move(node):
    # if single head node, only move it
    if node.prev == None and node.next == None:
        move_helper(node)
        return
    # else place the tail ahead of the head and make it the new head
    else:
        add_head(node)
        remove_tail(node)
# draw the snake's body (always called on head)
def draw_snake(node):
    if node.prev == None:
        window.blit(snakepiece,(node.x_pos, node.y_pos))
        return
    window.blit(snakepiece,(node.x_pos, node.y_pos))
    draw_snake(node.prev)
# check if snake collides with self or walls
def collision_check(node):
    global head
    if node == None:
        return
    elif node == head:
        if (head.y_pos > 640 or head.y_pos < 0) or (head.x_pos > 640 or head.x_pos < 0):
            fps = 0
            lose_message = game_font.render(f"Game Over! You Lose!", True, (255, 0, 0))
            window.blit(lose_message,(240,150))
        else:
            collision_check(node.prev)
    elif node.prev == None and node.next != None:
        if (head.x_pos == node.x_pos) and (head.y_pos == node.y_pos):
            fps = 0
            lose_message = game_font.render(f"Game Over! You Win!", True, (255, 0, 0))
            window.blit(lose_message,(240,150))
        else:
            return
    else:
        if (head.x_pos == node.x_pos) and (head.y_pos == node.y_pos):
            fps = 0
            lose_message = game_font.render(f"Game Over! You Win!", True, (255, 0, 0))
            window.blit(lose_message,(240,150))
        else:
            collision_check(node.prev)
# get the acceptable coordinate locations to spawn a coin (i.e, where snake is not)
def get_coords(node):
    if node.prev == None:
        ref_coords.append([node.x_pos, node.y_pos])
        return
    else:
        ref_coords.append([node.x_pos, node.y_pos])
        get_coords(node.prev)
        
# list of coordinates where coin can spawn
coords = []
#list of coords where snake is occupying
ref_coords = []

for x in range(0,640,40):
    for y in range(0,640,40):
        coords.append([x,y])
print(coords)

# representation of coin which snake must collect
coin = Coin(600,600, False)
# spawn a coin in random location
def spawn_coin():
    global coords
    global ref_coords
    global coin

    #coordinates not permitted if snake is occupying them
    permitted_coords = list(filter(lambda x: x not in ref_coords, coords))
    rand_index = randint(0, len(permitted_coords))
    rand_coords = permitted_coords[rand_index]

    coin.x_pos = rand_coords[0]
    coin.y_pos = rand_coords[1]
    
# draw coin at random coordinates
def draw_coin():
    global coin
    window.blit(coin_image,(coin.x_pos, coin.y_pos))
# check if coin collected - if yes remove and spawn new
def collect_check():
    global game_score
    if head.x_pos == coin.x_pos and head.y_pos == coin.y_pos:
        coin.collected = True
        add_tail(head)
        game_score += 1
    if game_score == 256:
        fps = 0
        win_message = game_font.render(f"Game Over! You Win!", True, (255, 0, 0))
        window.blit(win_message,(240,150))

#render image of a Node and a coin
snakepiece = pygame.image.load("snake-piece.png")
coin_image = pygame.image.load("coin.png")
#game fps (3 by default, 6 when player presses space to speed up)
fps = 3
#set game score as 0
game_score = 0
# set game font
game_font = pygame.font.SysFont("Arial", 24)
pygame.display.set_caption("Snake")

# game execution loop
while True:
    # event handlers
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                #prevent snake from moving into itself
                if head.direction == "right":
                    continue
                else:
                    head.direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                #prevent snake from moving into itself
                if head.direction == "left":
                    continue
                head.direction = "right"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                #prevent snake from moving into itself
                if head.direction == "down":
                    continue
                head.direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                #prevent snake from moving into itself
                if head.direction == "up":
                    continue
                head.direction = "down"
            if event.key == pygame.K_SPACE:
                fps = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fps = 3
    # move snake
    move(head)
    # check if snake collided - end game if yes
    collision_check(head)
    # check if snake collected coin - grow snake and respawn coin if yes
    collect_check()
    # check new acceptable coords for coin spawn
    get_coords(head)
    #draw coin at coordinates
    if coin.collected == True:
        spawn_coin()
        coin.collected = False
    draw_coin()
    # draw snake
    draw_snake(head)
    
    pygame.display.flip()
    # game FPS
    clock.tick(fps)
