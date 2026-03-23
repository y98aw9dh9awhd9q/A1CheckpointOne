import pygame
import const
from game.combat.entities.enemyHpBar import enemyHpBar

slotX = [225, 450, 675]
enemyCy = 105

class enemyDrawer:
    def __init__(self):
        self.hpBar = enemyHpBar(spriteHeight=90)

    def draw(self,screen,enemies,showHp=False,targeted=-1):
        positions = self.getPositions(len(enemies))
        for i, (ent, cx) in enumerate(zip(enemies, positions)):
            ox = ent.getShakeOffset()

            if ent.image:
                r = ent.image.get_rect(center=(cx + ox, enemyCy))
                screen.blit(ent.image, r)
            else:
                self.drawFallback(screen, cx + ox, enemyCy, ent.name)

            if showHp and i == targeted:
                self.hpBar.drawNameWithHp(screen, cx + ox, enemyCy, ent)
                self.drawTargetCursor(screen, cx + ox, enemyCy)
            else:
                self.hpBar.drawName(screen, cx + ox, enemyCy, ent)

    def drawTargetCursor(self, screen, cx, cy):
        spriteHalfH = 45
        tipY = cy - spriteHalfH - 28
        pygame.draw.polygon(screen, const.red, [
            (cx, tipY),
            (cx - 8, tipY - 14),
            (cx + 8, tipY - 14),
        ])

    def getPositions(self, count):
        if count == 1:
            return [slotX[1]]
        if count == 2:
            return [slotX[0], slotX[2]]
        return list(slotX)

    def drawFallback(self, screen, cx, cy, name):
        w,h =80,80
        pygame.draw.rect(screen, (180,60,60), (cx-w//2,cy-h//2,w,h))
        pygame.draw.rect(screen,const.white, (cx-w//2,cy-h//2,w,h),2)
        font = pygame.font.SysFont("Arial", 13, bold=True)
        lbl = font.render(name[:8], True, const.white)
        screen.blit(lbl, (cx - lbl.get_width() // 2, cy - lbl.get_height() // 2))