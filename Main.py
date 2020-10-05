import pygame
from Tiles import Tiles
from Nodes import Nodes
from copy import deepcopy
from tkinter import *
from tkinter import filedialog

def main():

	pygame.init(); #initiate pygame

	gray=(220,220,220);	#for colors if need be
	white=(245,245,245);
	green=(15,200,25);
	white=(255,255,255)

	row = 3 ; #for the 3x3
	col = 3;

	GameBoard=[[1,1,1],[1,1,1],[1,1,1]]; #creating my 3x3 list 
	count=0	#for the number to be put
	tilePosX=100; #initial tile position for the tile 1
	tilePosY=10;

	emptyTilePosI=0 #two markers for the placement of the empty tile. Useful later
	emptyTilePosJ=0

	movechecker=0; #this is for the printing of current move

	button_flags=True #flag for the appearance of the solve buttons and titles

	game_Finished=False #flag to know if the game is finished

	pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
	font = pygame.font.SysFont('Times New Roman', 30)
	font1 = pygame.font.SysFont('Times New Roman', 20)
	font2 = pygame.font.SysFont('Times New Roman', 15)


	with open("puzzle.in", "r") as file: #read the puzzle content in puzzle.in

		puzzle = file.readlines() #read it per line


	for i in range(3): #split the files
		puzzle[i]=puzzle[i].split(" ")

	for i in range(row):	#two loops so i can create an object of tiles in my 3x3 list
		for j in range(col):
			if int(puzzle[i][j]) == 0: #empty tile
					emptyTilePosI=i #get the position of the empty tile in the array for later use
					emptyTilePosJ=j
			GameBoard[i][j]=Tiles(int(puzzle[i][j]),tilePosX,tilePosY); #insert the object in my list by getting the text in the puzzle.in and converting it into an int
			tilePosX+=200;	#adjust the posiution so they wont stack
		tilePosX=100; #reset the tile to position 100 for the 2nd level of the list
		tilePosY+=200 #adjust the y value so they wont stack

	tilePosX=100; #initial tile position for the tile 1 #
	tilePosY=10; #set this to the original position for the reset of your puzzle later

	AIBOARD = [[1,1,1],[1,1,1],[1,1,1]] # board for my BFS and DFS

	for i in range(row):	#fill my ai board array
		for j in range(col):	
			AIBOARD[i][j]=int(puzzle[i][j]);

	initialStateNode = Nodes(AIBOARD,emptyTilePosI, emptyTilePosJ, None, None, 0, computeH(AIBOARD), computeF(0, computeH(AIBOARD))); #create my initial state node from my pizzle

	checker = False #flag for printing solvable or not
	if isBoardSolvable(GameBoard): #check if the board is solvable
		checker = True #if it's solvable, set the checker flag to true (will be used for printing later)

	gameDisplay=pygame.display.set_mode((1500,700)) #set my surface and screen size
	pygame.display.set_caption('Malonzo Exer 1 8-Game') #set the caption of the game

	clock = pygame.time.Clock() #for the fps of your game

	gameExit=False; #flag if you want to exit the game
	

	while not gameExit: #while the user is not clicking the exit
		

		gameDisplay.fill(white); #background color

		CONGRATULATIONS = font.render('YOU WON! CONGRATULATIONS!', False, (0, 0, 0)) #these are for my displaying of buttons and title in my GUI
		isSolvable = font.render('The puzzle is solvable! Go get em!!', False, (0, 0, 0))
		notSolvable = font.render('Unfortunately, the puzzle is not solvable! ', False, (0, 0, 0))

		BFS_BUTTON_NAME = font1.render('BFS ', False, (0, 0, 0))
		DFS_BUTTON_NAME = font1.render('DFS ', False, (0, 0, 0))
		A_BUTTON_NAME = font1.render('A* ', False, (0, 0, 0))
		BrowseFile_BUTTON_NAME = font1.render('Select File ', False, (0, 0, 0))
		BrowseFile_Name = font1.render('Browse A Puzzle Config: ', False, (0, 0, 0))

		DFS_BUTTON= pygame.draw.rect(gameDisplay, gray, [880, 180 ,60,40])
		BFS_BUTTON= pygame.draw.rect(gameDisplay, gray, [880, 120 ,60,40])
		A_BUTTON= pygame.draw.rect(gameDisplay, gray, [960, 120 ,60,40])
		BrowseFile_BUTTON= pygame.draw.rect(gameDisplay, gray, [1150, 120 ,120,40])

		NEXT_BUTTON_NAME = font1.render('NEXT ', False, (0, 0, 0))

		Show_Solution = font1.render('Click one of these to show  ', False, (0, 0, 0))
		Show_Solution_2 = font1.render('the Solution! ', False, (0, 0, 0))


		if button_flags==False: #if the user clicked any of the solution button, show these buttons and titles
			Solution_Name = font1.render('SOLUTION: ', False, (0, 0, 0)) #show the solution to found by the selected algo
			gameDisplay.blit(Solution_Name,(700,250))

			if game_Finished==True:

				Cost_Name = font.render("Path Cost: " +str(Cost), False, (0, 0, 0)) #print the path cost
				gameDisplay.blit(Cost_Name,(700,500))

			PathCC=""

			for character in PathCost: #get the literal path
				PathCC+=character

			PathC="" #this is the string for the revcersed string, to properly get the path

			index = len(PathCC) #get the length of the literal path

			while index > 0 : #reverse the string
				PathC+=PathCC[index-1]
				index-=1

			SolutionString = font1.render(PathC, False, (0, 0, 0)) #render the Path of the answer in the gui
			gameDisplay.blit(SolutionString,(700,300))


			NEXT_BUTTON= pygame.draw.rect(gameDisplay, gray, [870, 425 ,100,40]) #next button
			gameDisplay.blit(NEXT_BUTTON_NAME,(892,433))

			Current_Move = font1.render("Current Move: " + PathC[movechecker], False, (0, 0, 0))  #render the current move
			gameDisplay.blit(Current_Move,(700,375))


			if movechecker<Cost-1: #if it is not the last in the string, print the next move so the user will know
				Next_Move = font1.render("Next Move: " + PathC[movechecker+1], False, (0, 0, 0))
				gameDisplay.blit(Next_Move,(900,375))


		for event in pygame.event.get():	 #event handlers

		

			if event.type == pygame.QUIT: #if the user clicks the exit
				gameExit=True; #set the flag to true so the loop will end

			if game_Finished == False and checker == True: #if the game is not yet finished and board is solvable, you can interact with it

				if event.type == pygame.MOUSEBUTTONUP:

					if button_flags==False: #if user want to find the solution and the bfs or dfs button was clicked
						if NEXT_BUTTON.collidepoint(pygame.mouse.get_pos()): #if user clicks the next button
							# print("next")

							if PathC[movechecker] == "U": # if the move is up
								print("UP")
								GameBoard = GameBoard[emptyTilePosI][emptyTilePosI].swapTiles(GameBoard, emptyTilePosI,emptyTilePosJ, emptyTilePosI-1, emptyTilePosJ) #since you're switching an up tile, you need to -1 the i index to get the up tile
								emptyTilePosI=emptyTilePosI-1 #update the new I of the empty tile
							elif PathC[movechecker] == "R": #if the move is right
								print("R")
								GameBoard = GameBoard[emptyTilePosI][emptyTilePosI].swapTiles(GameBoard, emptyTilePosI,emptyTilePosJ, emptyTilePosI, emptyTilePosJ+1) #since you're switching a right tile, you need to +1 the j index to get the right tile
								emptyTilePosJ=emptyTilePosJ+1 #update the new J of the empty tile
							elif PathC[movechecker] == "L":
								print("L")
								GameBoard = GameBoard[emptyTilePosI][emptyTilePosI].swapTiles(GameBoard, emptyTilePosI,emptyTilePosJ, emptyTilePosI, emptyTilePosJ-1) #since you're switching a left tile, you need to -1 the j index to get the left tile
								emptyTilePosJ=emptyTilePosJ-1 #update the new J of the empty tile
							elif PathC[movechecker] == "D":
								print("D")
								GameBoard = GameBoard[emptyTilePosI][emptyTilePosI].swapTiles(GameBoard, emptyTilePosI,emptyTilePosJ, emptyTilePosI+1, emptyTilePosJ) #since you're switching a down tile, you need to +1 the i index to get the down tile
								emptyTilePosI=emptyTilePosI+1 #update the new I of the empty tile

							if movechecker<Cost-1: #update the movechecker for the next moves
								movechecker+=1;

							

					if button_flags==True: #if the player asks for the solution, stop the playabale board

						if BFS_BUTTON.collidepoint(pygame.mouse.get_pos()): #if the user clicked the BFS button
								print("BFS BUTTON CLICKED!")
								button_flags=False #indicate that the solution buttons were clicked

								BFSWINNINGSTATE=BFS(initialStateNode) #BFS solution
								PathCost=followPath(BFSWINNINGSTATE) #get the path and cost

								Cost=PathCost.pop() #pop the cost which is in the top most of my array

								#reset the board
								for i in range(row):	#two loops so i can create an object of tiles in my 3x3 list
									for j in range(col):
										if int(puzzle[i][j]) == 0: #empty tile
												emptyTilePosI=i #get the position of the empty tile in the array for later use
												emptyTilePosJ=j
										GameBoard[i][j]=Tiles(int(puzzle[i][j]),tilePosX,tilePosY); #insert the object in my list by getting the text in the puzzle.in and converting it into an int
										tilePosX+=200;	#adjust the posiution so they wont stack
									tilePosX=100; #reset the tile to position 100 for the 2nd level of the list
									tilePosY+=200 #adjust the y value so they wont stack

								
								SavePath(PathCost) #save the path


						if DFS_BUTTON.collidepoint(pygame.mouse.get_pos()): #if user clicked the dfs button
							print("DFS BUTTON CLICKED!")
							button_flags=False #tell the program that the solve button was clicked

							DFSWINNINGSTATE=DFS(initialStateNode) #solve by iDFS	
							PathCost=followPath(DFSWINNINGSTATE) #get path and cost

							Cost=PathCost.pop() #pop the cost 

							#Reset the Board
							for i in range(row):	#two loops so i can create an object of tiles in my 3x3 list
								for j in range(col):
									if int(puzzle[i][j]) == 0: #empty tile
											emptyTilePosI=i #get the position of the empty tile in the array for later use
											emptyTilePosJ=j
									GameBoard[i][j]=Tiles(int(puzzle[i][j]),tilePosX,tilePosY); #insert the object in my list by getting the text in the puzzle.in and converting it into an int
									tilePosX+=200;	#adjust the posiution so they wont stack
								tilePosX=100; #reset the tile to position 100 for the 2nd level of the list
								tilePosY+=200 #adjust the y value so they wont stack

							SavePath(PathCost) #save the path

						if A_BUTTON.collidepoint(pygame.mouse.get_pos()):
							print("A* BUTTON CLICKED!")
							button_flags=False #tell the program that the solve button was clicked

							AWINNINGSTATE=AStar(initialStateNode) #solve it by using A*
							PathCost=followPath(AWINNINGSTATE) #get the path and cost

							Cost=PathCost.pop() #pop the cost which is in the top most of my array

							#reset the board
							for i in range(row):	#two loops so i can create an object of tiles in my 3x3 list
								for j in range(col):
									if int(puzzle[i][j]) == 0: #empty tile
											emptyTilePosI=i #get the position of the empty tile in the array for later use
											emptyTilePosJ=j
									GameBoard[i][j]=Tiles(int(puzzle[i][j]),tilePosX,tilePosY); #insert the object in my list by getting the text in the puzzle.in and converting it into an int
									tilePosX+=200;	#adjust the posiution so they wont stack
								tilePosX=100; #reset the tile to position 100 for the 2nd level of the list
								tilePosY+=200 #adjust the y value so they wont stack

							
							SavePath(PathCost) #save the path

						if BrowseFile_BUTTON.collidepoint(pygame.mouse.get_pos()):
							print("Browse A File") #use tkinter as a file browswer
							root = Tk()
							root.title("Brows a Config")

							root.filename = filedialog.askopenfilename(initialdir="/puzzle_configs", title="Select A Puzzle Config", filetypes=[("in files" , "*.in")]) #browse files named .in
					
							# print(root.filename)
							tilePosY=10 #set the x and y again for the board rect positions in GUI
							tilePosX=100

							#load my new board configuration

							with open(root.filename, "r") as file: #read the puzzle content the selected in

								puzzle = file.readlines() #read it per line


							for i in range(3): #split the files
								puzzle[i]=puzzle[i].split(" ")

							for i in range(row):	#two loops so i can create an object of tiles in my 3x3 list
								for j in range(col):
									if int(puzzle[i][j]) == 0: #empty tile
											emptyTilePosI=i #get the position of the empty tile in the array for later use
											emptyTilePosJ=j
									GameBoard[i][j]=Tiles(int(puzzle[i][j]),tilePosX,tilePosY); #insert the object in my list by getting the text in the puzzle.in and converting it into an int
									tilePosX+=200;	#adjust the posiution so they wont stack
								tilePosX=100; #reset the tile to position 100 for the 2nd level of the list
								tilePosY+=200 #adjust the y value so they wont stack

							tilePosX=100; #initial tile position for the tile 1 #
							tilePosY=10; #set this to the original position for the reset of your puzzle later

							#create my problem solving board again
							AIBOARD = [[1,1,1],[1,1,1],[1,1,1]] # board for my BFS and DFS

							for i in range(row):	#fill my ai board array
								for j in range(col):	
									AIBOARD[i][j]=int(puzzle[i][j]);

							initialStateNode = Nodes(AIBOARD,emptyTilePosI, emptyTilePosJ, None, None, 0, computeH(AIBOARD), computeF(0, computeH(AIBOARD))); #create my initial state node from my pizzle

							print("New Puzzle Config Loaded")

							#check if the board is solvable again
							checker = False #flag for printing solvable or not
							if isBoardSolvable(GameBoard): #check if the board is solvable
								checker = True #if it's solvable, set the checker flag to true (will be used for printing later)
							
							root.withdraw() #to close my tkinter after clicking it
							# root.mainloop()


						for i in range(row): #loop to check what tile was clicked in the array
							for j in range(col):



								if GameBoard[i][j].rectangle.collidepoint(pygame.mouse.get_pos()): #to know which tile was

									if GameBoard[i][j].NotEmpty(): #check if it is not an empty tile
										# print("not empty")
										if GameBoard[i][j].neighborEmptyTile(GameBoard,emptyTilePosI, emptyTilePosJ, i, j): #check if it can be changed with the empty tile
											# print("CLICKABLE BECAUSE IT IS A NEIGHBOR OF AN EMPTY TILE!")

											GameBoard = GameBoard[i][j].swapTiles(GameBoard, emptyTilePosI, emptyTilePosJ, i, j) #go to the swap tiles function and swap the tiles

											emptyTilePosI=i;	#the new empty tile will be the the one you clicked
											emptyTilePosJ=j;



									break

		for i in range(row): #loop to make my tiles appear
			for j in range(col):
				gameDisplay.blit(GameBoard[i][j].image,(GameBoard[i][j].xPos,GameBoard[i][j].yPos)) #to make my tiles appear

		if isFinished(GameBoard):
			gameDisplay.blit(CONGRATULATIONS,(150,650))
			game_Finished=True #game is finished, you can no longer interact with the board

		if checker == True: #if my checked flag on top say that it is solvable then print solvable
			gameDisplay.blit(isSolvable,(150,600))
		else: #if it is not solvable, stop the game and print not solvable
			gameDisplay.blit(notSolvable,(150,600))


		
		gameDisplay.blit(BFS_BUTTON_NAME,(892,130)) #print the other text buttons and the button
		gameDisplay.blit(DFS_BUTTON_NAME,(892,190))
		gameDisplay.blit(A_BUTTON_NAME,(980,130))
		gameDisplay.blit(Show_Solution,(805,50))
		gameDisplay.blit(Show_Solution_2,(860,75))
		gameDisplay.blit(BrowseFile_BUTTON_NAME,(1165,128))
		gameDisplay.blit(BrowseFile_Name,(1100,70))




		pygame.display.update(); #update my game

		clock.tick(30); #how much fps you want


