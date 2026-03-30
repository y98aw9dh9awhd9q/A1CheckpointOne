import pygame
import math
import const
from game.combat.attacks.handlers.attackBase import attackBase

class totallyOriginalAttackTwo(attackBase):
    attackTimer = 12.0

    def start(self):
        super().start()
        self.phase = 0
        self.timer = 0.0
        self.box = None
        self.slashes = []
        self.pending = []
        self.waveIndex = 0
        self.waveDelay = 1.5
        self.waveTimer = 0.0
        self.maxWaves = 6

    def update(self, dt, box):
        if not self.running:
            return

        self.box = box
        self.timer += dt
        soul = self.boundary.player

        if self.phase == 0:
            self.waveTimer += dt

            if self.waveTimer >= self.waveDelay:
                self.waveTimer = 0.0
                self.spawnTelegraph(soul)
                self.waveIndex += 1

                if self.waveIndex >= self.maxWaves:
                    self.phase = 1

        for t in self.pending:
            t.update(dt)

        for t in self.pending:
            if t.ready:
                self.slashes.append(self.sanguineSlash(t.cx, t.cy, t.angle, t.length))
                t.done = True

        self.pending = [t for t in self.pending if not t.done]

        for s in self.slashes:
            s.update(dt)

        self.slashes = [s for s in self.slashes if s.alive]

        if self.phase == 1 and not self.pending and not self.slashes:
            self.done = True
            self.running = False

    def spawnTelegraph(self, soul):
        cx = soul.rect.centerx
        cy = soul.rect.centery
        length = max(self.box.width, self.box.height) * 2.6

        count = 4 + self.waveIndex
        base = self.waveIndex * 0.4

        for i in range(count):
            angle = base + i * (math.pi * 2 / count)
            self.pending.append(self.telegraph(cx, cy, angle, length))

    def draw(self, screen):
        if not self.box:
            return

        for t in self.pending:
            t.draw(screen)

        for s in self.slashes:
            s.draw(screen)

    def checkHit(self, soul):
        return any(s.collides(soul.rect) for s in self.slashes)

    class telegraph:
        def __init__(self, cx, cy, angle, length):
            self.cx = cx
            self.cy = cy
            self.baseAngle = angle
            self.angle = angle
            self.length = length
            self.timer = 0.0
            self.spinTime = 1
            self.holdTime = 0.2
            self.ready = False
            self.done = False

        def update(self, dt):
            self.timer += dt

            if self.timer < self.spinTime:
                self.angle += 1.2 * dt
            elif self.timer < self.spinTime + self.holdTime:
                self.angle = self.angle
            else:
                self.ready = True

        def draw(self, screen):
            surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

            alpha = 80 if self.timer < self.spinTime else 160

            sx = int(self.cx + math.cos(self.angle) * self.length * 0.5)
            sy = int(self.cy + math.sin(self.angle) * self.length * 0.5)
            ex = int(self.cx - math.cos(self.angle) * self.length * 0.5)
            ey = int(self.cy - math.sin(self.angle) * self.length * 0.5)

            pygame.draw.line(surf, (*const.red, alpha), (sx, sy), (ex, ey), 5)
            screen.blit(surf, (0, 0))

    class sanguineSlash: #ripped straight from the source
        def __init__(self, cx, cy, angle, length):
            self.cx = cx
            self.cy = cy
            self.angle = angle
            self.length = length
            self.timer = 0.0
            self.alive = True
            self.active = False
            self.width = 22
            self.alpha = 255

        def update(self, dt):
            self.timer += dt

            if self.timer >= 0.05:
                self.active = True

            if self.timer >= 0.2:
                fade = (self.timer - 0.2) / 0.35
                self.alpha = int(255 * (1 - min(fade, 1)))

            if self.timer >= 0.6:
                self.alive = False

        def collides(self, rect):
            if not self.active:
                return False

            steps = int(self.length / 8)
            for i in range(steps + 1):
                t = (i / steps) - 0.5
                x = self.cx + math.cos(self.angle) * self.length * t
                y = self.cy + math.sin(self.angle) * self.length * t
                if rect.collidepoint(x, y):
                    return True
            return False

        def draw(self, screen):
            if not self.alive:
                return

            sx = int(self.cx + math.cos(self.angle) * self.length * 0.5)
            sy = int(self.cy + math.sin(self.angle) * self.length * 0.5)
            ex = int(self.cx - math.cos(self.angle) * self.length * 0.5)
            ey = int(self.cy - math.sin(self.angle) * self.length * 0.5)

            surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

            color = (*const.white, self.alpha) if self.active else (*const.red, 120)

            pygame.draw.line(surf, color, (sx, sy), (ex, ey), self.width)
            screen.blit(surf, (0, 0))