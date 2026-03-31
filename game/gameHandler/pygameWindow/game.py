import os
import random
import pygame

import chkSum
import const
import json

from game.gameHandler.pygameWindow import nodes
from ai.chat import generateText
from game.gameHandler.pygameWindow.soundManager import playVineBoom, playBattleMusic, stopAudio, playYippie, playboss1Music, playboss2Music, playgenocideNAgra,playGenoBoss
from game.gameHandler.shops.shop import shop as shoppersDrugMart
from game.combat.entities.player import player as pl
from game.gameHandler.shops.trader import trader as tradar
from game.gameHandler.shops.quest import quest
from game.combat.combatManager import combatManager
from game.combat.entities.enemies import createEnemy
from game.endScreen.endScreenMain import playGenoEnding

global screen
global clock
global prompts
global blueStop
global shop
global trader
global questNpc
global generatedOptions
global player
global roundCounter
global manager
global bossIndex
global nagraAlive
global killedNagra

storyState  = 0
combatState = 1

noSaveData = {
    "hp"          : 20,
    "attack"      : 2,
    "defence"     : 2,
    "level"       : 1,
    "gold"        : 100,
    "maxHp"       : 20,
    "xp"          : 0,
    "kills"       : 0,
    "baseDef"     : 2,
    "baseATK"     : 2,
    "inventory"   : [],
    "round"       : 0,
    "killedNagra" : False,
    "chkSum" : ""
}# we must use ai formatting

nagraAlive  = True
killedNagra = False
running     = True

def readSave():
    try:
        data              = chkSum.decryptSave(open('save.json').read())
        for key, val in   noSaveData.items():
            if key not in data:
                data[key] = val
        chkSum.checkCheckSum()
        return            data
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        print("save error")
        return dict(noSaveData)

def saveGame():
    data = {
        "hp"          : player.hp,
        "attack"      : player.atk,
        "defence"     : player.defense,
        "level"       : player.level,
        "gold"        : player.gold,
        "maxHp"       : player.maxHp,
        "xp"          : player.xp,
        "kills"       : player.kills,
        "baseDef"     : player.baseDef,
        "baseATK"     : player.baseATK,
        "inventory"   : player.inventory,
        "round"       : roundCounter,
        "killedNagra" : killedNagra,
        "chkSum"      : ""
    }#and stick with it
    with open('save.json', 'w') as file:
        file.write(chkSum.encryptSave(data))

    data["chkSum"] = chkSum.chkSumGen()
    with open('save.json', 'w') as file:
        file.write(chkSum.encryptSave(data))


def startDisplay():
    pygame.init()
    pygame.display.set_caption("PharohTale")

    try:
        pygame.mixer.init()
    except:
        print("audio failed")

    global screen, clock
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()

    global shop, player, generatedOptions, trader, questNpc, roundCounter, manager, bossIndex, killedNagra

    save             = readSave()
    player           = pl(save)
    shop             = shoppersDrugMart(screen, player)
    trader           = tradar(screen, player)
    questNpc         = quest(screen, player)
    generatedOptions = False
    roundCounter     = save["round"]
    killedNagra      = save["killedNagra"]
    manager          = combatManager(screen, player, killedNagra)
    bossIndex        = 1


def generatePromts():
    global prompts
    prompts = ["physics"]
    for i in range(20):
        promptChosen = random.choice(prompts)
        prompts.append(
            generateText(
                promptChosen,
                length=20,
                temperature=random.randint(1, 20) / 10
            ).removeprefix(promptChosen)
        )
    prompts = list(set(prompts))

def generateStory():
    promtChosen = random.choice(prompts)
    story = generateText(
        promtChosen,
        length=100,
        temperature=random.randint(10, 30) / 10
    ).removeprefix(promtChosen)
    return story

def resetTypeWriter():
    if hasattr(typeWrite, "index"):
        del typeWrite.index

