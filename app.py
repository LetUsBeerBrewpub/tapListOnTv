# Example file showing a basic pygame "game loop"
import pygame
import logging
from notion_client import Client, APIErrorCode, APIResponseError
from configparser import ConfigParser
from pprint import pprint

# pygame setup
pygame.init()
flags = pygame.NOFRAME | pygame.FULLSCREEN
screen = pygame.display.set_mode(size=(100,200), flags = flags)
clock = pygame.time.Clock()
running = True

pprint(pygame.display.Info())

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()