def isFinished(GameBoard): #function that checks if the game is over
	count=1; #count for the tile checker
	for i in range(3): #loop to know if the tiles are in the right order
		for j in range(3):
			if(i == 2 and j == 2): #means that the last tile is 0, game won!
				break

			if(GameBoard[i][j].number != count): #if one is displaced. it's not over
				return False
			count+=1

	return True #means that the tiles are sorted, Game is won!


def isBoardSolvable(GameBoard):  #function that solves and determines if the board is solvable or not
	inversions=0	# I used the inversion method to count how many inversion in my board are there

	for i in range(3): #loop the tiles in my board
		for j in range(3):
			m=j #used this m so i can reset the m to col to 0 after the next row, to scan the tiles properly

			for k in range(i,3): #loop the tiles after the current tiles
				for l in range(m,3):


					if(GameBoard[k][l].number == 0): #should not include the 0/blank
						continue

					if GameBoard[i][j].number > GameBoard[k][l].number: #if the current tile is greater than the next tile
						inversions+=1 #then it is counted as an inversion
						
				m=0;

	print(inversions)

	if inversions%2 == 1:	#if inversions are odd, the board is not solvable
		return False
	return True #if the inversions are even, it is solvable
	

def BFS(Node):
	frontierQueue = [] #create my frontier list
	frontierQueue.append(Node) #appebd the first node to my froniter
	explored = [] #create my explored list
	while len(frontierQueue) > 0 : #while frontier isnot empty
		currentState = frontierQueue.pop(0) #pop the frontier to the current state
		explored.append(currentState.puzzle) #put the puzzle state of the current puzzle to the explored list



		if GoalTest(currentState): #check if it is the winning condutuib
		
			print("FOUND THE WINNING STATE BY BFS!")
			return currentState #return the current state which has reached the winning condition


		for a in Actions(currentState): #go to my current state function and see what actions I can do in my current state and loop those actions


			currentStateCopy = deepcopy(currentState.puzzle) #used deep copy to copy my board because lists in python are passed by reference

			newState = Result(currentState, currentStateCopy, a) #go to the action in this current state and put it in new state

			frontierBoards = [node.puzzle for node in frontierQueue] #create and get the array of puzzles in frontier


			if newState.puzzle not in explored and newState.puzzle not in frontierBoards: #if the new state's puzzle is not in explored list or the frontier's puzzle state list
				frontierQueue.append(newState); #append it in the frontier to be explored later
				print("Append!")

