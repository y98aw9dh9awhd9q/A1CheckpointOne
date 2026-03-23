import pygame
import const
import game.gameHandler.pygameWindow.soundManager as SM
from game.gameHandler.pygameWindow.soundManager import playVineBoom

class trader:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont("Arial", 28)
        self.smallFont = pygame.font.SysFont("Arial", 20)
        self.itemRects = {}
        self.equipRects = {}
        self.exitRect = None
        self.active = False

    def open(self):
        self.active = True

    def close(self):
        self.active = False

    def update(self, events):
        if not self.active:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in self.itemRects.items():
                    if rect.collidepoint(pos):
                        item = const.traderItems[i]
                        if not self.player.addItem(item):
                            print("inventory full")
                            playVineBoom()
                            return
                        if self.player.gold >= item["price"]:
                            self.player.gold -= item["price"]
                            print("bought", item["name"])
                            playVineBoom()
                        else:
                            self.player.inventory.remove(item)
                            print("brokie")
                            playVineBoom()
                for i, rect in self.equipRects.items():
                    if rect.collidepoint(pos):
                        item = self.player.inventory[i]
                        if item["type"] in ["weapon", "armor"]:
                            if self.player.weapon == item or self.player.armor == item:
                                self.player.unequip(item)
                                print("unequipped", item["name"])
                            else:
                                self.player.equip(item)
                                print("equipped", item["name"])
                        elif item["type"] == "potion":
                            self.player.useItem(item)
                            print("Used", item["name"])
                if self.exitRect and self.exitRect.collidepoint(pos):
                    self.close()

    def draw(self):
        if not self.active:
            return
        self.screen.fill(const.black)
        title = self.font.render("shop", True, const.white)
        self.screen.blit(title, (410,40))
        goldText = self.smallFont.render(f"Gold: {self.player.gold}", True, const.white)
        self.screen.blit(goldText, (20,20))
        atkText = self.smallFont.render(f"ATK: {self.player.getAtk()}", True, const.white)
        defText = self.smallFont.render(f"DEF: {self.player.getDef()}", True, const.white)
        hpText = self.smallFont.render(f"HP: {self.player.hp}/{self.player.maxHp}", True, const.white)
        self.screen.blit(atkText,(20,60))
        self.screen.blit(defText,(20,90))
        self.screen.blit(hpText,(20,120))
        y = 200
        self.itemRects = {}
        for i,item in const.traderItems.items():
            text = f"{item['name']} ({item.get('effect','')}) - {item['price']}g"
            surf = self.smallFont.render(text, True, const.white)
            rect = surf.get_rect(topleft=(120,y))
            self.screen.blit(surf,rect)
            self.itemRects[i] = rect
            y += 60
        invTitle = self.smallFont.render(f"inventory {len(self.player.inventory)}/15:", True, const.white)
        self.screen.blit(invTitle,(600,0))
        invY = 50
        self.equipRects = {}
        for i,item in enumerate(self.player.inventory):
            invText = self.smallFont.render(item["name"], True, const.white)
            self.screen.blit(invText,(600,invY))
            label = "unequip" if item == self.player.weapon or item == self.player.armor else ("use" if item["type"]=="potion" else "equip")
            equipSurf = self.smallFont.render(label, True, const.white)
            equipRect = equipSurf.get_rect(topleft=(850,invY))
            self.screen.blit(equipSurf,equipRect)
            self.equipRects[i] = equipRect
            invY += 30
        exitText = self.font.render("exit", True, const.white)
        self.exitRect = exitText.get_rect(center=(450,540))
        self.screen.blit(exitText,self.exitRect)