def typeWrite(screen, text):
    if not hasattr(typeWrite, "index"):
        typeWrite.index = 0
        typeWrite.lastUpdate = pygame.time.get_ticks()
        typeWrite.font       = pygame.font.SysFont("Arial", 24)
        words                = text.split(' ')
        lines                = []
        currentLine          = []
        maxWidth             = screen.get_width() - 40

        for word in words:
            testLine = ' '.join(currentLine + [word])
            if typeWrite.font.size(testLine)[0] < maxWidth:
                currentLine.append(word)
            else:
                lines.append(' '.join(currentLine))
                currentLine = [word]

        lines.append(' '.join(currentLine))
        typeWrite.wrappedLines = lines

    now = pygame.time.get_ticks()
    if now - typeWrite.lastUpdate > 10:
        typeWrite.index += 1
        typeWrite.lastUpdate = now

    charsToShow = typeWrite.index
    yOffset = 470

    for line in typeWrite.wrappedLines:
        if charsToShow <= 0:
            break
        visibleText = line[:charsToShow]
        surf = typeWrite.font.render(visibleText, True, const.white)
        screen.blit(surf, (20, yOffset))
        charsToShow -= len(line) + 1
        yOffset += typeWrite.font.get_linesize()
    return charsToShow > 0

def giveChestLoot():
    text                          = pygame.font.SysFont("Arial", 22)
    itemName                      = random.choice(list(const.loot.keys()))
    item                          = const.loot[itemName]
    if len(player.inventory) < 20:
        player.inventory.append(item)
        written                   = text.render(f"you got {itemName}", True, const.red)
    else:
        written                   = text.render(f"no loot for you", True, const.red)
    screen.blit(written, (20, 430))
    pygame.display.flip()

def generateNodeChoices(bossRound):
    if bossRound:
        return ["boss", "boss", "boss"]
    else:
        while True:
            choices = random.choices(const.nodeChoice, k=3)
            if "trader" in choices and player.kills > 10:
                choices = ["dead" if x == "trader" else x for x in choices]
            if "quest" in choices and player.kills > 10:
                choices = ["dead" if x == "quest" else x for x in choices]
            if "combat" in choices:
                print(choices)
                return choices

def nextRound(incrementRound=True):
    global roundCounter, generatedOptions, rah, storyText, bossIndex, running

    if incrementRound:
        roundCounter += 1
    screen.fill(const.black)
    resetTypeWriter()
    storyGenerated = generateStory().splitlines()
    storyText = " ".join(storyGenerated)
    generatedOptions = True
    player.hp = player.maxHp
    print(f"player kills: {player.kills}")
    saveGame()

    match roundCounter:
        case 10:
            rah = generateNodeChoices(True)
            if player.kills                >= 10:
                bossIndex                   = 10
            else:
                bossIndex                   = 1
        case 20:
            if player.kills >= 20 and killedNagra:
                bossIndex                   = 11
            else:
                bossIndex                   = 2
            print("pharoh is here")
            rah                             = generateNodeChoices(True)
        case 21:
            rah                             = generateNodeChoices(True)
            bossIndex                       = 3
        case 22:
            if(playGenoEnding()):
                running                     = False
        case _:
            rah                             = generateNodeChoices(False)

