import pygame
import math
import random
import const
from game.combat.attacks.handlers.attackBase import attackBase

class totallyOriginalAttackOneBuffed(attackBase):
    attackTimer = 6.0
    volley = 1

    def start(self):
        super().start()
        self.timer = 0.0
        self.box = None
        self.bullets = []
        self.volleysFired = 0
        self.volleyCooldown = 0.0
        self.circleAngle = 0.0
        self.circleTarget = (0, 0)

    def update(self, dt, box):
        if not self.running:
            return

        self.box = box
        self.timer += dt
        self.volleyCooldown -= dt

        if self.volleyCooldown <= 0 and self.volleysFired < self.volley:
            self.fireVolley()

        self.circleAngle += 0.5 * dt
        self.updateCircleTarget(dt)

        soul = self.boundary.player
        for b in self.bullets:
            b.update(dt, box, soul)
        self.bullets = [b for b in self.bullets if b.alive]

        if self.timer >= self.attackTimer:
            self.done = True
            self.running = False

    def updateCircleTarget(self, dt):
        if not self.circleTarget or random.random() < 0.01:
            cx = self.boundary.player.rect.centerx
            cy = self.boundary.player.rect.centery
            radius = 100
            self.circleTarget = (
                cx + random.uniform(-radius, radius),
                cy + random.uniform(-radius, radius)
            )

        tx, ty = self.circleTarget
        cx = self.boundary.player.rect.centerx
        cy = self.boundary.player.rect.centery

        dx = tx - cx
        dy = ty - cy
        dist = math.hypot(dx, dy)

        if dist < 5:
            return

        speed = 60
        moveX = (dx / dist) * speed * dt
        moveY = (dy / dist) * speed * dt

        self.circleTarget = (tx, ty)

    def fireVolley(self):
        soul = self.boundary.player
        cx = self.circleTarget[0]
        cy = self.circleTarget[1]

        dirs = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (0.707, 0.707), (-0.707, 0.707),
            (0.707, -0.707), (-0.707, -0.707),
        ]

        for i, (dx, dy) in enumerate(dirs):
            self.bullets.append(self.knife(cx, cy, dx, dy, i * 0.5))

        self.volleysFired += 1
        self.volleyCooldown = 9999

    def checkHit(self, soul):
        for b in self.bullets:
            if not b.alive:
                continue
            if not b.armed:
                continue
            if b.sweptCollides(soul.rect):
                return True
        return False

    class knife:
        speed = 900
        trackDuration = 0.15
        freezeDuration = 0.3
        flashDuration = 0.2
        offset = 60

        def __init__(self, x, y, dx, dy, delay):
            self.x = float(x)
            self.y = float(y)
            self.dx = dx
            self.dy = dy
            self.alive = True
            self.armed = False
            self.timer = 0.0
            self.delay = delay
            self.fired = False
            self.vx = 0.0
            self.vy = 0.0
            self.w = 10
            self.h = 28
            self.flashOn = False
            self.prevX = float(x)
            self.prevY = float(y)

        def update(self, dt, box, soul=None):
            self.timer += dt
            elapsed = self.timer - self.delay
            if elapsed < 0:
                return

            self.prevX = self.x
            self.prevY = self.y

            if not self.fired:
                if soul and elapsed < self.trackDuration:
                    self.x = soul.rect.centerx - self.dx * self.offset
                    self.y = soul.rect.centery - self.dy * self.offset

                self.flashOn = int(elapsed * 8) % 2 == 0

                if elapsed >= self.trackDuration + self.freezeDuration:
                    self.armed = True

                if elapsed >= self.trackDuration + self.freezeDuration + self.flashDuration:
                    self.fired = True
                    self.vx = self.dx * self.speed
                    self.vy = self.dy * self.speed
            else:
                self.x += self.vx * dt
                self.y += self.vy * dt
                if not self.rect.colliderect(box):
                    self.alive = False

        def sweptCollides(self, rect):
            steps = 8
            for i in range(steps + 1):
                t = i / steps
                sx = self.prevX + (self.x - self.prevX) * t
                sy = self.prevY + (self.y - self.prevY) * t
                check = pygame.Rect(int(sx) - self.w // 2, int(sy) - self.h // 2, self.w, self.h)
                if check.colliderect(rect):
                    return True
            return False

        def draw(self, screen):
            if not self.alive:
                return
            if self.timer < self.delay:
                return

            if not self.fired:
                color = const.red if (self.armed and self.flashOn) else const.white
            else:
                color = const.white

            angle = math.degrees(math.atan2(self.dy, self.dx)) + 90
            surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.rect(surf, color, (0, 0, self.w, self.h))
            rotated = pygame.transform.rotate(surf, -angle)
            screen.blit(rotated, rotated.get_rect(center=(int(self.x), int(self.y))))

        @property
        def rect(self):
            return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2, self.w, self.h)