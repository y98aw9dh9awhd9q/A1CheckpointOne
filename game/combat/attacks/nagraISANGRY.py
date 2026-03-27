import math
import pygame
import const
from game.combat.attacks.handlers.attackBase import attackBase

class nagraISANGRY(attackBase):
    spawnOffset = 150
    attackTimer = 9999

    toBeFired = {

        1: {"directions": [
            "u", "u", "u", "u", "u", "d", "d", "d", "d", "u", "u", "d", "u", "d","l","r","u","r","r"
        ], "speed": 220, "delay": 0.2},

        2: {"directions": [
            "u", "d", "l", "r", "u", "d", "l", "r",
            "u", "d", "l", "r", "d", "l", "r", "u"

        ], "speed": 250, "delay": 0.2},

        3: {"directions": [
            "u", "u", "u", "", "d", "d", "d", "", "l", "l", "l", "", "r", "r", "r","d","u","u","r","","d","u","l","R","d","r","l","u"
        ], "speed": 120, "delay": 0.22},

        4: {"directions": [
            "U", "U", "U", "d", "d", "d", "L", "L", "R", "R", "u", "u", "u", "D", "D","r","r","R","R","L","u","d"
        ], "speed": 140, "delay": 0.2},

        5: {"directions": [
            "u", "r", "d", "l", "u", "r", "d", "l",
            "U", "R", "D", "L", "u", "r", "d", "l",
            "u", "u", "u", "u", "u", "",
            "l", "u", "u", "U", "d", "u","","r","r"
        ], "speed": 100, "delay": 0.3},


        6: {"directions": [
            "u", "u", "d", "d", "l", "l", "r", "r",
            "U", "U", "D", "D", "L", "L", "R", "R"
            , "r", "d", "l", "u", "r", "d", "l", "U", "R", "D",
            "u", "d", "d", "l"
        ], "speed": 220, "delay": 0.4},

        7: {"directions": [
            "u", "d", "u", "d", "u", "d", "u", "d",
            "l", "r", "l", "r", "l", "r", "l", "r",
            "u", "l", "d", "r", "u", "l", "d", "r"
        ], "speed": 230, "delay": 0.4},

        8: {"directions": [
            "U", "d", "U", "d", "U", "d", "L", "r", "L", "r", "D", "u", "D", "u",
            "u", "r", "d", "l", "u", "r", "d", "l"
        ], "speed": 210, "delay": 0.3},

        9: {"directions": [
            "u", "u", "u", "u", "", "d", "d", "d", "d",
            "l", "l", "l", "l", "", "r", "r", "r", "r",
            "u", "l", "d", "r", "u", "l", "d", "r"
        ], "speed": 200, "delay": 0.3},

        10: {"directions": [
            "U", "U", "d", "d", "L", "L", "r", "r",
            "u", "u", "D", "D", "l", "l", "R", "R",
            "u", "r", "d", "l", "U", "R", "D", "L"
        ], "speed": 220, "delay": 0.3},

        11: {"directions": [
            "u", "r", "u", "r", "d", "l", "d", "l",
            "U", "R", "D", "L", "u", "r", "d", "l",
            "u", "u", "l", "l", "d", "d", "r", "r"
        ], "speed": 230, "delay": 0.3},

        12: {"directions": [
            "u", "u", "u", "d", "d", "d",
            "U", "U", "U", "D", "D", "D",
            "l", "l", "r", "r", "L", "L", "R", "R",
            "u", "l", "d", "r", "u", "l", "d", "r"
        ], "speed": 240, "delay": 0.25},

        13: {"directions": [
            "u", "d", "u", "d", "l", "r", "l", "r",
            "U", "D", "U", "D", "L", "R", "L", "R",
            "u", "l", "d", "r", "u", "l", "d", "r"
        ], "speed": 250, "delay": 0.25},

        14: {"directions": [
            "U", "U", "U", "U", "d", "d", "d", "d",
            "L", "L", "L", "L", "r", "r", "r", "r",
            "u", "l", "d", "r", "u", "l", "d", "r"
        ], "speed": 230, "delay": 0.5},

        15: {"directions": [
            "u", "r", "d", "l", "u", "r", "d", "l",
            "U", "R", "D", "L", "U", "R", "D", "L",
            "u", "r", "d", "l",
            "u", "u", "l", "l", "d", "d", "r", "r"
        ], "speed": 230, "delay": 0.35},

        16: {"directions": [
            "U", "d", "U", "d", "L", "r", "L", "r",
            "D", "u", "D", "u", "R", "l", "R", "l",
            "U", "D", "L", "R",
            "u", "r", "d", "l", "u", "r", "d", "l"
        ], "speed": 260, "delay": 0.40}
    }

    def __init__(self, boundary, attacker, roundStore=None):
        super().__init__(boundary, attacker, roundStore)
        self.box = None
        self.pendingDirs = []
        self.currentSpeed = 240
        self.currentDelay = 0.2
        self.bulletDelayTimer = 0.0
        self.roundDone = False

    def start(self):
        self.running = True
        self.done = False
        self.timer = 0.0
        self.bullets = []
        self.box = None
        self.pendingDirs = []
        self.bulletDelayTimer = 0.0
        self.roundDone = False

    def getCurrentRound(self):
        return self.roundStore.get("index", 1)

    def advanceRound(self):
        current = self.getCurrentRound()
        self.roundStore["index"] = (current % len(self.toBeFired)) + 1

    def fireRound(self):
        if self.box is None:
            return
        roundNum = self.getCurrentRound()
        config = self.toBeFired[roundNum]
        self.currentSpeed = config["speed"]
        self.currentDelay = config["delay"]
        self.pendingDirs = list(config["directions"])
        self.bulletDelayTimer = 0.0
        self.advanceRound()
        self.firePending()

    def firePending(self):
        if not self.pendingDirs or self.box is None:
            return

        d = self.pendingDirs.pop(0)

        if d == "":
            if self.pendingDirs:
                self.bulletDelayTimer = self.currentDelay
            return

        isUpper = d.isupper()
        du = d.upper()
        cx = float(self.box.centerx)
        cy = float(self.box.centery)
        off = self.spawnOffset
        speed = self.currentSpeed

        if du == "U":
            x, y, vx, vy    = cx, self.box.top - off, 0, speed
            mirrorX, mirrorY = cx, self.box.bottom + off
            finalVx, finalVy = 0.0, -speed
        elif du == "D":
            x, y, vx, vy    = cx, self.box.bottom + off, 0, -speed
            mirrorX, mirrorY = cx, self.box.top - off
            finalVx, finalVy = 0.0, speed
        elif du == "L":
            x, y, vx, vy    = self.box.left - off, cy, speed, 0
            mirrorX, mirrorY = self.box.right + off, cy
            finalVx, finalVy = -speed, 0.0
        elif du == "R":
            x, y, vx, vy    = self.box.right + off, cy, -speed, 0
            mirrorX, mirrorY = self.box.left - off, cy
            finalVx, finalVy = speed, 0.0
        else:
            if self.pendingDirs:
                self.bulletDelayTimer = self.currentDelay
            return

        self.bullets.append(greenBullet(
            x, y, vx, vy, 16, self.damage,
            isUpper=isUpper,
            mirrorX=mirrorX, mirrorY=mirrorY,
            finalVx=finalVx, finalVy=finalVy,
            speed=speed, boxCx=cx, boxCy=cy,
        ))

        if self.pendingDirs:
            self.bulletDelayTimer = self.currentDelay

    def update(self, dt, box):
        if not self.running:
            return

        self.box = box
        self.timer += dt

        if not self.pendingDirs and not self.roundDone and not self.bullets:
            self.fireRound()
            self.roundDone = True

        if self.pendingDirs:
            self.bulletDelayTimer -= dt
            if self.bulletDelayTimer <= 0:
                self.firePending()

        for b in self.bullets:
            b.update(dt, box)
        self.bullets = [b for b in self.bullets if b.alive]

        for b in self.bullets:
            b.isRed = False
        for b in self.bullets:
            if not (b.isUpper and not b.arcDone):
                b.isRed = True
                break

        if self.roundDone and not self.bullets and not self.pendingDirs:
            self.done = True
            self.running = False

    def checkHit(self, soul):
        shieldRect = soul.getShieldRect() if hasattr(soul, "getShieldRect") else None
        for b in self.bullets:
            if not b.alive:
                continue
            if shieldRect and b.rect.colliderect(shieldRect):
                print("sfx")
                b.alive = False
                continue
            if b.rect.colliderect(soul.rect) and not soul.moving:
                b.alive = False
                soul.damage(self.damage)
        return False

    def draw(self, screen):
        for b in self.bullets:
            b.draw(screen)

