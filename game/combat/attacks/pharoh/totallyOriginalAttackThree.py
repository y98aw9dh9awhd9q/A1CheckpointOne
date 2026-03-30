import math
import pygame
import const
from game.combat.attacks.handlers.attackBase import attackBase
from game.combat.attacks.blueBeam import blueBeam
from game.combat.attacks.orangeBeam import orangeBeam

class totallyOriginalAttackThree(attackBase):
    attackTimer = 15.0

    def start(self):
        super().start()
        self.timer = 0.0
        self.box = None
        self.sequence = ["orange", "blue", "blue", "orange", "blue", "orange"]
        self.index = 0
        self.state = 0
        self.flowers = []
        self.center = (0, 0)
        self.waitTimer = 0.0
        self.activeBeams = []
        self.beamsSpawned = False

    def update(self, dt, box):
        if not self.running:
            return

        self.box = box
        self.timer += dt
        soul = self.boundary.player

        for b in self.activeBeams:
            b.update(dt, box)
        self.activeBeams = [b for b in self.activeBeams if not b.done]

        if self.state == 0:
            self.beamsSpawned = False
            self.center = (soul.rect.centerx, soul.rect.centery)
            self.spawnFlowers()
            self.state = 1
            self.waitTimer = 0.0

        elif self.state == 1:
            for f in self.flowers:
                f.update(dt, self.center, circling=True)

            self.waitTimer += dt
            if self.waitTimer >= 0.7:
                self.waitTimer = 0.0
                self.state = 4

        elif self.state == 4:
            allDone = True

            for f in self.flowers:
                f.update(dt, self.center, circling=False)
                if not f.reached:
                    allDone = False

            if allDone and not self.beamsSpawned:
                self.spawnBeams()
                self.beamsSpawned = True
                self.flowers.clear()
                self.state = 3

        elif self.state == 3:
            if not self.activeBeams:
                self.index += 1

                if self.index >= len(self.sequence):
                    self.done = True
                    self.running = False
                else:
                    self.state = 0

        if self.timer >= self.attackTimer:
            self.done = True
            self.running = False

    def spawnFlowers(self):
        self.flowers = []
        cx, cy = self.center
        radius = max(self.box.width, self.box.height) * 0.35

        for i in range(6):
            a = i * (math.pi * 2 / 6)
            x = cx + math.cos(a) * radius
            y = cy + math.sin(a) * radius
            self.flowers.append(self.flower(x, y, a))

    def spawnBeams(self):
        kind = self.sequence[self.index]
        beamClass = blueBeam if kind == "blue" else orangeBeam
        b = beamClass(self.boundary, None, {})
        b.start()
        self.activeBeams.append(b)

    def draw(self, screen):
        for f in self.flowers:
            f.draw(screen)

        for b in self.activeBeams:
            b.draw(screen)

    def checkHit(self, soul):
        for b in self.activeBeams:
            if b.checkHit(soul):
                return True
        return False

    class flower:
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.angle = angle
            self.radius = 6
            self.reached = False

        def update(self, dt, center, circling):
            cx, cy = center

            if circling:
                self.angle += 1.2 * dt
                r = math.hypot(self.x - cx, self.y - cy)
                self.x = cx + math.cos(self.angle) * r
                self.y = cy + math.sin(self.angle) * r
            else:
                dx = cx - self.x
                dy = cy - self.y
                dist = math.hypot(dx, dy)

                if dist < 5:
                    self.reached = True
                    return

                speed = 320
                self.x += (dx / dist) * speed * dt
                self.y += (dy / dist) * speed * dt

        def draw(self, screen):
            pygame.draw.circle(screen, const.white, (int(self.x), int(self.y)), self.radius)