from rubiks import Rubiks_Cube
from typing import List, Any

class Solution(Rubiks_Cube):
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
        temp = []
        for face in self.faces.values():
            for a, b, c in zip([0, 0, 2, 2], [0, 2, 0, 2], [(3, 0), (0, 1), (2, 3), (1, 2)]):
                if face.grid[a][b] == colour:
                    colour1 = face.colour
                    colour2 = face.location[c[0]] # set as right
                    colour3 = face.location[c[1]] # set as left
                    temp.append((colour1, colour2, colour3))

        if side1:
            cleaned = []
            for center, top, right in temp:
                self.faces[top].set_as_right(center)
                self.faces[right].set_as_left(center)
                if self.faces[top].grid[0][2] == side1:
                    cleaned.append((center, top, right))
                elif self.faces[right].grid[0][0] == side1:
                    cleaned.append((center, top, right))
            temp = cleaned

        if side2:
            cleaned = []
            for center, top, right in temp:
                self.faces[top].set_as_right(center)
                self.faces[right].set_as_left(center)
                if self.faces[top].grid[0][2] == side2:
                    cleaned.append((center, top, right))
                elif self.faces[right].grid[0][0] == side2:
                    cleaned.append((center, top, right))
            temp = cleaned

        return temp


    def right_alg(self, colour, direction):
        start = self.faces[colour]
        start.set_as_top(direction)
        sides = [i for i in start.location]
        rotations = []

        rotations += self.rotate(colour, sides[0], 2)
        rotations += self.rotate(colour, sides[3], 2)
        rotations += self.rotate(colour, sides[2], 0)
        rotations += self.rotate(colour, sides[1], 0)

        return rotations


    def left_alg(self, colour, direction):
        start = self.faces[colour]
        start.set_as_top(direction)
        sides = [i for i in start.location]
        rotations = []

        rotations += self.rotate(colour, sides[0], 0)
        rotations += self.rotate(colour, sides[1], 0)
        rotations += self.rotate(colour, sides[2], 2)
        rotations += self.rotate(colour, sides[3], 2)

        return rotations

    def Cross(self, colour):
        '''returns the number of steps required to solve
        
        creates a <colour> cross
        <flow chart>
        step 1: <colour> is already in correct position we are done
        step 2: <colour> is on the side not between yellow
                or opposite colour skip step 4
        step 3: a corner piece is on the yellow side but not
                between the right colour ie yellow and red piece is
                between yellow and orange
        step 4: rotate each piece to the opposite side and find a 
                colour that matches ie yellow and red is between white and red
        step 5: fix it if twisted after u turn it back to yellow fix it
        '''

        temp = self.faces[self.faces[colour].location[0]]
        opp_colour = temp.location[temp.location.index(colour) - 2]
        rotations = []

        for c in [i for i in self.faces[colour].location]:
            sides = self.locate_side(colour, c)[0]
            if sides == (colour, c):
                continue

            elif colour not in sides and opp_colour not in sides:
                self.faces[sides[0]].set_as_top(opp_colour)
                if self.faces[sides[0]].location[1] == sides[1]:
                    rotations += self.right_alg(sides[0], opp_colour)

                else:
                    rotations +=self.left_alg(sides[0], opp_colour)

            elif colour in sides and c not in sides:
                rotations += self.rotate_face(sides[0] if sides[0] != colour else sides[1], 2)

            if opp_colour in self.locate_side(colour, c)[0]:
                while c not in self.locate_side(colour, c)[0]:
                    rotations += self.rotate_face(opp_colour)

                new = self.locate_side(colour, c)[0]

                rotations += self.rotate_face(new[0] if new[0] != opp_colour else new[1], 2)


            if self.locate_side(colour, c)[0] == (c, colour):
                rotations += self.rotate_face(colour, CLC=1)

                rotations += self.rotate(colour, c, 0)

                rotations += self.rotate_face(colour)

                rotations += self.rotate_face(c, CLC=1)

        return rotations


    def Corners(self, colour):
        '''returns the number of steps required to solve
        
        fixes the correct corners of the colour
        <flow chart>
        step 1: If the twisted corner piece is currently in between 3 pieces
                that contains <colour> pop it out. If all 3 colours on the piece 
                matches are located between the 3 faces ignore step 2
        step 2: Simply rotate the face opposite of <colour> and line up 2 colours
                with whats on the cube.
        step 3: preform the left or right algorithm and pop the piece down into
                the corner
        '''
        temp = self.faces[self.faces[colour].location[0]]
        opp_colour = temp.location[temp.location.index(colour) - 2]
        lst1 = [i for i in self.faces[colour].location]
        lst2 = lst1[:]
        lst2.insert(0, lst2.pop(-1))
        rotations = []

        for col1, col2, in zip(lst1, lst2):
            sides = self.locate_corner(colour, col1, col2)[0]

            if colour in sides and (col1 not in sides or col2 not in sides):
                c = next(i for i in sides if i != colour)
                self.faces[c].set_as_top(opp_colour)
                if self.faces[c].location[3] in sides:
                    rotations += self.left_alg(c, opp_colour)

                else:
                    rotations += self.right_alg(c, opp_colour)
                # right alg pop it and match

            sides = self.locate_corner(colour, col1, col2)[0]

            if opp_colour in sides:
                while not all(map(lambda x: x in sides, [col1, col2])):
                    rotations += self.rotate_face(opp_colour)
                    sides = self.locate_corner(colour, col1, col2)[0]
                # match up the two colours by rotating opp

            if all(map(lambda x: x in sides, [col1, col2, colour])) or\
               all(map(lambda x: x in sides, [col1, col2, opp_colour])):
                # fixing it in correct position
                self.faces[col1].set_as_top(opp_colour)

                if self.faces[col1].grid[0][0]:
                    while sides[0] != colour:
                        rotations += self.left_alg(col1, opp_colour)
                        sides = self.locate_corner(colour, col1, col2)[0]

                else:
                    while sides[0] != colour:
                        rotations += self.right_alg(col1, opp_colour)
                        sides = self.locate_corner(colour, col1, col2)[0]

        return rotations

    def Fix_sides(self, colour):
        side1 = self.faces[colour].location.copy()
        self.faces[colour].location.rotate()
        side2 = self.faces[colour].location.copy()
        self.faces[colour].location.rotate(-1)

        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        rotations = []

        for colour1, colour2 in zip(side1, side2):

            a = self.locate_side(colour1, colour2)
            if a[0][0] != opposite and a[0][1] != opposite and\
               (a[0][0] != colour1 or a[0][1] != colour2):

                self.faces[a[0][0]].set_as_top(opposite)
                if self.faces[a[0][0]].location[3] == a[0][1]:
                    rotations += self.left_alg(a[0][0], opposite)
                    rotations += self.right_alg(a[0][1], opposite)

                else:
                    rotations += self.right_alg(a[0][0], opposite)
                    rotations += self.left_alg(a[0][1], opposite)

                a = self.locate_side(colour1, colour2)

            if a[0][0] == side1 and a[0][1] == side2:
                pass

            elif a[0][0] == opposite:
                # rotate the top face until colour2 until it matches face
                rotations += self.fix_face(colour2, colour1, opposite)
            elif a[0][1] == opposite:
                # rotate the top face until colour1 matches face
                rotations += self.fix_face(colour1, colour2, opposite)

        return rotations

    def fix_face(self, c1, c2, opposite):

        rotations = []
        while self.locate_side(c1, c2)[0] != (c1, opposite):
            rotations += self.rotate_face(opposite)

        # print(self)
        self.faces[c1].set_as_top(opposite)
        if self.faces[c1].location[3] == c2:
            rotations += self.rotate_face(opposite, CLC=1)
            rotations += self.left_alg(c1, opposite)
            rotations += self.right_alg(c2, opposite)

        else:
            rotations += self.rotate_face(opposite)
            rotations += self.right_alg(c1, opposite)
            rotations += self.left_alg(c2, opposite)

        # pop it in correct corner
        return rotations

    def Top_cross(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        steps, rotations = 0, []
        a = [i for i in self.locate_side(opposite) if i[0] == opposite]
        if len(a) == 2:
            if self.faces[colour].location[0] in [a[1][1], a[1][0], a[0][0], a[0][1]] \
                and self.faces[colour].location[2] in [a[1][1], a[1][0], a[0][0], a[0][1]]:
                start = self.faces[self.faces[colour].location[1]]
                start.set_as_top(opposite)

                rotations += self.rotate(opposite, start.location[1], 2)

                rotations += self.right_alg(start.colour, opposite)

                start.set_as_top(opposite)

                rotations += self.rotate(start.location[1], opposite, 0)


            elif self.faces[colour].location[1] in [a[1][1], a[1][0], a[0][0], a[0][1]] \
                and self.faces[colour].location[3] in [a[1][1], a[1][0], a[0][0], a[0][1]]:
                start = self.faces[self.faces[colour].location[2]]
                start.set_as_top(opposite)

                rotations += self.rotate(opposite, start.location[1], 2)

                rotations += self.right_alg(start.colour, opposite)

                start.set_as_top(opposite)

                rotations += self.rotate(start.location[1], opposite, 0)

            else:
                if self.check_l_shape(colour, a):
                    # rotate back
                    self.faces[a[0][1]].set_as_top(opposite)
                    left = self.faces[a[0][1]].location[3]
                    rotations += self.rotate(opposite, left, 2)

                    rotations += self.right_alg(a[0][1], left)

                else:
                    self.faces[a[1][1]].set_as_top(opposite)
                    left = self.faces[a[1][1]].location[3]
                    rotations += self.rotate(opposite, left, 2)

                    self.faces[a[1][1]].set_as_top(opposite)
                    rotations += self.right_alg(a[1][1], left)

                rotations += self.rotate(left, opposite, 0)

        elif len(a) == 0:
            face_c = self.faces[colour].location[1]
            self.faces[face_c].set_as_top(opposite)

            save = self.faces[face_c].location[1]
            rotations += self.rotate(opposite, save, 2)

            rotations += self.right_alg(face_c, opposite)
            
            rotations += self.rotate(save, opposite, 0)

            rotations += self.Top_cross(colour)

        return rotations

    def check_l_shape(self, colour, location):
        spots = [(0, 1), (1, 2), (2, 3), (3, 0)]
        loc = self.faces[colour].location
        for x1, x2 in spots:
            if loc[x1] == location[0][1] and loc[x2] == location[1][1]:
                return True

        return False

    def Top_corners(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        rotations = []
        side1 = self.faces[opposite].location.copy()
        self.faces[opposite].location.rotate()
        side2 = self.faces[opposite].location.copy()
        self.faces[opposite].location.rotate(-1)

        num = self.count_corners(side1, side2, opposite)
        while len(num) < 2:
            rotations += self.rotate_face(opposite)
            num = self.count_corners(side1, side2, opposite)

        # print(self)
        if len(num) == 4:
            return rotations

        elif len(num) == 2:
            side = ''
            for i in side1:
                if i not in num[0] and i not in num[1]:
                    side += i

            if not side:
                # print('run')
                flip = num[0][1] if num[0][1] != opposite else num[0][2]
                self.faces[flip].set_as_top(opposite)
                if self.faces[flip].location[1] not in num[0]:
                    flip = self.faces[flip].location[3]
                    # right alg swap left alg 3 times and rotate
                self.faces[flip].set_as_top(opposite)
                save = self.faces[flip].location[1]
                count = 0
                # print(flip)
                # print(opposite)
                # print(save)
                while count < 3:
                    rotations += self.right_alg(flip, opposite)
                    count += 1

                while count > 0:
                    rotations += self.left_alg(save, opposite)
                    count -= 1

                # print(self)
                rotations += self.rotate(save, flip, 2)
                rotations += self.Top_corners(colour)
                return rotations


            if side:
                # print('run')
                num = self.count_corners(side1, side2, opposite)
                # print(num)
                self.faces[side].set_as_top(opposite)
                flip = self.faces[side].location[3]
                self.faces[flip].set_as_top(opposite)
                save = self.faces[flip].location[1]
                # print(flip)
                # print(save)

                count = 0
                while count < 3:
                    rotations += self.right_alg(flip, opposite)
                    count += 1

                while count > 0:
                    # print(self.faces[flip].location[1])
                    rotations += self.left_alg(save, opposite)
                    count -= 1

                rotations += self.rotate(flip, save, 0)

        return rotations


    def count_corners(self, side1, side2, opposite):
        count = []
        for c1, c2 in zip(side1, side2):
            if all(map(lambda x: x in {c1, c2, opposite}, \
                self.locate_corner(c1, c2, opposite)[0])): 
                count.extend(self.locate_corner(c1, c2, opposite))
        return count

    def Invert(self, colour):
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]
        sides = [i for i in self.locate_corner(opposite) if i[0] != opposite]
        rotations = []

        if len(sides) > 1:
            start = sides[0][0]
            self.faces[start].set_as_top(colour)
            if self.faces[start].location[1] not in sides[0]:
                start = self.faces[start].location[3]
                self.faces[start].set_as_top(colour)

            right = self.faces[start].location[1]
            while len(sides) != 0:
                rotations += self.right_alg(start, colour)
                new = [i for i in self.locate_corner(opposite) if i[0] != opposite]
                if len(new) < len(sides):
                    if len(new) == 0:
                        break
                    if right not in new[0] and start not in new[0]:

                        rotations += self.rotate(right, start, 0)
                        rotations += self.rotate(right, start, 0)

                    elif right in new[0]:
                        rotations += self.rotate(right, start, 0)

                    else: 
                        rotations += self.rotate(start, right, 2)

                    sides = new

        return rotations


    def Final_Solve(self, colour):
        rotations = []
        self.faces[self.faces[colour].location[0]].set_as_bottom(colour)
        opposite = self.faces[self.faces[colour].location[0]].location[0]

        if all(self._Solved_face(col) for col in self.faces[colour].location):
            return rotations

        for col in self.faces[colour].location:
            if self._Solved_face(col):
                rotations += self._Solve_alg(col, opposite)
                rotations += self.Final_Solve(colour)
                return rotations

        start = self.faces[colour].location[0]
        rotations += self._Solve_alg(start, opposite)
        rotations += self.Final_Solve(colour)
        return rotations


    def _Solve_alg(self, colour, loc):
        rotations = []
        rotations += self.right_alg(colour, loc)
        rotations += self.left_alg(colour, loc)

        count = 0
        while count < 5:
            rotations += self.right_alg(colour, loc)
            count += 1

        while count > 0:
            rotations += self.left_alg(colour, loc)
            count -= 1

        return rotations

    def _Solved_face(self, colour):
        for row in self.faces[colour].grid:
            if not all(col == colour for col in row):
                return False
        return True

    def parse_rotation(self, rotations: List[List[Any]], STEPS=4) -> List[List[Any]]:
        """turn every starting rotation point to be R, B, W"""
        parsed = []
        for rot in rotations:
            if rot[0] + rot[1] in 'RYOWR':
                if rot[2] == 0:
                    # vert[1] == -3 inverted rotation Y
                    parsed.extend([['Y', 1, 3, -STEPS]] * STEPS)
                elif rot[2] == 2: 
                    # vert[1] == 3 inverted rotation Y
                    parsed.extend([['Y', 1, -3, -STEPS]] * STEPS)

            elif rot[0] + rot[1] in 'BYGWB':
                if rot[2] == 0:
                    # vert[0] == 3 inverted rotation X
                    parsed.extend([['X', 0, -3, -STEPS]] * STEPS)
                elif rot[2] == 2: 
                    # vert[0] == -3 inverted rotation X
                    parsed.extend([['X', 0, 3, -STEPS]] * STEPS)

            elif rot[0] + rot[1] in 'RBOGR':
                if rot[2] == 0:
                    # vert[2] == 3 inverted rotation Z
                    parsed.extend([['Z', 2, 3, -STEPS]] * STEPS)

                elif rot[2] == 2: 
                    # vert[2] == - 3 inverted rotation Z
                    parsed.extend([['Z', 2, -3, -STEPS]] * STEPS)

            elif rot[0] + rot[1] in 'RWOYR':
                if rot[2] == 0:
                    # vert[1] == -3 original rotation Y
                    parsed.extend([['Y', 1, -3, STEPS]] * STEPS)
                    
                elif rot[2] == 2: 
                    # vert[1] == 3 original rotation Y
                    parsed.extend([['Y', 1, 3, STEPS]] * STEPS)

            elif rot[0] + rot[1] in 'BWGYB':
                if rot[2] == 0:
                    # vert[0] == 3 original rotation X
                    parsed.extend([['X', 0, 3, STEPS]] * STEPS)
                elif rot[2] == 2: 
                    # vert[0] == -3 original rotation X
                    parsed.extend([['X', 0, -3, STEPS]] * STEPS)
            elif rot[0] + rot[1] in 'RGOBR':
                if rot[2] == 0:
                    # vert[2] == 3 original rotation Z
                    parsed.extend([['Z', 2, -3, STEPS]] * STEPS)
                elif rot[2] == 2: 
                    # vert[2] == -3 original rotation Z
                    parsed.extend([['Z', 2, 3, STEPS]] * STEPS)
        return parsed[::-1]

    def Solve(self):
        faces = self.copy()
        total = float('inf')
        rotations = []
        for colour in 'RGYOBW':
            curr_rot = []
            curr_rot += self.Cross(colour)
            curr_rot += self.Corners(colour)
            curr_rot += self.Fix_sides(colour)
            curr_rot += self.Top_cross(colour)
            curr_rot += self.Top_corners(colour)
            curr_rot += self.Invert(colour)
            curr_rot += self.Top_corners(colour)
            curr_rot += self.Final_Solve(colour)
            if colour != 'W':
                self.faces = {key: item.copy() for key, item in faces.items()}
            if len(curr_rot) < total:
                total, rotations = len(curr_rot), curr_rot

        return rotations



if __name__ == '__main__':
    import time
    start = time.time()
    cube = Solution()
    total, steps = [], 0
    for i in range(1000):
        cube.Scramble()
        total += cube.Solve()
        for colour in 'RGWYBO':
            assert cube._Solved_face(colour)

    print(len(total) // 1000)
    print(f'6000 combinations solved in {time.time() - start}')