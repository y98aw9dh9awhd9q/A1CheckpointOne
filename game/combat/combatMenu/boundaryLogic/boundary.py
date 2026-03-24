import pygame

import const
from game.combat.combatMenu.boundaryLogic.soul import soul

class boundaryLogic:
    expandSpeed = 20
    shrinkSpeed = 25
    stateExpanding = 0
    stateActive = 1
    stateEnding = 2
    stateDone = 3

    def __init__(self,screen,player,soulMode = 0, boundarySize = 350):
        self.screen = screen
        w,h = screen.get_size()
        self.center = pygame.Vector2(w//2,h//2)
        self.width = 0
        self.height = 0
        self.state = self.stateExpanding
        self.player = soul(self.center,player, soulMode)
        self.attacks = []
        self.boundarySize = boundarySize

    def addAttack(self,attack):
        self.attacks.append(attack)

    def endBox(self):
        self.player=None
        self.attacks.clear()
        self.state = self.stateEnding

    def getRect(self):
        return pygame.Rect(
            self.center.x - self.width//2,
            self.center.y - self.height//2,
            self.width,
            self.height
        )

    def update(self,deltaTime):
        if self.state == self.stateExpanding:
            self.width += self.expandSpeed
            self.height += self.expandSpeed

            if self.width >= self.boundarySize:
                self.width = self.boundarySize
                self.height = self.boundarySize
                self.state = self.stateActive

        elif self.state == self.stateActive:
            box = self.getRect()

            if self.player:
                self.player.update(deltaTime,box)

            for attack in self.attacks:
                attack.update(deltaTime,box)

                if self.player and attack.checkHit(self.player):
                    self.player.damage(attack.damage)

        elif self.state == self.stateEnding:
            self.width -= self.shrinkSpeed
            self.height -= self.shrinkSpeed

            if self.width <=0:
                self.width = 0
                self.height = 0
                self.state = self.stateDone

    def draw(self):
        if self.state == self.stateDone:
            return
        if self.player:
            self.player.drawSoul(self.screen)
        rect = self.getRect()
        pygame.draw.rect(self.screen,const.white,rect,4)

    def getState(self):
        return self.state

