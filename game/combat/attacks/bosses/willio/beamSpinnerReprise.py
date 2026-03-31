import math
import random
import const
from game.combat.attacks.handlers.attackBase import attackBase

#the easy one <3
class beamSpinnerReprise(attackBase):
    damage = 5
    attackTimer = 6
    volley = 1
    numBeams = 12
    spinSpeed = math.pi / 3
    beamWidth = 20
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