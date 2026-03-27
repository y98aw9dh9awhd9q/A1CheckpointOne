import math
import random
import const
from game.combat.attacks.handlers.attackBase import attackBase

class beamSpinner(attackBase):
    damage = 2
    attackTimer = 6
    volley = 1
    numBeams = 8
    spinSpeed = math.pi / 6
    beamWidth = 14
    warningTime = 0.6

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay

        cx = self.box.centerx
        cy = self.box.centery
        direction = 1 if self.volleysFired % 2 == 0 else -1

        for i in range(self.numBeams):
            angle = i * (2 * math.pi / self.numBeams)
            self.bullets.append(
                self.beam(
                    cx,
                    cy,
                    angle,
                    self.spinSpeed * direction,
                    self.beamWidth,
                    const.white,
                    self.warningTime
                )
            )

class beamSpinnerCooler(attackBase):
    damage = 3
    attackTimer = 6
    volley = 3
    volleyDelay = 2
    numBeams = 4
    spinSpeed = math.pi / 3
    beamWidth = 14
    warningTime = 0.6

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay

        cx = self.box.centerx
        cy = self.box.centery
        direction = 1 if self.volleysFired % 2 == 0 else -1

        for i in range(self.numBeams):
            angle = i * (2 * math.pi / self.numBeams)
            colorType = random.choice(["blue", "orange"])
            color = const.blue if colorType == "blue" else const.orange

            beam = self.beam(
                cx,
                cy,
                angle,
                self.spinSpeed * direction,
                self.beamWidth,
                color,
                self.warningTime
            )

            beam.colorType = colorType
            self.bullets.append(beam)

    def checkHit(self, soul):
        for bullet in self.bullets:
            if not bullet.alive:
                continue
            if not bullet.collides(soul.rect):
                continue

            if getattr(bullet, "colorType", None) == "blue" and soul.moving:
                return True
            if getattr(bullet, "colorType", None) == "orange" and not soul.moving:
                return True

        return False