def DFS(Node):
	frontierStack = [] #create my frontier list
	frontierStack.append(Node) #appebd the first node to my froniter
	explored = [] #create my explored list
	while len(frontierStack) > 0 : #while frontier isnot empty
		currentState = frontierStack.pop() #pop the frontier to the current state
		explored.append(currentState.puzzle) #put the puzzle state of the current puzzle to the explored list



		if GoalTest(currentState): #check if it is the winning condutuib
			# for i in range(3):
			# 	print(str(currentState.puzzle[i][0])+str(currentState.puzzle[i][1])+str(currentState.puzzle[i][2]))
			print("FOUND THE WINNING STATE BY BFS!")
			return currentState #return the current state which has reached the winning condition


		for a in Actions(currentState): #go to my current state function and see what actions I can do in my current state and loop those actions

			for i in range(3):
				print(str(currentState.puzzle[i][0])+str(currentState.puzzle[i][1])+str(currentState.puzzle[i][2]))

			currentStateCopy = deepcopy(currentState.puzzle) #used deep copy to copy my board because lists in python are passed by reference

			newState = Result(currentState, currentStateCopy, a) #go to the action in this current state and put it in new state
			#print(a)

			frontierBoards = [node.puzzle for node in frontierStack] #create and get the array of puzzles in frontier

			print()
			for i in range(3):
				print(str(newState.puzzle[i][0])+str(newState.puzzle[i][1])+str(newState.puzzle[i][2]))
			print()
			# print("I'm here")

			if newState.puzzle not in explored and newState.puzzle not in frontierBoards: #if the new state's puzzle is not in explored list or the frontier's puzzle state list
				if GoalTest(newState): # put a checker here so that i can get the answer more quickly
					print("FOUND THE WINNING STATE BY DFS!")
					return newState

				frontierStack.append(newState); #append it in the frontier to be explored later
				print("Append!")


