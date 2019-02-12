from __future__ import annotations
from collections import deque
from typing import List
import random

class Face(object):
	def __init__(self, top, right, bottom, left, colour, items=False):
		self.location = deque([top, right, bottom, left])
		self.colour = colour
		if items:
			self.grid = items
		else:
			self.grid = [[colour for b in range(3)] for i in range(3)]

	def set_as_bottom(self, bottom):
		while self.location[2] != bottom:
			self.location.rotate()
			self.grid = [list(a) for a in zip(*self.grid[::-1])]


	def find_line(self, pos):
		return [self.grid[i][pos] for i in range(3)]


	def set_as_top(self, top):
		while self.location[0] != top:
			self.location.rotate()
			self.grid = [list(a) for a in zip(*self.grid[::-1])]


	def replace_line(self, line, pos):
		for ind, colour in enumerate(line):
			self.grid[ind][pos] = colour 


	def rotate_clockwise(self):
		# self.grid = [list(a) for a in zip(*self.grid[::-1])]
		self.location.rotate()
		# self.grid = [list(a) for a in zip(*self.grid[::-1])]


	def rotate_counter_clockwise(self):
		self.location.rotate(-1)
		# self.grid = [[b[i] for b in self.grid] for i in range(2, -1 ,-1)]


	def rotate(self, direction, start):
		self.set_as_top(direction)
		if start == self.location[3]:
			self.rotate_counter_clockwise()

		elif start == self.location[1]:
			self.rotate_clockwise()


class Rubiks_Cube(object):
	def __init__(self, items: List[Face]=None):
		if items:
			self.rubiks = {}
			for face in items:
				self.rubiks[face.colour, face]

		else:
			self.rubiks = {
				'R' : Face('Y', 'G', 'W', 'B', 'R'),
				'B' : Face('Y', 'R', 'W', 'O', 'B'),
				'O' : Face('Y', 'B', 'W', 'G', 'O'),
				'G' : Face('Y', 'O', 'W', 'R', 'G'),
				'Y' : Face('O', 'G', 'R', 'B', 'Y'),
				'W'	: Face('R', 'G', 'O', 'B', 'W')
			}


	def rotate(self, colour, direction, pos):
		start = colour
		currcolour = colour
		face = self.rubiks[currcolour]
		face.set_as_top(direction)
		currline = face.find_line(pos)
		newcolour = face.location[0]

		# fix orientation of side to right or left is currcolour and top is newcolour
		# if right is currcolour flip counter clockwise
		# if left is colour flip clockwise

		if pos == 2:
			side = self.rubiks[face.location[1]]
			side.rotate(newcolour, currcolour)
		elif pos == 0:
			side = self.rubiks[face.location[3]]
			side.rotate(newcolour, currcolour)

		while newcolour != start:
			newface = self.rubiks[newcolour]
			newface.set_as_bottom(currcolour)
			newline = newface.find_line(pos)
			newface.replace_line(currline, pos)
			currline = newline
			currcolour = newcolour
			newcolour = newface.location[0]

		self.rubiks[start].replace_line(currline, pos)


	def right_alg(self, colour, direction):
		start = self.rubiks[colour]
		start.set_as_top(direction)
		self.rotate(colour, start.location[0], 2)
		self.rotate(colour, start.location[3], 2)
		self.rotate(colour, start.location[2], 0)
		self.rotate(colour, start.location[1], 0)

	def left_alg(self, colour, direction):
		start = self.rubiks[colour]
		start.set_as_top(direction)
		self.rotate(colour, start.location[0], 0)
		self.rotate(colour, start.location[1], 0)
		self.rotate(colour, start.location[2], 2)
		self.rotate(colour, start.location[3], 2)

	def locate_side(self, colour, side1=None):
		temp = []
		for face in self.rubiks.values():
			if face.grid[0][1] == colour:
				temp.append((face.colour, self.rubiks[face.colour].location[0]))

			if face.grid[1][0] == colour:
				temp.append((face.colour, self.rubiks[face.colour].location[3]))

			if face.grid[1][2] == colour:
				temp.append((face.colour, self.rubiks[face.colour].location[1]))

			if face.grid[2][1] == colour:
				temp.append((face.colour, self.rubiks[face.colour].location[2]))

		location = temp
		if side1:
			location = []
			for block in temp:
				self.rubiks[block[0]].set_as_top(block[1]) 
				self.rubiks[block[1]].set_as_top(block[0])
				if self.rubiks[block[0]].grid[0][1] in [colour, side1] and \
				   self.rubiks[block[1]].grid[0][1] in [colour, side1]:
					location.append(block)
					break

		return location

	def locate_corner(self, colour, side1=None, side2=None):
		pass


	def scramble(self):
		for i in range(100):
			colours = 'RGBYOW'
			position = [0, 2]
			colour1 = random.choice(colours)
			colour2 = random.choice(self.rubiks[colour1].location)
			randpos = random.choice(position)

			self.rotate(colour1, colour2, randpos)

	def __str__(self):
		string = ''
		for i in self.rubiks:
			string += str(self.rubiks[i].location) + '\n'
			for b in self.rubiks[i].grid:
				string += str(b) + '\n'
		return string
	




if __name__ == '__main__':
	import time
	rubik = Rubiks_Cube()
	rubik.scramble()
	
	# print(rubik)
	# rubik.rotate('R', 'Y', 2)
	# print(rubik)
	# rubik.rotate('R', 'B', 2)
	# print(rubik)
	# rubik.rotate('R', 'W', 0)
	# print(rubik)
	# rubik.rotate('R', 'G', 0)
	# print(rubik)


	# test = Face('Y', 'G', 'W', 'B', 'R')
	# test.grid = [['R', 'R', 'W'], ['R', 'R', 'W'], ['R', 'R', 'W']]
	# test.set_as_top('B')
	# print(test.grid)
	# print(test.location)


	# print(test.location)
	# print(test.grid)
	# test.location.rotate()
	# print(test.location)