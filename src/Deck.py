import random

class Deck:
    def __init__(self, isNewRound):
        #Member Variables:
        #List of Cards
        self.cardDeck = []
        
        #check if it is new round else return without creating new cards
        #required when loading a game
        if isNewRound == True: 
            #assign values and suit to each of the 52 cards
            for i in range(52):
                #first character suit
                temp = 'D'
                if i < 13:
                    temp = 'S'
                elif i < 26:
                    temp = 'H'
                elif i < 26:
                    temp = 'C'

                #second character value
                tempValue = (i % 13)+1
                if tempValue == 1:
                    temp += 'A';
                elif tempValue < 10:
                    temp += str(tempValue);
                elif tempValue == 10:
                    temp += 'X';
                elif tempValue == 11:
                    temp += 'J';
                elif tempValue == 12:
                    temp += 'Q';
                else:
                    temp += 'K';

                #add the card to the deck
                self.cardDeck.append(temp)

            #shuffle the cards
            random.shuffle(self.cardDeck)

    #Selectors:
    #returns the first card of the cardDeck and removes it
    def getNewCard(self):
        return self.cardDeck.pop(0)

    #get veector of cards in deck
    def getDeck(self):
        return self.cardDeck[:]

    #returns the size of the cardDeck vector(number of cards)
    def getDeckSize(self):
        return len(self.cardDeck)

    #Mutators:
    #stores the given card in Deck
    def storeDeck(self,card):
        self.cardDeck.append(card)

    #Utilities
    def printDeckCards(self):
        print(self.cardDeck)