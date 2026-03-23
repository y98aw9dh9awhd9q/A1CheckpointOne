import random
import const
from game.combat.attacks.handlers.attackBase import attackBase, bullet

class blueBeam(attackBase):
    damage = 2
    attackTimer = 5
    volley = 3
    volleyDelay = 1
    speed = 250
    thickness = 16

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay
        rect = self.boundary.getRect()
        side = random.choice(["top","bottom","left","right"])
        cx = rect.centerx
        cy = rect.centery

        if side == "top":
            self.bullets.append(
                bullet(cx, rect.top, 0, self.speed, rect.width, self.thickness, const.blue)
            )

        elif side == "bottom":
            self.bullets.append(
                bullet(cx, rect.bottom, 0, -self.speed, rect.width, self.thickness, const.blue)
            )

        elif side == "left":
            self.bullets.append(
                bullet(rect.left, cy, self.speed, 0, self.thickness, rect.height, const.blue)
            )

        else:
            self.bullets.append(
                bullet(rect.right, cy, -self.speed, 0, self.thickness, rect.height, const.blue)
            )

    def canHit(self, soul):
        return soul.moving