def GoalTest(currentState): #check if the board is correct
	count=1; #count for the tile checker
	for i in range(3): #loop to know if the tiles are in the right order
		for j in range(3):
			if(i == 2 and j == 2): #means that the last tile is 0, game won!
				break

			if(currentState.puzzle[i][j] != count): #if one is displaced. it's not over
				return False
			count+=1

	return True #means that the tiles are sorted, Game is won!

def Actions(currentState):
	emptyTilePosI = currentState.emptyTilePosI #get the I position of the empty tile
	emptyTilePosJ = currentState.emptyTilePosJ #get the J position of the empty tile

	if(emptyTilePosI == 0 and emptyTilePosJ == 0 ): #if empty tile is in top left most
		Actions = ['R','D']
	elif(emptyTilePosI == 0 and emptyTilePosJ == 1 ): #if empty tile is in top left most
		Actions = ['L','R','D']
	elif(emptyTilePosI == 0 and emptyTilePosJ == 2 ): #if empty tile is in top left most
		Actions = ['L','D']
	elif(emptyTilePosI == 1 and emptyTilePosJ == 0 ): #if empty tile is in top left most
		Actions = ['U','R','D']
	elif(emptyTilePosI == 1 and emptyTilePosJ == 1 ): #if empty tile is in top left most
		Actions = ['U','L','R','D']
	elif(emptyTilePosI == 1 and emptyTilePosJ == 2 ): #if empty tile is in top left most
		Actions = ['U','L','D']
	elif(emptyTilePosI == 2 and emptyTilePosJ == 0 ): #if empty tile is in top left most
		Actions = ['U','R']
	elif(emptyTilePosI == 2 and emptyTilePosJ == 1 ): #if empty tile is in top left most
		Actions = ['U','R', 'L']
	elif(emptyTilePosI == 2 and emptyTilePosJ == 2 ): #if empty tile is in top left most
		Actions = ['U','L']

	return Actions