def startGame():
    global enemyCount, bossIndex, toBeUsedEnemies, killedNagra

    print("started game")
    state                   = storyState
    drawnNode               = False
    shopWasOpen             = False
    traderWasOpen           = False
    questWasOpen            = False
    toBeUsedEnemies         = []
    nextRound(roundCounter <= 0)
    global running

    while running:
        events             = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running    = False

        deltaTime          = clock.tick(const.fpsCap) / 1000

        if trader.active:
            traderWasOpen  = True
            screen.fill(const.black)
            trader.update(events)
            trader.draw()
        elif shop.active:
            shopWasOpen    = True
            screen.fill(const.black)
            shop.update(events)
            shop.draw()
        elif questNpc.active:
            questWasOpen   = True
            screen.fill(const.black)
            questNpc.update(events)
            questNpc.draw()
        else:
            if traderWasOpen or questWasOpen:
                drawnNode      = False
                traderWasOpen  = False
                questWasOpen   = False
                nextRound()
            if shopWasOpen:
                drawnNode      = False
                shopWasOpen    = False

            if state == storyState:
                finished = typeWrite(screen, storyText)
                if finished:
                    if not drawnNode:
                        nodes.initNodes(rah[0], rah[1], rah[2])
                        nodes.drawPath(screen)
                        nodes.putNodes(screen)
                        drawnNode = True
                        nodes.putPlayer(screen)
                        playVineBoom()
                    nodeCheck = nodes.checkClickNoInit()

                    if nodeCheck is not None:
                        match nodeCheck.lower():
                            case "shop": shop.open()
                            case "trader": trader.open()
                            case "quest": questNpc.open()
                            case "chest":
                                giveChestLoot()
                                nextRound()
                                drawnNode = False
                            case "dead":
                                playVineBoom()
                                deadImage = pygame.image.load(
                                    os.path.join(const.baseDir, "assets", "pictures", "deadOption.png")
                                )
                                deadImage = pygame.transform.flip(deadImage, 180, 0)
                                deadImage = pygame.transform.scale(deadImage, (900, 600))
                                screen.blit(deadImage, (0, 0))
                                pygame.display.flip()
                                frameCounter = 0
                                while frameCounter < 2000:
                                    frameCounter += 1
                                    playVineBoom()
                                nextRound()
                                drawnNode = False

                            case "boss":
                                state = combatState
                                screen.fill(const.black)
                                pygame.display.flip()
                                enemyCount = 1
                                print(bossIndex)
                                toBeUsedEnemies = [createEnemy(roundCounter, player.level, bossIndex)]
                                manager.startBattle(toBeUsedEnemies)
                                goldCalculatable = True
                                manager.soulMode = 1
                                print("boss started")
                                match bossIndex:
                                    case 1:  playboss1Music()
                                    case 2:  playboss2Music()
                                    case 10: playgenocideNAgra()
                                    case 11: playboss2Music()
                                    case 3: playGenoBoss()

                            case _:
                                state = combatState
                                screen.fill(const.black)
                                pygame.display.flip()
                                enemyCount = random.randint(1, 3)
                                toBeUsedEnemies = [createEnemy(roundCounter, player.level) for _ in range(enemyCount)]
                                manager.startBattle(toBeUsedEnemies)
                                goldCalculatable = True
                                playBattleMusic()
                                print("started combat")

            elif state == combatState:
                if not manager.started:
                    toBeUsedEnemies = [createEnemy(roundCounter, player.level)]
                    manager.startBattle(toBeUsedEnemies)

                if goldCalculatable:
                    goldCalculated = 0
                    for i in range(len(manager.enemies)):
                        try:
                            goldCalculated += manager.enemies[i].gold
                        except:
                            goldCalculated += manager.gold
                    goldCalculatable = False
                    print(f"calculated {goldCalculated} gold to add")

                manager.update(deltaTime, events)
                manager.draw()

                if manager.battleOver:
                    stopAudio()
                    if manager.badEnding:
                        print("bad ending triggered")
                        running = False
                    elif manager.goodEnding:
                        print("good ending triggered")
                        running = False
                    elif manager.victory:
                        player.levelUp()
                        playYippie()
                        if bossIndex in (1, 10):
                            killedNagra = not manager.MERCY
                            manager.killedNagra = killedNagra
                            print(f"killedNagra: {killedNagra}")
                        manager.reset()
                        state = storyState
                        drawnNode = False
                        screen.fill(const.black)
                        nextRound()
                        if not manager.MERCY:
                            player.gold += goldCalculated
                            player.kills += enemyCount
                        else:
                            player.gold += goldCalculated * 0.6
                    else:
                        if player.hp <= 0:
                            print("reset hp")
                            player.hp = manager.hpSnapshot
                        for e in toBeUsedEnemies:
                            e.hp = e.maxHp
                            e.alive = True
                            if hasattr(e, "attackRoundIndex"):
                                e.attackRoundIndex.clear()
                        if bossIndex in (1, 2, 3, 10, 11):
                            match bossIndex:
                                case 1:  playboss1Music()
                                case 2:  playboss2Music()
                                case 10: playgenocideNAgra()
                                case 11: playboss2Music()
                                case 3: playGenoBoss()
                        else:
                            playBattleMusic()
                        manager.startBattle(toBeUsedEnemies)

            if state == storyState:
                roundSurf = pygame.font.SysFont("Arial", 20).render(f"Round {roundCounter}", True, const.white)
                screen.blit(roundSurf, (780, 10))

        pygame.display.flip()