class greenBullet:
    arcAnimTime = 0.4
    def __init__(self, x, y, vx, vy, size, damage, isUpper=False, mirrorX=0.0, mirrorY=0.0, finalVx=0.0, finalVy=0.0, speed=240.0, boxCx=0.0, boxCy=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.damage = damage
        self.alive = True
        self.enteredBox = False
        self.isRed = False
        self.isUpper = isUpper
        self.speed = speed
        self.mirrorX = mirrorX
        self.mirrorY = mirrorY
        self.finalVx = finalVx
        self.finalVy = finalVy
        self.boxCx = boxCx
        self.boxCy = boxCy
        self.halfDist = math.hypot(boxCx - x, boxCy - y) / 2.0
        self.distTravelled = 0.0
        self.arcDone = not isUpper
        self.arcAnimating = False
        self.arcTimer = 0.0
        self.arcCx = 0.0
        self.arcCy = 0.0
        self.arcRadius = 0.0
        self.arcAngleStart = 0.0
        self.arcAngleDiff = 0.0

    def startArc(self):
        self.arcCx = (self.x + self.mirrorX) / 2.0
        self.arcCy = (self.y + self.mirrorY) / 2.0
        self.arcRadius = math.hypot(self.x - self.arcCx, self.y - self.arcCy)

        self.arcAngleStart = math.atan2(self.y - self.arcCy, self.x - self.arcCx)
        endAngle = math.atan2(self.mirrorY - self.arcCy, self.mirrorX - self.arcCx)

        diff = endAngle - self.arcAngleStart
        if diff > math.pi:
            diff -= math.tau
        elif diff < -math.pi:
            diff += math.tau
        self.arcAngleDiff = diff
        self.arcTimer = 0.0
        self.arcAnimating = True

    def update(self, dt, box):
        if self.arcAnimating:
            self.arcTimer += dt
            frac  = min(1.0, self.arcTimer / self.arcAnimTime)
            angle = self.arcAngleStart + self.arcAngleDiff * frac
            self.x = self.arcCx + math.cos(angle) * self.arcRadius
            self.y = self.arcCy + math.sin(angle) * self.arcRadius

            if self.arcTimer >= self.arcAnimTime:
                self.arcAnimating = False
                self.arcDone = True
                self.x = self.mirrorX
                self.y = self.mirrorY
                self.vx = self.finalVx
                self.vy = self.finalVy
                extra = self.arcTimer - self.arcAnimTime
                self.x += self.vx * extra
                self.y += self.vy * extra
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        if not self.arcDone:
            self.distTravelled += self.speed * dt
            if self.distTravelled >= self.halfDist:
                overshoot  = self.distTravelled - self.halfDist
                self.x -= self.vx * (overshoot / self.speed)
                self.y -= self.vy * (overshoot / self.speed)
                self.startArc()
            return

        inside = box.collidepoint(self.x, self.y)
        if inside:
            self.enteredBox = True
        if self.enteredBox and not inside:
            self.alive = False

    def draw(self, screen):
        if self.isRed:
            color = const.red
        elif self.isUpper and not self.arcDone:
            color = const.yellow
        else:
            color = const.blue
        pygame.draw.rect(screen, color,(int(self.x) - self.size // 2, int(self.y) - self.size // 2, self.size, self.size))

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x) - self.size // 2,
            int(self.y) - self.size // 2,
            self.size, self.size
        )