class Table:
    # Constructor
    def __init__(self):
        #list of list of cards
        # Rules for single card --> the first element, the value of the build
        #                         the second, the card 
        # * Rules for build --> the first element, the value of the build
        # *           the second, owner of the build: Human or Computer
        # *           the third, if the build is multi or single build: Single or Multi
        # *           the fourth, if single build then start inputting card else
        # *               if multi then "[" then start inputting card on fifth
        # *           nth, for multi "]" to end a single build inside multi
        self.gameBoard = []

    #stores the given card in a vector 
    def storeTable(self,card):

        #check if the card is string type
        if isinstance(card, str):
            #store the numeric value as string     
            if card[1] == 'A':
                cardValue = "1"
            elif card[1] == 'K':
                cardValue = "13"
            elif card[1] == 'Q':
                cardValue = "12"
            elif card[1] == 'J':
                cardValue = "11"
            elif card[1] == 'X':
                cardValue = "10"
            else:
                cardValue = str(card[1])

            #add info in a list
            temp = [cardValue,card]
            #append the list to the list of list
            self.gameBoard.append(temp)


        #the card is a list type
        #stores the value of card,string as first element of the card 
        else:
            self.gameBoard.append(card)

    #returns the table card of given index
    def popTableCard(self, index):
        temp = self.gameBoard[index]
        
        #check for loose or build card
        if len(temp) > 2:
            #build card
            #remove the brackets if multi build
            if temp[2] == "Multi":
                temp.remove("[")
                temp.remove("]")
            
            #remove the first three elements since card info starts form fourth
            for i in range(3):
                del temp[0]
        else:
            #loose card has 2 elements value and card
            #removing the value
            del temp[0]
    

        #erased the card and return
        #(index+1)th element
        del self.gameBoard[index]
        return temp

    #returns the size of the cardDeck vector(number of cards)
    def getTableSize(self):
        return len(self.gameBoard)

    #returns copy of board
    def getAllCards(self):
        return self.gameBoard[:]

    #print cards in table board
    def printTable(self):
        print (self.gameBoard)
