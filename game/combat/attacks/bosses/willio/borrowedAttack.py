import pygame
import const
from game.combat.attacks.handlers.attackBase import attackBase

#kitsune? we dont talk about the bugs
class borrowedAttack(attackBase):
    attackTimer = 4.0

    def start(self):
        super().start()
        self.timer = 0.0
        self.phase = 0
        self.phaseTimer = 0.0
        self.center = None
        self.telegraphTime = 0.6
        self.fireTime = 0.35
        self.radius = 90
        self.beamWidth = 18

    def update(self, dt, box):
        if not self.running:
            return

        self.timer += dt
        self.phaseTimer += dt

        soul = self.boundary.player

        if self.center is None:
            self.center = (soul.rect.centerx, soul.rect.centery)

        if self.phaseTimer >= self.telegraphTime + self.fireTime:
            self.phase += 1
            self.phaseTimer = 0.0
            self.center = (soul.rect.centerx, soul.rect.centery)

        if self.phase >= 3 or self.timer >= self.attackTimer:
            self.done = True
            self.running = False

    def checkHit(self, soul):
        if self.phase >= 3:
            return False

        if self.phaseTimer < self.telegraphTime:
            return False

        cx, cy = self.center
        px, py = soul.rect.centerx, soul.rect.centery

        if self.phase == 0:
            if abs(px - cx) < self.beamWidth:
                return True

        elif self.phase == 1:
            if abs(py - cy) < self.beamWidth:
                return True

        elif self.phase == 2:
            if abs(px - cx) < self.beamWidth or abs(py - cy) < self.beamWidth:
                return True

        return False

    def draw(self, screen):
        if not self.running or self.phase >= 3:
            return

        soul = self.boundary.player

        if self.center is None:
            self.center = (soul.rect.centerx, soul.rect.centery)

        cx, cy = self.center

        t = min(self.phaseTimer / self.telegraphTime, 1.0)

        diamond = [
            (cx, cy - self.radius),
            (cx + self.radius, cy),
            (cx, cy + self.radius),
            (cx - self.radius, cy),
        ]

        teleColor = (
            255,
            int(255 * (1 - t)),
            int(255 * (1 - t))
        )

        pygame.draw.polygon(screen, teleColor, diamond, 3)

        if self.phaseTimer >= self.telegraphTime:
            if self.phase == 0 or self.phase == 2:
                rect = pygame.Rect(cx - self.beamWidth // 2, 0, self.beamWidth, screen.get_height())
                pygame.draw.rect(screen, const.red, rect)

            if self.phase == 1 or self.phase == 2:
                rect = pygame.Rect(0, cy - self.beamWidth // 2, screen.get_width(), self.beamWidth)
                pygame.draw.rect(screen, const.red, rect)