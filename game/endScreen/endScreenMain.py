import pygame
import os
import math
from const import baseDir
from game.gameHandler.pygameWindow.soundManager import playVineBoom

def loadAssets():
    return {
        "player": pygame.transform.scale(
            pygame.image.load(os.path.join(baseDir, "assets", "pictures", "player.png")).convert_alpha(),
            (120, 120)
        ),
        "pharoh": pygame.transform.scale(
            pygame.image.load(os.path.join(baseDir, "assets", "pictures", "pharoh.png")).convert_alpha(),
            (120, 120)
        ),
        "nagra": pygame.transform.scale(
            pygame.image.load(os.path.join(baseDir, "assets", "pictures", "nagraNotGeno.png")).convert_alpha(),
            (120, 120)
        ),
        "geno": pygame.transform.scale(
            pygame.image.load(os.path.join(baseDir, "assets", "pictures", "nagraGeno.png")).convert_alpha(),
            (120, 120)
        )
    }

def drawCentered(screen, img, x, y):
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

def playGoodEnding():
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    assets = loadAssets()
    width, height = screen.get_size()
    pharoh = assets["pharoh"]
    nagra = assets["nagra"]
    geno = assets["geno"]

    leftX = width // 2 - 200
    rightX = width // 2 + 200
    centerY = height // 2

    timer = 0
    state = 0
    angle = 0
    boom1 = False
    boom2 = False

    while True:
        dt = clock.tick(60)
        timer += dt
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if state == 0:
            drawCentered(screen, pharoh, rightX, centerY)
            if timer > 800:
                state = 1
                timer = 0

        elif state == 1:
            drawCentered(screen, pharoh, rightX, centerY)
            drawCentered(screen, nagra, leftX, centerY)
            if timer > 800:
                state = 2
                timer = 0
                if not boom1:
                    playVineBoom()
                    boom1 = True

        elif state == 2:
            drawCentered(screen, pharoh, rightX, centerY)
            drawCentered(screen, geno, leftX, centerY)
            if timer > 600:
                state = 3
                timer = 0

        elif state == 3:
            angle += 8
            scale = 1 + abs(math.sin(timer * 0.007)) * 2
            transformed = pygame.transform.rotozoom(geno, angle, scale)
            drawCentered(screen, pharoh, rightX, centerY)
            drawCentered(screen, transformed, leftX, centerY)
            if timer > 1500:
                state = 4
                timer = 0

        elif state == 4:
            drawCentered(screen, geno, leftX, centerY)
            pygame.draw.line(screen, (255, 0, 0), (leftX, centerY), (rightX, centerY), 10)
            if timer > 600:
                if not boom2:
                    playVineBoom()
                    boom2 = True
                state = 5

        elif state == 5:
            screen.fill((0, 0, 0))
            drawCentered(screen, geno, leftX, centerY)
            pygame.display.flip()
            return

        pygame.display.flip()

def playBadEnding():
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    assets = loadAssets()
    width, height = screen.get_size()
    pharoh = assets["pharoh"]
    player = assets["player"]

    leftX = width // 2 - 200
    rightX = width // 2 + 200
    centerY = height // 2

    timer = 0
    state = 0
    boom = False

    while True:
        dt = clock.tick(60)
        timer += dt
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if state == 0:
            drawCentered(screen, pharoh, leftX, centerY)
            if timer > 800:
                state = 1
                timer = 0

        elif state == 1:
            drawCentered(screen, pharoh, leftX, centerY)
            drawCentered(screen, player, rightX, centerY)
            if timer > 800:
                state = 2
                timer = 0

        elif state == 2:
            drawCentered(screen, pharoh, leftX, centerY)
            drawCentered(screen, player, rightX, centerY)
            pygame.draw.line(screen, (255, 0, 0), (leftX, centerY), (rightX, centerY), 10)
            if timer > 600:
                if not boom:
                    playVineBoom()
                    boom = True
                state = 3

        elif state == 3:
            screen.fill((0, 0, 0))
            drawCentered(screen, pharoh, leftX, centerY)
            pygame.display.flip()
            return

        pygame.display.flip()