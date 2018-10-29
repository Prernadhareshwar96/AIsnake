import pygame
import sys
import time
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
clock = pygame.time.Clock()
dir = 1
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #ballrect = ballrect.move(speed)

    ballrect.x += (1*dir)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        ballrect.x=max(0,ballrect.x-10)
    if key[pygame.K_RIGHT]:
        ballrect.x=min(width,ballrect.x+10)
    if key[pygame.K_UP]:
        ballrect.y=max(0,ballrect.y-10)
    if key[pygame.K_DOWN]:
        ballrect.y=min(height,ballrect.y+10)

    if ballrect.left<0 or ballrect.right>width:
        dir = (dir*-1)

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(100)