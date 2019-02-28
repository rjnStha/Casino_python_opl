from GameMoveCheck import GameMoveCheck
from Table import Table
from Player import Player
import os


gameTable = Table()
player = Player()
movesStorage =["human"]
moveCheck = GameMoveCheck(movesStorage, gameTable, player)
#moveCheck.moveCheck()

#casino.saveGame("a")

