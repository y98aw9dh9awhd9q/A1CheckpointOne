shopNode      = "shop"
combatNode    = "combat"
questNode     = "quest"
traderNode    = "trader"
bossNode      = "boss"
black         = (0,0,0)
white         = (255,255,255)
red           = (255,0,0)
green         = (0,255,0)
blue          = (0,0,255)
yellow        = (255,255,0)
gray          = (55,55,55)
orange        = (255,255,0)
soulModeRed   = 0
soulModeGreen = 1
soulModeBlue  = 2

labels = {
    shopNode     : "Shop"   ,
    combatNode   : "Combat" ,
    questNode    : "Quest"  ,
    traderNode   : "Trader" ,
    bossNode     : "Boss"   ,
}

descriptions = {
    shopNode     : "buy stuff from shop" ,
    combatNode   : "fight enemy"         ,
    questNode    : "accept quest?"       ,
    traderNode   : "buy special stuff"   ,
    bossNode     : "WE ARE COOKING"      ,
}

fpsCap = 60

import os
baseDir   = os.path.dirname(os.path.abspath(__file__))
playerDir = os.path.join(baseDir, "assets","pictures", "player.png")


shopItems = {
    1: {"name": "healing potion", "effect": "+5 hp", "price": 10, "type": "potion","value":5},
    2: {"name": "greater healing potion", "effect": "+10 hp", "price": 20, "type": "potion","value":10},
    3: {"name": "calculator", "effect": "+2.5 attack", "price": 20, "type": "weapon", "value":2.5},
    4: {"name": "ai calculator", "effect": "+5 attack", "price": 40,"type":"weapon","value": 5},
    5: {"name": "broken hinge gigabyte laptop", "effect": "+2 armor", "price": 20,"type": "armor", "value":2},
    6: {"name": "perfume", "effect": "+5 armor", "price": 40, "type": "armor", "value": 5},
}

traderItems = {
    1: {"name": "9v battery infused capacitor", "effect": "+7 attack", "price": 50,"type": "weapon", "value": 7},
    2: {"name": "Ta'ameya (Egyptian Falafel)", "effect": "+15 hp", "price": 30, "type": "potion","value":15},
    3: {"name": "battery acid", "effect": "+20 hp", "price": 40, "type": "potion","value":20},
    4: {"name": "Bergentrück", "effect": "+67 attack", "price": 676767, "type": "weapon", "value": 67},

}

nodeChoice = [
    "combat",
    "trader",
    "chest" ,
    "quest"
]

loot ={
    1: {"name": "healing potion", "effect": "+5 hp", "price": 10, "type": "potion"},
    2: {"name": "greater healing potion", "effect": "+10 hp", "price": 20, "type": "potion"},
    3: {"name": "calculator", "effect": "+2.5 attack", "price": 20, "type": "weapon", "value":2.5},
    4: {"name": "ai calculator", "effect": "+5 attack", "price": 40,"type":"weapon","value": 5},
    5: {"name": "broken hinge gigabyte laptop", "effect": "+2 armor", "price": 20,"type": "armor", "value":2},
    6: {"name": "perfume", "effect": "+5 armor", "price": 40, "type": "armor", "value": 5},
}