def Result(currentState, currentBoard, Action): #function that determines the result puzzle state if you do that action in your current puzzle state (for BFS and DFS)
	if(Action == 'L'):
		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI, currentState.emptyTilePosJ-1) #since you're switching a left tile, you need to -1 the j index to get the left tile

		newState = Nodes(newBoard, currentState.emptyTilePosI, currentState.emptyTilePosJ-1, 'L', currentState, 0, 0, 0) #instantiate a new node for this move with L as the move and current state as its parent

	elif(Action == 'R'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI, currentState.emptyTilePosJ+1) #since you're switching a right tile, you need to +1 the j index to get the rihgt tile

		newState = Nodes(newBoard, currentState.emptyTilePosI, currentState.emptyTilePosJ+1, 'R', currentState, 0, 0, 0) #instantiate a new node for this move with R as the move and current state as its parent

	elif(Action == 'U'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI-1, currentState.emptyTilePosJ) #since you're switching an up tile, you need to -1 the i index to get the up tile

		newState = Nodes(newBoard, currentState.emptyTilePosI-1, currentState.emptyTilePosJ, 'U', currentState, 0, 0, 0) #instantiate a new node for this move with U as the move and current state as its parent

	elif(Action == 'D'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI+1, currentState.emptyTilePosJ) #since you're switching down tile, you need to +1 the i index to get the down tile

		newState = Nodes(newBoard, currentState.emptyTilePosI+1, currentState.emptyTilePosJ, 'D', currentState, 0, 0,0) #instantiate a new node for this move with D as the move and current state as its parent

	return newState


