class attack:
    def __init__(self,damage=1):
        self.finished = False
        self.damage = damage

    def update(self,deltaTime):
        pass

    def draw(self,screen):
        pass

    def checkHit(self,player):
        return False