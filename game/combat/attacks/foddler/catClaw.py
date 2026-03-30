import random
import pygame
import const
from game.combat.attacks.handlers.attackBase import attackBase

class catClaw(attackBase):
    damage = 2
    attackTimer = 4
    volley = 3
    volleyDelay = 0.8
    dashSpeed = 420
    verticalVariation = 10
    delay = 0.25
    angleFactor = 0.35

    class claw:
        def __init__(self, x, y, vx, vy, delay, color):
            self.x = float(x)
            self.y = float(y)
            self.vx = 0
            self.vy = 0
            self.targetVX = vx
            self.targetVY = vy
            self.delay = delay
            self.timer = 0
            self.w = 80
            self.h = 14
            self.color = color
            self.alive = True

        def update(self, dt, box):
            self.timer += dt
            if self.timer >= self.delay:
                self.vx = self.targetVX
                self.vy = self.targetVY
            self.x += self.vx * dt
            self.y += self.vy * dt
            if not self.rect.colliderect(box):
                self.alive = False

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

        @property
        def rect(self):
            return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2, self.w, self.h)

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay

        rect = self.boundary.getRect()
        soul = self.boundary.player

        side = random.choice(["left", "right"])
        clawCount = 3
        spacing = rect.height // (clawCount + 1)

        ys = [rect.top + spacing * (i + 1) for i in range(clawCount)]

        avgY = sum(ys)/len(ys)
        shift = (soul.rect.centery - avgY) * 0.35
        ys = [y + shift for y in ys]

        mid_index = clawCount // 2
        mid_y = ys[mid_index]

        for i, y in enumerate(ys):
            y += random.uniform(-self.verticalVariation, self.verticalVariation)

            y = max(rect.top + 10, min(y, rect.bottom - 10))

            if side == "left":
                vx = self.dashSpeed
                x = rect.left
            else:
                vx = -self.dashSpeed
                x = rect.right

            if soul.rect.centery > mid_y:
                vy = (soul.rect.centery - y) * self.angleFactor + 20 * (i - mid_index)
            else:
                vy = (soul.rect.centery - y) * self.angleFactor - 20 * (i - mid_index)

            self.bullets.append(self.claw(x, y, vx, vy, self.delay, const.white))