def Result2(currentState, currentBoard, Action, g): #function that determines the result puzzle state if you do that action in your current puzzle state (for A* search)
	if(Action == 'L'):
		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI, currentState.emptyTilePosJ-1) #since you're switching a left tile, you need to -1 the j index to get the left tile

		newState = Nodes(newBoard, currentState.emptyTilePosI, currentState.emptyTilePosJ-1, 'L', currentState, g, computeH(newBoard), computeF(g, computeH(newBoard))) #instantiate a new node for this move with L as the move and current state as its parent

	elif(Action == 'R'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI, currentState.emptyTilePosJ+1) #since you're switching a right tile, you need to +1 the j index to get the rihgt tile

		newState = Nodes(newBoard, currentState.emptyTilePosI, currentState.emptyTilePosJ+1, 'R', currentState, g, computeH(newBoard), computeF(g, computeH(newBoard))) #instantiate a new node for this move with R as the move and current state as its parent

	elif(Action == 'U'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI-1, currentState.emptyTilePosJ) #since you're switching an up tile, you need to -1 the i index to get the up tile

		newState = Nodes(newBoard, currentState.emptyTilePosI-1, currentState.emptyTilePosJ, 'U', currentState, g, computeH(newBoard), computeF(g, computeH(newBoard))) #instantiate a new node for this move with U as the move and current state as its parent

	elif(Action == 'D'):

		newBoard = swapTiles(currentBoard, currentState.emptyTilePosI,currentState.emptyTilePosJ, currentState.emptyTilePosI+1, currentState.emptyTilePosJ) #since you're switching down tile, you need to +1 the i index to get the down tile

		newState = Nodes(newBoard, currentState.emptyTilePosI+1, currentState.emptyTilePosJ, 'D', currentState, g, computeH(newBoard), computeF(g, computeH(newBoard))) #instantiate a new node for this move with D as the move and current state as its parent

	return newState


