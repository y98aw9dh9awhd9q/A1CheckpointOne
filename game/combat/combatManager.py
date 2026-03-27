import random
import pygame
import const
from game.gameHandler.pygameWindow.soundManager import playVineBoom
from game.combat.entities.enemyDrawer import enemyDrawer
from game.combat.attacks.handlers.attackHandler import attackHandler

class damagePopup:
    def __init__(self, x, y, amount, color):
        self.x = x
        self.y = y
        self.amount = amount
        self.color = color
        self.alpha = 255.0
        self.alive = True
        self.font = pygame.font.SysFont("Arial", 22, bold=True)

    def update(self, dt):
        self.y -= 55 * dt
        self.alpha -= 290 * dt
        if self.alpha <= 0:
            self.alive = False

    def draw(self, surf):
        s = self.font.render(f"-{self.amount}", True, self.color)
        s.set_alpha(max(0, int(self.alpha)))
        surf.blit(s, (int(self.x) - s.get_width() // 2, int(self.y)))


class combatManager:
    screenW = 900
    screenH = 600
    panelY = 420
    btnW = 130
    btnH = 44
    btnGap = 16
    menuLabels = ["FIGHT", "SKIP", "ITEM", "MERCY"]
    stateMenu          = "menu"
    stateTargetSelect  = "targetSelect"
    stateFightAnim     = "fightAnim"
    stateDodging       = "dodging"
    stateAct           = "act"
    stateItem          = "item"
    stateMercy         = "mercy"
    stateWin           = "win"
    stateLose          = "lose"
    statePharohGoodEnd = "pharohGoodEnd"
    statePharohBadEnd  = "pharohBadEnd"

    def __init__(self, screen, player, killedNagra=False):
        self.MERCY = False
        self.enemyLogger = []
        self.screen = screen
        self.player = player
        self.killedNagra = killedNagra
        self.enemies = []
        self.started = False
        self.battleOver = False
        self.victory = False
        self.goodEnding = False
        self.badEnding = False
        self.state = self.stateMenu
        self.selected = 0
        self.targeted = 0
        self.animTimer = 0.0
        self.cutsceneTimer = 0.0
        self.msg = ""
        self.hpFlash = 0.0
        self.popups = []
        self.hpSnapshot = 0
        self.itemCursor = 0
        self.drawer = enemyDrawer()
        self.attHandler = attackHandler(screen, player)
        self.fontLarge = pygame.font.SysFont("Arial", 28, bold=True)
        self.fontMed   = pygame.font.SysFont("Arial", 22, bold=True)
        self.fontSmall = pygame.font.SysFont("Arial", 16, bold=True)
        self.gold = 10

    def startBattle(self, enemies):
        self.enemies = enemies[:3]
        self.started = True
        self.battleOver = False
        self.victory = False
        self.goodEnding = False
        self.badEnding = False
        self.MERCY = False
        self.state = self.stateMenu
        self.selected = 0
        self.targeted = 0
        self.popups = []
        self.msg = ""
        self.hpFlash = 0.0
        self.attHandler.reset()
        self.hpSnapshot = self.player.hp
        self.itemCursor = 0
        self.turnsInBattle = 0
        self.attackedThisTurn = False
        self.cutsceneTimer = 0.0

    def reset(self):
        self.started = False
        self.enemies = []
        self.attHandler.reset()

    def update(self, dt, events):
        if self.battleOver:
            return

        keyEvents = [e for e in events if e.type == pygame.KEYDOWN]

        if self.state == self.stateMenu:
            self.updateMenu(keyEvents)
        elif self.state == self.stateTargetSelect:
            self.updateTargetSelect(keyEvents)
        elif self.state == self.stateFightAnim:
            self.updateFightAnim(dt)
        elif self.state == self.stateDodging:
            self.updateDodging(dt)
        elif self.state in (self.stateAct, self.stateItem, self.stateMercy):
            self.updateSubMenu(keyEvents)
        elif self.state in (self.stateWin, self.stateLose):
            self.updateEnd(keyEvents)
        elif self.state == self.statePharohGoodEnd:
            self.updatePharohGoodEnd(dt, keyEvents)
        elif self.state == self.statePharohBadEnd:
            self.updatePharohBadEnd(dt, keyEvents)

        for entity in self.enemies:
            entity.update(dt)

        self.popups = [p for p in self.popups if p.alive]
        for p in self.popups:
            p.update(dt)

        self.hpFlash = max(0.0, self.hpFlash - dt)

    def draw(self):
        surf = self.screen
        surf.fill(const.black)

        if self.state not in (self.stateDodging, self.statePharohGoodEnd, self.statePharohBadEnd):
            showHp = self.state in (self.stateTargetSelect, self.stateFightAnim)
            self.drawer.draw(surf, self.enemies, showHp=showHp, targeted=self.targeted)
            self.drawMsgBox(surf)

        if self.state == self.stateDodging:
            self.attHandler.draw()
            for atk in self.attHandler.attacks:
                atk.draw(self.screen)

        if self.state == self.stateFightAnim:
            self.drawFightSlash(surf)

        if self.state == self.stateItem:
            self.drawItemMenu(surf)

        if self.state in (self.statePharohGoodEnd, self.statePharohBadEnd):
            self.drawCutscene(surf)
        else:
            self.drawHud(surf)
            self.drawMenu(surf)

        for p in self.popups:
            p.draw(surf)

    def updateMenu(self, keyEvents):
        for e in keyEvents:
            if e.key in (pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % 4
            elif e.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % 4
            elif e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                self.activateMenu()

    def hasMercyableEnemies(self):
        for e in self.enemies:
            if not e.alive:
                continue
            if getattr(e, "mercyable", False) and self.turnsInBattle >= getattr(e, "mercyTurns", 0):
                return True
        return False

    def activateMenu(self):
        choice = self.menuLabels[self.selected]
        if choice == "FIGHT":
            aliveIdx = [i for i, e in enumerate(self.enemies) if e.alive]
            if not aliveIdx:
                return
            self.targeted = aliveIdx[0]
            self.state = self.stateTargetSelect
        elif choice == "SKIP":
            self.startDodge()
        elif choice == "ITEM":
            if not self.player.inventory:
                return
            self.itemCursor = 0
            self.state = self.stateItem
            self.msg = ""
        elif choice == "MERCY":
            if self.hasMercyableEnemies():
                pharohSpared = False
                for e in self.enemies:
                    if not e.alive:
                        continue
                    if getattr(e, "mercyable", False) and self.turnsInBattle >= getattr(e, "mercyTurns", 0):
                        e.alive = False
                        if getattr(e, "isPharoh", False):
                            pharohSpared = True

                if pharohSpared:
                    self.cutsceneTimer = 0.0
                    if not self.killedNagra:
                        self.state = self.statePharohGoodEnd
                    else:
                        self.state = self.statePharohBadEnd
                elif all(not e.alive for e in self.enemies):
                    self.state = self.stateWin
                    self.msg = "mercy"
                    self.victory = True
                    self.MERCY = True
                else:
                    self.startDodge()
            else:
                self.state = self.stateMercy
                self.msg = "not yet"

    def updatePharohGoodEnd(self, dt, keyEvents):
        self.cutsceneTimer += dt
        for e in keyEvents:
            if e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE) and self.cutsceneTimer > 2.0:
                self.goodEnding = True
                self.victory = True
                self.MERCY = True
                self.battleOver = True

    def updatePharohBadEnd(self, dt, keyEvents):
        self.cutsceneTimer += dt
        for e in keyEvents:
            if e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE) and self.cutsceneTimer > 2.0:
                self.badEnding = True
                self.victory = False
                self.battleOver = True

    def drawCutscene(self, surf):
        surf.fill(const.black)
        if self.state == self.statePharohGoodEnd:
            lines = [
                "HES HERE",
                "MR NAGRA",
                "good ending"
            ]
            col = const.yellow
        else:
            lines = [
                "nagra is dead",
                '"youre cooked"',
                "bad ending",
            ]
            col = const.red

        visibleLines = min(len(lines), max(1, int(self.cutsceneTimer / 0.8)))
        y = 160
        for line in lines[:visibleLines]:
            s = self.fontMed.render(line, True, col)
            surf.blit(s, (self.screenW // 2 - s.get_width() // 2, y))
            y += s.get_height() + 18
            playVineBoom()

        if self.cutsceneTimer > 2.0:
            hint = self.fontSmall.render("z or enter to continue", True, const.white)
            surf.blit(hint, (self.screenW // 2 - hint.get_width() // 2, self.screenH - 40))

    def updateTargetSelect(self, keyEvents):
        aliveIdx = [i for i, entity in enumerate(self.enemies) if entity.alive]
        for entity in keyEvents:
            if entity.key in (pygame.K_LEFT, pygame.K_a):
                pos = aliveIdx.index(self.targeted) if self.targeted in aliveIdx else 0
                self.targeted = aliveIdx[(pos - 1) % len(aliveIdx)]
            elif entity.key in (pygame.K_RIGHT, pygame.K_d):
                pos = aliveIdx.index(self.targeted) if self.targeted in aliveIdx else 0
                self.targeted = aliveIdx[(pos + 1) % len(aliveIdx)]
            elif entity.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.stateFightAnim
                self.animTimer = 0.55
                self.msg = ""
                self.attackedThisTurn = True
            elif entity.key in (pygame.K_x, pygame.K_ESCAPE):
                self.state = self.stateMenu

    def updateFightAnim(self, dt):
        self.animTimer -= dt
        if self.animTimer <= 0:
            positions = self.drawer.getPositions(len(self.enemies))
            entity = self.enemies[self.targeted]
            if entity.alive:
                atk = max(1, self.player.atk + random.randint(1, 3))
                entity.takeDamage(atk + self.player.getAtk())
                self.popups.append(damagePopup(positions[self.targeted], 40, atk, const.yellow))

            if all(not e.alive for e in self.enemies):
                self.state = self.stateWin
                self.msg = "W nagra"
                self.victory = True
            else:
                self.startDodge()

    def drawFightSlash(self, surf):
        progress = max(0.0, 1.0 - self.animTimer / 0.55)
        positions = self.drawer.getPositions(len(self.enemies))
        cx = positions[self.targeted]
        x1 = cx - 55
        x2 = cx - 55 + int(110 * progress)
        cy = 105
        for offset, width in ((-4, 2), (0, 5), (4, 2)):
            pygame.draw.line(surf, const.yellow, (x1, cy + offset), (x2, cy + offset), width)

    def startDodge(self):
        self.attHandler.reset()
        aliveEnemies = [e for e in self.enemies if e.alive]
        random.shuffle(aliveEnemies)
        turns = []
        for i, e in enumerate(aliveEnemies):
            if i > 0 and random.random() < 0.4:
                continue
            atkClass = random.choice(e.attacks)
            roundStore = getattr(e, "attackRoundIndex", {})
            turns.append((atkClass, e, roundStore))
        if not turns:
            e = aliveEnemies[0]
            atkClass = random.choice(e.attacks)
            turns.append((atkClass, e, getattr(e, "attackRoundIndex", {})))
        self.attHandler.startTurn(turns)
        self.state = self.stateDodging
        self.msg = ""

    def updateDodging(self, dt):
        self.attHandler.update(dt)

        soulHp = self.attHandler.getSoulHp()
        if soulHp is not None:
            newHp = max(0, soulHp)
            if newHp < self.player.hp:
                self.hpFlash = 0.3
            self.player.hp = newHp

        if not self.attHandler.soulAlive():
            self.state = self.stateLose
            self.msg = "skill issue"
            self.victory = False
            self.hpFlash = 0.6
            self.attHandler.reset()
            return

        if self.attHandler.isDone():
            if not self.attackedThisTurn:
                self.turnsInBattle += 1
            self.attackedThisTurn = False
            self.state = self.stateMenu
            self.selected = 0

    def updateSubMenu(self, keyEvents):
        if self.state == self.stateItem:
            self.updateItemMenu(keyEvents)
            return
        for e in keyEvents:
            if e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE, pygame.K_x, pygame.K_ESCAPE):
                self.state = self.stateMenu
                self.selected = 0
                self.msg = ""

    def updateItemMenu(self, keyEvents):
        inv = self.player.inventory
        for e in keyEvents:
            if e.key in (pygame.K_UP, pygame.K_w):
                self.itemCursor = max(0, self.itemCursor - 1)
            elif e.key in (pygame.K_DOWN, pygame.K_s):
                self.itemCursor = min(len(inv) - 1, self.itemCursor + 1)
            elif e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                if inv:
                    item = inv[self.itemCursor]
                    if item.get("type") == "potion":
                        self.player.useItem(item)
                    elif item.get("type") in ("weapon", "armor"):
                        if self.player.weapon == item or self.player.armor == item:
                            self.player.unequip(item)
                        else:
                            self.player.equip(item)
                    self.itemCursor = min(self.itemCursor, max(0, len(inv) - 1))
                    self.startDodge()
            elif e.key in (pygame.K_x, pygame.K_ESCAPE):
                self.state = self.stateMenu
                self.selected = 0

    def updateEnd(self, keyEvents):
        for e in keyEvents:
            if e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                self.battleOver = True

    def drawMsgBox(self, surf):
        skipStates = (self.stateWin, self.stateLose, self.stateMenu, self.stateFightAnim, self.stateTargetSelect, self.stateItem)
        if not self.msg or self.state in skipStates:
            return
        boxX, boxY = 30, 215
        boxW, boxH = 840, 90
        pygame.draw.rect(surf, const.black, (boxX, boxY, boxW, boxH))
        pygame.draw.rect(surf, const.white, (boxX, boxY, boxW, boxH), 3)
        y = boxY + 12
        for line in self.msg.split("*"):
            line = line.strip()
            if not line:
                continue
            ls = self.fontSmall.render("* " + line, True, const.white)
            surf.blit(ls, (boxX + 14, y))
            y += ls.get_height() + 6

    def drawItemMenu(self, surf):
        inv = self.player.inventory
        boxX, boxY = 30, 215
        boxW, boxH = 840, 185
        pygame.draw.rect(surf, const.black, (boxX, boxY, boxW, boxH))
        pygame.draw.rect(surf, const.white, (boxX, boxY, boxW, boxH), 3)

        if not inv:
            empty = self.fontSmall.render("pov youre homeless", True, const.white)
            surf.blit(empty, (boxX + 14, boxY + 12))
            return

        visibleCount = 5
        startIdx = max(0, self.itemCursor - visibleCount + 1)
        visible = inv[startIdx: startIdx + visibleCount]

        y = boxY + 12
        for i, item in enumerate(visible):
            actualIdx = startIdx + i
            isCursor = actualIdx == self.itemCursor
            itemType = item.get("type", "")
            if itemType == "potion":
                action = "use"
            elif self.player.weapon == item or self.player.armor == item:
                action = "unequip"
            else:
                action = "equip" if itemType in ("weapon", "armor") else ""
            label = f"{item['name']}  ({item.get('effect', itemType)})"
            if action:
                label += f"  [{action}]"
            col = const.yellow if isCursor else const.white
            ls = self.fontSmall.render(("* " if isCursor else "  ") + label, True, col)
            surf.blit(ls, (boxX + 14, y))
            y += ls.get_height() + 8

    def drawHud(self, surf):
        py = self.panelY
        pygame.draw.line(surf, const.white, (0, py - 2), (self.screenW, py - 2), 2)

        nameSurf = self.fontMed.render("LIBOR", True, const.yellow)
        lvSurf   = self.fontSmall.render(f"LV  {self.player.level}", True, const.white)
        surf.blit(nameSurf, (30, py + 10))
        surf.blit(lvSurf,   (30, py + 10 + nameSurf.get_height() + 2))

        hpLabel = self.fontMed.render("HP", True, const.white)
        cx   = self.screenW // 2
        barW = 220
        barH = 14
        barX = cx - barW // 2
        barY = py + 18

        frac = max(0.0, self.player.hp / max(1, self.player.maxHp))
        if self.hpFlash > 0:
            barCol = const.white
        elif frac < 0.25:
            barCol = const.red
        else:
            barCol = const.yellow

        surf.blit(hpLabel, (barX - hpLabel.get_width() - 10, barY + barH // 2 - hpLabel.get_height() // 2))
        pygame.draw.rect(surf, const.gray,  (barX, barY, barW, barH))
        pygame.draw.rect(surf, barCol,      (barX, barY, int(barW * frac), barH))
        pygame.draw.rect(surf, const.white, (barX, barY, barW, barH), 2)

        hpNums = self.fontSmall.render(f"{max(0, int(self.player.hp))}  /  {int(self.player.maxHp)}", True, const.white)
        surf.blit(hpNums, (barX + barW + 10, barY + barH // 2 - hpNums.get_height() // 2))

    def drawMenu(self, surf):
        if self.state in (self.stateWin, self.stateLose):
            col = const.yellow if self.state == self.stateWin else const.red
            msgSurf  = self.fontLarge.render(self.msg, True, col)
            surf.blit(msgSurf, (self.screenW // 2 - msgSurf.get_width() // 2, self.panelY + 90))
            contSurf = self.fontSmall.render("z or enter", True, const.white)
            surf.blit(contSurf, (self.screenW // 2 - contSurf.get_width() // 2, self.panelY + 130))
            return

        if self.state == self.stateDodging:
            return

        totalW = 4 * self.btnW + 3 * self.btnGap
        startX = (self.screenW - totalW) // 2
        btnY   = self.panelY + 68
        canMercy = self.hasMercyableEnemies()

        for i, label in enumerate(self.menuLabels):
            bx = startX + i * (self.btnW + self.btnGap)
            isSelected = (i == self.selected) and (self.state == self.stateMenu)
            isMercyBtn = label == "MERCY"

            bgCol = const.white if isSelected else const.black
            fgCol = const.black if isSelected else (const.yellow if isMercyBtn and canMercy else const.white)

            pygame.draw.rect(surf, bgCol, (bx, btnY, self.btnW, self.btnH))
            borderCol = const.yellow if isMercyBtn and canMercy and not isSelected else const.white
            pygame.draw.rect(surf, borderCol, (bx, btnY, self.btnW, self.btnH), 2)

            if isSelected:
                acx = bx + 14
                acy = btnY + self.btnH // 2
                pygame.draw.polygon(surf, const.red, [
                    (acx, acy),
                    (acx - 10, acy - 7),
                    (acx - 10, acy + 7),
                ])

            txt = self.fontMed.render(label, True, fgCol)
            surf.blit(txt, (bx + self.btnW // 2 - txt.get_width() // 2, btnY + self.btnH // 2 - txt.get_height() // 2))