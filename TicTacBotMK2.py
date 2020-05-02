from random import *
import os

#Retuns the player whose turn it is
def getPlayer(state):
	xnum = 0
	onum = 0
	for pos in state:
		if pos == "X":
			xnum = xnum + 1
		if pos == "O":
			onum = onum + 1
	if xnum > onum:
		return "O"
	else:
		return "X"

#Returns a list of all free positions
def getActions(state):
	posibleActions=[]
	i=0
	while i < len(state):
		if state[i]==" ":
			posibleActions.append(i)
		i = i + 1
	return posibleActions

#Returns the board after doing a specific action
def getResult(state,action):
	newstate=state.copy()
	newstate[action]=getPlayer(state)
	return newstate

#Returns true if the game is over
def isTerminal(state):
	terminal = 1
	for pos in state:
		if pos == " ":
			 terminal = 0
	pairs=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
	for pair in pairs:
		if state[pair[0]] == state[pair[1]] == state[pair[2]] != " ":
			terminal=1
	return terminal

#Returns the Score of a terminal state
#1 when X is the winner
#-1 when O is the winner
#0 when tied
def getScore(state):
	pairs=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
	for pair in pairs:
		if state[pair[0]] == state[pair[1]] == state[pair[2]] != " ":
			if state[pair[0]] == "X":
				return 1
			if state[pair[0]] == "O":	
				return -1
	return 0

#Get max value out of all possible actions in a state
def maxValue(state):
	#If it's terminal, returns the score
	if isTerminal(state):
		return getScore(state)
	value=-2
	#If it's not, calls minValue get the value from the potential moves of the other player
	for action in getActions(state):
		value=max(value,minValue(getResult(state,action)))
	return value

#Get min value out of all possible actions in a state
def minValue(state):
	#If it's terminal, returns the score
	if isTerminal(state):
		return getScore(state)
	value=2
	#If it's not, calls maxValue get the value from the potential moves of the other player
	for action in getActions(state):
		value=min(value,maxValue(getResult(state,action)))
	return value

#Print the board in terminal with the state provided
def printBoard(state):
	i=0
	j=1
	print("  A B C\n")
	while i < 8 :
		if i > 2 :
			print("  -+-+-")
		print(str(j)+" "+state[i]+"|"+state[i+1]+"|"+state[i+2])
		i = i + 3
		j = j + 1
	print("\n")

#Ask the player for input, checks if it's valid and modifies the state
#playerSymbol is X or O depending on which one is the player
def askInput(state, playerSymbol):
	row = -1
	col = -1
	while row == -1 or col == -1: 
		#Ask the player for input
		inputPos= input("You are "+playerSymbol+", your movement:")
		inputPos = inputPos.lower()
		#Check that it contains 1,2,3 and a,b,c
		if inputPos.find("1") != -1:
			row = 0
		elif inputPos.find("2") != -1:
			row = 1
		elif inputPos.find("3") != -1:
			row = 2
		if inputPos.find("a") != -1:
			col = 0
		elif inputPos.find("b") != -1:
			col = 1
		elif inputPos.find("c") != -1:
			col = 2
		#If it's not valid, notify user and ask again
		if row == -1 or col == -1 or state[col+(row*3)] != " ":
			print("Invalid movement")
			row = -1
			col = -1
		else :
			state[col+(row*3)] = playerSymbol

#Fro clearing the terminal
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
clear()
#Initial state is an empty board
board = [" "," "," "," "," "," "," "," "," "]
#If the quotes file is available, load them
if os.path.isfile("./TicTacQuotes.txt"):
	f = open('./TicTacQuotes.txt', 'r')
	quotes = f.readlines()
	f.close()
else:
	quotes = []
#Ask player for a coin toss, and assign the turn order
coinguess= input("(H)eads or (t)ails?:")
cointhrow = randint(0,1)
if cointhrow == 0:
	cointhrow = "h"
else:
	cointhrow = "t"
if coinguess.lower() == cointhrow:
	print("You guessed right, you are X")
	playerTurn="X"
else:
	print("You guessed wrong, you are O") 
	playerTurn="O"
printBoard(board)
#main loop, ends when the board is terminal
while isTerminal(board) == 0:
	#When it's the player's turn, ask for input and print the board
	if getPlayer(board) == playerTurn:
		askInput(board, playerTurn)
		clear()
		printBoard(board)
	#If it's the machine's turn
	if isTerminal(board) == 0 and getPlayer(board) != playerTurn:
		#If the quotes are available, print one at random
		if len(quotes) > 0:
			print(quotes[randint(0,len(quotes)-1)])
			print("      ― Sun Tzu, The Art of War \n\n\n")
		newstate=board.copy()
		#Depending who the machine is, get the best possible move
		if playerTurn == "X":
			value=2
			for action in getActions(board):
				currentvalue=maxValue(getResult(board,action))
				if currentvalue < value:
					value=currentvalue
					newstate=getResult(board,action)
		else:
			value=-2
			for action in getActions(board):
				currentvalue=minValue(getResult(board,action))
				if currentvalue > value:
					value=currentvalue
					newstate=getResult(board,action)
		board=newstate
		printBoard(board)
#Get winner and print a message
if getScore(board) == 1:
	if playerTurn == "X":
		print("I know you probably cheated, meatbag\n\n\n")
	else:
		print("You are no match for my superior intellect\n\n\n")
if getScore(board) == -1:
	if playerTurn == "O":
		print("I know you probably cheated, meatbag\n\n\n")
	else:
		print("You are no match for my superior intellect\n\n\n")
if getScore(board) == 0:
	print("You'll have to do better\n\n\n")