import os
import math
import pygame
import const
from game.combat.entities.entitySuper import livingEntity

class enemy(livingEntity):
    def __init__(self, name, hp, attack, defense, assetFile, scale=(80, 80),gold = 4):
        super().__init__(name, hp, attack, defense)
        self.shakeTimer = 0.0
        self.alive = True
        self.maxHp = self.hp
        self.gold = gold

        try:
            raw = pygame.image.load(os.path.join(const.baseDir, "assets", "pictures", assetFile))
            self.image = pygame.transform.scale(raw, scale)
        except Exception:
            print("skill issue")
            self.image = None

    def takeDamage(self, damage):
        super().takeDamage(damage)
        self.shakeTimer = 0.35
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, deltaTime):
        if self.shakeTimer > 0:
            self.shakeTimer = max(0.0, self.shakeTimer-deltaTime)

    def getShakeOffset(self):
        if self.shakeTimer > 0:
            return int(math.sin(self.shakeTimer*55)*7)
        return 0