def swapTiles(GameBoard, emptyTilePosI,emptyTilePosJ, i, j): #if you the tiles are being swapped
		
		GameBoard[i][j], GameBoard[emptyTilePosI][emptyTilePosJ] = GameBoard[emptyTilePosI][emptyTilePosJ], GameBoard[i][j] #switch the position of the tile and empty tile in thje array

		return GameBoard

def followPath(WinningNode): #function that follows the path of the winning node
	Path=[]
	Cost=0

	node=WinningNode
	while(node.parentTile!=None): #while it is not the root node
		Path.append(node.Action) #append the action to the list
		Cost+=1; #add it to the cost
		node=node.parentTile #go to the parent node

	Path.append(Cost);

	return Path

def SavePath(PathCost): #function that saves the answer to puzzle.out
	with open("puzzle.out", "w") as file: #Save the Path to puzzle.out
		for i in range(len(PathCost)-1,-1, -1):
			file.write(PathCost[i])
			file.write(" ")

def computeH(GameBoard):
	sumofH=0;
	for i in range(3):
		for j in range(3):
			if GameBoard[i][j] == 0: #if it is the empty tile skip it
				continue;
			elif GameBoard[i][j] == 1: #if it is 1
				sumofH += abs(i-0) + abs(j-0) #the correct position is (0,0)
			elif GameBoard[i][j] == 2: #if it is 2
				sumofH += abs(i-0) + abs(j-1) #the correct position is (0,1)
			elif GameBoard[i][j] == 3: #if it is 3
				sumofH += abs(i-0) + abs(j-2) #the correct position is (0,2)
			elif GameBoard[i][j] == 4: #if it is 4
				sumofH += abs(i-1) + abs(j-0) #the correct position is (1,0)
			elif GameBoard[i][j] == 5: #if it is 5
				sumofH += abs(i-1) + abs(j-1) #the correct position is (1,1)
			elif GameBoard[i][j] == 6: #if it is 6
				sumofH += abs(i-1) + abs(j-2) #the correct position is (1,2)
			elif GameBoard[i][j] == 7: #if it is 7
				sumofH += abs(i-2) + abs(j-0) #the correct position is (2,0)
			else:  #if it is 8
				sumofH += abs(i-2) + abs(j-1) #the correct position is (2,1)
	return sumofH

