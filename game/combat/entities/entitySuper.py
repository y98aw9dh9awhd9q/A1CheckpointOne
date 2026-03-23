class livingEntity:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.attack = attack
        self.defense = defense

    def takeDamage(self, damage):
        self.hp -= max(1, damage - self.defense)
        self.hp = max(0, self.hp)

    def isAlive(self):
        return self.hp > 0