import pygame
import const

font = None

class node:
    def __init__(self,x,y,w,h,label):
        self.rect = pygame.Rect(x,y,w,h)
        self.label = label

    def draw(self,screen):
        pygame.draw.rect(screen,const.blue,self.rect,2)
        text = font.render(self.label,True,const.white)
        textRect = text.get_rect(center=self.rect.center)
        screen.blit(text,textRect)
        pygame.display.flip()

    def checkClick(self):
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()[0]

        if mousePressed and self.rect.collidepoint(mousePos):
            return(self.label)
        return None

centerY = 300
shopX = 420
branchX = 620
option2X = 760
topY = 140
bottomY = 440
nodeW = 120
nodeH = 40

global nodes
def initNodes(optionOne,optionTwo,optionThree):
    option1 = node(740, topY, nodeW, nodeH, optionOne)
    option2 = node(option2X, centerY - nodeH // 2, nodeW, nodeH, optionTwo)
    option3 = node(740, bottomY, nodeW, nodeH, optionThree)
    shop = node(shopX, topY, nodeW, nodeH, "Shop")
    global nodes
    nodes = [shop, option1, option2, option3]

def drawLine(screen,p1,p2):
    pygame.draw.line(screen,const.blue,p1,p2,3)

def drawPath(screen):
    global font
    font = pygame.font.SysFont("Arial", 22)
    startX = 80
    shopCenterX = shopX + nodeW//2
    branchCenterX = branchX
    option1Y = topY + nodeH//2
    option3Y = bottomY + nodeH//2
    drawLine(screen,(startX,centerY),(option2X,centerY))
    drawLine(screen,(shopCenterX,centerY),(shopCenterX,topY + nodeH))
    drawLine(screen,(branchCenterX,topY + nodeH),(branchCenterX,bottomY + nodeH//2))
    drawLine(screen,(branchCenterX,centerY),(branchCenterX,topY + nodeH))
    drawLine(screen,(branchCenterX,centerY),(branchCenterX,bottomY + nodeH//2))
    drawLine(screen,(branchCenterX,option1Y),(740,option1Y))
    drawLine(screen,(branchCenterX,option3Y),(740,option3Y))

def putNodes(screen):
    for node in nodes:
        node.draw(screen)

def checkClickNoInit():
    for node in nodes:
        if node.checkClick() != None:
            return node.checkClick()

def putPlayer(screen):
    screenRect = screen.get_rect()
    emmanuelImage = pygame.image.load(const.playerDir)
    emmanuelImage = pygame.transform.flip(emmanuelImage,180,0)
    emmanuelImage = pygame.transform.scale(emmanuelImage,(100,200))
    emmanuelRect = emmanuelImage.get_rect()
    emmanuelRect.midleft = screenRect.midleft
    screen.blit(emmanuelImage,emmanuelRect)

