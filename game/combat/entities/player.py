from game.combat.entities import entitySuper

class player(entitySuper.livingEntity):
    def __init__(self, saveData, name="LIBOR",):
        super().__init__(name, saveData["hp"], saveData["attack"], saveData["defence"])
        self.level = saveData["level"]
        self.gold = saveData["gold"]
        self.maxHp = saveData["maxHp"]
        self.hp = saveData["hp"]
        self.inventory = saveData["inventory"]
        self.weapon = None
        self.armor = None
        self.baseDef = saveData["baseDef"]
        self.baseATK = saveData["baseATK"]
        self.atk = saveData["attack"]
        self.LOVE = saveData["xp"]
        self.kills = saveData["kills"]

    def getAtk(self):
        return self.atk

    def getDef(self):
        return self.defense

    def equip(self, item):
        if item["type"] == "weapon":
            self.weapon = item
            self.atk = item["value"] + self.baseATK
            print(self.atk)
        elif item["type"] == "armor":
            self.armor = item
            self.defense = item["value"] + self.baseDef

    def unequip(self, item):
        if item == self.weapon:
            self.weapon = None
            self.atk = self.baseATK
        elif item == self.armor:
            self.armor = None
            self.defense = self.baseDef

    def useItem(self, item):
        if item["type"] == "potion":
            self.hp += item["value"]
            print(item["value"])
            if self.hp > self.maxHp:
                self.hp = self.maxHp
            if item in self.inventory:
                self.inventory.remove(item)

    def addItem(self, item):
        if len(self.inventory) >= 15:
            return False
        self.inventory.append(item)
        return True

    def removeItem(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def levelUp(self):
        self.level += 1
        self.maxHp = round(self.maxHp*1.1,2)
        self.baseATK = round(self.baseATK*1.1,2)
        self.baseDef = round(self.baseDef*1.1,2)