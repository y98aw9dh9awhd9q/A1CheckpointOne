import pygame
import math

class attackBase:
    damage = 1
    attackTimer = 3.0
    volley = 1
    volleyDelay = 0.4

    def __init__(self, boundary, attacker, roundStore=None):
        self.timer = 0.0
        self.done = False
        self.running = False
        self.volleysFired = 0
        self.volleyCooldown = 0.0
        self.bullets = []
        self.boundary = boundary
        self.damage = attacker.attack if attacker else self.__class__.damage
        self.roundStore = roundStore if roundStore is not None else {}
        self.box = None

    def start(self):
        self.running = True
        self.volleysFired = 0
        self.volleyCooldown = 0.0
        self.timer = 0.0
        self.done = False
        self.bullets = []

    def fireVolley(self):
        pass

    def update(self, dt, box):
        if not self.running:
            return

        self.box = box
        self.timer += dt

        self.volleyCooldown -= dt
        if self.volleyCooldown <= 0 and self.volleysFired < self.volley:
            self.fireVolley()

        for b in self.bullets:
            b.update(dt, box)
        self.bullets = [b for b in self.bullets if b.alive]

        if self.timer >= self.attackTimer:
            self.done = True
            self.running = False

    def checkHit(self, soul):
        for bullet in self.bullets:
            if not bullet.alive:
                continue
            if hasattr(bullet, "collides"):
                if bullet.collides(soul.rect) and self.canHit(soul):
                    return True
            elif bullet.rect.colliderect(soul.rect):
                if self.canHit(soul):
                    bullet.alive = False
                    return True
        return False

    def canHit(self, soul):
        return True

    def draw(self, screen):
        for b in self.bullets:
            b.draw(screen)

    class beam:
        def __init__(self, cx, cy, angle, spinSpeed, width, color, warningTime=0.5):
            self.cx = cx
            self.cy = cy
            self.angle = angle
            self.spinSpeed = spinSpeed
            self.width = width
            self.color = color
            self.warningTime = warningTime
            self.timer = 0
            self.active = False
            self.alive = True
            self.length = 2000
            self.warnColor = (180, 180, 180)

        def update(self, dt, box):
            if not self.alive:
                return
            self.timer += dt
            self.angle += self.spinSpeed * dt
            if self.timer >= self.warningTime:
                self.active = True

        def getEndPoint(self):
            ex = self.cx + math.cos(self.angle) * self.length
            ey = self.cy + math.sin(self.angle) * self.length
            return ex, ey

        def draw(self, screen):
            if not self.alive:
                return
            ex, ey = self.getEndPoint()
            color = self.color if self.active else self.warnColor
            width = self.width if self.active else 3
            pygame.draw.line(
                screen,
                color,
                (int(self.cx), int(self.cy)),
                (int(ex), int(ey)),
                width
            )

        def collides(self, rect):
            if not self.active:
                return False
            ex, ey = self.getEndPoint()
            steps = int(self.length / 10)
            for i in range(steps):
                t = i / steps
                x = self.cx + (ex - self.cx) * t
                y = self.cy + (ey - self.cy) * t
                if rect.collidepoint(x, y):
                    return True
            return False

class bullet:
    def __init__(self, x, y, vx, vy, w, h, color):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
        self.alive = True

    def update(self, dt, box):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if not self.rect.colliderect(box):
            self.alive = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (int(self.x) - self.w // 2, int(self.y) - self.h // 2, self.w, self.h))

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2, self.w, self.h)