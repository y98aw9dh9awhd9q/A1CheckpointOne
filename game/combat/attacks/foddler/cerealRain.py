import random
import const
from game.combat.attacks.handlers.attackBase import attackBase, bullet

class cerealRain(attackBase):
    damage = 3
    attackTimer = 5
    volley = 7
    volleyDelay = 0.45
    speed = 300

    def fireVolley(self):
        self.volleysFired += 1
        self.volleyCooldown = self.volleyDelay
        rect = self.boundary.getRect()
        for i in range(8):
            x = random.randint(rect.left, rect.right)
            size = random.choice([12, 18])
            self.bullets.append(bullet(x, rect.top, 0, self.speed, size, size, const.white))