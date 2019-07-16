from tkinter import *
from GameEngine import GameEngine
from Human import Human
from Computer import Computer
from Table import Table
from Deck import Deck
import os
import copy
from pathlib import Path

#const defining the font type and size
LARGE_FONT= ("Verdana", 16)
SMALL_FONT= ("Verdana", 14)
TINY_FONT= ("Verdana", 12)


#main class
class SeaofBTCapp(Tk):

    #args - any num of arguments, passing variables
    #kwargs - kewy word arguments, passing through dictionaries
    def __init__(self, *args, **kwargs):
        
        #initializing tkinter
        Tk.__init__(self, *args, **kwargs)
        #conatins everything that we populate
        #frame = window
        container = Frame(self)

        #pack for quick window with less elements
        #fill -> fill in the space of pack
        #expan -> if there are any whitespace can expand
        container.pack(side="top", fill="both", expand = True)

        #part of tkinter.Tk, inheritance
        #simple configuration
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #dictionary
        self.frames = {}

        # Add any new windows here in (StartPage, LoadGame, NewGame, ....)
        #frames over frames
        for F in (StartPage, LoadGame, NewGame, NewRound,SaveGame): 

            frame = F(container, self)
            self.frames[F] = frame
            #grid what row and column want to be in
            #sticky -> alignment and stretch nsew
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    #shows the frame defined by controller, cont
    def show_frame(self, cont):

        frame = self.frames[cont]
        #raises the frame to the front
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

