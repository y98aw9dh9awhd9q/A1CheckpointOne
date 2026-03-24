from game.gameHandler.pygameWindow import game as game
import json, os
saveName = "save.json"
noSaveData = {
      "hp"    : 200 ,
     "attack" :  2  ,
    "defence" :  2  ,
     "level"  :  1  ,
      "gold"  : 100 ,
     "maxHp"  :  20 ,
      "xp"    :  0  ,
     "kills"  :  0  ,
    "baseDef" : 2 ,
    "baseATK" : 2 ,
    "inventory" : [],
    "round": 0
}

if not os.path.exists(saveName):
    with open(saveName,"w") as f:
        json.dump(noSaveData,f,indent=4)
elif os.path.getsize(saveName) == 0:
    with open(saveName,"w") as f:
        json.dump(noSaveData,f,indent=4)

game.readSave()
game.startDisplay()
game.generatePromts()
game.generateStory()

game.startGame()


