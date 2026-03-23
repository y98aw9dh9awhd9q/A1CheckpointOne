import pygame
import const

class soul:
    soulSpeed = 220
    immuFrameTime = 0.5
    def __init__(self, pos, player, soulMode):
        self.image = pygame.image.load(const.playerDir)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.hp = player.hp
        self.moving = False
        self.invincibilityTimer = 0
        self.pos = pos
        self.centerSelf = True
        self.soulMode = soulMode
        self.prevSoulMode = soulMode
        self.shieldDir = 0

    def getShieldRect(self):
        if not self.soulMode:
            return None
        if self.shieldDir == 0:
            return pygame.Rect(self.rect.centerx - 20, self.rect.top - 10, 40, 10)
        elif self.shieldDir == 1:
            return pygame.Rect(self.rect.centerx - 20, self.rect.bottom, 40, 10)
        elif self.shieldDir == 2:
            return pygame.Rect(self.rect.left - 10, self.rect.centery - 20, 10, 40)
        else:
            return pygame.Rect(self.rect.right, self.rect.centery - 20, 10, 40)

    def update(self, deltaTime, boundary):
        dx, dy = 0, 0

        if self.centerSelf:
            self.rect.center = self.pos
            self.centerSelf = False

        if self.invincibilityTimer > 0:
            self.invincibilityTimer -= deltaTime

        key = pygame.key.get_pressed()

        if self.soulMode != self.prevSoulMode:
            if not self.soulMode:
                self.rect.center = boundary.center
            self.prevSoulMode = self.soulMode

        if not self.soulMode:
            if key[pygame.K_LEFT]:
                dx -= 1
            if key[pygame.K_RIGHT]:
                dx += 1
            if key[pygame.K_UP]:
                dy -= 1
            if key[pygame.K_DOWN]:
                dy += 1
        else:
            if key[pygame.K_UP]:
                self.shieldDir = 0
            if key[pygame.K_DOWN]:
                self.shieldDir = 1
            if key[pygame.K_LEFT]:
                self.shieldDir = 2
            if key[pygame.K_RIGHT]:
                self.shieldDir = 3

        velocity = pygame.Vector2(dx, dy)

        if velocity.length() > 0:
            velocity = velocity.normalize() * self.soulSpeed * deltaTime

        self.moving = velocity.length() > 0
        self.rect.x += velocity.x
        self.rect.y += velocity.y

        if self.rect.left < boundary.left:
            self.rect.left = boundary.left
        if self.rect.right > boundary.right:
            self.rect.right = boundary.right
        if self.rect.top < boundary.top:
            self.rect.top = boundary.top
        if self.rect.bottom > boundary.bottom:
            self.rect.bottom = boundary.bottom

    def drawSoul(self, screen):
        screen.blit(self.image, self.rect)

        if self.soulMode:
            shieldRect = self.getShieldRect()
            pygame.draw.rect(screen, (0, 255, 0), shieldRect)

    def damage(self, damage):
        if self.invincibilityTimer > 0:
            return
        self.hp -= damage
        self.invincibilityTimer = self.immuFrameTime