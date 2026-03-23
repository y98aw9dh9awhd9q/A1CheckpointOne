import pygame
import const

class enemyHpBar:
    barW = 110
    barH = 10
    offset = 8

    def __init__(self, spriteHeight=80):
        self.spriteHalfH = spriteHeight // 2
        self.fontName = pygame.font.SysFont("Arial", 14, bold=True)
        self.fontNums = pygame.font.SysFont("Arial", 13, bold=True)

    def drawName(self, screen, cx, cy, ent):
        topOfSprite = cy - self.spriteHalfH
        barY = topOfSprite - self.offset - self.barH
        nameSurf = self.fontName.render(ent.name.upper(), True, const.white)
        screen.blit(nameSurf, (cx - nameSurf.get_width() // 2, barY - nameSurf.get_height() - 2))

    def drawNameWithHp(self, screen, cx, cy, ent):
        topOfSprite = cy - self.spriteHalfH
        barY = topOfSprite - self.offset - self.barH
        nameStr = ent.name.upper()
        hpStr = f"  {max(0, int(ent.hp))}/{int(ent.maxHp)}"
        nameSurf = self.fontName.render(nameStr, True, const.white)
        hpSurf = self.fontNums.render(hpStr, True, const.yellow)
        totalW = nameSurf.get_width() + hpSurf.get_width()
        startX = cx - totalW // 2
        labelY = barY - nameSurf.get_height() - 2
        screen.blit(nameSurf, (startX, labelY))
        screen.blit(hpSurf, (startX + nameSurf.get_width(), labelY))