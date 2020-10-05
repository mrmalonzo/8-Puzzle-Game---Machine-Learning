import pygame

class Tiles:

	def __init__(self, number, xPos, yPos):

		self.number=number; #mark the number attribute for later use
		self.xPos = xPos; #positions of the tile
		self.yPos = yPos;


		if(self.number==1): #load the image numbers according to the tiles number
			self.image=pygame.image.load("One.png");
		elif(self.number==2):
			self.image=pygame.image.load("Two.png");
		elif(self.number==3):
			self.image=pygame.image.load("Three.png");
		elif(self.number==4):
			self.image=pygame.image.load("Four.png");
		elif(self.number==5):
			self.image=pygame.image.load("Five.png");
		elif(self.number==6):
			self.image=pygame.image.load("Six.png");
		elif(self.number==7):
			self.image=pygame.image.load("Seven.png");
		elif(self.number==8):
			self.image=pygame.image.load("Eight.png");
		elif(self.number==0):
			self.image=pygame.image.load("Blank.jpg");

		self.image=pygame.transform.scale(self.image,(175,175)); #adjust my tile size

		self.rectangle=self.image.get_rect(); #to not make my rectangle go to 0,0 after creating it for the image
		self.rectangle.center=(xPos+87.5,yPos+87.5)
			

	def Move(self):
		print("MOVE")

	def NotEmpty(self):
		if self.number!=0:
			return True
		else:
			return False;
		

	def neighborEmptyTile(self, GameBoard, emptyTilePosI, emptyTilePosJ, tilePosI, tilePosJ): #checker if the tile that was clicked can be moved to the emprty tile
		if(tilePosI == 0 and tilePosJ == 0): #if it is a top left tile
			print("Top left")
			if(emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ): #if the tile can be interchangeable, that means that the empty tile ahs to be a bottom neighbor or right neighbor of the tile
				return True
		elif(tilePosI == 2 and tilePosJ == 0): #if it is a bottom left tile
			print("Bottom Left")
			if(emptyTilePosI+1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ): #if the tile can be interchangeable, that means that the empty tile ahs to be a top neighbor or right neighbor of the tile
				return True
		elif(tilePosI == 0 and tilePosJ== 2): #if it is a top right tile
			print("Top Right")
			if(emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ): #if the tile can be interchangeable, that means that the empty tile ahs to be a bottom neighbor or left neighbor of the tile
				return True
		elif(tilePosI == 2 and tilePosJ ==2): #if it is a bottom right right tile
			print("Bottom Right")
			if(emptyTilePosI+1 == tilePosI and emptyTilePosJ== tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ): #if the tile can be interchangeable, that means that the empty tile ahs to be a top neighbor or left neighbor of the tile
				return True
		elif(tilePosJ == 0): #its a left tile
			print("Left")
			if(emptyTilePosI+1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ or emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ): #check the top, right and bottom neighbor tile if it an empty tile
				return True
		elif(tilePosJ == 2): #its a right tile
			print("Right")
			if(emptyTilePosI+1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ or emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ): #check the top, left and bottom neighbor tile if it an empty tile
				return True
		elif(tilePosI == 0): #its a Top tile
			print("Top")
			if(emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ or emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ): #check the left, right and bottom neighbor tile if it an empty tile
				return True
		elif(tilePosI == 2): #its a bottom tile
			print("Bottom")
			if(emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ or emptyTilePosI+1 == tilePosI and emptyTilePosJ == tilePosJ): #check the top, right and left neighbor tile if it an empty tile
				return True
		else: #that means it is a middle tile and the empty tile could be among its 4 neighbor tile so we have to check it all
			print("Middle tile")
			if(emptyTilePosI == tilePosI and emptyTilePosJ+1 == tilePosJ or emptyTilePosI == tilePosI and emptyTilePosJ-1 == tilePosJ or emptyTilePosI+1 == tilePosI and emptyTilePosJ == tilePosJ or emptyTilePosI-1 == tilePosI and emptyTilePosJ == tilePosJ): #check the top, right, left and bottom neighbor tile if it an empty tile
				return True


	def swapTiles(self, GameBoard, emptyTilePosI,emptyTilePosJ, i, j): #if you the tile is being swapped
		temporaryX=GameBoard[emptyTilePosI][emptyTilePosJ].xPos #get the temporary position of the empty tile in the gui and the gameboard
		temporaryY=GameBoard[emptyTilePosI][emptyTilePosJ].yPos
		GameBoard[emptyTilePosI][emptyTilePosJ].xPos=GameBoard[i][j].xPos	#switch their positions (coordinates in GUI and position in array)
		GameBoard[emptyTilePosI][emptyTilePosJ].yPos=GameBoard[i][j].yPos
		GameBoard[i][j].xPos=temporaryX
		GameBoard[i][j].yPos=temporaryY

		GameBoard[i][j].setRectangle(); #set the rectangle of the image again of the tile switched

		GameBoard[emptyTilePosI][emptyTilePosJ].setRectangle(); #set the rectangle of the empty tile


		GameBoard[i][j], GameBoard[emptyTilePosI][emptyTilePosJ] = GameBoard[emptyTilePosI][emptyTilePosJ], GameBoard[i][j] #switch the position of the tile and empty tile in thje array

		return GameBoard


	def setRectangle(self): #to set my tile's image rectangle again

		self.rectangle=self.image.get_rect(); #to not make my rectangle go to 0,0 after creating it for the image
		self.rectangle.center=(self.xPos+87.5,self.yPos+87.5)