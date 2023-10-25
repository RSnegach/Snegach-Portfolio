import pygame

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
            exit()
        else:
            collision_check(node.prev)
    elif node.prev == None and node.next != None:
        if (head.x_pos == node.x_pos) and (head.y_pos == node.y_pos):
            exit()
        else:
            return
    else:
        if (head.x_pos == node.x_pos) and (head.y_pos == node.y_pos):
            exit()
        else:
            collision_check(node.prev)
#generate a coin in a random location
#render image of a Node and a coin
snakepiece = pygame.image.load("snake-piece.png")
coin = pygame.image.load("coin.png")

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
                add_tail(head)
    move(head)
    draw_snake(head)
    collision_check(head)
    pygame.display.flip()
    # game FPS
    clock.tick(3)
