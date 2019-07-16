from Human import Human
from Computer import Computer
from Table import Table
from Deck import Deck
from Player import Player
from random import randint
from GameMoveCheck import GameMoveCheck

class GameEngine:

	#Constructors:
	def __init__(self,isHumanTurn = None):
		#Member Variables:
		#round of the game
		self.round = 0
		#flag for human as last capturer
		self.lastCapturer = "None"
		#set true as deafault
		self.humanTurn = True

		#Game inheriting all the class
		self.gameTable = Table()
		#empty deck as default
		self.gameDeck = Deck(False)
		self.human = Human() 
		self.computer = Computer()

		#for new game
		if isHumanTurn is not None:
			#set the human turn
			self.humanTurn = isHumanTurn
			#create new new deck with cards
			self.gameDeck = Deck(True)
			#deal cards
			self.newDealCards(True)

	#Selectors:
	#returns game Table object
	def getGameTable(self):
		return self.gameTable

	#returns human object
	def getHuman(self):
		return self.human

	#returns computer object
	def getComputer(self): 
		return self.computer

	#returns the boolean value for human turn
	def isHumanTurn(self):
		return self.humanTurn

	def getDeck(self):
		return self.gameDeck

	def getLastCapturer(self):
		return self.lastCapturer
	
	def getRound(self):
		return self.round

	#Utilities:
	#deals 4 new cards for each players, table if dealTable==true
	def newDealCards(self, dealTable):
		
		#Distribute card from the deck to table and hands
		if dealTable == True:
			for i in range(4):
				self.gameTable.storeTable(self.gameDeck.getNewCard())
		for i in range(4):
			self.computer.storeHand(self.gameDeck.getNewCard())
		for i in range(4):
			self.human.storeHand(self.gameDeck.getNewCard())

	#prints all the cards in table and player's hand in systematic layout
	def printGameBoard(self):
		
		print(" Deck:",end='')
		self.gameDeck.printDeckCards()

		print(" |--------------------------------")

		#Display the round
		print(" | Round: "+str(self.round)+"\n |")

		#Display the round
		print(" | Last Capturer: "+self.lastCapturer)
		print(" |")

		#score
		print(" | \t: Score: " + str(self.computer.getScore()))

		#isplay the comp hand 
		print(" | Comp: Hand:",end='')
		self.computer.printHandOrPile(True)

		#Display the comp pile 
		print(" | \t: Pile:",end='' )
		self.computer.printHandOrPile(False)

		print(" |")

		#Display table cards
		print(" | Table: ",end='')
		self.gameTable.printTable()
		print(" |")

		#score
		print(" | \t: Score: " + str(self.human.getScore()))

		#isplay the comp hand 
		print(" | Human: Hand:",end='')
		self.human.printHandOrPile(True)

		#Display the comp pile 
		print(" | \t: Pile:", end='')
		self.human.printHandOrPile(False)

		print(" |")

		print(" |--------------------------------\n\n")

	#called by GUI
	#return a string as a way to communicate with GUI after executing move
	def makeMove(self,moveInfo):

		self.printGameBoard()

		feedBack = []

		if moveInfo[0] == "Help":

			feedBack = "HELP: \n"
			#clearing the vector to store moveInfo following the convention of first element 
			#storing the player turn information
			moveInfo.clear()
			#adding the turn as the first element
			#For help only turn in the moveInfo
			moveInfo.append("Human")
			moveCheck = GameMoveCheck(moveInfo,self.gameTable,self.human)

			bestValidCaptureMove = moveCheck.getBestValidMove(True)
			bestValidBuildMove = moveCheck.getBestValidMove(False)

			if len(bestValidCaptureMove) == 2 and len(bestValidBuildMove) == 2:
				#no valid cpature or build move
				#trail the first card
				feedBack += "No Better Move: Trail"
			else:
				#get the num of cards to compare
				#and  remove from the list
				numCardCapture = int(bestValidCaptureMove.pop())
				numCardBuild = int(bestValidBuildMove.pop())

				#get the score of cards to compare
				#and remove the info from the vector
				scoreCapture = int(bestValidCaptureMove.pop())
				scoreBuild = int(bestValidBuildMove.pop())

				#get the build value and erase from the bestValidBuildMove
				#check size since invlaid build move lacks buildValue info
				buildValue = -1
				if bestValidBuildMove: 
					buildValue = int(bestValidBuildMove.pop())

				#store the best build,best capture and best move in the feedBack
				#to return to the GUi

				feedBack+= "The Best Capture Move: "
				for pos in bestValidCaptureMove:
					feedBack += str(pos)+" "
				feedBack += "\nScore: "+str(scoreCapture)+" NumCards: "+ str(numCardCapture)+"\n"

				feedBack+= "The Best build Move: "
				for pos in bestValidBuildMove:
					feedBack += str(pos)+" "
				feedBack += "\nScore: "+str(scoreBuild)+" NumCards: "+ str(numCardBuild)+"\n The Best Move: "
				
				#get the best move
				if scoreCapture > scoreBuild or (scoreCapture == scoreBuild and numCardCapture >=numCardBuild ):
					feedBack += "Capture: "
					feedBack += self.human.getHandCard(int(bestValidCaptureMove.pop(0)))+" and "
					tempTable = self.gameTable.getAllCards() 
					for pos in bestValidCaptureMove:
						tempInfo = ''.join(tempTable[int(pos)])
						feedBack += tempInfo+" "
				else:
					feedBack += "Build: "
					feedBack += self.human.getHandCard(int(bestValidBuildMove.pop(0)))+" and "
					tempTable = self.gameTable.getAllCards() 
					for pos in bestValidBuildMove:
						tempInfo = ''.join(tempTable[int(pos)])
						feedBack += tempInfo+" "

		elif moveInfo[0] == "Computer":

			feedBack = "Computer: \n"
			#clearing the vector to store moveInfo following the convention of first element 
			#storing the player turn information
			moveInfo.clear()
			#adding the turn as the first element
			#For help only turn in the moveInfo
			moveInfo.append("Computer")
			moveCheck = GameMoveCheck(moveInfo,self.gameTable,self.computer)
			bestValidCaptureMove = moveCheck.getBestValidMove(True)
			bestValidBuildMove = moveCheck.getBestValidMove(False)
			print(bestValidCaptureMove,bestValidBuildMove)

			if len(bestValidCaptureMove) == 2 and len(bestValidBuildMove) == 2:
				#no valid cpature or build move
				#trail the first card
				feedBack += "No Better Move: Trailed 0"
				self.trail(0)

			else:
				#get the num of cards to compare
				#and  remove from the list
				numCardCapture = int(bestValidCaptureMove.pop())
				numCardBuild = int(bestValidBuildMove.pop())

				#get the score of cards to compare
				#and remove the info from the vector
				scoreCapture = int(bestValidCaptureMove.pop())
				scoreBuild = int(bestValidBuildMove.pop())

				#get the build value and erase from the bestValidBuildMove
				#check size since invlaid build move lacks buildValue info
				buildValue = -1
				if bestValidBuildMove: 
					buildValue = int(bestValidBuildMove.pop())

				#store the best build,best capture and best move in the feedBack
				#to return to the GUi
				feedBack+= "The Best Capture Move: "
				for pos in bestValidCaptureMove:
					feedBack += str(pos)+" "
				feedBack += "\nScore: "+str(scoreCapture)+" NumCards: "+ str(numCardCapture)+"\n"

				feedBack+= "The Best build Move: "
				for pos in bestValidBuildMove:
					feedBack += str(pos)+" "
				feedBack += "\nScore: "+str(scoreBuild)+" NumCards: "+ str(numCardBuild)+"\n The Best Move: "
				
				#get the best move
				if scoreCapture > scoreBuild or (scoreCapture == scoreBuild and numCardCapture >=numCardBuild ):
					#capture as best move
					feedBack += "Capture: "

					handPosition = int(bestValidCaptureMove.pop(0))
					tableCardPosition = bestValidCaptureMove[:]

					feedBack += self.computer.getHandCard(handPosition)+" and "
					tempTable = self.gameTable.getAllCards()
					for pos in bestValidCaptureMove:
						tempInfo = ''.join(tempTable[int(pos)])
						feedBack += tempInfo+" "

					#calling the capture function
					self.capture(handPosition,tableCardPosition)
					#setting the last capturer to the given turn
					self.lastCapturer = "Computer"

				else:
					#build as best move
					feedBack += "Build: "
					#get the hand position and erase from the vector
					handPosition = int(bestValidBuildMove.pop(0))

					tableCardPosition = bestValidBuildMove[:]

					feedBack += self.computer.getHandCard(handPosition)+" and "
					tempTable = self.gameTable.getAllCards() 
					for pos in bestValidBuildMove:
						tempInfo = ''.join(tempTable[int(pos)])
						feedBack += tempInfo+" "

					#set the hand and table position and generate build pairs
					moveCheck.setPosTableHand(handPosition,tableCardPosition)
					moveCheck.generateBuildPairs(buildValue);

					#calling the capture function
					self.build(handPosition,tableCardPosition,moveCheck.getCurrentBuildPairds())
			#change the turn
			self.humanTurn = True

		else:
			feedBack = "Human: \n"
			moveInfo.append("Human")

			#check if the move is valid
			moveCheck = GameMoveCheck(moveInfo,self.gameTable,self.human)
			if not moveCheck.moveCheck():
				feedBack += "InValid move..Please Enter Valid Move"
				return feedBack

			feedBack += "The move is VALID\n"
			#Check for move type and valid move
			#trail
			if moveCheck.getMoveType() == "t":
				#trail
				feedBack += "Trailed: "+ str(moveCheck.getHandPosition())
				self.trail(moveCheck.getHandPosition())
			
			elif moveCheck.getMoveType() == "c": 

				feedBack += "Captured: "+ str(moveCheck.getHandPosition())+" "
				for pos in moveCheck.getTablePosition():
					feedBack += str(pos)+" "				

				#capture
				self.capture(moveCheck.getHandPosition(),moveCheck.getTablePosition())
				#Setting the last capturer to the given turn
				self.lastCapturer = "Human"
				
			else:
				#build
				feedBack += "Build: "+ str(moveCheck.getHandPosition())+" "
				for pos in moveCheck.getTablePosition():
					feedBack += str(pos)+" "				

				self.build(moveCheck.getHandPosition(),moveCheck.getTablePosition(),moveCheck.getCurrentBuildPairds())

			#change the turn
			self.humanTurn = False

		return feedBack

	#carries out trail action for human or computer with given hand position
	def trail(self,handPosition): 
		#Check human or computer
		#get the card from hand and store in the table board
		if self.humanTurn:
			self.gameTable.storeTable(self.human.popHandCard(handPosition))
		else:
			self.gameTable.storeTable(self.computer.popHandCard(handPosition))

		self.humanTurn = not self.humanTurn

		return True
	
	#carries out capture action for human or computer with given hand position and table card position
	def capture(self, handPosition, tableCardPosition):

		#since Capture involves deleting elements from table
		#arrange the tableCardPosition in descending order
		#prevents removing less indexed element before higher ones
		localTableCardPos = sorted(tableCardPosition,reverse=True)
		
		#get the current player
		currentPlayer = Player()
		if self.humanTurn:
			currentPlayer = self.human
		else:
			currentPlayer = self.computer

		#remove the card from hand and store into human pile
		currentPlayer.storePile(currentPlayer.popHandCard(handPosition))

		#storing selected table cards into human pile
		for currentTableCardPos in localTableCardPos:
			
			#convert from string to int
			currentTableCardPos = int(currentTableCardPos)

			#check for build cards
			if len(self.gameTable.getAllCards()[currentTableCardPos]) > 2:

				#local variable to store the vector with buildInfo
				buildCard = self.gameTable.popTableCard(currentTableCardPos)

				#get each card from the build
				for card in buildCard:
					#bug when poping a multi build from the build
					#deletes the first [ and ] but fails to delete other occasions
					if card !="[" and card !="]":
						currentPlayer.storePile(card)
			else:
				#loose card
				currentPlayer.storePile(self.gameTable.popTableCard(currentTableCardPos)[0])

		return True

	#carries out build action for human or computer with given hand position,table card position and build pairs
	def build(self, handPosition, tableCardPosition, buildPairs):

		#since build involves deleting elements from table
		#arrange the tableCardPosition in descending order
		#prevents removing less indexed element before higher ones
		localTableCardPos = sorted(tableCardPosition,reverse=True)

		#removing selected table cards
		for card in localTableCardPos:
			self.gameTable.popTableCard(int(card)) 

		#removing the hand cards from the player 
		if self.humanTurn:
			self.human.popHandCard(handPosition)
		else:
			self.computer.popHandCard(handPosition)

		#storing the build info as string to store in table
		buildCurrent = []

		#value
		buildCurrent.append(buildPairs[0][0])
		#owner
		buildCurrent.append(buildPairs[0][1])
		#Multi or Single, multi as default, change to single when required in the loop below
		buildCurrent.append("Multi")
		#make a local copy of the parameter
		buildPairsLocal = buildPairs[:]
		#remove the first element which is the information of value and owner
		del buildPairsLocal[0]

		#replace the multi
		if len(buildPairsLocal) == 1:
			buildCurrent[2] = "Single"

		#loop to get each pair
		for pairCurrent in buildPairsLocal:
			
			#if single card then 
			if len(pairCurrent) == 1:
				buildCurrent.append(pairCurrent[0])
				continue

			#store "[" as start of single builds
			if buildCurrent[2] == "Multi":
				buildCurrent.append("[")
			#for pairs access each of them and store in the table
			for card in pairCurrent:
				buildCurrent.append(card) 
			#store "]" as the end of single builds
			if buildCurrent[2] == "Multi":
				buildCurrent.append("]")


		#store the build vector in table
		self.gameTable.storeTable(buildCurrent)
		return True

	#loads the game with given file name
	def loadGame(self,fileName):
		file = open(fileName, "r")
		loadHuman = False
		for line in file:
			#splitting the line by delimiter space and storing in list
			lineList = line.split( )
			#ignore empty list
			if len(lineList) > 0:
				#Check the label
				if lineList[0] == "Round:":
					#Round
					#converting string to int
					self.round = int(lineList[1])

				elif lineList[0] == "Computer:":
					#Computer data
					loadHuman = False

				elif lineList[0] == "Human:":
					#Human Data
					loadHuman = True

				elif lineList[0] == "Score:":
					#get the score, check the player type and set the score
					score = lineList[1]
					if loadHuman:
						self.human.setScore(score)
					else:
						self.computer.setScore(score)

				elif lineList[0] == "Hand:":
					#delete the label, Hand:
					del lineList[0]
					#store each card in specified player hand
					for card in lineList:
						if loadHuman:
							self.human.storeHand(card)
						else:
							self.computer.storeHand(card)

				elif lineList[0] == "Pile:":
					#delete the label, Pile:
					del lineList[0]
					#store each card in specified player hand
					for card in lineList:
						if loadHuman:
							self.human.storePile(card)
						else:
							self.computer.storePile(card)

				elif lineList[0] == "Table:":
					#delete the label, Table:
					del lineList[0]
					#store each card in table ignoring build cards
					while(True and lineList):
						card = lineList.pop(0)
						#if build table found remove the card
						if card == "[":
							while card != "]":
								card = lineList.pop(0)

						elif card.find("[") != -1:
							while card.find("]") == -1:
								card = lineList.pop(0)
						else:
							#add the single cards to table
							self.gameTable.storeTable(card)

						#break if list empty
						if not lineList:
							break

				elif lineList[0] == "Build":
					#build ownership
					#delete the label, Build
					del lineList[0]
					#delete the label, Owner:
					del lineList[0]
					#ignored build cards at label "Table"
					#call store build function
					self.storeBuildTable(lineList)

				elif lineList[0] == "Last":
					self.lastCapturer = lineList[2]

				elif lineList[0] == "Deck:":
					#delete the label, Deck:
					del lineList[0]
					#store each card in deck
					for card in lineList:
						self.gameDeck.storeDeck(card)

				elif lineList[0] == "Next":
					#check for human or computer to set the turn
					if lineList[2] == "Computer":
						self.humanTurn = False 
					else:
						self.humanTurn = True

	#stores one build multi or single into the table for human and computer
	def storeBuildTable(self,data):
		#make a copy of the data
		listCard = data[:]
		#get next card
		card = listCard.pop(0)
		buildCards = []
		buildValue = 0

		if card == "[":
			#multi build
			buildCards.append("Multi")
			#get next card
			card = listCard.pop(0)

			#6 types of card info
			# [ , [S8 , S8, S8], [S8] , ]
			#but ony [S8] and [S8 starts the single build

			#loop until the end of the build
			while card != "]" :
				#type S8
				if len(card)==3 and card[0] == "[":

					#adding [ and S8 from [S8 to vector as separate elements
					buildCards.append("[")
					#removing the "[" form the card
					card = card.replace("[","")
					buildCards.append(card)

					#get next card
					card = listCard.pop(0)

					#loop until the end of the single build of type [S8 .. S8]
					#end means data with value S8]
					while len(card) != 3:

						#if not the end card S8]
						#then the value must be individual card S8
						buildCards.append(card)
						#get next card
						card = listCard.pop(0)
					#adding ] and S8 from S8] to vector as separate elements
					#removing the "]" form the card S8]
					card = card.replace("]","")
					buildCards.append(card)
					buildCards.append("]")

				else:
					#type [S8]

					#removing the "[" and "]" form the card and adding only S8 part
					card = card.replace("[","")
					card = card.replace("]","")
					buildCards.append(card)

				#get new single build or "]" as end of the multi build
				card = listCard.pop(0)

			start = buildCards.index('[')+1
			end = buildCards.index(']')

		elif len(card) == 3 and card[0] == '[':
			#single build
			buildCards.append("Single")

			#type [S8
			#erasing "[" and adding S8 from [S8 to vector
			card = card.replace("[","")
			buildCards.append(card)

			#get new card
			card = listCard.pop(0)

			#loop until the end of the single build of type [S8 .. S8]
			#end means data with value S8]
			while len(card) != 3:

				#if not the end card S8]
				#then the value must be individual card S8
				buildCards.append(card)
				#get new  card to compare as single card
				card = listCard.pop(0)

			#erasing "]" and adding S8 from S8] to vector and ending the single build
			card = card.replace("]","")
			buildCards.append(card)

			#calculate the build value start and end index
			start = 1
			end = len(buildCards)


		#calculating the build value
		#fails to calculate the buildValue for case
		# [0,Human, Multi, H6,C6, S6] since no [ and ]
		for i in range(start, end):
			buildValue += self.cardStringToValue(buildCards[i])

		#for case: [0,Human, Multi, H6,C6, S6]
		if buildValue == 0: 
			buildValue = self.cardStringToValue(buildCards[1])

		#print "build:", buildCards,"value",buildValue

		#adding build value
		buildCards.insert(0,str(buildValue))
		#get the build owner info
		card = listCard.pop(0)
		buildCards.insert(1,card)

		self.gameTable.storeTable(buildCards)

	#converts card value in character to numeric value
	def cardStringToValue(self,key):
		if key[1] == "A" :
			return 1
		elif key[1] == "K" :
			return 13
		elif key[1] == "Q" :
			return 12
		elif key[1] == "J" :
			return 11
		elif key[1] == "X" :
			return 10
		else:
			return int(key[1])

	#saves game of given filename
	def saveGame(self,fileName):

		#add .txt and path to the user input file name
		pathFileName = str(Path().absolute())+'\\serializationTest\\'
		pathFileName += fileName + ".txt"

		print(pathFileName)
		f = open(pathFileName, "w")
		#prompts
		f.write("Round: "+str(self.round)+"\n\nComputer: \n   Score: "
			+str(self.computer.getScore())+"\n   Hand: ")
		#hand Cards
		for card in self.computer.getAllHandCards():
			f.write(card+" ")
		#pile Cards
		f.write("\n   Pile: ")
		for card in self.computer.getAllPileCards():
			f.write(card+" ")
		#Storing Human info
		f.write("\n\nHuman: \n   Score: "+str(self.human.getScore())+"\n   Hand: ")
		#hand Cards
		for card in self.human.getAllHandCards():
			f.write(card+" ")
		#pile Cards
		f.write("\n   Pile: ")
		for card in self.human.getAllPileCards():
			f.write(card+" ")
		#table
		f.write("\n\nTable: ")
		#empty vector to store all build info for Build Owner Section of file
		vectorCards = []
		for cardVector in self.gameTable.getAllCards():
			#accessing elements of the table board

			#check the table element size for build
			#>2 means its a build
			if len(cardVector) == 2:
				f.write(cardVector[1]+" ")
			else:
				#build

				#to store each build seperately
				buildInfo = ""

				#check if multi or single build, stored as 3rd element of the table
				if cardVector[2] == "Single":
					buildInfo +="["

					#Single build so simply store the cards
					for i in range(3,len(cardVector)):

						#adding the cards without any space in between
						buildInfo += cardVector[i]

						#Check if it's the last element of the build
						#since no need to add " " to the last element
						if i != len(cardVector)-1 :
							buildInfo += " "
				else:
					#multi build
					buildInfo +="[ "

					#loop to get the cards form the given element of the table
					#card's info starts from index 3
					i = 3
					while i<len(cardVector):
						
						#find if it's single or multi card
						if cardVector[i] == "[":

							#multi card build
							#/adding start
							buildInfo += "["

							#increasing index to get new card
							i += 1

							while (cardVector[i]) != "]":

								buildInfo += cardVector[i]
								i += 1
								if cardVector[i] != "]":
									buildInfo += " "

							#adding end
							buildInfo += "] "

						else:

							#single card
							#no bs just write the card inside [ ]
							buildInfo += "["+cardVector[i]+"] "
						
						#increase the index
						i += 1

				#addding the build info in "Table: " section of file
				f.write(buildInfo+"] ")

				buildInfo += "] "+cardVector[1]
				vectorCards.append(buildInfo)

		#adding the build owner info from vector to the content
		for build in vectorCards:
			f.write("\n\nBuild Owner: "+build)
		
		#last capturer
		f.write("\n\nLast Capturer: "+self.lastCapturer
			+"\n\nDeck: ")

		#Deck
		for card in self.gameDeck.getDeck():
			f.write(card+" ")

		#adding the next Player
		f.write("\n\nNext Player: ")
		if self.humanTurn:
			f.write("Human")
		else:
			f.write("Computer")

		f.close()

	#check for changes for dealing cards, new round and end of the tournamemt
	def checkGameChanges(self):

		feedBack =""

		dealTable = False
			
		#check if both player's hand is empty
		if self.human.getHandSize() ==0 and self.computer.getHandSize() == 0: 
			
			if self.gameDeck.getDeckSize() == 0:

				#Round "<<round<<" Complete 
				feedBack += "\n****** Round Complete ****** \n"

				#clear the table and store the cards to the pile of last capturer
				tableCards = self.gameTable.getAllCards()
				for card in tableCards:
					if self.lastCapturer == "Human":
						self.human.storePile(card[1])
					else:
						self.computer.storePile(card[1])

				#create new table
				self.gameTable = Table()

				#calculate and display score
				humanScoreInfo = self.calculatePlayerScore(self.human)
				computerScoreInfo = self.calculatePlayerScore(self.computer)
				
				humanScore = int(humanScoreInfo[0] )
				computerScore = int(computerScoreInfo[0])

				#check for player with higher num of cards
				if humanScoreInfo[1] > computerScoreInfo[1]:
					humanScore += 3 
				elif humanScoreInfo[1] < computerScoreInfo[1]:
					computerScore += 3 


				#check for player with higher num of spade cards
				if humanScoreInfo[2] > computerScoreInfo[2]:
					humanScore +=1
				elif humanScoreInfo[2] < computerScoreInfo[2]:
					computerScore +=1


				feedBack += "Total Num of Cards: Human: "+ str(humanScoreInfo[1])+" Computer: "+str(computerScoreInfo[1])+"\n Num of Spades: Human: "+ str(humanScoreInfo[2])+" Computer: "+str(computerScoreInfo[2])+"\n Score for this round: Human: "+str(humanScore)+" Computer: "+str(computerScore)

				#update score and round
				humanScore += int(self.human.getScore())
				computerScore += int(self.computer.getScore())
				self.human.setScore(humanScore)
				self.computer.setScore(computerScore)
				
				#get the final score to compare
				finalScoreHuman = self.human.getScore()
				finalScoreComputer = self.computer.getScore()
				
				feedBack += "\nTournament score: Human: "+str(finalScoreHuman)+" Computer: "+str(finalScoreComputer)

				#add the pile info 
				feedBack+="\n Human Pile: "
				for card in self.human.getAllPileCards():
					feedBack+= str(card)+" "

				feedBack+="\n Computer Pile: "
				for card in self.computer.getAllPileCards():
					feedBack+= str(card)+" "
					
				#check if the score of any player is above 21
				if finalScoreHuman > 21 or finalScoreComputer > 21: 
					#find the winner
					feedBack += "\n****** Game Over ******\n Winner: "
					#std::cout<<"\tWinner of the game: "
					if finalScoreHuman > finalScoreComputer:
						feedBack+="Human"
					elif finalScoreHuman < finalScoreComputer:
						feedBack+="Computer"
					else:
						feedBack+="Draw"					

					#exit
					return feedBack

				#increase the round num
				self.round+=1
				#create new deck
				self.gameDeck = Deck(True)
				#clear pile for both player
				self.human.clearPile()
				self.computer.clearPile()

				#deal table
				dealTable =True

			#set the turn for next round based on last Capturer
			if self.lastCapturer == "Human":
				self.humanTurn = True
			else:
				self.humanTurn = False

			feedBack += "\n**Dealt New 4 Cards for each player**"
			self.newDealCards(dealTable)
			
		return feedBack

	#calculates and returns the score for given player pile,also finds
	# the num of total cards and num of spade cards
	def calculatePlayerScore(self,player):

		#varibles to store the info
		scoreData = []
		score = 0
		countSpade = 0

		#get the list of pile cards from the player
		pile = player.getAllPileCards()

		for card in pile:
			if card[0] == 'S':
				countSpade+=1
			score += self.scoreCalculator(card)


		#store the info in the vector
		scoreData.append(score)
		scoreData.append(len(pile))
		scoreData.append(countSpade)

		return scoreData
	
	#Check the card for aces and DX and S2 and calculates the score
	def scoreCalculator(self, card):
		score = 0
		if card == "CA" or card == "DA" or card == "SA" or card == "HA" or card == "S2":
			score = 1
		elif card == "DX":
			score = 2
		return score