def computeG(Node): #function that computes my g
	sumofG=0; #the sum of g
	NodePointer=Node #the pointer that points to the node
	while(NodePointer.parentTile!=None): #while it is not the root node, iterate it
		sumofG+=1; #add 1 to g
		NodePointer=NodePointer.parentTile; #go to the parent tile of the current node

	return sumofG; #return the sum of g and it is the g of your current node

def computeF(g,h): # compute f by adding g and h
	return g+h

def AStar(Node):

	openList = [] #create my frontier list
	openList.append(Node) #append the first node to my froniter
	closedList = [] #create my explored list
	while len(openList) > 0:
		bestNode = minimumF(openList);  #get the minimum node that contains an f
		print(bestNode.f)
		closedList.append(bestNode.puzzle); #add it to the explored list

		if GoalTest(bestNode): #check if it is the winning condition
			print("FOUND THE WINNING STATE BY A*!")
			return bestNode #return the current state which has reached the winning condition

		for a in Actions(bestNode): #go to my current state function and see what actions I can do in my current state and loop those actions

			bestNodeCopy = deepcopy(bestNode.puzzle) #used deep copy to copy my board because lists in python are passed by reference

			newState = Result2(bestNode, bestNodeCopy, a, computeG(bestNode)+1) #go to the action in this current state and put it in new state, also compute the g for the result 2 by getting the parent's g then adding 1 because it's a child
			
			for i in range(3):
				print(str(newState.puzzle[i][0])+str(newState.puzzle[i][1])+str(newState.puzzle[i][2]))
			print(newState.f)

			openListBoards = [node.puzzle for node in openList] #create and get the array of puzzles in frontier

			if (newState.puzzle not in closedList and newState.puzzle not in openListBoards) or newStateGLess(newState, openListBoards, openList): #if the new state's puzzle is not in explored list or the frontier's puzzle state list
				openList.append(newState); #append it in the frontier to be explored later
				print("Append!")







def minimumF(openList): #function that computes for the minimum f among the nodes and pops it
	count = len(openList)
	minimumF=9999999999 #set my minimum f to the biggest first
	minimumNode=0;

	for i in range(count):
		if openList[i].f < minimumF: # compare all the node's f value if its less than the minimum
			minimumF=openList[i].f #set the value of node f into the new minimum f
			minimumNode=i #set it as the new minimum node to be popped

	return openList.pop(minimumNode) #pop the minimum node on the list

def newStateGLess(newNode, ListOfPuzzles ,ListOfNodes): #function that checks if the newnode is already in the frontier and if so, if it less than the g of the g it's duplicate in the frontier
	if(newNode.puzzle in ListOfPuzzles): #if the new board is in the list of boards
		count = len(ListOfPuzzles)
		for i in range(count):
			if (ListOfPuzzles[i] == newNode.puzzle and ListOfNodes[i].g > newNode.g): #find the duplicate and check if the g is lower
				print("TRUE!");
				return True

	else:
		return False #if it is not in the list of nodes or it's duplicate has lower g then return false


main();
pygame.quit(); #quit my pygame
quit(); #quit python