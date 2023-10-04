import pygame
import math
from datetime import datetime


pygame.init()
window = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
#system time
    now = datetime.now()
    # putting hours, minutes, seconds into own object
    time = [now.hour,now.minute,now.second]
    pygame.display.set_caption(f"{time[0]}:{time[1]}:{time[2]}")

    window.fill((0, 0, 0))
# no. of radians in a circle / 60 (for second hand positions)
    second_angle = (time[2] - 15) * (2*math.pi)/60
    second_endpoint = [320+math.cos(second_angle)*150,240+math.sin(second_angle)*150]
# no. of radians in a circle / 60 (for minute hand positions)
    minute_angle = (time[1] - 15) * (2*math.pi)/60
    minute_endpoint = [320+math.cos(minute_angle)*150,240+math.sin(minute_angle)*150]
# no. of radians in a circle / 12 (for hour hand positions)
    hour_angle = (time[0] - 2) * (2*math.pi)/12
    hour_endpoint = [320+math.cos(hour_angle)*100,240+math.sin(hour_angle)*100]
#visual representation of clock hands
    pygame.draw.circle(window, (255, 0, 255), (320, 240), 180)
    pygame.draw.circle(window, (255, 255, 255), (320, 240), 160)
    pygame.draw.line(window, (0, 0, 255), (320, 240), (second_endpoint[0], second_endpoint[1]), 2)
    pygame.draw.line(window, (0, 0, 255), (320, 240), (minute_endpoint[0], minute_endpoint[1]), 4)
    pygame.draw.line(window, (0, 0, 255), (320, 240), (hour_endpoint[0], hour_endpoint[1]), 6)


    
    

    pygame.display.flip()

    clock.tick(60)
