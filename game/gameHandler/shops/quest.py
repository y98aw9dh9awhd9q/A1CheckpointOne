import pygame
import const
import random

from game.gameHandler.pygameWindow.soundManager import playVineBoom

class quest:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont("Arial", 28)
        self.smallFont = pygame.font.SysFont("Arial", 20)
        self.active = False
        self.acceptRect = None
        self.exitRect = None
        self.requiredItem = None
        self.rewardItem = None

    def open(self):
        self.active = True
        self.generateQuest()

    def close(self):
        self.active = False

    def generateQuest(self):
        items = list(const.shopItems.values())
        self.requiredItem = random.choice(items)
        self.rewardItem = random.choice(items)

    def update(self, events):
        if not self.active:
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.acceptRect and self.acceptRect.collidepoint(pos):
                    for item in self.player.inventory:
                        if item["name"] == self.requiredItem["name"]:
                            self.player.inventory.remove(item)
                            self.player.inventory.append(self.rewardItem)
                            break

                    playVineBoom()
                    print("broke")

                if self.exitRect and self.exitRect.collidepoint(pos):
                    self.close()

    def draw(self):
        if not self.active:
            return

        self.screen.fill(const.black)

        title = self.font.render("quest", True, const.white)
        self.screen.blit(title,(400,60))

        text1 = f"giveth: {self.requiredItem['name']}"
        text2 = f"get scammed by: {self.rewardItem['name']}"

        surf1 = self.smallFont.render(text1,True,const.white)
        surf2 = self.smallFont.render(text2,True,const.white)

        self.screen.blit(surf1,(300,200))
        self.screen.blit(surf2,(300,240))

        accept = self.font.render("accept",True,const.white)
        self.acceptRect = accept.get_rect(center=(450,350))
        self.screen.blit(accept,self.acceptRect)

        exitText = self.font.render("you dare reject?",True,const.white)
        self.exitRect = exitText.get_rect(center=(450,450))
        self.screen.blit(exitText,self.exitRect)