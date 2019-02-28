class Player:
    # Constructor
    def __init__(self):
        #Member Variables:
        #score of the player
        self.score = 0
        #list to store the captured cards in pile
        self.pile = []
        #list to store the cards in the player's hand
        self.hand = []
                
    #returns the score of the player
    def getScore(self):
        return self.score

    #returns the size of the hand
    def getHandSize(self):
        return len(self.hand)
   
    #returns the card at given position
    def getHandCard(self, index):
        return self.hand[index]

    #returns the hand card of given index and erases the card    
    def popHandCard(self, index):
        return self.hand.pop(index)

    #returns copy of hand
    def getAllHandCards(self):
        return self.hand[:]     

    #returns copy of pile
    def getAllPileCards(self):
        return self.pile[:]
    
    #Mutators:
    #stores the given card in player hand
    def storeHand(self,card):
        self.hand.append(card)

    #stores the given card in player pile
    def storePile(self,card):
        self.pile.append(card)

    #adds the value to the score of the player
    def setScore(self,value):
        self.score = value

    #clears the pile
    def clearPile(self):
        self.pile.clear()

    #Utilities:
    #print cards in hand / pile
    #True for hand
    def printHandOrPile(self,isHand):
        if isHand == True:
            print(self.hand)
        else:
            print(self.pile)