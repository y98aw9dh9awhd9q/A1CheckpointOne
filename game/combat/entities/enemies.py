import random

from game.combat.attacks.nagraISANGRY import nagraISANGRY
from game.combat.attacks.nagraIsGrinch import nagraIsGrinch
from game.combat.entities.enemy import enemy
from game.combat.attacks.blueBeam import blueBeam
from game.combat.attacks.orangeBeam import orangeBeam
from game.combat.attacks.catClaw import catClaw
from game.combat.attacks.cerealRain import cerealRain
from game.combat.attacks.keyspinnah import keySpinnah
from game.combat.attacks.beamSpinner import beamSpinner, beamSpinnerCooler

scale = (120, 120)

def cat(playerLevel=1):
    hp = 18 + playerLevel
    e = enemy("Cat", hp, 2, 2, "cat.png", scale, 5)
    e.attacks = [catClaw]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 0
    return e

def cerealBowl(playerLevel=1):
    hp = 22 + playerLevel
    e = enemy("Cereal Bowl", hp, 3, 3, "cereal bowl.png", scale, 10)
    e.attacks = [orangeBeam, blueBeam, cerealRain]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 0
    e.isPharoh = False
    return e

def keyno(playerLevel=1):
    hp = 30 + playerLevel * 2
    e = enemy("Keyno", hp, 4, 4, "keyno.png", scale, 15)
    e.attacks = [keySpinnah]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 1
    e.isPharoh = False
    return e

def rust(playerLevel=1):
    hp = 35 + playerLevel * 2
    e = enemy("Rust", hp, 5, 4, "rust.png", scale, 20)
    e.attacks = [orangeBeam]
    e.attackRoundIndex = {}
    e.mercyable = False
    e.mercyTurns = 0
    e.isPharoh = False
    return e

def worm(playerLevel=1):
    hp = 40 + playerLevel * 2
    e = enemy("Worm", hp, 6, 5, "worm.png", scale, 25)
    e.attacks = [blueBeam, orangeBeam]
    e.attackRoundIndex = {}
    e.mercyable = False
    e.mercyTurns = 0
    e.isPharoh = False
    return e

def circleAngel(playerLevel=1):
    hp = 50 + playerLevel * 3
    e = enemy("Circle Angel", hp, 7, 6, "circle angel thing.png", scale, 30)
    e.attacks = [beamSpinnerCooler, beamSpinner]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 2
    e.isPharoh = False
    return e

def nagraNotGeno(playerLevel=1):
    hp = 100
    e = enemy("NAGRA", hp, 5, 5, "nagraNotGeno.png", scale, 100)
    e.attacks = [nagraIsGrinch]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 10
    e.isPharoh = False
    return e

def nagraGeno(playerLevel=1):
    hp = 250 + playerLevel * 2
    e = enemy("NAGRA >:(", hp, 8, 6, "nagraGeno.png", scale, 100)
    e.attacks = [nagraISANGRY]
    e.attackRoundIndex = {}
    e.mercyable = False
    e.mercyTurns = 0
    e.isPharoh = False
    return e

def pharoh(playerLevel=1):
    hp = 99999999
    e = enemy("PHAROH", hp, 10, 8, "pharoh.png", scale, 130)
    e.attacks = [nagraIsGrinch]
    e.attackRoundIndex = {}
    e.mercyable = True
    e.mercyTurns = 1
    e.isPharoh = True
    return e

def pharohGeno(playerLevel=1):
    hp = 99999999
    e = enemy("PHAROH", hp, 10, -99999999999999999, "pharoh.png", scale, 130)
    e.attacks = [nagraIsGrinch]
    e.attackRoundIndex = {}
    e.mercyable = False
    e.mercyTurns = 0
    e.isPharoh = True
    return e

def genoBoss(playerlevel = 20):
    hp = 1500
    e = enemy("willio", hp, 10, 10, "genoBoss.png", scale, 6767)
    e.attacks = [nagraIsGrinch]
    e.attackRoundIndex = {}
    e.mercyable = False
    e.mercyTurns = 0
    e.isPharoh = False
    return e

roster = [cat, cerealBowl, keyno, circleAngel]

def createEnemy(roundNum, playerLevel, bossIndex=0):
    print(bossIndex)
    match bossIndex:
        case 0:
            maxIndex = min(len(roster) - 1, roundNum // 3)
            fn = random.choice(roster[:maxIndex + 1])
        case 1:  fn = nagraNotGeno
        case 2:  fn = pharoh
        case 10: fn = nagraGeno
        case 11: fn = pharohGeno
        case 3: fn = genoBoss
    return fn(playerLevel)