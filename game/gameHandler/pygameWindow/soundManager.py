import pygame
import const
import os
pygame.mixer.init()

vineBoom = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "sfx", "vineBoom.mp3"))
battleMusic = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "music", "battleMusic.mp3"))
yippie = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "sfx", "yippie.mp3"))
boss1Music = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "music", "boss1Music.mp3"))
boss2Music = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "music", "boss2Music.mp3"))
genocideNAgra = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "music", "genocideNAgra.mp3"))
genoBossMusic = pygame.mixer.Sound(os.path.join(const.baseDir, "assets", "audio", "music", "genoBossMusic.mp3"))
def playVineBoom():
    vineBoom.play()

global playing
playing = False
def playBattleMusic():
    global playing
    if not playing:
        battleMusic.play(-1)
        print("playing audio")
        playing = True

def stopAudio():
    global playing
    playing = False
    pygame.mixer.stop()

def playYippie():
    yippie.play()

def playboss1Music():
    boss1Music.play()

def playboss2Music():
    boss2Music.play()

def playgenocideNAgra():
    genocideNAgra.play()

def playGenoBoss():
    genoBossMusic.play()
