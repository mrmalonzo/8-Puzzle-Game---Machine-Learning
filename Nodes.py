import pygame 

class Nodes:

	def __init__(self, puzzle, emptyTilePosI, emptyTilePosJ, Action, parentTile, g, h, f):

		self.puzzle=puzzle;
		self.emptyTilePosI=emptyTilePosI;
		self.emptyTilePosJ=emptyTilePosJ;
		self.Action=Action;
		self.parentTile=parentTile;
		self.g=g;
		self.h=h;
		self.f=f;

