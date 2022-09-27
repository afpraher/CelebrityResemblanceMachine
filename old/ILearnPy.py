#Ich konnte nicht wirklich beim Projekt helfen deshalb habe ich mir Python gelernt. --Benedikt Christain

##TicTacToe

class GameLogic:
    gameboard = [["-","-","-"],["-","-","-"],["-","-","-"]]
    symbolturn = "x"

    def __init__(self):
        #This is a method that gets called when the objekt is created
        gameboard = [["-","-","-"],["-","-","-"],["-","-","-"]]
        symbolturn = "x"

    def check(self):
        #This method checks if there is any full row on the board and returnes true if there is
        if self.gameboard[0][0] == self.gameboard[1][0] and self.gameboard[2][0] == self.gameboard[1][0] and self.gameboard[1][0]!="-":
            return True
        elif self.gameboard[0][1] == self.gameboard[1][1] and self.gameboard[2][1] == self.gameboard[1][1] and self.gameboard[1][1]!="-":
            return True
        elif self.gameboard[0][2] == self.gameboard[1][2] and self.gameboard[2][2] == self.gameboard[1][2] and self.gameboard[1][2]!="-":
            return True
        elif self.gameboard[0][0] == self.gameboard[0][1] and self.gameboard[0][2] == self.gameboard[0][1] and self.gameboard[0][1]!="-":
            return True
        elif self.gameboard[1][0] == self.gameboard[1][1] and self.gameboard[1][2] == self.gameboard[1][1] and self.gameboard[1][1]!="-":
            return True
        elif self.gameboard[2][0] == self.gameboard[2][1] and self.gameboard[2][2] == self.gameboard[2][1] and self.gameboard[2][1]!="-":
            return True
        elif self.gameboard[2][0] == self.gameboard[1][1] and self.gameboard[0][2] == self.gameboard[1][1] and self.gameboard[1][1]!="-":
            return True
        elif self.gameboard[0][0] == self.gameboard[1][1] and self.gameboard[2][2] == self.gameboard[1][1] and self.gameboard[1][1]!="-":
            return True
        else:
            return False

    def newGame(self):
        #This method resets the board so you can continue playing
        self.gameboard = [["-","-","-"],["-","-","-"],["-","-","-"]]
    
    def setPosToSymTurn(cord1,cord2,self):
        #This method checks if the selected space is empty("-") and replaces it with a Symbol
        #check
        if self.gameboard[cord2][cord1] == "-":
            #replace
            self.gameboard[cord2][cord1] = self.symbolturn
            #change symbol to use next
            if self.symbolturn == "x":
                self.symbolturn = "o"
            elif self.symbolturn == "o":
                self.symbolturn = "x"
            return True
        else:
            return False

    def getSymbol(self):
        #This method returnes the symbol(x/o) of the curent turn
        return self.symbolturn


class GameUI:
    def showBoard(board):
        #This method prints the gameboard for the user to see
        print(" ")
        print(" ","0","1","2","Cordinate 1")
        print("0",board[0][0],board[0][1],board[0][2])
        print("1",board[1][0],board[1][1],board[1][2])
        print("2",board[2][0],board[2][1],board[2][2])
        print("Cordinate 2")
        print(" ")


class Background:
    def checkInForInt(inp):
        #This method checks the variable(inp) to see if it is an intager
        try:
            int(inp)
            it_is = True
        except ValueError:
            it_is = False
        return it_is

#The 'main' method of the programm
#When the programm is started it starts hier
#create the class variables
gl = GameLogic
gui = GameUI
bg = Background
#start the game in endless loop
while True:
    #check for win
    if gl.check(gl):
        print("Congrats",gl.getSymbol(gl),"you won this game")
        #ask to continue playing
        continu = input("Will you play another game? (y/n)")
        if continu == "y":
            #if reset gameboard
            gl.newGame(gl)
        elif continu == "n":
            #if not exit endless loop
            print("See you soon sucker")
            break
        else:
            print("Not a valid answere")
    #show board
    gui.showBoard(gl.gameboard)
    #get input cords
    cord1 = input("Cordinate 1:")
    cord2 = input("Cordinate 2:")
    #check for valid inputs
    if bg.checkInForInt(cord1) and bg.checkInForInt(cord2):
        cord1 = int(cord1)
        cord2 = int(cord2)
        if cord1>2 or cord2>2 or cord1<0 or cord2<0:
            print("Not a valid answere")
            continue
        #try to set space to symbol
        ret = gl.setPosToSymTurn(cord1,cord2,gl)
        if not ret:
            print("This space is already in use")
    else:
        print("Not a vlaid answere")