#start page
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller
        label = Label(self, text="Casino", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #buttons for Load and New Game
        #lambda allows create throwaway funciton when we call it
        #problem saving the returned value
        buttonNewGame = Button(self, text="New Game",
                            command=lambda: controller.show_frame(NewGame))
        buttonNewGame.pack()

        buttonLoadGame = Button(self, text="Load Game",
                            command=lambda: controller.show_frame(LoadGame))
        buttonLoadGame.pack()

#load page
class LoadGame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="New Game", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.fileName=""

        mypath = str(Path().absolute())+'\\serializationTest'
        fileList = os.listdir(mypath)

        for file in fileList:
            button = Button(self,text=file, command=lambda x=file:self.setFileName(x))
            button.pack()

        label = Label(self, text="Select a file", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        buttonLoad = Button(self,text="Load", command=lambda :self.controller.show_frame(NewRound))
        buttonLoad.pack()

    def setFileName(self, fileName):
        self.fileName = str(Path().absolute())+'\\serializationTest\\'+fileName
        #print(self.fileName)
    def getFileName(self):
        return self.fileName

#Coin toss
class NewGame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Select a button", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.button1 = Button(self, text="***", 
                            command= lambda: self.showTossResult(True) )
        self.button1.pack(side = "left")

        self.button2 = Button(self, text="***", 
                            command= lambda: self.showTossResult(False) )
        self.button2.pack(side = "right")
        self.flag = -2
        
    def showTossResult(self, heads):
        if heads:
            winnerString = "Human plays first"
            loserString = "Computer plays second"
            self.flag = 0
        else:
            winnerString = "Computer plays first"
            loserString = "Human plays second"
            self.flag = 1
            
        label1 = Label(self, text=winnerString)
        label1.pack()

        label2 = Label(self, text=loserString)
        label2.pack()

        self.button1.config(state=DISABLED)
        self.button2.config(state=DISABLED)

        self.setUpNewGame()
        
    def setUpNewGame(self):
        button1 = Button(self, text="Start Game", 
                            command= lambda: self.controller.show_frame(NewRound) )
        button1.pack(side = "bottom")

    def getFlag(self):
        return self.flag

#new round
class NewRound(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Game", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #self.round = casino.getGameTable()
        #flag for human as last capturer
        #self.lastCapturer = "None"
        #set true as deafault

        #NewGameReference = self.controller.get_page(NewGame)
        self.LoadGameReference = self.controller.get_page(LoadGame)
        self.NewGameReference = self.controller.get_page(NewGame)


        #required to prevent reloading the game when clicking the update button
        self.flag = -1

        self.casino = GameEngine()
        self.moveInfo = []

        self.buttonUpdate = Button(self, text="Update Board",command=lambda: self.updateBoard())
        self.buttonUpdate.pack()
        self.buttonSave = Button(self, text="Save",bg="blue", command=lambda: self.controller.show_frame(SaveGame))
        self.buttonSave.pack(side = TOP)

        #updateable varibales
        self.listHumanHand = []
        self.listComputerHand = []
        self.listTableCard = []
        self.prompt = Label(self)
        self.labelHuman = Label(self)
        self.labelComputer = Label(self)
        self.labelHumanPile = Label(self)
        self.labelComputerPile = Label(self)
        self.labelTable = Label(self)
        self.status = Label(self)
        
        self.buttonTrail = Button(self)
        self.buttonCapture = Button(self)
        self.buttonBuild = Button(self)
        self.buttonHelp = Button(self)
        self.buttonComputer = Button(self)
    
    def onSelect(self,pos,containerType):
        if(containerType == 'h'):
            self.moveInfo.clear()
        self.moveInfo.append(pos)
        print(self.moveInfo)

    def updateBoard(self,actionInfo = None):
        
        #load new game if the flag is -1
        if self.flag == -1:
            fileName = self.LoadGameReference.getFileName()
            self.flag = self.NewGameReference.getFlag()

            #load or new game
            if(self.flag == 0):
                self.casino = GameEngine(True)
                self.casino.printGameBoard()
            elif(self.flag == 1):
                self.casino = GameEngine(False)
                self.casino.printGameBoard()
            else:
                print(fileName)
                self.casino.loadGame(fileName)

            #indicate that the game has already been loaded once
            self.flag = -2
            #disable the update button
            self.buttonUpdate.config(state=DISABLED)
        
        #forget the button form the previous state
        for button in self.listHumanHand:
            button.pack_forget()
        for button in self.listComputerHand:
            button.pack_forget()
        for button in self.listTableCard:
            button.pack_forget()
        self.labelHuman.pack_forget()    
        self.labelComputer.pack_forget()
        self.labelTable.pack_forget()
        self.labelHumanPile.pack_forget()
        self.labelComputerPile.pack_forget()
        self.status.pack_forget()

        self.buttonComputer.pack_forget()
        self.buttonTrail.pack_forget()
        self.buttonCapture.pack_forget()
        self.buttonBuild.pack_forget()
        self.buttonHelp.pack_forget()
        self.prompt.pack_forget()

        #get the turn of the player to display
        if self.casino.isHumanTurn():
            turn = "Human"
        else:
            turn = "Computer"

        data = "Round: "+str(self.casino.getRound())+"\n Turn: "+turn+"\n Human Score: "+str(self.casino.getHuman().getScore())+"\n Computer Score: "+str(self.casino.getComputer().getScore())+"\nLast Capturer: "+self.casino.getLastCapturer()
        self.status = Label(self, text=data, font=TINY_FONT, borderwidth=3, relief="sunken")
        self.status.pack(pady=10,padx=10)

        #pack only the required button depending upon the turn of the player
        if self.casino.isHumanTurn():
            self.buttonTrail = Button(self, text="Trail",command=lambda: self.makeMove("t"))
            self.buttonTrail.pack(side = TOP)
            self.buttonCapture = Button(self, text="Capture",command=lambda: self.makeMove("c"))
            self.buttonCapture.pack(side = TOP)
            self.buttonBuild = Button(self, text="Build",command=lambda: self.makeMove("b"))
            self.buttonBuild.pack(side = TOP)
            self.buttonHelp = Button(self, text="Help",bg="red",command=lambda: self.makeMove("Help"))
            self.buttonHelp.pack(side = TOP)
        else:
            self.buttonComputer = Button(self, text="ComputerMove",command=lambda: self.makeMove("Computer"))
            self.buttonComputer.pack(side = TOP)

        #check if the argument is not empty
        #display the feedback from each move
        if actionInfo is not None:
            self.prompt = Label(self, text = actionInfo, font=TINY_FONT,borderwidth=3, relief="sunken")
            self.prompt.pack()

        #human hand
        self.labelHuman = Label(self, text="Human:", font=LARGE_FONT)
        self.labelHuman.pack(pady=10,padx=10)
        index = 0
        for card in self.casino.getHuman().getAllHandCards():
            button = Button(self, text=card, command=lambda x=index: self.onSelect(x,'h'))
            button.pack(side = TOP)
            self.listHumanHand.append(button)
            index += 1 
        
        #human pile
        info=""
        for card in self.casino.getHuman().getAllPileCards():
            info+=card+" "
        self.labelHumanPile = Label(self, text="Pile: "+info, font=TINY_FONT,borderwidth=3, relief="sunken")
        self.labelHumanPile.pack()


        #computer hand
        self.labelComputer = Label(self, text="Computer:", font=LARGE_FONT)
        self.labelComputer.pack(pady=10,padx=10)
        index = 0
        for card in self.casino.getComputer().getAllHandCards():
            button = Button(self, text=card)
            button.pack(side = TOP)
            self.listComputerHand.append(button)
            index += 1 
        
        #comuter pile
        info=""
        for card in self.casino.getComputer().getAllPileCards():
            info+=card+" "
        self.labelComputerPile = Label(self, text="Pile: "+info, font=TINY_FONT, borderwidth=3, relief="sunken")
        self.labelComputerPile.pack()

        #table
        self.labelTable = Label(self, text="Table:", font=LARGE_FONT)
        self.labelTable.pack(pady=10,padx=10)
        index = 0
        for card in self.casino.getGameTable().getAllCards():
            button = Button(self, text=card, command=lambda x=index: self.onSelect(x,'t'))
            button.pack(side = LEFT)
            self.listTableCard.append(button)
            index += 1 

    def makeMove(self,moveType):

        #add the move type to the move info and make move
        self.moveInfo.insert(0,moveType)
        feedback = self.casino.makeMove(self.moveInfo[:])
        self.moveInfo.clear()
        feedback += self.casino.checkGameChanges()
        self.updateBoard(feedback)

    def returnGame(self):
        return self.casino

#save game
class SaveGame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Save Game", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        L1 = Label(self, text="Enter fileName")
        L1.pack( side = LEFT)
        self.E1 = Entry(self, bd =5)
        self.E1.pack(side = RIGHT)

        NewRoundReference = self.controller.get_page(NewRound)
        self.casino = NewRoundReference.returnGame()
        
        buttonSave = Button(self, text="Save",command=lambda: self.save())
        buttonSave.pack()        

    def save(self):
        fileName = self.E1.get()
        print(fileName)
        self.casino.saveGame(fileName)
        close_window()

def close_window(): 
    app.destroy()

app = SeaofBTCapp()
#create an object of Game
app.mainloop()

