from game.combat.attacks.nagraISANGRY import nagraISANGRY
from game.combat.combatMenu.boundaryLogic.boundary import boundaryLogic
from game.combat.attacks.nagraIsGrinch import nagraIsGrinch
#bro so special he needs to be imported
class attackHandler:
    def __init__(self, screen, player):
        self.screen = screen
        self.boundary = None
        self.active = False
        self.attacks = []
        self.turnTimer = 0.0
        self.turnDuration = 0.0
        self.endCalled = False
        self.player = player

    def startTurn(self, enemyAttacks, greenSoul=False):
        isGreen = greenSoul or any(
            (atkClass is nagraIsGrinch or atkClass is nagraISANGRY)
            for entry in enemyAttacks
            for atkClass in [entry[0] if isinstance(entry, tuple) else entry]
        )
        if isGreen:
            self.boundary = boundaryLogic(self.screen, self.player, 25, True)
        else:
            self.boundary = boundaryLogic(self.screen, self.player)

        self.attacks = []
        self.turnTimer = 0.0
        self.endCalled = False

        chosen = []
        for entry in enemyAttacks:
            if isinstance(entry, tuple) and len(entry) == 3:
                atkClass, attacker, roundStore = entry
                inst = atkClass(self.boundary, attacker, roundStore)
            elif isinstance(entry, tuple) and len(entry) == 2:
                atkClass, attacker = entry
                inst = atkClass(self.boundary, attacker, {})
            else:
                inst = entry(self.boundary, None, {})
            chosen.append(inst)

        self.turnDuration = max(a.attackTimer for a in chosen)

        for atk in chosen:
            atk.start()
            self.boundary.addAttack(atk)
            self.attacks.append(atk)

        self.active = True

    def update(self, dt):
        if not self.active or not self.boundary:
            return
        self.turnTimer += dt
        self.boundary.update(dt)

        allDone = all(a.done for a in self.attacks)

        if allDone and not self.endCalled:
            self.boundary.endBox()
            self.endCalled = True

        if self.turnTimer >= self.turnDuration and not self.endCalled:
            self.boundary.endBox()
            self.endCalled = True

        if self.boundary.getState() == boundaryLogic.stateDone:
            self.active = False

    def draw(self):
        if self.boundary:
            self.boundary.draw()

    def isDone(self):
        return not self.active

    def getSoulHp(self):
        if self.boundary and self.boundary.player:
            return self.boundary.player.hp
        return None

    def soulAlive(self):
        if self.boundary and self.boundary.player:
            return self.boundary.player.hp > 0
        return True

    def reset(self):
        self.boundary = None
        self.active = False
        self.attacks = []
        self.turnTimer = 0.0
        self.turnDuration = 0.0
        self.endCalled = False