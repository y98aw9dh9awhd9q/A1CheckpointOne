import pygame
import math
import random
import const
from game.combat.attacks.handlers.attackBase import attackBase

class beamOfPharaoh(attackBase):
    attackTimer = 4
    volley = 1
    blasterCount = 50

    def fireVolley(self):
        box = self.boundary.getRect()

        positions = self.getSpawnPositions(box)
        random.shuffle(positions)

        for i, (x, y) in enumerate(positions[:self.blasterCount]):
            tx = random.randint(box.left, box.right)
            ty = random.randint(box.top, box.bottom)
            angle = math.atan2(ty - y, tx - x)
            delay = i * 0.2
            self.bullets.append(self.blaster(x, y, angle, delay))

        self.volleysFired += 1
        self.volleyCooldown = 9999

    def getSpawnPositions(self, box):
        positions = []
        steps = 8
        for i in range(steps):
            t = i / steps
            if t < 0.25:
                x = box.left + (t / 0.25) * box.width
                y = box.top - 40
            elif t < 0.5:
                x = box.right + 40
                y = box.top + ((t - 0.25) / 0.25) * box.height
            elif t < 0.75:
                x = box.right - ((t - 0.5) / 0.25) * box.width
                y = box.bottom + 40
            else:
                x = box.left - 40
                y = box.bottom - ((t - 0.75) / 0.25) * box.height
            positions.append((x, y))
        return positions

    class blaster:
        warningTime = 1.0
        beamDuration = 0.5
        beamWidth = 50
        size = 30

        def __init__(self, x, y, angle, delay):
            self.x = float(x)
            self.y = float(y)
            self.angle = angle
            self.delay = delay
            self.timer = 0.0
            self.alive = True
            self.firing = False
            self.alpha = 0

        def update(self, dt, box):
            if not self.alive:
                return
            self.timer += dt

            elapsed = self.timer - self.delay
            if elapsed < 0:
                return

            if elapsed < self.warningTime:
                self.alpha = int(255 * (elapsed / self.warningTime))
                self.firing = False
            elif elapsed < self.warningTime + self.beamDuration:
                self.alpha = 255
                self.firing = True
            else:
                self.alive = False

        def collides(self, rect):
            if not self.firing:
                return False
            length = 2000
            ex = self.x + math.cos(self.angle) * length
            ey = self.y + math.sin(self.angle) * length
            steps = int(length / 8)
            for i in range(steps):
                t = i / steps
                px = self.x + (ex - self.x) * t
                py = self.y + (ey - self.y) * t
                if rect.collidepoint(px, py):
                    return True
            return False

        def draw(self, screen):
            if not self.alive:
                return

            elapsed = self.timer - self.delay
            if elapsed < 0:
                return

            surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

            tipX = int(self.x + math.cos(self.angle) * self.size * 2)
            tipY = int(self.y + math.sin(self.angle) * self.size * 2)
            leftX = int(self.x + math.cos(self.angle + 2.4) * self.size)
            leftY = int(self.y + math.sin(self.angle + 2.4) * self.size)
            rightX = int(self.x + math.cos(self.angle - 2.4) * self.size)
            rightY = int(self.y + math.sin(self.angle - 2.4) * self.size)

            pygame.draw.polygon(surf, (*const.red, self.alpha), [(tipX, tipY), (leftX, leftY), (rightX, rightY)])

            if self.firing:
                length = 2000
                ex = self.x + math.cos(self.angle) * length
                ey = self.y + math.sin(self.angle) * length
                pygame.draw.line(surf, (*const.white, 255), (int(self.x), int(self.y)), (int(ex), int(ey)), self.beamWidth)

            screen.blit(surf, (0, 0))