from Human import Human
from Computer import Computer
from Table import Table
from Deck import Deck
from operator import itemgetter
import math

class GameMoveCheck:

	#Constructors:
	def __init__(self, movesStorage, gameTable, player):

		#store the required objects as memeber variables
		self.gameTable = gameTable
		self.player = player
		self.moveType = 't'
		self.handPosition = 0
		self.tablePosition = []
		self.currentBuildPairs = []

		#get the last elemet from the movesStorage which is the turn of the player
		turn = movesStorage[-1]
		if turn == "Human":
			self.humanTurn = True
		else:
			self.humanTurn = False

		#check of the size of the move info is > 1
		#false -> called by Computer or Help
		#true -> called by human to make move
		if len(movesStorage) > 1:

			#extract the move information
			self.moveType = movesStorage[0]

			#get hand position
			# converting string to int
			self.handPosition = int(movesStorage[1])

			#check if table section of the information is empty -> empty meaning trail
			#store in the table position
			if len(movesStorage) > 2:

				self.tablePosition = movesStorage
				#removing the first two elements (action and hand position)
				del self.tablePosition[0]
				del self.tablePosition[0]
				#removing the turn info
				del self.tablePosition[-1]

	#calls respective action move Check function
	def moveCheck(self):

		#hand Card and its numeric value
		handCard = self.player.getHandCard(self.handPosition)
		handCardValue = self.cardStringToValue(handCard)

		if self.moveType == "t": 

			#moveCheck for trail
			#get local vector<vector> for cards in table
			tableCards = self.gameTable.getAllCards()
			#loop through each table cards and find build
			#check if the build is own by the player, true -> restrict trailing
			for card in tableCards:
				for i in range(len(card)):
					#find the build
					if len(card)>2:
						if (self.humanTurn and card[1]=="Human") or (not self.humanTurn and card[1]=="Computer"):
							return False 


			return True

		elif self.moveType == "c": 
			#move Check for capture
			return self.captureBuildSumChecker(handCardValue)

		else :
			#moveCheck for build

			#get the vector of hand cards
			handCardList = self.player.getAllHandCards()

			#flag to find if build valued card in hand
			buildValueFound = False
			buildValue = 0
			#loop through all the hand cards to find the build valued hand card
			for i in range(len(handCardList)):
				
				#check for selected hand card and ignore if found
				if i == self.handPosition:
					continue 

				#build value equals the value of given Hand Card
				buildValue = self.cardStringToValue(handCardList[i])

				#check validity for given hand card
				if buildValue >= handCardValue and self.captureBuildSumChecker(buildValue): 
					#found a hand card whose value is equal to build Value
					buildValueFound = True
					break

			#if build move valid generate pairs to make move
			if buildValueFound:
				self.generateBuildPairs(buildValue)

			return buildValueFound

	#returns the handposition
	def getHandPosition(self):
		return self.handPosition

	#returns moveType
	def getMoveType(self):
		return self.moveType

	#returns the table postions as vector
	def getTablePosition(self):
		return self.tablePosition

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

	#returns the current BuildPairds
	def getCurrentBuildPairds(self):
		return self.currentBuildPairs

	#buffer function to check if the set of user given table and hand positions
	#is a valid set of move
	#calls recursiveSumChecker
	def captureBuildSumChecker(self, valueCompare):
		#get local vector<vector> for cards in table
		tableCards = self.gameTable.getAllCards()

		# 1. Get all cards of given position and their numeric value from the table 
		# 2. Check if the value is less or greater than compare value
		#		a. if greater return false, in valid move 
		#		b. if less than add to the list, need further checking for validity
		#		c. equal than ignore, no futher check needed


		#to store the values of cards in vector
		selectedPosValue = []

		#add hand value for build, since hand card would be part of the pair with table cards to get value = compareValue
		handCardValue = self.cardStringToValue(self.player.getHandCard(self.handPosition))
		#check with valueCompare
		if self.moveType == "b" and handCardValue < valueCompare:
			selectedPosValue.append(handCardValue)

		#loop to get each cards from the given positions
		for pos in self.tablePosition:
	
			#get the value of the card
			tableValue = 0
			#get the index(position) of the table card
			index = int(pos)
			currentTableCard = tableCards[index]

			#check for build or loose card
			if len(currentTableCard) > 2:

				tableValue = int(currentTableCard[0])

				if self.moveType == "b":
					#Check for Multi build for action build and return false since multi build cannot be further build into
					if currentTableCard[2] == "Multi" and tableValue != valueCompare:
						return False
					#check for build owned by the same player
					#"..Invalid move to use own build to extend build.."
					#if self.humanTurn and currentTableCard[1] == "Human":
						#return False
					#if not self.humanTurn and currentTableCard[1] == "Computer":
						#return False
				
				#possible to capture table card with build only if build value = valueCompare
				if self.moveType == "c" and tableValue != valueCompare:
					return False          

			else:
				tableValue = self.cardStringToValue(currentTableCard[1])

			#the given table value can never be greater than the valueCompare
			#only add values less than valueCompare
			if tableValue > valueCompare:
				return False
			elif tableValue < valueCompare:
				selectedPosValue.append(tableValue)
			#else don't add to the list, equal

		# 3. Sort tbe list of values of the selected table cards in descending order
		# 4. 	a. Get the first element(highset values) from the list
		#      for(size of list)
		#  	b. Add the given value with next elements in the list and check the sum for =< valueCompare
		# 	   	c. If equal then remove both the elements
		#   	d. If less than get another value from the list and add to the sum, check for condition
		# 		e. If greater than get next value
		# 5. repeat 4 until no element in the list --> valid move

		#sort the the table values list in descending order with respect to their values
		selectedPosValue.sort(reverse=True)

		#std::cout<<"captureBuildSumChecker::Move Validation.."<<std::endl
		#check for empty vector
		while len(selectedPosValue):

			#get the max value, the first value and erase the value from the vector
			currentMax = selectedPosValue[0]
			del selectedPosValue[0]

			#vector storing the remaining values to compare with current Max value
			tempSelectedPosValue = selectedPosValue[:]
			#vector to store the vector returned after recursiveSumChecker call
			#if returned vector not empty --> pair found
			returnedRemPosValue = []

			#get tempSelectedPosValue 
			while len(tempSelectedPosValue) >0 :

				#recursively finds the pair for current Max value
				returnedRemPosValue = self.recursiveSumChecker(currentMax,valueCompare,tempSelectedPosValue[:])

				#break since pair for current Max found
				if returnedRemPosValue:
					break

				#remove the first element of the tempSelectedPosValue
				#to get new element to compare with the current Max value
				del tempSelectedPosValue[0]
			

			#check if the returned vector is empty after loop --> no pair found --> invalid move
			if not returnedRemPosValue:
				return False
			else:
				#valid values
				#find their poistion and remove from the list 
				for value in returnedRemPosValue:
					#search the element
					#removing the element
					del selectedPosValue[selectedPosValue.index(value)]

		return True

	#utility function for captureBuildSumChecker that recursively checks for valid sets of card for given move
	def recursiveSumChecker(self, sum, valueCompare, selectedPosValue):

		#print("recursiveSumChecker:: ",sum," ",valueCompare," ",selectedPosValue)

		#empty vector
		tempValidValue = []

		#recursion when the sum is less the valueCompare
		currentLowerValue = selectedPosValue[0]
		tempSum = sum + currentLowerValue

		#only delete when found equal
		#and return true
		if tempSum == valueCompare:
			#print(":: =")
			del selectedPosValue[0]
			#returning the value that lead to the required sum
			temp = []
			temp.append(currentLowerValue)
			return temp
			
		elif tempSum < valueCompare:
			
			#print(":: < ")

			#remove the first element from the temp selectedPosValue
			tempValueSetTable = selectedPosValue[:]
			del tempValueSetTable[0]

			#loop until the list is empty
			while tempValueSetTable:
				tempValidValue = self.recursiveSumChecker(tempSum,valueCompare,tempValueSetTable[:])

				#Check for non empty vector
				#end of the recursion
				if tempValidValue:
					tempValidValue.append(currentLowerValue)
					return tempValidValue
					
				del tempValueSetTable[0]
			
			#returns empty list
			return tempValueSetTable
		
		else:
			#print(":: > ")
			#std::cout<<":: > "<<std::endl

			#tempSum > valueCompare
			return tempValidValue
		
	#generates string info of build in format --> [ [DX] [H9 SA] ] Human
	def generateBuildPairs(self,buildValue):
		
		#add value of build to the currentBuildPair
		buildXInfo = []
		#value of build
		buildXInfo.append(str(buildValue))
		#player info
		if self.humanTurn:
			buildXInfo.append("Human") 
		else:
			buildXInfo.append("Computer") 
		self.currentBuildPairs.append(buildXInfo)

		#get vector of table cards  
		tableCards = self.gameTable.getAllCards()

		#Vector of vector for build
		#Vector of String for both card and its value, sorted 
		buildCards = []

		#store selected hand card and it's value in a vector 
		#store the vector in buildCards
		tempCard = []
		#get position card --> get int value --> convert to string --> store in vector
		tempCard.append(str(self.cardStringToValue(self.player.getHandCard(self.handPosition))) )
		tempCard.append(self.player.getHandCard(self.handPosition))
		buildCards.append(tempCard)

		#store all the selected table cards
		for pos in self.tablePosition:
			buildCards.append(tableCards[int(pos)])

		#sorts the cards in descending order based on the card value
		#starts building from highest value therefore highest values are removed first
		# in order to prevent removing lower indexed elements before higher ones
		buildCards = sorted(buildCards,key=itemgetter(0),reverse=True)
		
		# #copy the value of cards from buildCards to selectedPosValue
		# #required to find tha pair
		selectedPosValueOG = []
		selectedPosValue = []

		for cardValue in buildCards:
			#make a permanent copy of selectedPosValue since elements are erased when checking
			selectedPosValueOG.append(int(cardValue[0]))
			selectedPosValue.append(int(cardValue[0]))
		
		#print("\ngenerateBuildPairs::Finding Build Pairs...\n")
		#check if the list is empty
		while selectedPosValue:
			
			#get the max value, the first value and erase the value from the vector
			currentMax = selectedPosValue[0]
			#removing any values equal to buildValue since they don't have pair
			while currentMax == buildValue:
				
				#search the element and get the index
				index = selectedPosValueOG.index(currentMax)
				#mark that the position of the value is added
				#prevents double counting same element when using std::find
				selectedPosValueOG[index] = -1

				#adding the single set of cards to currentBuildPairs
				#get the index -> access the element in buildCards --> store individual card into tempairs --> store tempPairs into currentBuildPairs
				#size of vector 
				size = len(buildCards[index])

				#check for build and single cards
				if size > 2:
					#builds
					#get the build type
					buildType = buildCards[index][2]
					#loop through the vector containg build 
					i = 3
					while i<size:
						#vector to store the pair of cards
						tempPairs = []
						#get next element
						#i++ increasing index to get next value
						card = buildCards[index][i]
						#check for multi since they are already pairs,
						#[ [CA C8] [C9] ] -- > two pairs

						if buildType == "Multi":

							if card == "[":
								#get next card
								i+=1
								card = buildCards[index][i]
								#get all the cards within single build [..]
								while card != "]":
									#add the card to the vector
									tempPairs.append(card)
									#i++ --> for next iteration
									i+=1
									#get the next card of the single build
									card = buildCards[index][i]
							else :
								#single cards whose value should equal to build value
								#add them separately since they don't have pair
								tempPairs.append(card)

							#add the vector to thhe pair list
							self.currentBuildPairs.append(tempPairs)

						else:
							#Single Build
							#break and store outside loop
							#had problem using temPairs as local variable in this for loop
							break
				
					#get the pairs for single build
					if buildType == "Single":
						self.currentBuildPairs.append(self.addPairdsBuild(buildCards[:],index)) 

				else:
					self.currentBuildPairs.append(self.addPairdsBuild(buildCards[:],index)) 

				#erase the first element since it equals buildValue
				del selectedPosValue[0]
				#get new max value
				currentMax = selectedPosValue[0]

			#removing the first element which is the current max value
			del selectedPosValue[0]

			#vector storing the remaining values to compare with current Max value
			tempSelectedPosValue = selectedPosValue[:]
			#vector to store the vector returned after recursiveSumChecker call
			#if returned vector not empty --> pair found
			returnedRemPosValue = []


			#get tempSelectedPosValue 
			while tempSelectedPosValue:

				#recursively finds the pair for current Max value
				returnedRemPosValue = self.recursiveSumChecker(currentMax,buildValue,tempSelectedPosValue[:])

				#break since pair for current Max found
				if returnedRemPosValue:
					break 

				#remove the first element of the tempSelectedPosValue
				#to get new element to compare with the current Max value
				del tempSelectedPosValue[0]

			#check if the returned vector is empty after loop --> no pair found --> error
			if not returnedRemPosValue:
				print("generateBuildPairs:: error")
			else:
				#valid values
				#pair up all the values that come up
				#search the element and get the index
				index = selectedPosValueOG.index(currentMax)
				#mark that the position of the value is added
				selectedPosValueOG[index] = -1
				#get the card in vector
				tempPairs1 = self.addPairdsBuild(buildCards[:],index)

				#find their poistion and remove from the list
				for value in returnedRemPosValue:
					#search the element and get the index
					index = selectedPosValueOG.index(value)
					#mark that the position of the value is added
					selectedPosValueOG[index] = -1

					#get the vector with individual cards and merge to the local vector
					tempPairs2 = self.addPairdsBuild(buildCards[:],index)
					for pair in tempPairs2:
						tempPairs1.append(pair)

					#get the iterator to erase from the selectedPosValue
					#since pair found erase the pairs since it helps in finding other pairs using recursion
					index = selectedPosValue.index(value)
					#removing the element
					del selectedPosValue[index]

				#add the pair individual cards to the list of pair vectors
				self.currentBuildPairs.append(tempPairs1)
	
	# #also holds the info about player and value of build
	# #returns the vector with the card info from the buildCards, required by the build action 
	# #to generate pairs for build 
	def addPairdsBuild(self, buildCards, index):
		#adding the single set of cards to currentBuildPairs
		#get the index -> access the element in buildCards --> store individual card into tempairs --> store tempPairs into currentBuildPairs
		tempPairs = []
		#size of vector 
		size = len(buildCards[index])
		#check for build and single cards
		if size > 2 :
			#builds
			for card in buildCards[index]:
				#check for multi build brackets and ignore it
				if len(card) == 2 :
					tempPairs.append(card)
		else:
			tempPairs.append(buildCards[index][1])

		return tempPairs

	#returns power set of all possible combination of table cards for a given hand card
	def tablePositionPowerSet(self):
		
		#get the size of the table
		set_size = self.gameTable.getTableSize()
		#adding index to vector and look for it's power set
		tablePositionList = []
		for i in range(set_size):
			tablePositionList.append(str(i))

		#vector of vector to store the power set
		tablePosPowerSet = []
	      
		# set_size of power set of a set 
		# with set_size n is (2**n -1) 
		pow_set_size = (int) (math.pow(2, set_size)) 
		counter = 0
		j = 0 

		# Run from counter 000..0 to 111..1 
		for counter in range(0, pow_set_size):
			#tem list to store each set
			currenSet = []

			for j in range(0, set_size):
	            
				# Check if jth bit in the  
				# counter is set If set then  
				# add the element from set  
				if((counter & (1 << j)) > 0): 
					currenSet.append(tablePositionList[j])

			#adding the set to the powerSet
			tablePosPowerSet.append(currenSet)


		#remove the first element which is the empty set
		del tablePosPowerSet[0]

		return tablePosPowerSet

	#returns a list of all the valid moves for action Capture
	def getValidCaptureList(self):
		
		#indicates the move type, required since further checking functions uses the variable
		self.moveType = "c"

		#list to store all the valid capture moves
		validCaptureList = []

		#get the power set
		powerSet = self.tablePositionPowerSet()

		#get the local variable of the hand of the player
		playerHand = self.player.getAllHandCards()
		#loop through each element of the power set
		for testTablePosition in powerSet:
			#set the table memeber variable to the set
			self.tablePosition = testTablePosition
			#loop through each hand position
			for i in range(len(playerHand)):
				#set the memmber variable handPosition
				self.handPosition = i

				#get the hand card for given position and get the value
				handCard = self.player.getHandCard(self.handPosition)
				handCardValue = self.cardStringToValue(handCard)
				#check if the given move is valid, if valid --> store in vector

				#to temoporarily hold the valid positions
				tempValidMove = []
				#check for valid move
				if self.captureBuildSumChecker(handCardValue):
					#add hand and table position to the list
					tempValidMove.append(str(self.handPosition))
					for position in self.tablePosition:
						tempValidMove.append(position)
					#addding the valid move vector to the list
					validCaptureList.append(tempValidMove)

		return validCaptureList

	# #returns a list of all the valid moves for action Build
	def getValidBuildList(self):

		#indicates the move type, required since further checking functions uses the variable
		self.moveType = "b"

		#list to store all the valid capture moves
		validBuildList = []
		#get the power set
		powerSet = self.tablePositionPowerSet()
		#get the vector of hand cards
		handCardList = self.player.getAllHandCards()

		#get the local variable of the hand of the player 
		playerHand = self.player.getAllHandCards()
		#loop through each element of the power set
		for testTablePosition in powerSet:
			#set the table memeber variable to the set
			self.tablePosition = testTablePosition[:]
			#loop through each hand position
			for i in range(len(playerHand)):
				#set the memmber variable handPosition
				self.handPosition = i
				#get the hand card for given position and get the value
				handCard = self.player.getHandCard(self.handPosition)
				handCardValue = self.cardStringToValue(handCard)

				#moveCheck for build

				#get the vector of hand cards
				handCardList = self.player.getAllHandCards()

				#flag to find if build valued card in hand
				buildValueFound = False
				buildValue = 0
				#loop through all the hand cards to find the build valued hand card
				for k in range(len(handCardList)):

					#check for selected hand card and ignore if found
					if k == self.handPosition:
						continue

					#build value equals the value of given Hand Card
					buildValue = self.cardStringToValue(handCardList[k])

					#check validity for given hand card
					if buildValue >= handCardValue and self.captureBuildSumChecker(buildValue):
						#found a hand card whose value is equal to build Value
						buildValueFound = True

						#to temoporarily hold the valid positions
						tempValidMove = []
						tempValidMove.append(str(buildValue))
						tempValidMove.append(str(self.handPosition))
						for pos in self.tablePosition:
							tempValidMove.append(pos)
						#addding the valid move vector to the list
						validBuildList.append(tempValidMove)

						break
	
		return validBuildList

	#returns the best capture or build move
	def getBestValidMove(self,isCapture):

		#to store the list of all the valid moves
		validMoveList = []
		#stores the best valid move
		bestValidMove = []

		#check for capture or build
		if isCapture:
			validMoveList = self.getValidCaptureList()  
		else:
			validMoveList = self.getValidBuildList()  
		
		#get all the table cards
		tableCards = self.gameTable.getAllCards()

		#highscore and num cards to check when looping
		highestScore = -1
		prevNumCards = -1

		#loop through the list of all the valid capture moves
		for tempValidMove in validMoveList:

			#print(tempValidMove,": ",end='')
			#to calculate the score for given move
			score = 0
			currentNumCards = 0

			#if build ignore the first element since it is the build value
			buildValue = "-1"
			if not isCapture:
				buildValue = tempValidMove[0]
				del tempValidMove[0]

			#print(tempValidMove,": ",end='')  

			#get the hand card and add to the score
			card = self.player.getHandCard(int(tempValidMove[0]))
			#print(tempValidMove[0],card,end='')
			currentNumCards+=1
			score += self.scoreCalculator(card)
			#print(score,"_",end='')


			#get each table position
			for i in range(1,len(tempValidMove)):

				#std::cout<<tempValidMove.at(j)

				#get table card vector
				cardVector = tableCards[(int(tempValidMove[i]))]

				#print(cardVector,end='')


				#check for build or single card
				if len(cardVector)>2:
					j = 3
					for j in range(3,len(cardVector)):
						card = cardVector[j]
						if card!="[" and card!="]":
							#print(card,end='')
							score += self.scoreCalculator(card)
							#print(score," ",end='')
							currentNumCards+=1

				else:
					card = cardVector[1]
					#print(card,end='')
					score += self.scoreCalculator(card)
					#print(score," ",end='')
					currentNumCards+=1

			if score > highestScore or (score == highestScore and currentNumCards > prevNumCards):

				#set new highScore
				highestScore = score
				#set new best move
				bestValidMove = tempValidMove

				#add back the build value for build
				if not isCapture:
					bestValidMove.append(buildValue)

				#store the num cards, prevNumCards required to check for moves having same score
				#Changing the prevNumCards when new score is updated allows the numCard comparision
				#  only when the score are equal
				prevNumCards = currentNumCards

			#print("finalScore = ",score," currentNumCards:",currentNumCards," prevNumCards:",prevNumCards," HighScore = ",highestScore,"\n\n")

		#add the score at the end of the vector
		bestValidMove.append(str(highestScore))
		#add the number of cards 
		bestValidMove.append(str(prevNumCards))

		return bestValidMove

	#Check the card for aces and DX and S2 and calculates the score
	def scoreCalculator(self, card):
		score = 0
		if card == "CA" or card == "DA" or card == "SA" or card == "HA" or card == "S2":
			score = 1
		elif card == "DX":
			score = 2
		return score

	#sets the table and hand position
	def setPosTableHand(self, handPos, tablePos):
		self.handPosition = handPos
		self.tablePosition = tablePos[:]