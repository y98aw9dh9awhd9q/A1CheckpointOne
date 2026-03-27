from game.gameHandler.pygameWindow import game as game
import json, os

game.readSave()
game.startDisplay()
game.generatePromts()
game.generateStory()

game.startGame()


