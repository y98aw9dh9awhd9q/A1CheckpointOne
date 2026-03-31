import math
import const
from game.combat.attacks.handlers.attackBase import attackBase
import pygame

class keySpinnahReprise(attackBase):
    damage = 2
    attackTimer = 6
    volley = 5
    volleyDelay = 1.0
    numKeys = 10
    startRadius = 200
    minRadius = 20
    spinSpeed = math.pi / 3
    convergeSpeed = 70

    class keyBullet:
        def __init__(self, centerX, centerY, angle, radius, spinSpeed, convergeSpeed, damage):
            self.centerX = centerX
            self.centerY = centerY
            self.angle = angle
            self.radius = radius
            self.spinSpeed = spinSpeed
            self.convergeSpeed = convergeSpeed
            self.damage = damage
            self.alive = True
            self.color = const.white
            self.w = 48
            self.h = 10
            self.updatePosition()

        def updatePosition(self):
            self.x = self.centerX + math.cos(self.angle) * self.radius
            self.y = self.centerY + math.sin(self.angle) * self.radius

        def update(self, dt, box):
            if not self.alive:
                return
            self.angle += self.spinSpeed * dt
            speed = self.convergeSpeed * (1 + (self.radius / self.radius))
            self.radius = max(self.radius - speed * dt, 0)
            self.updatePosition()
            if self.radius <= 5:
                self.alive = False

        def draw(self, screen):
            if not self.alive:
                return
            rect = pygame.Rect(0, 0, self.w, self.h)
            rect.center = (int(self.x), int(self.y))
            dx = self.centerX - self.x
            dy = self.centerY - self.y
            angle = math.degrees(math.atan2(dy, dx))
            surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            surf.fill(self.color)
            rotated = pygame.transform.rotate(surf, -angle)
            rrect = rotated.get_rect(center=rect.center)
            screen.blit(rotated, rrect.topleft)

        @property
        def rect(self):
            return pygame.Rect(int(self.x) - self.w // 2,
                               int(self.y) - self.h // 2,
                               self.w, self.h)

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay
        cx = self.boundary.player.rect.centerx
        cy = self.boundary.player.rect.centery
        for i in range(self.numKeys):
            angle = i * (2 * math.pi / self.numKeys)
            self.bullets.append(
                self.keyBullet(
                    cx, cy, angle, self.startRadius,
                    self.spinSpeed, self.convergeSpeed,
                    self.damage
                )
            )