from rubiks import Rubiks_Cube

class Solution(Rubiks_Cube):
	def __init__(self, faces):
		self.faces = faces

	def locate_side(self, colour, side1=None):
		temp = []
		for face in self.faces.values():
			if face.grid[0][1] == colour:
				temp.append((face.colour, self.faces[face.colour].location[0]))

			if face.grid[1][0] == colour:
				temp.append((face.colour, self.faces[face.colour].location[3]))

			if face.grid[1][2] == colour:
				temp.append((face.colour, self.faces[face.colour].location[1]))

			if face.grid[2][1] == colour:
				temp.append((face.colour, self.faces[face.colour].location[2]))

		location = temp
		if side1:
			location = []
			for block in temp:
				self.faces[block[0]].set_as_top(block[1]) 
				self.faces[block[1]].set_as_top(block[0])
				if self.faces[block[0]].grid[0][1] in [colour, side1] and \
				   self.faces[block[1]].grid[0][1] in [colour, side1]:
					location.append(block)
					break

		return location

	def locate_corner(self, colour, side1=None, side2=None):
		pass


	def right_alg(self, colour, direction):
		start = self.faces[colour]
		start.set_as_top(direction)
		sides = [i for i in start.location]

		self.rotate(colour, sides[0], 2)
		self.rotate(colour, sides[3], 2)
		self.rotate(colour, sides[2], 0)
		self.rotate(colour, sides[1], 0)


	def left_alg(self, colour, direction):
		start = self.faces[colour]
		start.set_as_top(direction)
		sides = [i for i in start.location]

		self.rotate(colour, sides[0], 0)
		self.rotate(colour, sides[1], 0)
		self.rotate(colour, sides[2], 2)
		self.rotate(colour, sides[3], 2)

	def Cross(self, colour) -> int:
		'''
		creates a colour cross

		<flow chart>
		step 1: colour is already in correct position we are done
		step 2: colour is on the side not between yellow
				or opposite colour skip step 4
		step 3: a corner piece is on the yellow side but not
			    between the right colour ie yellow and red piece is
		        between yellow and orange
		step 4: rotate each piece to the opposite side and find a 
		        colour that matches ie yellow and red is between white and red
		step 5: fix it if twisted after u turn it back to yellow fix it

		returns the number of steps required to solve
		'''

		temp = self.faces[self.faces[colour].location[0]]
		opp_colour = temp.location[temp.location.index(colour) - 2]

		for c in [i for i in self.faces[colour].location]:
			sides = self.locate_side(colour, c)[0]
			if sides == (colour, c):
				continue

			elif colour not in sides and opp_colour not in sides:
				self.faces[sides[0]].set_as_top(opp_colour)
				if self.faces[sides[0]].location[1] == sides[1]:
					self.right_alg(sides[0], opp_colour)
				else:
					self.left_alg(sides[0], opp_colour)

			elif colour in sides and c not in sides:
				self.rotate_face(sides[0] if sides[0] != colour else sides[1], 2)

			if opp_colour in self.locate_side(colour, c)[0]:
				while c not in self.locate_side(colour, c)[0]:
					self.rotate_face(opp_colour)
				new = self.locate_side(colour, c)[0]
				self.rotate_face(new[0] if new[0] != opp_colour else new[1], 2)


			if self.locate_side(colour, c)[0] == (c, colour):
				self.rotate_face(colour, CLC=1)
				self.rotate(colour, c, 0)
				self.rotate_face(colour)
				self.rotate_face(c, CLC=1)

if __name__ == '__main__':
	a = Solution(Rubiks_Cube().faces)
	# a.rotate_face('R', 1)
	# a.rotate('R', 'Y', 0)
	# a.rotate_face('Y', 1)
	a.scramble()
	print(a)
	a.Cross('Y')
	print('-----')
	print(a)
	# a.rotate_face('R',2)
	# print(a)